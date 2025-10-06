
<a name="(nexus_workflow=0x0)_default_gas_extension"></a>

# Module `(nexus_workflow=0x0)::default_gas_extension`



-  [Struct `ExpiryCostPerMinuteKey`](#(nexus_workflow=0x0)_default_gas_extension_ExpiryCostPerMinuteKey)
-  [Struct `ExpiryGasOwnerCapKey`](#(nexus_workflow=0x0)_default_gas_extension_ExpiryGasOwnerCapKey)
-  [Constants](#@Constants_0)
-  [Function `buy_expiry_gas_ticket`](#(nexus_workflow=0x0)_default_gas_extension_buy_expiry_gas_ticket)
-  [Function `enable_expiry`](#(nexus_workflow=0x0)_default_gas_extension_enable_expiry)
-  [Function `disable_expiry`](#(nexus_workflow=0x0)_default_gas_extension_disable_expiry)


<pre><code><b>use</b> (nexus_primitives=0x0)::data;
<b>use</b> (nexus_primitives=0x0)::event;
<b>use</b> (nexus_primitives=0x0)::owner_cap;
<b>use</b> (nexus_primitives=0x0)::proof_of_uid;
<b>use</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>;
<b>use</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas">gas</a>;
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



<a name="(nexus_workflow=0x0)_default_gas_extension_ExpiryCostPerMinuteKey"></a>

## Struct `ExpiryCostPerMinuteKey`

How many [SUI] tokens should be paid for each minute.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/default_gas_extension.md#(nexus_workflow=0x0)_default_gas_extension_ExpiryCostPerMinuteKey">ExpiryCostPerMinuteKey</a> <b>has</b> <b>copy</b>, drop, store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
</dl>


</details>

<a name="(nexus_workflow=0x0)_default_gas_extension_ExpiryGasOwnerCapKey"></a>

## Struct `ExpiryGasOwnerCapKey`

Will hold the gas owner cap to do requests on behalf of the tool owner.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/default_gas_extension.md#(nexus_workflow=0x0)_default_gas_extension_ExpiryGasOwnerCapKey">ExpiryGasOwnerCapKey</a> <b>has</b> <b>copy</b>, drop, store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
</dl>


</details>

<a name="@Constants_0"></a>

## Constants


<a name="(nexus_workflow=0x0)_default_gas_extension_EThisMethodIsNotEnabled"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/default_gas_extension.md#(nexus_workflow=0x0)_default_gas_extension_EThisMethodIsNotEnabled">EThisMethodIsNotEnabled</a>: vector&lt;u8&gt; = b"This method is not enabled";
</code></pre>



<a name="(nexus_workflow=0x0)_default_gas_extension_buy_expiry_gas_ticket"></a>

## Function `buy_expiry_gas_ticket`



<pre><code><b>public</b> <b>entry</b> <b>fun</b> <a href="../nexus_workflow/default_gas_extension.md#(nexus_workflow=0x0)_default_gas_extension_buy_expiry_gas_ticket">buy_expiry_gas_ticket</a>(gas_service: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">gas::GasService</a>, <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry">tool_registry</a>: &(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, minutes: u64, pay_with: &<b>mut</b> <a href="../dependencies/sui/coin.md#sui_coin_Coin">sui::coin::Coin</a>&lt;<a href="../dependencies/sui/sui.md#sui_sui_SUI">sui::sui::SUI</a>&gt;, clock: &<a href="../dependencies/sui/clock.md#sui_clock_Clock">sui::clock::Clock</a>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_default_gas_extension_enable_expiry"></a>

## Function `enable_expiry`

Enables buying gas tickets that expire after a certain time in token
[SUI] for [cost_per_minute] of those tokens.

To update the cost just call this function again with the new value.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/default_gas_extension.md#(nexus_workflow=0x0)_default_gas_extension_enable_expiry">enable_expiry</a>(gas_service: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">gas::GasService</a>, <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry">tool_registry</a>: &(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, owner_cap: (nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_OverGas">gas::OverGas</a>&gt;, cost_per_minute: u64, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_default_gas_extension_disable_expiry"></a>

## Function `disable_expiry`

Disables this extension.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/default_gas_extension.md#(nexus_workflow=0x0)_default_gas_extension_disable_expiry">disable_expiry</a>(gas_service: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_GasService">gas::GasService</a>, <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry">tool_registry</a>: &(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, owner_cap: &(nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas_OverGas">gas::OverGas</a>&gt;, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>)
</code></pre>




