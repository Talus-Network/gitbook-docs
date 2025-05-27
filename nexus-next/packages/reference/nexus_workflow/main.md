
<a name="(nexus_workflow=0x0)_main"></a>

# Module `(nexus_workflow=0x0)::main`



-  [Constants](#@Constants_0)
    -  [Important](#@Important_1)
-  [Function `init`](#(nexus_workflow=0x0)_main_init)


<pre><code><b>use</b> (nexus_interface=0x0)::v1;
<b>use</b> (nexus_interface=0x0)::version;
<b>use</b> (nexus_primitives=0x0)::data;
<b>use</b> (nexus_primitives=0x0)::event;
<b>use</b> (nexus_primitives=0x0)::owner_cap;
<b>use</b> (nexus_primitives=0x0)::proof_of_uid;
<b>use</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>;
<b>use</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap">default_sap</a>;
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



<a name="@Constants_0"></a>

## Constants


<a name="(nexus_workflow=0x0)_main_DEV_ADDRESSES"></a>

Each dev can list their local addresses and when we deploy the contract
relevant addresses will obtain leader cap.
Useful mainly for testing and going into testnet.


<a name="@Important_1"></a>

### Important

This is development only configuration.
When we go into later stages of development, we will remove this in favour
of a proper deploy script.


<pre><code><b>const</b> <a href="../nexus_workflow/main.md#(nexus_workflow=0x0)_main_DEV_ADDRESSES">DEV_ADDRESSES</a>: vector&lt;<b>address</b>&gt; = vector[0x9f205ddfe4be3c9c07a57d8e1ef233f7b7537a1248dd46b1514ba93261621d52, 0x4fbfd7d8b5683bf9adc9936c026ec79a559e5d6420123ebcdfb85e1c9b2fd84c];
</code></pre>



<a name="(nexus_workflow=0x0)_main_LEADER_CAPS_PER_ADDRESS"></a>

Amount of leader caps to clone per [DEV_ADDRESSES] address.


<pre><code><b>const</b> <a href="../nexus_workflow/main.md#(nexus_workflow=0x0)_main_LEADER_CAPS_PER_ADDRESS">LEADER_CAPS_PER_ADDRESS</a>: u64 = 5;
</code></pre>



<a name="(nexus_workflow=0x0)_main_init"></a>

## Function `init`



<pre><code><b>fun</b> <a href="../nexus_workflow/main.md#(nexus_workflow=0x0)_main_init">init</a>(ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>)
</code></pre>




