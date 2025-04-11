
<a name="(nexus_workflow=0x0)_gas"></a>

# Module `(nexus_workflow=0x0)::gas`



-  [Struct `GasService`](#(nexus_workflow=0x0)_gas_GasService)
-  [Struct `ExecutionGas`](#(nexus_workflow=0x0)_gas_ExecutionGas)
-  [Struct `GasBudgets`](#(nexus_workflow=0x0)_gas_GasBudgets)
-  [Struct `ToolGas`](#(nexus_workflow=0x0)_gas_ToolGas)
-  [Struct `GasTicket`](#(nexus_workflow=0x0)_gas_GasTicket)
-  [Struct `OverGas`](#(nexus_workflow=0x0)_gas_OverGas)
-  [Struct `GasSettlementUpdateEvent`](#(nexus_workflow=0x0)_gas_GasSettlementUpdateEvent)
-  [Struct `LeaderClaimedGasEvent`](#(nexus_workflow=0x0)_gas_LeaderClaimedGasEvent)
-  [Enum `ModusOperandi`](#(nexus_workflow=0x0)_gas_ModusOperandi)
-  [Enum `Scope`](#(nexus_workflow=0x0)_gas_Scope)
    -  [For Clients](#@For_Clients_0)
-  [Constants](#@Constants_1)
-  [Function `modus_operandi_limited_invocations`](#(nexus_workflow=0x0)_gas_modus_operandi_limited_invocations)
-  [Function `modus_operandi_expiry`](#(nexus_workflow=0x0)_gas_modus_operandi_expiry)
-  [Function `modus_operandi_upon_discretion_of_the_tool`](#(nexus_workflow=0x0)_gas_modus_operandi_upon_discretion_of_the_tool)
-  [Function `scope_invoker_address`](#(nexus_workflow=0x0)_gas_scope_invoker_address)
-  [Function `scope_worksheet_type`](#(nexus_workflow=0x0)_gas_scope_worksheet_type)
-  [Function `scope_execution`](#(nexus_workflow=0x0)_gas_scope_execution)
-  [Function `new_service`](#(nexus_workflow=0x0)_gas_new_service)
-  [Function `share_service`](#(nexus_workflow=0x0)_gas_share_service)
-  [Function `set_single_invocation_cost_mist`](#(nexus_workflow=0x0)_gas_set_single_invocation_cost_mist)
-  [Function `claim_gas`](#(nexus_workflow=0x0)_gas_claim_gas)
-  [Function `add_gas_ticket`](#(nexus_workflow=0x0)_gas_add_gas_ticket)
-  [Function `revoke_gas_ticket`](#(nexus_workflow=0x0)_gas_revoke_gas_ticket)
-  [Function `get_tool_gas_setting_mut`](#(nexus_workflow=0x0)_gas_get_tool_gas_setting_mut)
-  [Function `deescalate`](#(nexus_workflow=0x0)_gas_deescalate)
-  [Function `claim_leader_gas`](#(nexus_workflow=0x0)_gas_claim_leader_gas)
    -  [How does the leader estimate the amount?](#@How_does_the_leader_estimate_the_amount?_2)
    -  [Trust the leader?](#@Trust_the_leader?_3)
-  [Function `sync_gas_state`](#(nexus_workflow=0x0)_gas_sync_gas_state)
-  [Function `sync_gas_state_for_vertex`](#(nexus_workflow=0x0)_gas_sync_gas_state_for_vertex)
-  [Function `donate_to_tool`](#(nexus_workflow=0x0)_gas_donate_to_tool)
-  [Function `add_gas_budget`](#(nexus_workflow=0x0)_gas_add_gas_budget)
-  [Function `refund_execution_gas_budget`](#(nexus_workflow=0x0)_gas_refund_execution_gas_budget)
-  [Function `refund_invoker_gas_budget`](#(nexus_workflow=0x0)_gas_refund_invoker_gas_budget)
-  [Function `refund_worksheet_gas_budget`](#(nexus_workflow=0x0)_gas_refund_worksheet_gas_budget)
-  [Function `is_execution_vertex_settled`](#(nexus_workflow=0x0)_gas_is_execution_vertex_settled)
-  [Function `get_tool_gas_setting`](#(nexus_workflow=0x0)_gas_get_tool_gas_setting)
-  [Function `try_settle_execution_for_vertex`](#(nexus_workflow=0x0)_gas_try_settle_execution_for_vertex)
-  [Function `try_stamp`](#(nexus_workflow=0x0)_gas_try_stamp)
-  [Function `try_stamp_scope`](#(nexus_workflow=0x0)_gas_try_stamp_scope)
    -  [Important](#@Important_4)
-  [Function `try_one_time_charge`](#(nexus_workflow=0x0)_gas_try_one_time_charge)
-  [Function `get_or_insert_tool_gas_mut`](#(nexus_workflow=0x0)_gas_get_or_insert_tool_gas_mut)


<pre><code><b>use</b> (nexus_primitives=0x0)::data;
<b>use</b> (nexus_primitives=0x0)::event;
<b>use</b> (nexus_primitives=0x0)::owner_cap;
<b>use</b> (nexus_primitives=0x0)::proof_of_uid;
<b>use</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>;
<b>use</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/leader_cap.md#(nexus_workflow=0x0)_leader_cap">leader_cap</a>;
<b>use</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry">tool_registry</a>;
<b>use</b> <a href="../dependencies/std/address.md#std_address">std::address</a>;
<b>use</b> <a href="../dependencies/std/ascii.md#std_ascii">std::ascii</a>;
<b>use</b> <a href="../dependencies/std/bcs.md#std_bcs">std::bcs</a>;
<b>use</b> <a href="../dependencies/std/option.md#std_option">std::option</a>;
<b>use</b> <a href="../dependencies/std/string.md#std_string">std::string</a>;
<b>use</b> <a href="../dependencies/std/type_name.md#std_type_name">std::type_name</a>;
<b>use</b> <a href="../dependencies/std/vector.md#std_vector">std::vector</a>;
<b>use</b> <a href="../dependencies/sui/address.md#sui_address">sui::address</a>;
<b>use</b> <a href="../dependencies/sui/bag.md#sui_bag">sui::bag</a>;
<b>use</b> <a href="../dependencies/sui/balance.md#sui_balance">sui::balance</a>;
<b>use</b> <a href="../dependencies/sui/clock.md#sui_clock">sui::clock</a>;
<b>use</b> <a href="../dependencies/sui/coin.md#sui_coin">sui::coin</a>;
<b>use</b> <a href="../dependencies/sui/config.md#sui_config">sui::config</a>;
<b>use</b> <a href="../dependencies/sui/deny_list.md#sui_deny_list">sui::deny_list</a>;
<b>use</b> <a href="../dependencies/sui/dynamic_field.md#sui_dynamic_field">sui::dynamic_field</a>;
<b>use</b> <a href="../dependencies/sui/dynamic_object_field.md#sui_dynamic_object_field">sui::dynamic_object_field</a>;
<b>use</b> <a href="../dependencies/sui/event.md#sui_event">sui::event</a>;
<b>use</b> <a href="../dependencies/sui/hex.md#sui_hex">sui::hex</a>;
<b>use</b> <a href="../dependencies/sui/object.md#sui_object">sui::object</a>;
<b>use</b> <a href="../dependencies/sui/object_bag.md#sui_object_bag">sui::object_bag</a>;
<b>use</b> <a href="../dependencies/sui/object_table.md#sui_object_table">sui::object_table</a>;
<b>use</b> <a href="../dependencies/sui/sui.md#sui_sui">sui::sui</a>;
<b>use</b> <a href="../dependencies/sui/table.md#sui_table">sui::table</a>;
<b>use</b> <a href="../dependencies/sui/transfer.md#sui_transfer">sui::transfer</a>;
<b>use</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context">sui::tx_context</a>;
<b>use</b> <a href="../dependencies/sui/types.md#sui_types">sui::types</a>;
<b>use</b> <a href="../dependencies/sui/url.md#sui_url">sui::url</a>;
<b>use</b> <a href="../dependencies/sui/vec_map.md#sui_vec_map">sui::vec_map</a>;
<b>use</b> <a href="../dependencies/sui/vec_set.md#sui_vec_set">sui::vec_set</a>;
</code></pre>



<a name="(nexus_workflow=0x0)_gas_GasService"></a>

## Struct `GasService`

Shared object.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">GasService</a> <b>has</b> key
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>id: <a href="../dependencies/sui/object.md#sui_object_UID">sui::object::UID</a></code>
</dt>
<dd>
</dd>
<dt>
<code>executions_gas: <a href="../dependencies/sui/object_table.md#sui_object_table_ObjectTable">sui::object_table::ObjectTable</a>&lt;<a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a>, (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_ExecutionGas">gas::ExecutionGas</a>&gt;</code>
</dt>
<dd>
 Can be queried to see which vertices in the execution have their gas
 settled.
 The key is the [DAGExecution]'s ID.
</dd>
<dt>
<code>tools_gas: <a href="../dependencies/sui/table.md#sui_table_Table">sui::table::Table</a>&lt;<a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_ToolGas">gas::ToolGas</a>&gt;</code>
</dt>
<dd>
 Holds information about who has prepaid for gas, gas configuration
 for tools, etc.
 The keys is the tool's FQN.
</dd>
<dt>
<code>gas_budgets: (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasBudgets">gas::GasBudgets</a></code>
</dt>
<dd>
 Gas budget is used to pay for [DAGExecution].
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_gas_ExecutionGas"></a>

## Struct `ExecutionGas`

Dynamic object field.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_ExecutionGas">ExecutionGas</a> <b>has</b> key, store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>id: <a href="../dependencies/sui/object.md#sui_object_UID">sui::object::UID</a></code>
</dt>
<dd>
</dd>
<dt>
<code>settled_vertices: <a href="../dependencies/sui/vec_set.md#sui_vec_set_VecSet">sui::vec_set::VecSet</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>&gt;</code>
</dt>
<dd>
 Gas for these vertices has been settled and they can be invoked once.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_gas_GasBudgets"></a>

## Struct `GasBudgets`

The value is always <code>Balance&lt;SUI&gt;</code>.

This budget will be used to buy invocations from tools unless there
exist gas tickets that can be stamped instead.

This budget will also be used to pay for leader gas.

The key is a [Scope].


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasBudgets">GasBudgets</a> <b>has</b> store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>inner: <a href="../dependencies/sui/bag.md#sui_bag_Bag">sui::bag::Bag</a></code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_gas_ToolGas"></a>

## Struct `ToolGas`

Dynamic field.

Holds prepaid gas tickets for a tool that can get stamped resulting in gas
settlement for an execution's vertex.

When resolving a gas ticket for a [DAGExecution] the gas service:

1. looks for a ticket belonging to an execution.
2. If none ok then it looks for a ticket for the worksheet type.
3. If none ok then it looks for a ticket for the address.
4. If none ok then the the gas payment is invalid.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_ToolGas">ToolGas</a> <b>has</b> store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>vault: <a href="../dependencies/sui/balance.md#sui_balance_Balance">sui::balance::Balance</a>&lt;<a href="../dependencies/sui/sui.md#sui_sui_SUI">sui::sui::SUI</a>&gt;</code>
</dt>
<dd>
 Holds funds collected for gas settlements.
</dd>
<dt>
<code>single_invocation_cost_mist: u64</code>
</dt>
<dd>
 If this is set to 0 then the tool doesn't require gas to be invoked.
 Otherwise if no other existing gas tickets are found then the gas
 service will take this amount from the gas budget if possible.
 The complexity of gas settlement cannot be captured in a single number.
 However, a single number is a good enough default for most tools.
 More complex gas settlement can be achieved with [add_gas_ticket].
 For tools that expect other modes it is recommended to set this value
 higher than alternatives to have this as a last resort option but
 provide a less expensive alternative for the happy path.
 Those tools that don't want to allow payments for a single invocation
 at all can set this to u64::MAX.
 TODO: <https://github.com/Talus-Network/nexus-next/issues/249>
</dd>
<dt>
<code>settings: <a href="../dependencies/sui/bag.md#sui_bag_Bag">sui::bag::Bag</a></code>
</dt>
<dd>
 Settings for gas extensions.
 Can be read without any extra access permissions and written to with
 tool's owner cap.
</dd>
<dt>
<code>tickets: <a href="../dependencies/sui/bag.md#sui_bag_Bag">sui::bag::Bag</a></code>
</dt>
<dd>
 The value is always [GasTicket].
 Keys:
 - execution ID
 - worksheet type
 - invoker address
 If the key is an execution ID:
 The gas tickets that apply to a specific execution only.
 If the key is a worksheet's [TypeName]:
 The gas tickets that apply to a specific worksheet type only.
 If the key is an address:
 The gas tickets that apply to a specific address only.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_gas_GasTicket"></a>

## Struct `GasTicket`

Someone has prepaid for tool with expectations defined in this state.

See [try_stamp] for info on mutations to this state.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasTicket">GasTicket</a> <b>has</b> drop, store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>created_at_ms: u64</code>
</dt>
<dd>
 State of the [Clock] when the ticket was created.
</dd>
<dt>
<code>modus_operandi: (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_ModusOperandi">gas::ModusOperandi</a></code>
</dt>
<dd>
 How should the ticket behave.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_gas_OverGas"></a>

## Struct `OverGas`

Generic for owner cap that allows adding and removing gas tickets and
changing settings.

This is a de-escalated version of the [OverTool] owner cap.
It should make tool owners more comfortable using gas extensions as they
don't give them access to important state.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_OverGas">OverGas</a> <b>has</b> drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
</dl>


</details>

<a name="(nexus_workflow=0x0)_gas_GasSettlementUpdateEvent"></a>

## Struct `GasSettlementUpdateEvent`



<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasSettlementUpdateEvent">GasSettlementUpdateEvent</a> <b>has</b> <b>copy</b>, drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>execution: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
<dt>
<code>vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a></code>
</dt>
<dd>
</dd>
<dt>
<code>tool_fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a></code>
</dt>
<dd>
</dd>
<dt>
<code>was_settled: bool</code>
</dt>
<dd>
 Whether the gas ticket was stamped ok.
 Multiple of these events can be emitted for the same execution/vertex/tool_fqn
 combination, but only one of them will have this field set to true.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_gas_LeaderClaimedGasEvent"></a>

## Struct `LeaderClaimedGasEvent`

If anyone wants to verify that the leader is claiming an honest amount of
gas they can use this event to track the gas claimed.
The event's ID comprises also the tx hash and so the verifier can use it to
cross check the gas claimed with the tx gas budget spent.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_LeaderClaimedGasEvent">LeaderClaimedGasEvent</a> <b>has</b> <b>copy</b>, drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>network: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
 Who is the leader.
</dd>
<dt>
<code>amount: u64</code>
</dt>
<dd>
 How much was claimed.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_gas_ModusOperandi"></a>

## Enum `ModusOperandi`

How should the gas ticket behave.


<pre><code><b>public</b> <b>enum</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_ModusOperandi">ModusOperandi</a> <b>has</b> <b>copy</b>, drop, store
</code></pre>



<details>
<summary>Variants</summary>


<dl>
<dt>
Variant <code>Expiry</code>
</dt>
<dd>
 How long is the ticket valid for.
</dd>

<dl>
<dt>
<code>_variant_name: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a></code>
</dt>
<dd>
</dd>
</dl>


<dl>
<dt>
<code>valid_for_ms: u64</code>
</dt>
<dd>
 Since the ticket was created.
</dd>
</dl>

<dt>
Variant <code>LimitedInvocations</code>
</dt>
<dd>
 How many invocations are allowed.
</dd>

<dl>
<dt>
<code>_variant_name: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a></code>
</dt>
<dd>
</dd>
</dl>


<dl>
<dt>
<code>total: u64</code>
</dt>
<dd>
 How many invocations to begin with.
 Is always greater than or equal to the used invocations.
</dd>
</dl>


<dl>
<dt>
<code>used: u64</code>
</dt>
<dd>
 When this equals the total then all invocations are used up.
</dd>
</dl>

<dt>
Variant <code>UponDiscretionOfTheTool</code>
</dt>
<dd>
 The tool has a complete control over whether the ticket is valid or not.
 This means it can add or remove gas tickets at will.
</dd>

<dl>
<dt>
<code>_variant_name: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a></code>
</dt>
<dd>
</dd>
</dl>

</dl>


</details>

<a name="(nexus_workflow=0x0)_gas_Scope"></a>

## Enum `Scope`

See the docs to understand how scopes work.


<a name="@For_Clients_0"></a>

### For Clients


We ignore enum variant convention out of convenience as in this specific
example the variant is unambiguous.

<https://github.com/Talus-Network/nexus-next/wiki/Conventions:-Sui-Move#enums-_variant_name>


<pre><code><b>public</b> <b>enum</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_Scope">Scope</a> <b>has</b> <b>copy</b>, drop, store
</code></pre>



<details>
<summary>Variants</summary>


<dl>
<dt>
Variant <code>Execution</code>
</dt>
<dd>
</dd>

<dl>
<dt>
<code>0: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
</dl>

<dt>
Variant <code>WorksheetType</code>
</dt>
<dd>
</dd>

<dl>
<dt>
<code>0: <a href="../dependencies/std/type_name.md#std_type_name_TypeName">std::type_name::TypeName</a></code>
</dt>
<dd>
</dd>
</dl>

<dt>
Variant <code>InvokerAddress</code>
</dt>
<dd>
</dd>

<dl>
<dt>
<code>0: <b>address</b></code>
</dt>
<dd>
</dd>
</dl>

</dl>


</details>

<a name="@Constants_1"></a>

## Constants


<a name="(nexus_workflow=0x0)_gas_ECannotRevokeGasTicket"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_ECannotRevokeGasTicket">ECannotRevokeGasTicket</a>: vector&lt;u8&gt; = b"Tickets with expiry or limited number of invocations cannot be revoked";
</code></pre>



<a name="(nexus_workflow=0x0)_gas_ECannotClaimLeaderGas"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_ECannotClaimLeaderGas">ECannotClaimLeaderGas</a>: vector&lt;u8&gt; = b"There is not enough <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas">gas</a> in the budget to pay <b>for</b> leader <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas">gas</a>";
</code></pre>



<a name="(nexus_workflow=0x0)_gas_modus_operandi_limited_invocations"></a>

## Function `modus_operandi_limited_invocations`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_modus_operandi_limited_invocations">modus_operandi_limited_invocations</a>(total: u64, used: u64): (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_ModusOperandi">gas::ModusOperandi</a>
</code></pre>





<a name="(nexus_workflow=0x0)_gas_modus_operandi_expiry"></a>

## Function `modus_operandi_expiry`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_modus_operandi_expiry">modus_operandi_expiry</a>(valid_for_ms: u64): (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_ModusOperandi">gas::ModusOperandi</a>
</code></pre>





<a name="(nexus_workflow=0x0)_gas_modus_operandi_upon_discretion_of_the_tool"></a>

## Function `modus_operandi_upon_discretion_of_the_tool`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_modus_operandi_upon_discretion_of_the_tool">modus_operandi_upon_discretion_of_the_tool</a>(): (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_ModusOperandi">gas::ModusOperandi</a>
</code></pre>





<a name="(nexus_workflow=0x0)_gas_scope_invoker_address"></a>

## Function `scope_invoker_address`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_scope_invoker_address">scope_invoker_address</a>(invoker_address: <b>address</b>): (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_Scope">gas::Scope</a>
</code></pre>





<a name="(nexus_workflow=0x0)_gas_scope_worksheet_type"></a>

## Function `scope_worksheet_type`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_scope_worksheet_type">scope_worksheet_type</a>(worksheet_type_name: <a href="../dependencies/std/type_name.md#std_type_name_TypeName">std::type_name::TypeName</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_Scope">gas::Scope</a>
</code></pre>





<a name="(nexus_workflow=0x0)_gas_scope_execution"></a>

## Function `scope_execution`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_scope_execution">scope_execution</a>(execution_id: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_Scope">gas::Scope</a>
</code></pre>





<a name="(nexus_workflow=0x0)_gas_new_service"></a>

## Function `new_service`



<pre><code><b>public</b>(package) <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_new_service">new_service</a>(ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">gas::GasService</a>
</code></pre>





<a name="(nexus_workflow=0x0)_gas_share_service"></a>

## Function `share_service`



<pre><code><b>public</b>(package) <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_share_service">share_service</a>(self: (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">gas::GasService</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_gas_set_single_invocation_cost_mist"></a>

## Function `set_single_invocation_cost_mist`

Changes how much tool charges per single invocation.

Note that this enables gas collection by the tool so the tool owner should
be interested in calling this.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_set_single_invocation_cost_mist">set_single_invocation_cost_mist</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">gas::GasService</a>, <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry">tool_registry</a>: &(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, owner_cap: &(nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_OverGas">gas::OverGas</a>&gt;, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, single_invocation_cost_mist: u64, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_gas_claim_gas"></a>

## Function `claim_gas`

Claims all gas settlement for the given tool.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_claim_gas">claim_gas</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">gas::GasService</a>, <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry">tool_registry</a>: &(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, owner_cap: &(nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_OverTool">tool_registry::OverTool</a>&gt;, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): <a href="../dependencies/sui/balance.md#sui_balance_Balance">sui::balance::Balance</a>&lt;<a href="../dependencies/sui/sui.md#sui_sui_SUI">sui::sui::SUI</a>&gt;
</code></pre>





<a name="(nexus_workflow=0x0)_gas_add_gas_ticket"></a>

## Function `add_gas_ticket`

The tool owner can add a gas ticket at will.

By using either "invocations" or "expiry" modes the tool owner promises to
deliver the service otherwise they might be slashed, subject to the rules
defined by the Talus/Nexus terms - see the docs.

The tool owner can use "upon discretion of the tool" mode to be able to
[revoke_gas_ticket] at will.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_add_gas_ticket">add_gas_ticket</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">gas::GasService</a>, <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry">tool_registry</a>: &(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, owner_cap: &(nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_OverGas">gas::OverGas</a>&gt;, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, scope: (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_Scope">gas::Scope</a>, modus_operandi: (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_ModusOperandi">gas::ModusOperandi</a>, clock: &<a href="../dependencies/sui/clock.md#sui_clock_Clock">sui::clock::Clock</a>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_gas_revoke_gas_ticket"></a>

## Function `revoke_gas_ticket`

The tool owner can revoke a gas ticket with mode "upon discretion of the tool".

This means that the tool owner can invalidate a gas ticket at any time.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_revoke_gas_ticket">revoke_gas_ticket</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">gas::GasService</a>, <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry">tool_registry</a>: &(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, owner_cap: &(nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_OverGas">gas::OverGas</a>&gt;, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, scope: (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_Scope">gas::Scope</a>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_gas_get_tool_gas_setting_mut"></a>

## Function `get_tool_gas_setting_mut`

The tool owner can set the gas settings for the tool.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_get_tool_gas_setting_mut">get_tool_gas_setting_mut</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">gas::GasService</a>, <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry">tool_registry</a>: &(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, owner_cap: &(nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_OverGas">gas::OverGas</a>&gt;, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): &<b>mut</b> <a href="../dependencies/sui/bag.md#sui_bag_Bag">sui::bag::Bag</a>
</code></pre>





<a name="(nexus_workflow=0x0)_gas_deescalate"></a>

## Function `deescalate`

Lowers privileges of the tool owner cap into a gas owner cap.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_deescalate">deescalate</a>(<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry">tool_registry</a>: &(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, owner_cap: &(nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_OverTool">tool_registry::OverTool</a>&gt;, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): (nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_OverGas">gas::OverGas</a>&gt;
</code></pre>





<a name="(nexus_workflow=0x0)_gas_claim_leader_gas"></a>

## Function `claim_leader_gas`

The leader claims just about the amount of gas it costs to pay for the tx.


<a name="@How_does_the_leader_estimate_the_amount?_2"></a>

### How does the leader estimate the amount?


The leader dry runs the tx and reads how much gas it would cost to pay for
the tx.
Then it sets the gas budget for the tx to the amount obtained in the dry-run
(with a few % extra as a buffer) and actually submits the tx.
The submitted tx will use <code><a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_claim_leader_gas">claim_leader_gas</a></code> with the amount obtained in the
dry-run.


<a name="@Trust_the_leader?_3"></a>

### Trust the leader?


At the moment the leader can claim any amount of gas it wants from anybody
who uploads gas budgets.
To hold the leader accountable we emit <code><a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_LeaderClaimedGasEvent">LeaderClaimedGasEvent</a></code> event which
can be read by 3rd parties that check that the amount claimed is not over
the top.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_claim_leader_gas">claim_leader_gas</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">gas::GasService</a>, execution: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>, <a href="../nexus_workflow/leader_cap.md#(nexus_workflow=0x0)_leader_cap">leader_cap</a>: &(nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/leader_cap.md#(nexus_workflow=0x0)_leader_cap_OverNetwork">leader_cap::OverNetwork</a>&gt;, amount: u64): <a href="../dependencies/sui/balance.md#sui_balance_Balance">sui::balance::Balance</a>&lt;<a href="../dependencies/sui/sui.md#sui_sui_SUI">sui::sui::SUI</a>&gt;
</code></pre>





<a name="(nexus_workflow=0x0)_gas_sync_gas_state"></a>

## Function `sync_gas_state`

Calls [sync_gas_state_for_vertex] for each vertex invoked in this tx.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_sync_gas_state">sync_gas_state</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">gas::GasService</a>, <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>, execution: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>, request_walk_execution: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_RequestWalkExecution">dag::RequestWalkExecution</a>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_gas_sync_gas_state_for_vertex"></a>

## Function `sync_gas_state_for_vertex`

Syncs gas payment with an execution.

This function is a no-op if
1. The vertex is not in the registry.
2. The vertex is not invoked.
3. The vertex is already settled.

This function aborts if
1. The DAG doesn't contain the provided vertex.

This function is permission-less and idempotent.
Anyone can sync the gas state for a vertex and this function will only do
work provided the above conditions are met.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_sync_gas_state_for_vertex">sync_gas_state_for_vertex</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">gas::GasService</a>, <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>, execution: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>, vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_gas_donate_to_tool"></a>

## Function `donate_to_tool`

Donate given balance to the tool's gas total.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_donate_to_tool">donate_to_tool</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">gas::GasService</a>, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, amount: <a href="../dependencies/sui/balance.md#sui_balance_Balance">sui::balance::Balance</a>&lt;<a href="../dependencies/sui/sui.md#sui_sui_SUI">sui::sui::SUI</a>&gt;)
</code></pre>





<a name="(nexus_workflow=0x0)_gas_add_gas_budget"></a>

## Function `add_gas_budget`

Adds gas budget for the given scope.
Gas budget will be used to pay for invocation if no gas ticket is present.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_add_gas_budget">add_gas_budget</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">gas::GasService</a>, scope: (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_Scope">gas::Scope</a>, budget: <a href="../dependencies/sui/balance.md#sui_balance_Balance">sui::balance::Balance</a>&lt;<a href="../dependencies/sui/sui.md#sui_sui_SUI">sui::sui::SUI</a>&gt;)
</code></pre>





<a name="(nexus_workflow=0x0)_gas_refund_execution_gas_budget"></a>

## Function `refund_execution_gas_budget`

Can be called once the execution finishes.

The gas will be refunded to the invoker's address if finished.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_refund_execution_gas_budget">refund_execution_gas_budget</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">gas::GasService</a>, execution: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_gas_refund_invoker_gas_budget"></a>

## Function `refund_invoker_gas_budget`

Can be called by the invoker.
Will be empty if not present.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_refund_invoker_gas_budget">refund_invoker_gas_budget</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">gas::GasService</a>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): <a href="../dependencies/sui/balance.md#sui_balance_Balance">sui::balance::Balance</a>&lt;<a href="../dependencies/sui/sui.md#sui_sui_SUI">sui::sui::SUI</a>&gt;
</code></pre>





<a name="(nexus_workflow=0x0)_gas_refund_worksheet_gas_budget"></a>

## Function `refund_worksheet_gas_budget`

Can be called by the SAP.
Will be empty if not present.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_refund_worksheet_gas_budget">refund_worksheet_gas_budget</a>&lt;T&gt;(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">gas::GasService</a>, _witness: &T): <a href="../dependencies/sui/balance.md#sui_balance_Balance">sui::balance::Balance</a>&lt;<a href="../dependencies/sui/sui.md#sui_sui_SUI">sui::sui::SUI</a>&gt;
</code></pre>





<a name="(nexus_workflow=0x0)_gas_is_execution_vertex_settled"></a>

## Function `is_execution_vertex_settled`

Can the vertex be invoked once?


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_is_execution_vertex_settled">is_execution_vertex_settled</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">gas::GasService</a>, execution: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>, vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>): bool
</code></pre>





<a name="(nexus_workflow=0x0)_gas_get_tool_gas_setting"></a>

## Function `get_tool_gas_setting`

Anyone can read the tool gas settings.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_get_tool_gas_setting">get_tool_gas_setting</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">gas::GasService</a>, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>): &<a href="../dependencies/sui/bag.md#sui_bag_Bag">sui::bag::Bag</a>
</code></pre>





<a name="(nexus_workflow=0x0)_gas_try_settle_execution_for_vertex"></a>

## Function `try_settle_execution_for_vertex`

Updates state of gas settlement for the given execution.


<pre><code><b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_try_settle_execution_for_vertex">try_settle_execution_for_vertex</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">gas::GasService</a>, <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>, execution: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>, vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_gas_try_stamp"></a>

## Function `try_stamp`

Tries to stamp a ticket for the given execution.

The caller must ensure that it is appropriate to stamp the ticket.


<pre><code><b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_try_stamp">try_stamp</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_ToolGas">gas::ToolGas</a>, execution: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>): bool
</code></pre>





<a name="(nexus_workflow=0x0)_gas_try_stamp_scope"></a>

## Function `try_stamp_scope`

Returns true if the gas ticket is valid.
The key determines the scope we're stamping.


<a name="@Important_4"></a>

### Important


This function mutates the ticket state.
It's important that the return values are used to update the state of the
caller.

Once a [GasTicket] cannot be stamped anymore it is removed.


<pre><code><b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_try_stamp_scope">try_stamp_scope</a>&lt;K: <b>copy</b>, drop, store&gt;(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_ToolGas">gas::ToolGas</a>, key: K, execution_created_at: u64): bool
</code></pre>





<a name="(nexus_workflow=0x0)_gas_try_one_time_charge"></a>

## Function `try_one_time_charge`

Balance is either empty if no gas could be used or it contains the exact
amount requested.


<pre><code><b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_try_one_time_charge">try_one_time_charge</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasBudgets">gas::GasBudgets</a>, execution: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>, amount: u64): <a href="../dependencies/sui/balance.md#sui_balance_Balance">sui::balance::Balance</a>&lt;<a href="../dependencies/sui/sui.md#sui_sui_SUI">sui::sui::SUI</a>&gt;
</code></pre>





<a name="(nexus_workflow=0x0)_gas_get_or_insert_tool_gas_mut"></a>

## Function `get_or_insert_tool_gas_mut`



<pre><code><b>fun</b> <a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_get_or_insert_tool_gas_mut">get_or_insert_tool_gas_mut</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">gas::GasService</a>, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_ToolGas">gas::ToolGas</a>
</code></pre>




