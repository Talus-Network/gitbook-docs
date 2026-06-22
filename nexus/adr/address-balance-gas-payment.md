# ADR-4: Address-Balance Gas Payments (SIP-58) — Removing the Leader Gas Pool

**Status:** Proposed
**Date:** 2026-06-15
**Authors:** Pavel ([@kouks](https://github.com/kouks))
**Deciders:** Pavel ([@kouks](https://github.com/kouks))
**Consulted:** Engineering Team
**Informed:** Engineering Team

**Constraint Tags:** Technical | Architectural

**Supersedes:** [ADR-2: Multi-Coin Gas Payment for the Leader Gas Pool](multi-coin-gas-payment.md)

---

## Context

### What problem are we solving?

The leader pays for Sui transactions from a pool of `Coin<SUI>` gas objects it
owns. Sustaining that pool requires a large, stateful subsystem:

- discovery and seeding of owned coins at startup
  (`be/leader/src/onchain/gas_pool.rs`);
- per-transaction acquisition of enough coins to cover a dry-run budget, plus
  release/quarantine on failure (`be/leader/src/merchant/pipeline.rs`);
- settlement of survivor coins from transaction effects and dropping of smashed
  coins (`be/leader/src/onchain/gas_pool.rs`);
- a Redis source of truth for coin metadata
  (`be/leader/src/store/redis/redis_gas_manager.rs`);
- a consolidator loop that merges small claimed coins into reusable ones
  (`be/leader/src/merchant/consolidator.rs`).

The churn is driven by how the leader is reimbursed. On every verified walk
submission, the user's execution payment reimburses the leader's gas by
**minting a brand-new `Coin<SUI>`** to the leader and transferring it
(`consume_payment_for_verified_leader_submission` →
`settle_nonzero_balance` in `sui/interface/sources/tap.move:1295-1308, 3840-3846`,
which does `public_transfer(coin::from_balance(balance, ctx), leader)`). The pool
then has to re-discover and consolidate those coins to keep them usable. ADR-2
made this workable by paying each transaction with _multiple_ coins and tracking
metadata in Redis, but it kept the entire pool/consolidator/quarantine machinery
in place.

Sui's **address balances** (SIP-58) let a transaction pay gas directly from the
sender's `SUI` address balance, with no gas coin objects at all. If the leader
pays gas from its address balance — and is reimbursed _into_ that balance instead
of into fresh coins — the whole gas-coin subsystem becomes unnecessary.

### Relevant Constraints

**Technical:**

- The pinned `sui-transaction-builder` rejects gas-less transactions:
  `TransactionBuilder::try_build()` returns `Err(MissingGasObjects)` when no gas
  object is set (`builder.rs:322`). However, the `sui_sdk_types::Transaction` it
  returns exposes a **public** `gas_payment: GasPayment` whose
  `objects: Vec<ObjectReference>` field is public
  (`transaction/mod.rs:36-40, 124-138`). We can therefore finish the build with a
  throwaway placeholder gas object and then clear `gas_payment.objects` on the
  returned transaction — no fork or SDK change required.
- SIP-58 requires a transaction paying gas from an address balance to set
  `expiration = TransactionExpiration::ValidDuring { min_epoch, max_epoch,
chain, nonce, .. }` with `min_epoch == max_epoch ==` the current epoch
  (`transaction/mod.rs:90-103`). The leader must fetch the current epoch and the
  chain identifier at submission time and supply a nonce for replay prevention.
- The framework primitive `balance::send_funds<SUI>(balance, recipient)` deposits
  a `Balance<SUI>` directly into the recipient's address balance.

**Architectural:** The transaction's gas budget is only known after a dry run.
The merchant already dry-runs before submission, so the budget is available
before the transaction is finalized.

### Architectural Position

This decision affects the **leader gas pool**, the **merchant submission
pipeline**, and a single **on-chain settlement helper**. Rather than maintaining
a pool of gas coins, the leader pays gas from its address balance and is
reimbursed into that same balance.

---

## Decision

### What are we doing?

We pay transaction gas from the leader's **Sui address balance** and delete the
gas-coin subsystem.

1. **Address-balance gas payment.** The merchant builds each PTB as today, then
   finishes it through a leader-local extension trait
   (`FinishWithAddressBalanceGas` on `sui::tx::TransactionBuilder`): it feeds the
   builder one placeholder gas object to satisfy the builder's non-empty check,
   calls `finish()`, clears `gas_payment.objects` on the resulting transaction,
   and sets a `ValidDuring` expiration pinned to the current epoch with a chain
   digest and a retry-distinct nonce.

1. **Remove the gas pool.** The gas pool, the gas-manager coin methods and Redis
   coin keys, the consolidator process, the quarantine mechanism, and
   effects-based coin settlement are deleted. Payment-lock storage (per
   `(execution, vertex)`) is unrelated to gas coins and is retained.

1. **Reimburse into the address balance.** Only the leader-reimbursement path
   changes on-chain: `consume_payment_for_verified_leader_submission` settles the
   charged balance via `balance::send_funds<SUI>` into the leader's address
   balance instead of minting and transferring a new coin. Payer/user refunds and
   tool-owner/collateral claims continue to materialize coins.

1. **Funding and observability.** The operator funds the leader's address balance
   out-of-band. The leader adds a read-only startup check that warns or fails
   below a configurable floor (`SUI_MIN_ADDRESS_BALANCE_MIST`) and a periodic task
   that exports the current address balance as a gauge
   (`leader_address_balance_mist`). Auto-converting owned coins into the address
   balance at startup is left as a documented TODO.

### Why this approach?

Address-balance gas removes the root cause of the pool's existence: there are no
gas coins to size, select, smash, settle, consolidate, or quarantine, and no
per-transaction coin-count ceiling. The builder limitation is worked around with
a few lines against public types, so no SDK fork or multi-repo lockstep is
needed. Scoping the on-chain change to the leader-reimbursement path keeps the
blast radius minimal and avoids changing behavior for external payers and tool
owners, who may not be able to redeem funds from an address balance.

---

## Alternatives Considered

### Alternative 1: Keep the multi-coin gas pool (ADR-2)

**Description:** Retain the pool, paying each transaction with as many coins as
needed and tracking metadata in Redis.

**Why not:** ADR-2 is a sophisticated solution to a problem that address balances
remove entirely. It keeps a large stateful subsystem (pool, consolidator,
quarantine, effects settlement, Redis schema) with its own failure modes —
balance drift, equivocation windows on re-add, the 256-coin per-transaction
limit. Address balances make all of it unnecessary.

### Alternative 2: Put the builder bypass in the SDK

**Description:** Add the address-balance finish helper to the sibling `nexus-sdk`
`sui` wrapper so it is reusable across repos.

**Why not:** The bypass uses only public `sui_sdk_types` fields and compiles
locally in the leader crate. Putting it in the SDK would require the SDK-spanning
workflow (path-link, push a branch, switch back) for a change that does not need
it. It can be promoted to the SDK later if another consumer appears.

### Alternative 3: Route all settlement paths to address balances

**Description:** Change `settle_nonzero_balance` in place so refunds,
tool-owner claims, and collateral also deposit into address balances.

**Why not:** Recipients of address-balance funds must be able to redeem them or
pay gas from them. The leader gains that capability; arbitrary payers, users, and
tool owners may not, and silently moving their funds out of coin objects is a UX
regression and an SDK-compatibility risk for external integrators. We add a
second helper and switch only the leader path, leaving the rest byte-identical.

### Alternative 4: Auto-convert owned coins into the address balance at startup

**Description:** On boot, deposit the leader's owned `Coin<SUI>` into its address
balance via `send_funds` so the leader is self-funding.

**Why not (now):** It depends on the framework `send_funds` entry being exposed
through the SDK idents, which may require an SDK change. External funding plus a
startup balance check is sufficient for the first cut; auto-conversion is recorded
as a follow-up TODO.

---

## Consequences

### Positive Consequences

- A large, stateful, failure-prone subsystem (pool, manager coin state,
  consolidator, quarantine, effects settlement) is deleted.
- No per-transaction gas-coin ceiling and no coin-distribution drift; gas
  payment is stateless and needs no current object references.
- The on-chain change is a single, surgical settlement-sink switch with no impact
  on payer/user refunds or tool-owner claims.

### Negative Consequences

- The gas payment relies on a builder bypass (clearing `gas_payment.objects` on
  the returned transaction); a future `sui-transaction-builder` change to those
  public fields could require revisiting it.
- The network must have the address-balance / funds-accumulator protocol feature
  enabled, and the leader's address balance must be funded out-of-band; an empty
  balance halts submissions.
- The leader must fetch the current epoch and chain identifier per submission and
  derive a nonce, adding a small RPC dependency to the hot path (epoch can no
  longer be assumed static across the process lifetime).

### Neutral Consequences

- Reimbursements no longer appear as coins in the leader's wallet; they accrue in
  the address balance, observed via the new gauge.

### Reversibility Assessment

- **Reversibility:** Medium
- **Reversal cost:** The offchain change is internal to the leader and mechanical
  to revert. The on-chain settlement switch is the stickier part: reverting it
  after funds have accrued in address balances requires a deliberate migration
  back to coin materialization.
- **Point of no return:** None in code; operationally, once reimbursements flow
  to the address balance, reverting requires draining/redeeming that balance.

---

## Context Evolution Tracking

### Review Schedule

- **Next review:** After e2e confirms address-balance gas on localnet and after
  observing the leader's address-balance drawdown over a representative period in
  a real deployment.
- **Review criteria:** The builder bypass holding across SDK bumps; address-
  balance protocol availability on target networks; whether external funding plus
  the startup check is operationally sufficient or auto-conversion is warranted.
