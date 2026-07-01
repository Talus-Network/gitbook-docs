# ADR-5: Auto-Abort of Expired DAG-Walk Executions

**Status:** Proposed
**Date:** 2026-06-25
**Authors:** Pavel ([@kouks](https://github.com/kouks))
**Deciders:** Pavel ([@kouks](https://github.com/kouks))
**Consulted:** Engineering Team
**Informed:** Engineering Team

**Constraint Tags:** Technical | Architectural | Operational

---

## Context

### What problem are we solving?

A DAG execution runs as a set of concurrent **walks**. Each active walk pins a
`next_vertex` and a deadline: on-chain it is `created_at + timeout_ms * 2`
(`sui/workflow/sources/execution.move` → `DAGWalk::Active`,
`is_active_walk_expired`). Off-chain, the same walk is distributed to leaders
with a matching deadline budget: the `RequestWalkExecution` event carries
distribution metadata (`requested_at`, `deadline`, an ordered `leaders` vector),
and `Distribution::decide` (`be/leader/src/onchain/distribution.rs`) computes
`deadline_at = requested_at + deadline` (the primary's window) and
`double_deadline_at = deadline_at + deadline` (the backup's window). The latter
coincides with the on-chain `created_at + timeout_ms * 2` expiry.

The on-chain contract already provides a permissionless way to clear an expired
walk — `execution_resolution::abort_expired_execution` and, when the expired
vertex still holds a locked TAP payment, `gas_extension::abort_expired_execution_with_tool_gas`
— and the nexus-sdk already exposes builders for both. Our e2e tests exercise
these by submitting the abort by hand.

**No production leader code ever calls them.** When a walk passes
`double_deadline_at` without being evaluated, `Distribution::decide` returns
`Ignore` and the leader simply forgets the walk. Nothing on chain advances:

- the walk stays `Active` forever,
- the vertex's TAP payment stays **locked** (the invoker's funds are stuck),
- `ExecutionFinished` is never emitted, so the execution never settles or
  refunds.

### Impact

Every walk that a primary fails to evaluate and a backup does not pick up leaves
a permanently stalled execution with funds locked on chain. This is silent — no
leader is responsible for the cleanup — and only resolves through manual,
out-of-band abort submission. As walk timeouts are routine (slow tools, leader
restarts, transient failures), this is a recurring source of stuck executions
and trapped invoker funds rather than a rare edge case.

### Relevant Constraints

**Technical:** The abort entries are **permissionless** — they take the
`leader_registry` for bookkeeping but require no leader capability, and the Move
code re-checks `is_active_walk_expired` itself, so an abort against an
already-resolved or not-yet-expired walk is a safe no-op/rejection rather than a
corruption risk. The leader already has, for every walk it handled, the data
needed to identify it: the `DAGExecution` id and the `walk_index`. It also
already tracks which vertices have locked payments (`save_gas_lock` on
`PaymentLockUpdate`), which is exactly the signal that decides plain-vs-tool-gas
abort. The leader pays its own gas via address-balance gas
(`finish_with_address_balance_gas`); an abort **refunds** the invoker, so there
is no execution payment to recoup the abort's gas from.

**Architectural:** The leader's submission path is the merchant pipeline: every
outbound transaction is a `NexusTransactionKind` variant implementing
`TransactionLike` (build the PTB, declare capabilities, run a `preflight` that
may `Skip`, finish with gas). Transactions are delivered through a Redis-backed
**scheduled high-integrity channel** that (a) can defer a payload to a wall-clock
time (`ScheduleSpec::at`), (b) deduplicates by the payload's `Identifiable::id()`,
and (c) **survives process restart** — a scheduled item persists in Redis and
fires after a restart. The event listener already holds both the event sender
and this merchant sender.

That channel, however, **bounds retries**: a transaction is attempted at most
`MERCHANT_MAX_RETRIES + 1` times (default 4) with only immediate / fixed-500ms
backoff, and on exhaustion it is **permanently deleted** from Redis — there is no
dead-letter queue and no retry-forever path (the drop is centralized in the
scheduler queue discipline, `be/leader/src/channel/scheduler/queue.rs`, in
`on_nack` and `on_enqueue`). During a multi-hour chain outage every submission
attempt fails transiently, so an abort would exhaust its budget within minutes
and be dropped — leaving the execution stalled exactly as before. The fix must
therefore make the abort **retry until it lands**, not just retry a few times.

**Operational:** Leaders restart routinely (Cloud Run instance refreshes — see
[ADR-3](leader-status-ownership-versioning.md)). Any abort mechanism must keep
working across a restart without re-deriving in-flight state from scratch, and
must not depend on a clean shutdown. There is no on-chain index of "all active
executions assigned to me," so enumerating every expired walk from chain is not
cheaply available.

### Architectural Position

This decision adds an **abort responsibility** to the leader's existing walk
lifecycle. It spans the distribution decision (`onchain/distribution.rs`), the
event listener (`onchain/listener.rs`), and the merchant transaction set
(`merchant/transaction.rs`, a new `executor/handlers/abort_expired.rs`). It is
purely off-chain leader behavior — no Move or SDK change — because the on-chain
entries and SDK builders already exist.

---

## Decision

### What are we doing?

For every walk a leader is responsible for, the leader **arms a deferred
abort-check transaction** at the walk's double-deadline, reusing the existing
Redis-backed scheduled merchant channel. When the abort-check fires, it re-reads
chain state and either aborts the still-expired walk or no-ops if the walk has
since resolved.

1. **New transaction kind `AbortExpiredExecution`.** A `NexusTransactionKind`
   variant (params in `executor/handlers/abort_expired.rs`, modeled on
   `ExecuteScheduledOccurrenceTxParams`) carrying the `DAGExecution` id and
   `walk_index`. Its `Identifiable::id()` is `abort-expired-{execution}-{walk_index}`
   — distinct from event ids and execute transactions, and stable so the channel
   deduplicates redundant arming.

1. **Self-verifying preflight.** Before submission the merchant runs
   `preflight`, which fetches the `DAGExecution`, indexes `walks[walk_index]`,
   and calls `DagExecutionWalk::expired_active_vertex(now)` against a trusted
   `CheckpointClock` snapshot. If the walk is no longer an expired active walk
   (it advanced, failed, was aborted, cancelled, or is already pending-abort) the
   transaction returns `PreflightOutcome::Skip` and never hits the chain. This is
   how "if the walk resolved, drop it" is realized — no explicit cancellation is
   needed.

1. **Plain-vs-tool-gas chosen at fire time.** When the expired vertex still holds
   a locked payment (per the gas-lock store), `preflight` resolves the relevant
   `ToolGas` object references and `into_sui_tx_data` emits one
   `abort_expired_execution_with_tool_gas` call per `ToolGas` (unlocking/refunding
   the vertex payment before recording abort intent); otherwise it emits the
   plain `abort_expired_execution`. Resolving this at fire time — not at arm time
   — keeps the decision correct even as lock state changes during the window.

1. **Leader sponsors the abort gas.** `is_sponsored()` returns `true`: the abort
   refunds the invoker, so there is no execution payment to recoup from, and the
   leader eats the gas (like `ActivateLeader`/`RequestCapability`).

1. **Arming, at decision time, in the listener.** `Distribution` gains a sibling
   helper `abort_schedule(event, claimed_token)` (leaving `decide` and
   `HandlingDecision` untouched). It returns an abort-check to arm **iff** the
   event is an abortable walk event (`RequestWalkExecution`, or the inner request
   of `RequestScheduledWalk`), this instance is the current claim owner
   ([ADR-3](leader-status-ownership-versioning.md)), and this instance's leader
   cap is in the event's `leaders` vector. The fire time is
   `double_deadline_at` plus a position-dependent grace stagger (see item 6 —
   the primary fires at `+auto_abort_grace_period`). The listener schedules the
   resulting `AbortExpiredExecution` onto the merchant channel via
   `ScheduleSpec::at(...)`, behind a config toggle.

1. **Any tracking leader may abort, staggered by position.** Both the primary
   (`leaders[0]`) and backup (`leaders[1]`) arm the abort, but the fire time is
   staggered by the leader's position in the distribution vector: the primary
   fires at `double_deadline_at + grace`, the backup at `double_deadline_at +
   2*grace` (position `n` at `+ (n+1)*grace`). Staggering means the primary
   normally lands the abort first and the backup's copy self-skips, so the two
   do not submit competing transactions against the same shared execution object
   at the same instant (which would otherwise cause transient version-conflict
   errors). The Move call is permissionless and self-rejects once the walk is no
   longer active+expired, so the backup's copy is harmless whether it skips or
   lands. This still maximizes liveness: if the primary is down, the backup
   aborts one `grace` window later.

1. **Durable retry through chain outages.** The merchant channel normally drops a
   transaction after `MERCHANT_MAX_RETRIES` attempts; for the abort that would
   lose the cleanup during a long outage. We add an **opt-in unbounded-retry
   policy to the scheduler core**: a payload may declare
   `RetryPolicy::Unbounded { base_ms, cap_ms }` (via a new `Schedulable::retry_policy()`,
   default `Bounded`), carried in the `SchedulerHint` and persisted on the
   `SchedulerMetadata`. For such a message, the queue discipline
   (`queue.rs::on_nack`/`on_enqueue`) **never deletes on exhaustion** and instead
   re-schedules it with **capped exponential backoff**
   (`min(cap_ms, base_ms * 2^attempts)`, defaults base 1s / cap 5min,
   configurable). The next-ready time is persisted in Redis, so the backoff
   survives restart. The `AbortExpiredExecution` tx opts into this policy; all
   other transactions are unchanged (`Bounded`). The retry loop terminates by
   construction: once the walk resolves, `preflight` returns `Skip` (which
   **acks** and removes the message); a deterministic on-chain failure is `Fatal`
   (also acks); only transient/chain-down failures back off and retry. So an
   abort retries every ≤5min until the chain recovers and the abort lands or the
   walk is otherwise resolved.

   For this to hold, the merchant pipeline must classify an **unreachable Sui**
   as a transient (retryable) failure, never `Fatal` — a `Fatal` acks and drops
   the message. The pipeline already does this: every RPC-connectivity boundary
   (gRPC client construction, submission-context fetch, dry-run simulation, and
   the live execute-and-wait) returns a transient error, while the only `Fatal`
   paths are deterministic (transaction-data conversion errors and dry-run
   rejections the chain actually executed and returned). We keep this invariant:
   the abort's `preflight` (and its preflight-time ref resolution) surfaces RPC
   failures as transient errors and never as `Skip`, and `into_sui_tx_data` does
   no network I/O.

1. **Best-effort restart coverage.** Scheduled abort-checks persist in Redis and
   fire after a restart, so a leader that armed an abort before crashing still
   aborts after coming back. Replayed terminal events keep the rest of the store
   consistent. We do **not** enumerate chain state to abort walks the leader
   never armed.

### Why this approach?

The scheduled channel already solves the hard parts of this problem — durable
deferral to a wall-clock deadline, deduplication, and restart survival — so the
abort rides it as just another transaction kind. The `preflight`/`Skip`
machinery already exists for exactly this shape (see
`ExecuteScheduledOccurrenceTxParams`, which skips stale scheduled occurrences),
so "abort only if still expired" needs no new control flow and no per-walk
bookkeeping to tear down. Keeping `decide` unchanged and adding a parallel
`abort_schedule` avoids forking the decision logic across its two call sites
(the listener and `decide_task_handling`), which is where subtle distribution
bugs hide. The result is additive: no Move change, no SDK change, no new
long-running task, and a single feature flag to disable it.

---

## Alternatives Considered

### Alternative 1: Background reaper over the persistent task store

**Description:** Persist every owned walk in the Redis task store, and run a
periodic background task that scans the store, computes each walk's
double-deadline, fetches the `DAGExecution` for those past it, and submits an
abort for any still expired. Resolution is handled by the existing terminal-event
`drop_walk_task` cleanup; restart re-enumerates the persistent store.

**Why not:** It is a strictly larger surface for the same outcome. It introduces
a new always-on loop, broadens task-store writes to every walk (today only the
single-leader-primary and backup branches persist), adds a `list_tasks`
enumeration method, and pays a periodic RPC cost to poll chain state. The
scheduler-reuse approach gets durable timing and restart survival from
infrastructure we already run, with no polling. The reaper's one genuine
advantage — re-deriving tracking purely from the store on restart — is matched
closely enough by the scheduled channel's own Redis persistence. Worth
reconsidering if we later need coverage of walks the leader never armed (see
Alternative 3).

### Alternative 2: New `HandlingDecision::AbortExpired` variant threaded through `decide`

**Description:** Rather than a sibling helper, extend `HandlingDecision` with
abort-bearing variants (e.g. `ExecuteNowThenAbort`, `WaitThenAbort`,
`AbortExpired`) and rewrite the `decide` match arms so the doubly-expired
branches produce an abort instead of `Ignore`.

**Why not:** `decide` is invoked from two places (the listener and the consumer's
`decide_task_handling`) that must agree; the consumer path would need new arms to
map the abort variants back to execute/ignore, and any drift between the two call
sites silently breaks distribution. A second scheduled **event** delivery is also
awkward because the channel deduplicates by event id and would collide with the
in-flight execute delivery. Producing a distinct **transaction** (different id,
merchant channel) and computing it via a side helper sidesteps both problems.

### Alternative 3: Full on-chain enumeration of assigned expired walks

**Description:** On startup (and/or periodically) enumerate all in-flight
executions assigned to this leader from chain and abort any expired walk —
including walks this leader never observed (e.g. created before the feature
shipped, or during an outage).

**Why not:** There is no cheap on-chain index of active executions assigned to a
leader, so this requires significant query machinery and ongoing RPC cost for a
small tail. We explicitly accept best-effort coverage for now. This remains the
upgrade path if the uncovered tail proves material in practice.

### Alternative 4: Restrict abort to the primary, with a backup fallback window

**Description:** Only `leaders[0]` arms the abort at the double-deadline; the
backup waits a further grace window (e.g. a triple-deadline) before attempting,
mirroring the primary/backup execution handoff.

**Why not (and what we shipped):** A full primary-only handoff with a large
extra fallback window adds windowing complexity and latency before a down
primary's walks get cleaned up. Instead we ship a lightweight middle ground:
both leaders arm, but staggered by one `grace` window per position (primary at
`+grace`, backup at `+2*grace`). The stagger gives the primary first attempt —
so the backup's permissionless copy almost always self-skips rather than racing
the primary on the shared execution object — while still falling back to the
backup just one `grace` window later if the primary never lands it. This keeps
liveness without the same-instant version-conflict races that arming both at the
identical time would cause.

### Alternative 5: Bounded retry tweaks instead of an unbounded policy

**Description:** To survive outages, either (a) raise `MERCHANT_MAX_RETRIES` to a
large value, or (b) keep the scheduler core untouched and have the abort tx
re-arm itself on transient failure by scheduling a fresh delivery (a distinct
"epoch" id) at `now + backoff` before it can be dropped.

**Why not:** (a) is global (affects every transaction class), still finite, and
hammers the RPC with the current near-zero backoff — not "until success." (b)
works but builds bespoke retry bookkeeping outside the scheduler (epoch ids,
ack-then-reschedule crash windows, its own backoff state) and is not reusable.
Adding a first-class `RetryPolicy::Unbounded` to the scheduler keeps one message
identity, reuses the existing Redis-persisted ready-time/backoff machinery, has a
clean restart story, and is opt-in so bounded transactions are unaffected — and
it becomes a capability any future durable transaction can use.

### Alternative 6: Do nothing (manual abort)

**Description:** Keep clearing stalled expired executions by submitting aborts
out of band.

**Why not:** Walk timeouts are routine, the failure is silent, and it traps
invoker funds until a human intervenes. It does not self-correct.

---

## Consequences

### Positive Consequences

- Expired walks are cleared automatically: the execution settles/refunds, locked
  invoker funds are released, and `ExecutionFinished` is emitted instead of the
  execution stalling forever.
- No on-chain or SDK change — the feature is entirely additive leader behavior
  over existing Move entries, SDK builders, and channel infrastructure.
- Restart-resilient by construction: armed aborts persist in Redis and fire after
  a restart, with no dependence on a clean shutdown.
- Survives prolonged chain outages: the abort retries with capped exponential
  backoff until it lands (or the walk resolves), instead of being dropped after
  the merchant's bounded retries. The new `RetryPolicy::Unbounded` is reusable by
  any future durable transaction.
- Liveness under leader failure: a down primary no longer blocks cleanup because
  the backup arms the same abort.
- Disable-able via a single config toggle for safe rollout.

### Negative Consequences

- An abort-check is armed for **every** owned walk, including walks that complete
  normally; those fire at the double-deadline and incur a chain read in
  `preflight` before Skipping. This is wasted work proportional to throughput
  (mitigated by the dedup id and the Skip-without-submission path; a future
  optimization could cancel armed aborts on terminal events if the channel grows
  a cancel API).
- Walks of the same execution each arm their own abort; the first to land aborts
  all currently-expired walks, and later firings no-op via Skip — bounded
  redundancy, but redundancy nonetheless.
- Distinct leaders (primary and backup, separate Redis) both arm an abort, but
  staggered by one `grace` window per position so the primary fires first and the
  backup's copy usually self-skips. In the rare overlap (primary lands within the
  stagger window) the backup's copy is a rejected/Skipped no-op — at most a little
  extra gas on the loser, not a same-instant version-conflict race.
- The unbounded-retry policy modifies the shared scheduler core
  (`channel/scheduler/`). The change is guarded so bounded transactions keep
  their exact current drop-on-exhaustion behavior, but it widens the blast radius
  of this work beyond the abort path and needs its own focused tests.
- An `Unbounded` message never self-expires: it stops only on `Skip`/success/
  `Fatal`. For the abort this is the intended behavior (resolution always
  produces a `Skip`), but it means a bug that never produces a terminal outcome
  would retry indefinitely — bounded only by the ≤5min cap, and observable via
  the backoff metrics/logs.
- **Gas-griefing vector (accepted risk).** The abort is permissionless and
  **leader-sponsored** (`is_sponsored() == true`): the leader pays the abort gas
  from its own address balance while the invoker's execution payment is fully
  refunded. There is **no per-invoker or aggregate cap** on how many aborts a
  leader will arm/fire. An actor can therefore create executions and deliberately
  let their walks expire, draining a small amount of leader gas per abort while
  getting refunded. We accept this for now: the alternative — leaving expirations
  unaborted — is the status-quo failure this ADR exists to fix (stalled
  executions, indefinitely locked invoker funds), and refusing the abort would
  not recover the gas anyway. The per-abort gas cost is small, and abuse is
  observable: the `leader_auto_abort_armed_total` counter (and the
  `leader_auto_abort_outcomes_total` breakdown) make an anomalous arming rate
  visible. **Mitigation: alert on the armed-total rate** (see Review criteria); if
  abuse becomes material, follow-ups include rate-limiting arming per invoker,
  charging abort gas against the refund, or an on-chain expiry deposit — none of
  which are needed for the initial rollout.

### Neutral Consequences

- Best-effort coverage only: walks armed before the feature shipped, or lost to a
  crash between `abort_schedule` and the `schedule` call, are not aborted. Accepted
  (Alternative 3 is the upgrade path).
- The abort is sponsored by the leader (`is_sponsored() == true`); abort gas is
  not recouped, consistent with refunding the invoker.
- `decide` and `HandlingDecision` are unchanged; the abort is an independent,
  parallel concern.

### Reversibility Assessment

- **Reversibility:** High
- **Reversal cost:** Set `EXECUTOR_AUTO_ABORT_EXPIRED_ENABLED=false` to disable
  at runtime; fully reverting removes a transaction kind and a listener call with
  no on-chain or migration impact.
- **Point of no return:** None — no schema, contract, or persisted-format change.

---

## Context Evolution Tracking

### Review Schedule

- **Next review:** After observing auto-abort behavior on testnet across normal
  walk timeouts and at least one leader rolling restart.
- **Review criteria:** Whether expired executions reliably clear and funds
  unlock; the volume of `preflight`-Skipped abort-checks (cost of arming for
  every walk) and whether a cancel-on-terminal optimization is warranted; the
  rate of redundant cross-leader aborts; whether the best-effort coverage gap
  bites in practice (motivating Alternative 3); whether `auto_abort_grace_period`
  and the retry base/cap backoff are tuned correctly; whether the unbounded-retry
  policy behaves well in a real outage (aborts land promptly on recovery, no
  runaway retry loops, bounded transactions unaffected).
- **Required alert:** wire an alert on the **rate** of
  `leader_auto_abort_armed_total` (and watch `leader_auto_abort_outcomes_total`):
  a sustained spike signals either a systemic execution failure or the
  gas-griefing vector above. Alerts live outside this repo (the leader only
  exposes `/metrics`); this is an operational follow-up to configure where the
  fleet's Prometheus rules are managed. Revisit whether a per-invoker arming cap
  or charging abort gas to the refund is warranted based on what the alert shows.

---
