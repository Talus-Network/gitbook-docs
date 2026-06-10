# Gas Service

The concepts related to tokenomics as explained in [the tokenomics section][tokenomics] are implemented in the `GasService` shared object in Nexus.

## Overview

The gas payment and settlement system in Nexus provides a flexible and **two-phase gas locking model** for tool invocations.

Gas is:

1. **Locked before invocation**
1. **Finalized (paid) only after successful execution**
1. **Refunded if execution aborts**

This ensures:

- Tools only get paid for successful invocations.
- Users never permanently lose funds for aborted executions.
- Gas settlement is deterministic and idempotent.
- Offchain actors can verify settlement state.

---

# Core Concepts

## GasService

`GasService` is a shared object that:

- Tracks tool default invocation costs
- Derives `ToolGas`, `ExecutionGas`, and `InvokerGas`
- Coordinates gas locking and settlement

It does **not** hold funds directly — funds live in:

- `ToolGas.vault`
- `InvokerGas.vault`

---

## ExecutionGas

`ExecutionGas` is derived per `DAGExecution`.

It maintains:

- `locked_vertices` → vertices whose gas has been locked
- `tool_cost_snapshot` → price snapshot at execution start
- `claimed_leader_gas` → audit trail for leader claims

### Important Semantics

A vertex being “locked” means:

> Gas has been reserved and the vertex can be invoked once.

It does **not** mean the tool has been paid yet.

Payment happens later via:

```move
finalize_gas_state_for_vertex(...)
```

If execution aborts, locked entries are refunded via:

```move
refund_aborted_execution_gas_for_tool(...)
```

---

## ToolGas

Derived per tool (`tool.fqn()`).

Holds:

- `vault` → collected payments
- `tickets` → prepaid access
- `settings` → extension config

The vault only increases when:

```move
finalize_gas_state_for_vertex(...)
```

is called successfully.

---

## InvokerGas

Derived per invoker address.

Holds gas budgets scoped by:

- Execution
- Worksheet type
- Invoker address

Each budget tracks:

```move
GasFunds {
  bal: Balance<SUI>,
  locked: u64
}
```

`locked` ensures:

- Funds are reserved before invocation
- Funds are reduced only on finalization
- Locked funds can be unlocked on abort

---

# Gas Tickets

Gas tickets represent prepaid access to tool invocations. They are implemented in [the default gas extension][default-gas-extension].

They are stored in `ToolGas.tickets` and can operate in three modes:

## 1. Expiry

Unlimited invocations until:

```move
created_at_ms + valid_for_ms
```

Validation is performed against:

```move
execution.execution_created_at()
```

(not current time).

No funds are locked per invocation.

---

## 2. Limited Invocations

Allows a fixed number of invocations.

Tracks:

```move
total
used
locked
```

Lock phase:

- `locked += 1`

Finalize phase:

- `used += 1`
- `locked -= 1`
- ticket removed if fully consumed

Abort phase:

- `locked -= 1`
- `used` unchanged

This ensures correct accounting across retries and aborts.

---

## 3. Upon Discretion of Tool

Tool owner can revoke at any time.

No internal locking counters.
No automatic accounting.
Used for custom gas strategies.

---

# Scopes

Gas tickets and budgets can be associated with:

1. **Execution Scope**
1. **Agent Scope**
1. **Worksheet Type Scope**
1. **Invoker Address Scope**

The historical generic workflow path searches in this order:

```move
Execution → WorksheetType → InvokerAddress
```

The standard TAP path searches in this order:

```move
Execution → Agent → InvokerAddress
```

Agent scope is keyed by the standard TAP `Agent`. It lets a TAP package or
operator fund repeated execution for an agent without relying on worksheet-type
lookup or the current invoker's budget.

---

# Gas Locking Model

The system follows a strict two-phase model.

---

## Phase 1 — Lock

Triggered via:

```move
lock_gas_state_for_vertex(...)
```

or

```move
lock_gas_state_for_tool(...)
```

Internally calls:

```move
try_lock_gas_state_for_vertex(...)
```

Locking:

1. Attempts to stamp a valid gas ticket.
1. Otherwise attempts to reserve budget.
1. Otherwise marks vertex as Free (if cost is zero).

If successful:

- Entry added to `ExecutionGas.locked_vertices`
- Budget `locked` value increased (if budget used)
- `GasLockUpdateEvent` emitted

Locking is:

- Permissionless
- Idempotent
- Safe to call multiple times

---

## Phase 2 — Finalize (Success Path)

Called after successful tool invocation:

```move
finalize_gas_state_for_vertex(...)
```

Behavior depends on how the vertex was settled:

