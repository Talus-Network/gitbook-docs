# ADR-2: Multi-Coin Gas Payment for the Leader Gas Pool

**Status:** Proposed
**Date:** 2026-06-03
**Authors:** Pavel ([@kouks](https://github.com/kouks))
**Deciders:** Pavel ([@kouks](https://github.com/kouks))
**Consulted:** Engineering Team
**Informed:** Engineering Team

**Constraint Tags:** Technical | Architectural

---

## Context

### What problem are we solving?

The leader pays for Sui transactions from a pool of gas coins it owns. To avoid
equivocation on Sui, only one transaction may use a given gas coin at a time, so
the number of available coins directly bounds our transaction parallelism. Coins
are tracked in Redis (`be/leader/src/store/redis/redis_gas_manager.rs`); today
only the object ID is stored and the balance/version/digest are re-fetched from
Sui on every acquisition.

During execution the leader claims payments from users into separate coins
(`be/leader/src/executor/handlers/walk_execution.rs`). A consolidator loop
(`be/leader/src/merchant/consolidator.rs`) merges these small claimed coins into
coins of at least a configured `gas_coin_min_balance_mist` threshold so they can
be reused to pay for transactions.

With the current logic, the wallet drifts toward many coins each holding roughly
`gas_coin_min_balance_mist`. The consequence: **from time to time a transaction
needs more gas than the balance held on any single coin, and that transaction
fails.** Simply raising the threshold would let those transactions succeed but
would collapse parallelism by producing fewer, larger coins.

### Relevant Constraints

**Technical:** Sui forbids equivocation — a coin in flight in one transaction
must not be used by another. A single Sui transaction may, however, list **up to
256 gas coins**; the protocol "smashes" them, merging all into the first coin to
pay the fee. Transaction effects report `gas_used`, the gas object, and the
changed objects, which is enough to know what happened to the coins without a
follow-up query.

**Architectural:** Coin selection must be driven by the transaction's actual gas
cost, which is only known after a dry run. The merchant already dry-runs before
acquiring a coin (see the dry-run/live submission split), so the budget is known
before coins are picked.

### Architectural Position

This decision affects the **leader gas pool** and the **merchant submission
pipeline**. Rather than sizing coins, we exploit Sui's multi-coin gas payment:
keep many low-balance coins and hand the chain as many as needed to cover a
transaction's budget.

---

## Decision

### What are we doing?

We fund each transaction with **multiple gas coins** and make Redis the source of
truth for coin metadata, updated from transaction effects.

1. **Multi-coin gas payment.** After the dry run computes the gas budget, the
   merchant acquires as many pool coins as needed for their combined balance to
   cover the budget, and submits the transaction listing all of them as the gas
   payment. Sui smashes them into the first coin.

1. **Per-transaction budget cap.** A configurable maximum gas budget (default
   **5 SUI**) bounds a single transaction. It is also the dry-run placeholder
   budget. If the budget computed from the dry run exceeds the cap, the
   transaction fails right after the dry run (fatal). This keeps the number of
   coins any one transaction needs well under the 256 limit, so the pool itself
   may hold arbitrarily many coins.

1. **Redis stores coin metadata.** The gas pool stores `{version, digest,
   balance}` per coin, seeded at startup. After a transaction, effects tell us
   the surviving (first) gas coin's new version/digest and its balance
   (`sum(acquired balances) − effective gas used`); the smashed coins are
   deleted. Redis is updated from this — **the per-acquisition on-chain refresh
   is removed**.

1. **Reconciliation.** Startup seeds the pool; transaction effects keep it
   current on the hot path; the consolidator's existing discovery loop reconciles
   drift and adds newly claimed coins (fetching their metadata once).

1. **Ambiguous failures drop coins.** When a transaction is signed but its
   execution outcome is unknown, the acquired coins are dropped from the pool;
   the discovery loop re-adds them later with fresh on-chain metadata.

1. **Dust floor retained.** `gas_coin_min_balance_mist` stays as the floor below
   which coins are not tracked individually and are left for the consolidator to
   merge.

1. **Consolidator unchanged in spirit.** It still discovers claimed coins and
   merges low-balance ones; it carries no coin-size or distribution logic.

### Why this approach?

Multi-coin gas payment lets a small transaction use one coin and a large one use
many, with no per-coin size ceiling and no rebalancing algorithm — the chain does
the merging at submission. Storing metadata in Redis and updating it from effects
removes a Sui round-trip from every acquisition and removes the coin-refresh code
path. The budget cap gives a single, easily-reasoned-about safety bound. The
result is markedly simpler than maintaining coin-size categories, especially in
the consolidator.

---

## Alternatives Considered

### Alternative 1: Coin size categories (S / M / L / XL)

**Description:** Configure an ascending tuple of MIST thresholds mapped to size
categories. Partition the pool into per-size Redis sets, route each transaction
to the smallest size that can fund it (falling back to larger sizes), and have
the consolidator maintain a target distribution (more small coins, fewer large)
derived from total balance — merging and promoting coins to converge on it.

**Why not:** It is substantially more complex for a strictly worse outcome. Size
selection is coarse (a transaction between thresholds over-provisions to the next
size up); the consolidator needs a bin-packing/promotion algorithm with
equivocation-safe claiming of in-flight coins; and the storage layer fragments
into per-size sets. Multi-coin gas payment achieves the same goal — funding
transactions of any cost while preserving parallelism — without any of this,
because the chain merges coins for us. This was the originally planned design and
was abandoned in favor of the decision above.

### Alternative 2: Raise the single balance threshold

**Description:** Keep one threshold but increase it so coins are always large
enough for expensive transactions.

**Why not:** Fewer, larger coins directly reduce transaction parallelism, which
is bounded by the number of available coins. It trades one failure mode
(insufficient balance) for another (throughput collapse).

### Alternative 3: Single balance-scored sorted set (ZSET)

**Description:** Store all coins in one Redis sorted set scored by balance and
acquire the single smallest coin whose balance meets the budget via an atomic Lua
script.

**Why not:** It still relies on a single coin covering the whole budget, so it
does not solve the large-transaction case any better than raising the threshold;
it only optimizes selection.

### Alternative 4: Do nothing

**Description:** Accept occasional failures of expensive transactions and rely on
retries.

**Why not:** The failures are not self-correcting — the wallet's coin
distribution drifts steadily toward uniform threshold-sized coins, so large
transactions fail increasingly often with no recovery path.

---

## Consequences

### Positive Consequences

- Expensive transactions succeed by combining as many coins as needed, while
  parallelism is preserved through a population of small coins.
- An on-chain query is removed from every gas-coin acquisition; coin metadata
  comes from transaction effects.
- The design is simple: no coin sizes, no distribution algorithm, no per-size
  storage. The consolidator keeps its existing shape.
- A single config value (max gas budget) gives a clear safety bound and a
  fast-fail for pathologically expensive transactions.

### Negative Consequences

- The gas pool and its Redis schema require a non-trivial refactor (storing and
  updating coin metadata, acquiring sets of coins, settling from effects).
- Redis becomes the source of truth for balances/versions; a bug in
  effects-based updates could let it drift until the discovery loop reconciles.
- Dropping coins on ambiguous failure has a small equivocation window if the
  original transaction is still in flight when discovery re-adds the coin
  (mitigated by a short quarantine before re-adding).

### Neutral Consequences

- A transaction may lock several coins at once, momentarily reducing parallelism
  for large transactions — the intended trade-off.
- The pool may contain many coins; only the per-transaction count is bounded (by
  the budget cap and the dust floor), not the pool size.

### Reversibility Assessment

- **Reversibility:** High
- **Reversal cost:** The change is internal to the leader; reverting to
  single-coin acquisition with on-chain refresh is mechanical.
- **Point of no return:** None.

---

## Context Evolution Tracking

### Review Schedule

- **Next review:** After observing transaction success rates and pool size in
  production for a representative period.
- **Review criteria:** Transactions hitting the 256-coin limit despite the budget
  cap; Redis balance drift in practice; need to revisit the budget cap default.

---
