# Gas Service

<!-- Gitbook syntax -->
{% hint style="warning" %} The documentation provided here documents code that is currently implemented in the Nexus onchain packages but not yet in the offchain leader node.

Consequently, these concepts are not enforced as of yet and serve only as informational purpose for future reference. {% endhint %}

## Overview

The gas payment and settlement system in Nexus provides a flexible way to handle gas payments for tool invocations. It supports multiple modes of operation and allows for different payment strategies through gas extensions.

## Core Concepts

### Gas Service

The `GasService` is a shared object that manages all gas-related operations. It maintains:
- Gas tickets for tools.
- Gas budgets for different scopes.
- Execution gas settlement state.
- Tool-specific gas settings.

### Gas Tickets

Gas tickets represent prepaid access to tool invocations. They can be configured with different modes of operation:

1. **Expiry Mode**: Allows unlimited invocations within a specific time period.
2. **Limited Invocations Mode**: Allows a fixed number of invocations.
3. **Upon Discretion of Tool Mode**: Tool owner has complete control over ticket validity.

### Scopes

Gas tickets and budgets can be associated with different scopes:

1. **Execution Scope**: Specific to a single DAG execution.
2. **Worksheet Type Scope**: Applies to all executions of a specific worksheet type, i.e. the SAP.
3. **Invoker Address Scope**: Applies to all executions initiated by a specific address.

{% hint style="warning" %} Gas is secured before the tool is invoked to ensure that the tool always gets paid for its usage according to the selected mode.

This does expose the tool owner to slashing risk, if they do not deliver the service according to the Nexus defined protocol. {% endhint %}

### Other Data Structures

#### ExecutionGas
Tracks gas settlement state for a specific DAG execution. This struct maintains a record of which vertices in the execution have had their gas settled. Once a vertex is marked as settled, it can be invoked once.