### Ticket (Expiry / UponDiscretion)

No fund transfer.

### Ticket (LimitedInvocations)

- Decrement `locked`
- Increment `used`
- Remove ticket if exhausted

### Budget

- Reduce `locked`
- Split funds from `bal`
- Transfer to `ToolGas.vault`

Emits:

```move
GasUnlockUpdateEvent { was_refunded: false }
```

---

## Phase 3 — Abort (Failure Path)

Called for aborted executions:

```move
refund_aborted_execution_gas_for_tool(...)
```

For each locked vertex:

### Budget

- Reduce `locked`
- Funds remain in user balance

### Ticket (LimitedInvocations)

- Decrement `locked`
- `used` unchanged

### Ticket (Expiry / UponDiscretion)

No state mutation needed

Emits:

```move
GasUnlockUpdateEvent { was_refunded: true }
```

After all tools are processed:

```move
assert_aborted_execution_fully_refunded(...)
```

can be called as a sanity check.

---

# Gas Payment Modes

## 1. Default Gas Budget

If no ticket applies:

System attempts to reserve from budgets in order:

1. Execution scope
1. Worksheet type scope
1. Invoker address scope

Reservation occurs during lock.
Transfer occurs during finalize.

---

## 2. Gas Extensions

Gas extensions rely on:

- ToolGas settings
- Custom tickets
- Ticket logic

Extensions can:

- Implement time-based access
- Implement subscription models
- Implement metered invocations

---

# Leader Gas

Leaders claim gas for:

- Execution
- Priority
- Pre-key handshake

Functions:

```move
claim_leader_gas(...)
claim_leader_gas_for_self(...)
claim_leader_gas_for_pre_key(...)
```

Leader gas is charged immediately from `InvokerGas`.

Each claim emits:

```move
LeaderClaimedGasEvent {
    network,
    amount,
    purpose
}
```

Claims are recorded in:

```move
ExecutionGas.claimed_leader_gas
```

⚠ Current limitation:
Leader can claim arbitrary amounts.
External observers must validate via events.

---

# Events

## GasLockUpdateEvent

Emitted on lock attempt.

```rust
public struct GasLockUpdateEvent {
    execution: ID,
    vertex: dag::RuntimeVertex,
    tool_fqn: AsciiString,
    was_locked: bool,
}
```

- Multiple events may be emitted
- Only one will have `was_locked = true`

---

## GasUnlockUpdateEvent

Emitted on finalize or refund.

```rust
public struct GasUnlockUpdateEvent {
    execution: ID,
    vertex: dag::RuntimeVertex,
    tool_fqn: AsciiString,
    was_refunded: bool,
}
```

- `was_refunded = false` → successful payment
- `was_refunded = true` → refund after abort

---

## LeaderClaimedGasEvent

```rust
public struct LeaderClaimedGasEvent {
    network: ID,
    amount: u64,
    purpose: AsciiString,
}
```

Used for auditing leader behavior.

---

# Checking Gas Payment Status

## 1. Onchain

Use:

```move
is_execution_vertex_locked(...)
```

If `true`, the vertex can be invoked once.

After finalization, it will no longer appear locked.

---

## 2. Events

Monitor:

- `GasLockUpdateEvent`
- `GasUnlockUpdateEvent`
- `LeaderClaimedGasEvent`

---

# Refunds

Users can reclaim unused funds:

- `refund_execution_gas_budget`
- `refund_invoker_gas_budget`
- `refund_worksheet_gas_budget`

Execution refund transfers remaining unlocked funds to invoker.

Aborted executions require:

```move
refund_aborted_execution_gas_for_tool(...)
```

for each tool involved.

---

# Owner Capabilities

Two caps exist:

## `OverTool`

Full tool control (including vault withdrawal)

## `OverGas`

Restricted to gas management only:

- Add tickets
- Revoke discretionary tickets
- Modify settings

De-escalation:

```move
deescalate(...)
```

---

# Security Considerations

1. Gas is locked before invocation.
1. Tools are paid only after successful execution.
1. Aborted executions must be explicitly refunded.
1. Expiry and Limited tickets cannot be revoked.
1. Leader claims must be externally audited.

---

# Key Semantics Summary

| Stage    | Budget           | Limited Ticket         | Expiry Ticket |
| -------- | ---------------- | ---------------------- | ------------- |
| Lock     | locked += amount | locked += 1            | mark locked   |
| Finalize | transfer to tool | used += 1, locked -= 1 | remove lock   |
| Abort    | locked -= amount | locked -= 1            | remove lock   |

<!-- List of references -->

[tokenomics]: tokenomics.md
[default-gas-extension]: default-gas-extension.md
