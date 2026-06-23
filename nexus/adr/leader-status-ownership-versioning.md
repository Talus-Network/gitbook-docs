# ADR-3: Claim-Token-Guarded Leader Activation and Suspension

**Status:** Proposed
**Date:** 2026-06-10
**Authors:** Pavel ([@kouks](https://github.com/kouks))
**Deciders:** Pavel ([@kouks](https://github.com/kouks))
**Consulted:** Engineering Team
**Informed:** Engineering Team

**Constraint Tags:** Technical | Architectural | Operational

---

## Context

### What problem are we solving?

A leader's on-chain liveness is a single `LeaderStatus` (`Active` / `Suspended` /
`Slashed`) field on its per-leader record in `nexus_registry::leader`
(`sui/registry/sources/leader.move`). Only `Active` leaders are selected into the
distribution committee. The leader process sets itself `Active` on startup once
its event listener has caught up to the live checkpoint
(`be/leader/src/onchain/listener.rs` → `ensure_leader_status_active`), and sets
itself `Suspended` on shutdown in the SIGTERM handler
(`be/leader/src/services.rs` → `set_leader_inactive`).

The shutdown handler suspends **unconditionally**. It does not check whether this
instance is the one that owns the current `Active` state, or whether another
instance is still alive serving as the leader. During a Cloud Run rolling restart
— which briefly runs two instances of the same leader before consolidating back to
one — the shutdown of _any_ instance flips the shared record to `Suspended`,
removing the leader from the distribution vector even though a healthy instance is
still running.

This is independent of, and additional to, the activation-on-catchup feature
(shipped 2026-04-23): that only protects the **activation** side of the race, not
the **deactivation** side.

### Production impact

Observed on testnet leaders:

- **leader-0 (us-east1):** `Suspended` for at least 36 days, recovered only by a
  manual `scale 0→1`. Zero work served as primary or backup over the window.
- **leader-2 (us-west1):** `Suspended` for ~23.5 hours after a Cloud Run instance
  refresh on 2026-05-28 (no deploy that day). Reproduced from logs: instance A
  starts and catches up, the old instance suspends correctly, instance B starts,
  A activates correctly, B no-ops, then Cloud Run kills one of the two instances
  and the unconditional suspend flips the record to `Suspended` — with no further
  status change until manual intervention.
- **leader-1 (eu-west1)** carried the entire testnet workload alone throughout —
  a single point of failure with no backup leader for any execution.

This recurs on **every** Cloud Run instance refresh (zone maintenance, instance
auto-refresh, hardware recovery), with unpredictable timing.

### Relevant Constraints

**Technical:** `status` is one field on **one** shared record per leader, not
per-instance. Any instance holding a valid leader capability can write it. To
distinguish "the instance that owns the current `Active` state" from "any other
instance," we need a per-activation **ownership token** that is unique across
instances with no inter-instance coordination — uniqueness, not ordering, is what
the problem requires. Sui already gives us exactly that: every transaction has a
globally unique digest (the protocol forbids digest replay), readable on-chain via
`tx_context::digest(ctx)` (`public fun digest(&TxContext): &vector<u8>`, already
used in `sui/workflow/sources/dag.move` and `sui/scheduler/sources/scheduler.move`).
Transactions on the shared registry object are serialized by consensus, giving a
well-defined last writer. The shutdown suspend TX runs inside a bounded
shutdown-timeout budget (`timeout_tx`, 2/5 of the configured shutdown timeout), so
it must not abort or retry on the expected "I am not the owner" path.

**Architectural:** Move functions that off-chain code calls are exported through
the nexus-sdk ident registry (`sdk/src/idents/workflow.rs`), so any new Move entry
point requires an SDK change landed before the leader can call it. This ships as
part of a new framework version that redeploys the registry package and
re-registers leaders, so changing the on-chain `Leader` struct layout is free.

**Operational:** The orchestrator (Cloud Run) may run two instances of the same
leader during a rolling restart and may terminate either one. A killed instance
cannot run its shutdown handler at all; a gracefully-stopped instance can.

### Architectural Position

This decision affects the **leader status lifecycle** spanning the Move
`nexus_registry::leader` module, the leader's activation path
(`onchain/listener.rs`, `onchain/leader_status.rs`) and suspension path
(`services.rs`). It introduces a notion of **ownership** of the active state, keyed
by a unique per-activation **claim token**, so that only the instance that
currently owns `Active` can suspend it.

---

## Decision

### What are we doing?

We make activation **claim ownership** by writing a unique claim token, and make
suspension **conditional** on still holding that exact token. The token is the
digest of the activating transaction itself; ownership is decided by last writer
(Sui serializes writes to the shared registry). A periodic recheck heals the
record if it is left `Suspended` while a live instance remains.

1. **On-chain ownership field.** Add `claim_token: vector<u8>` to the Move `Leader`
   struct. `bootstrap_leader_record` initializes it to the bootstrap transaction's
   own digest (`*ctx.digest()`) — a unique, non-empty starting value that no
   instance holds, so it can never accidentally match a suspender's token.

1. **Token = activating transaction digest.** On activation, Move stores
   `claim_token = *ctx.digest()`. Sui guarantees this is globally unique (no digest
   replay), so two instances activating concurrently always write distinct tokens —
   there is no version to collide and no tiebreak to design. The activating
   instance learns the digest of its own activation transaction from that
   transaction's receipt and remembers it in process (`LeaderState.claimed_token`).

1. **Two new Move entry points**, leaving `set_status` untouched for admin/CLI:
   - `activate_and_claim(registry, leader_cap, clock, ctx)` — aborts only if the
     leader is `Slashed`; sets `status = Active`; sets `claim_token = *ctx.digest()`;
     emits a `LeaderClaimedEvent { claim_token }`. Takes no token argument; the
     token is intrinsic to the transaction.
   - `suspend_if_token(registry, leader_cap, token, clock, ctx) -> bool` — **never
     aborts on mismatch**. No-ops (returns `false`) if `status != Active`; suspends
     and returns `true` only if `claim_token == token`; otherwise emits a
     `LeaderSuspensionSkippedEvent { attempted, owner }` and returns `false`. It
     does not clear the token; the next activation overwrites it.

1. **Capture at activation, replay at suspension.** The instance records the
   activation transaction's digest (from the receipt of the activation it just
   landed) into `LeaderState.claimed_token`, and the shutdown handler sends **that
   stored token**. There is nothing to recompute at shutdown — the token is a fixed
   value tied to a specific past activation, which is precisely why a departing
   instance that no longer owns the record cannot match.

1. **Activation always claims.** The existing "already `Active` → no-op early
   return" in `ensure_leader_status_active` is removed, so a newer instance writes
   its own token and takes ownership instead of passively remaining a non-owner.

1. **Periodic recheck.** A live, caught-up, non-shutting-down instance re-reads its
   status every `APP_LEADER_STATUS_RECHECK_INTERVAL` (default **60s**, env-config).
   If it observes `Suspended`, it re-activates (writing a fresh token it then
   stores) and reclaims ownership; if `Active`, it does nothing.

### Task-acceptance gate

The claim token is not only the suspend guard — it also decides _which instance
does the work_. Without this, two `Active` siblings of one leader (the rolling-restart
window) would both accept and execute the same distributed tasks, doubling on-chain
submissions and gas spend.

1. **Publish the claim to Redis — immediately, then via the event.** When an
   instance activates, it writes its own claim token into Redis right where it
   captures the activation digest (post-receipt), so it can serve tasks at once
   without waiting to index its own event. Separately, `activate_and_claim` emits
   `LeaderClaimedEvent { registry, leader_cap_id, claim_token }`; the listener
   delivers it like any other event and a consumer handler writes `claim_token`
   into the leader's Redis namespace. The event is what tells a _sibling_ — an
   already-running instance that did not just activate — that a newer instance has
   claimed, so it stops accepting tasks. The handler filters by `leader_cap_id`,
   so another leader's claim never clobbers this one. Because instances of the
   same leader share one namespace, the latest claim is visible to every sibling.

1. **Gate `decide` on ownership.** When `Distribution::decide` handles a
   _distributed_ task, it compares this instance's in-process `claimed_token`
   against the claim stored in Redis. Only the instance whose token matches acts
   on the task; a non-owner returns `Ignore`. Non-distributed events are never
   gated — they keep syncing on every instance (including `LeaderClaimedEvent`
   itself).

1. **Permissive fallback.** If no claim has been synced yet (the startup window),
   the gate is permissive so single-instance behavior is never regressed. A Redis
   failure surfaces as a transient error rather than a silently dropped task.

### Why this approach?

The unconditional suspend is the bug; the minimal correct fix is to make suspend
conditional on ownership. A per-activation token decided by Sui's transaction
digest is the simplest possible ownership primitive: it is **unique by
construction**, needs no clock, no monotonic counter, and no coordination between
instances, and it eliminates the entire class of "two instances picked the same
value" races outright — there is no tiebreak to get wrong. Ownership is "whoever
wrote the token currently on record," resolved deterministically by consensus
ordering of writes to the shared registry. Non-aborting Move semantics keep the
shutdown path within its time budget and turn the expected race into a logged
no-op plus an on-chain event (the observability that was missing during the
incident).

The recheck is **load-bearing, not cosmetic.** Because `status` is a single
per-record field, a rolling restart can deliver the graceful SIGTERM to the
_owner_ while a sibling is still alive: the owner suspends legitimately, the whole
record goes `Suspended`, and the surviving non-owner would otherwise idle forever
against it. The recheck reclaims within one interval, bounding downtime to ~60s
instead of days. The "killed owner, no sibling" case is intentionally **not**
handled in code — the orchestrator spins up a replacement that activates, writes a
new token, and overwrites the dead owner.

---

## Alternatives Considered

### Alternative 1: Monotonic version from the checkpoint clock

**Description:** Store a `u64` version on the record sourced from the
`CheckpointClock`'s latest checkpoint sequence number; activation claims with
`max(stored, version)`, suspension requires `stored == version` ("highest version
wins"). This was the prior shape of this decision.

**Why not:** It is strictly more machinery for the same guarantee. It introduces a
dependency on the checkpoint clock (and plumbing the sequence number through the
clock's state), an unseeded-clock guard so we never claim version `0`, and a
monotonic `max()` rule — and it still has a non-zero collision window (two
instances reading the same checkpoint) that has to be argued away. The transaction
digest removes the dependency, the guard, and the collision case entirely: it is
unique by protocol, so equality alone suffices and there is nothing to order.

### Alternative 2: Owner check on suspend only (no always-claim, no recheck)

**Description:** Add the token and the conditional suspend, but keep the "already
`Active` → no-op" activation and add no recheck.

**Why not:** Insufficient. If the instance that receives the graceful SIGTERM is
the legitimate owner while a sibling lives, the owner suspends correctly and the
sibling — never having claimed ownership — is stranded against a `Suspended`
record. This reproduces the same outage by a different path. The always-claim
activation and the recheck close that gap.

### Alternative 3: Leader-generated random token passed as an argument

**Description:** Instead of `ctx.digest()`, the leader generates a random 32-byte
token off-chain and passes it into `activate_and_claim(token)`, storing it
optimistically.

**Why not:** Functionally equivalent and collision-free as well, and marginally
simpler to capture (the leader already holds the value, no receipt read). We prefer
the transaction digest because it is self-generating on-chain, guaranteed unique by
the protocol's no-replay rule rather than by trusting an RNG, and idiomatic in this
codebase. Worth keeping as a fallback if reading the landed digest from the receipt
proves awkward.

### Alternative 4: Dynamic field on the `Leader` UID for the token

**Description:** Store the token in a Sui dynamic field keyed by leader cap ID
instead of a struct field, to avoid changing the `Leader` struct layout (Sui
package upgrades reject layout changes).

**Why not:** Moot here — this ships in a framework version that redeploys the
registry and re-registers leaders, so a plain typed field is free and strictly
simpler. The dynamic-field approach would be the right call only if we needed an
in-place upgrade with no migration.

### Alternative 5: Aborting Move guards

**Description:** Make `suspend_if_token` abort on token mismatch.

**Why not:** The suspend path `bail!`s on TX execution failure inside the bounded
shutdown-timeout budget; an aborting mismatch — the _expected_ path during a
rolling restart — would burn that budget and spam errors on every normal restart.
Non-abort + event is the right shape.

### Alternative 6: Do nothing (manual recovery)

**Description:** Keep recovering stuck leaders with a manual `scale 0→1`.

**Why not:** The failure recurs on every instance refresh with unpredictable
timing, has produced multi-day outages, and silently removes backup-leader
redundancy. It is not self-correcting.

---

## Consequences

### Positive Consequences

- A departing instance can no longer suspend a leader that another live instance
  owns; rolling restarts stop stranding the record in `Suspended`.
- Ownership collisions are impossible by construction — the token is a unique
  transaction digest, so there is no version-tie case to reason about and no clock
  to depend on.
- Stuck-`Suspended` states self-heal within ~60s instead of requiring manual
  intervention, covering both this race and unrelated causes.
- `LeaderSuspensionSkippedEvent` gives on-chain visibility into ownership
  conflicts that was entirely absent during the incident.
- Ownership is derived from on-chain data with no inter-instance coordination,
  shared lease store, or clock plumbing.

### Negative Consequences

- Changes span three layers (Move contract, nexus-sdk idents, leader runtime) and
  require the SDK change to land before the leader compiles against it.
- The activation path must capture the landed activation transaction's digest from
  its receipt and thread it onto `LeaderState`; a bug there leaves `claimed_token`
  stale, which fails _safe_ (a non-matching token simply no-ops the suspend) but
  could delay a legitimate suspend until the next recheck.
- A healthy single instance now issues a status TX on activation and one cheap read
  per recheck interval; a suspended record drives a reclaim TX.

### Neutral Consequences

- The on-chain `Leader` struct layout changes — acceptable only because this ships
  with a registry redeploy and leader re-registration.
- The token is an internal ownership value; `is_active` / `is_eligible` / ranking
  remain keyed on `status` alone and are unaffected.
- Ownership is last-writer-wins, not "newest instance wins": a late-landing
  activation from an older instance can take the token, but this only ever costs a
  ≤60s recheck blip and never a stuck `Suspended`, because suspension stays
  token-guarded and the recheck reclaims.
- A killed owner with no surviving sibling leaves the record `Active` with a dead
  claimer until a replacement instance writes a new token — accepted, and resolved
  by the orchestrator rather than in code.

### Reversibility Assessment

- **Reversibility:** Medium
- **Reversal cost:** Reverting requires backing out the Move field/functions (a
  contract change), the SDK idents, and the runtime wiring. The runtime can fall
  back to the unconditional `set_status` path mechanically, but undoing the
  on-chain field needs a redeploy.
- **Point of no return:** The registry redeploy that introduces the field. After
  that, removing the field is another layout change.

---

## Context Evolution Tracking

### Review Schedule

- **Next review:** After observing leader status stability across several Cloud Run
  rolling restarts and instance refreshes on testnet.
- **Review criteria:** Any recurrence of stuck-`Suspended`; frequency of
  `LeaderSuspensionSkippedEvent` and recheck-driven reclaims in practice; whether
  the 60s recheck interval is appropriately tuned; whether capturing the activation
  digest from the receipt proved robust or warranted switching to a
  leader-generated token (Alternative 3); whether the killed-owner-no-sibling
  window ever bites in a single-instance configuration.

---