#### GasBudgets
Manages gas budgets for different scopes in the system. The inner Bag stores balances of SUI coins, with the key being a Scope. These budgets are used as a fallback payment method when no gas tickets are available. See [Default Gas Budget](#1-default-gas-budget).

#### ToolGas
Manages all gas-related state for a specific tool. This includes:
- Collected gas payments in the vault
- Default cost per invocation
- Tool-specific gas settings
- Available gas tickets for different scopes

## Gas Payment Modes

### 1. Default Gas Budget

Tools can set a default cost per invocation. When no gas tickets are available, the system will attempt to charge from the gas budget in the following order:
1. Execution-specific budget
2. Worksheet type budget
3. Invoker address budget

### 2. Gas Extensions

Gas extensions provide alternative payment strategies. The default extension ([`default_gas_extension`][default-gas-extension]) implements an expiry-based system where users can:
- Buy access for a specific duration (e.g., 10 minutes).
- Pay a fixed rate per minute.
- Get unlimited invocations during the purchased period.

## Gas Settlement Process

1. When a vertex (tool) is invoked, the system checks if gas has been settled.
2. If not settled, it attempts to find a valid gas ticket for the different scopes in order.
3. Gas tickets are validated against the execution's creation timestamp, not the current time.
4. If no valid ticket is found, it attempts to charge from the gas budget.
5. Once settled, the vertex can be invoked.
6. Gas settlement is idempotent - subsequent checks won't charge again.

### Events

The system emits several types of events for gas-related operations:

1. `GasSettlementUpdateEvent` for each gas settlement attempt:
```rust
public struct GasSettlementUpdateEvent has copy, drop {
    execution: ID,
    vertex: dag::Vertex,
    tool_fqn: AsciiString,
    /// Whether the gas ticket was stamped ok.
    ///
    /// Multiple of these events can be emitted for the same execution/vertex/tool_fqn
    /// combination, but only one of them will have this field set to true.
    was_settled: bool,
}
```

2. `LeaderClaimedGasEvent` for tracking gas claims by leaders:
```rust
public struct LeaderClaimedGasEvent has copy, drop {
    /// Who is the leader.
    network: ID,
    /// How much was claimed.
    amount: u64,
}
```

### Checking Gas Payment Status

There are several ways to check if gas has been paid for a tool invocation:

1. **Using GasService State**
   - Anyone can check if gas has been settled for a specific vertex in an execution using [`is_execution_vertex_settled`](#view-operations).
   - This is useful both for onchain and offchain actors.
   - This is the most direct way to verify gas payment status.
   - Returns a boolean indicating whether the vertex can be invoked.

2. **Listening to Events**
   - The system emits `GasSettlementUpdateEvent` for each gas settlement attempt.
   - Anyone can listen to these events to track gas settlement status.

3. **Checking Gas Tickets**
   - Tool owners can check their tool's gas tickets and settings.
   - Users can check their own gas budgets and tickets.
   - This is useful _before_ the invocation is requested to know whether it's possible to execute with given gas tickets.

4. **Viewing Gas Budgets**
   - Users can check their remaining gas budgets for different scopes.
   - This is useful _before_ the invocation is requested to know whether it's possible to execute with given gas budgets.

## Security Considerations

1. Gas tickets with expiry or limited invocations cannot be revoked.
2. Only tickets in "Upon Discretion of Tool" mode can be revoked.
3. Tool owners can claim gas at any time.
4. Gas budgets can be refunded if the execution is finished. 
5. Workflows that want to pay gas on behalf of the user must assert that they execute in a network with a trusted leader. See [current limitation below](#current-limitation)

### Current limitation

In the current implementation the Nexus leader can claim any amount of gas it wants from anybody who uploads gas budgets.
To hold the leader accountable we emit `LeaderClaimedGasEvent` event which can be read by 3rd parties that check that the amount claimed is not over the top.

However, this implies that as of right now, the leader is has to be trusted.

## Key Operations

<details>
<summary>Tool Owner Operations</summary>

### Gas Cost Management

1. **Setting Default Cost**
   Sets the default cost in MIST for a single tool invocation. Calling this function enables gas collection by the tool so it's imperative the tool owners calls it to collect fees for tool execution.

   ```rust
   public fun set_single_invocation_cost_mist(
       gas_service: &mut GasService,
       tool_registry: &ToolRegistry,
       owner_cap: &CloneableOwnerCap<OverGas>,
       fqn: AsciiString,
       single_invocation_cost_mist: u64,
       ctx: &mut TxContext,
   )
   ```
   > Set `single_invocation_cost_mist` to 2^64-1 to enable gas collection but require a gas extension to do it.

1. **Claiming Gas**
   Allows the tool owner to withdraw all collected gas payments for their tool.

   ```rust
   public fun claim_gas(
       gas_service: &mut GasService,
       tool_registry: &ToolRegistry,
       owner_cap: &CloneableOwnerCap<OverTool>,
       fqn: AsciiString,
       ctx: &mut TxContext,
   ): Balance<SUI>
   ```

### Gas Ticket Management

1. **Adding Gas Tickets**
   Creates a new gas ticket with specified scope and mode of operation.

   ```rust
   public fun add_gas_ticket(
       gas_service: &mut GasService,
       tool_registry: &ToolRegistry,
       owner_cap: &CloneableOwnerCap<OverGas>,
       fqn: AsciiString,
       scope: Scope,
       modus_operandi: ModusOperandi,
       clock: &Clock,
       ctx: &mut TxContext,
   )
   ```

The tool owner can use "upon discretion of the tool" mode to be able to `revoke_gas_ticket` _at will_.

2. **Revoking Gas Tickets**
   Revokes a gas ticket that was created with the "Upon Discretion of Tool" mode.

   ```rust
   public fun revoke_gas_ticket(
       gas_service: &mut GasService,
       tool_registry: &ToolRegistry,
       owner_cap: &CloneableOwnerCap<OverGas>,
       fqn: AsciiString,
       scope: Scope,
       ctx: &mut TxContext,
   )
   ```

3. **Managing Gas Settings**
   The tool owner can set the gas settings for the tool.

   ```rust
   public fun get_tool_gas_setting_mut(
       gas_service: &mut GasService,
       tool_registry: &ToolRegistry,
       owner_cap: &CloneableOwnerCap<OverGas>,
       fqn: AsciiString,
       ctx: &mut TxContext,
   ): &mut Bag
   ```

4. **De-escalating Permissions**
   Converts a tool owner cap into a gas owner cap with reduced permissions.

   ```rust
   public fun deescalate(
       tool_registry: &ToolRegistry,
       owner_cap: &CloneableOwnerCap<OverTool>,
       fqn: AsciiString,
       ctx: &mut TxContext,
   ): CloneableOwnerCap<OverGas>
   ```

</details>

<details>
<summary>User Operations</summary>

### Gas Budget Management

1. **Donating to Tool**
Donate given balance to the tool's gas total. This is used to charge the user from gas extensions and make it available to the tool.

```rust
public fun donate_to_tool(
    self: &mut GasService, fqn: AsciiString, amount: Balance<SUI>,
) {
    let tool_gas = self.tools_gas.borrow_mut(fqn);
    tool_gas.vault.join(amount);
}
```

1. **Adding Gas Budget**
   Adds a gas budget for a specific scope (execution, worksheet type, or invoker address).

   ```rust
   public fun add_gas_budget(
       gas_service: &mut GasService,
       scope: Scope,
       budget: Balance<SUI>,
   )
   ```

1. **Refunding Execution Gas Budget**
   Refunds any remaining gas budget for a completed execution to the invoker. This operation also cleans up storage by removing the execution gas state, helping to reduce storage costs.

   ```rust
   public fun refund_execution_gas_budget(
       gas_service: &mut GasService,
       execution: &dag::DAGExecution,
       ctx: &mut TxContext,
   )
   ```

1. **Refunding Invoker Gas Budget**
   Refunds any remaining gas budget associated with the invoker's address.

   ```rust
   public fun refund_invoker_gas_budget(
       gas_service: &mut GasService,
       ctx: &mut TxContext,
   ): Balance<SUI>
   ```

1. **Refunding Worksheet Gas Budget**
   Refunds any remaining gas budget associated with a specific worksheet type.

   ```rust
   public fun refund_worksheet_gas_budget<T>(
       gas_service: &mut GasService,
       _witness: &T,
   ): Balance<SUI>
   ```

</details>

<details>
<summary>View Operations</summary>

### View Operations

1. **Checking Vertex Settlement**
   Verifies if gas has been settled for a specific vertex in an execution.

   ```rust
   public fun is_execution_vertex_settled(
       gas_service: &GasService,
       execution: &dag::DAGExecution,
       vertex: dag::Vertex,
   ): bool
   ```

2. **Reading Tool Gas Settings**
   Gets read-only access to a tool's gas settings.

   ```rust
   public fun get_tool_gas_setting(
       gas_service: &GasService,
       fqn: AsciiString,
   ): &Bag
   ```

</details>

<!-- List of references -->

[default-gas-extension]: https://github.com/Talus-Network/nexus-next/tree/main/sui/workflow/sources/default_gas_extentsion.move 