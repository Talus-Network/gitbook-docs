
<a name="(nexus_workflow=0x0)_tool_registry"></a>

# Module `(nexus_workflow=0x0)::tool_registry`



-  [Struct `ToolRegistry`](#(nexus_workflow=0x0)_tool_registry_ToolRegistry)
-  [Struct `OffChainTool`](#(nexus_workflow=0x0)_tool_registry_OffChainTool)
-  [Struct `OverSlashing`](#(nexus_workflow=0x0)_tool_registry_OverSlashing)
-  [Struct `OverTool`](#(nexus_workflow=0x0)_tool_registry_OverTool)
-  [Struct `ToolRegistryCreatedEvent`](#(nexus_workflow=0x0)_tool_registry_ToolRegistryCreatedEvent)
-  [Struct `OffChainToolRegisteredEvent`](#(nexus_workflow=0x0)_tool_registry_OffChainToolRegisteredEvent)
-  [Struct `ToolUnregisteredEvent`](#(nexus_workflow=0x0)_tool_registry_ToolUnregisteredEvent)
-  [Struct `ToolSlashedEvent`](#(nexus_workflow=0x0)_tool_registry_ToolSlashedEvent)
-  [Constants](#@Constants_0)
-  [Function `new`](#(nexus_workflow=0x0)_tool_registry_new)
-  [Function `share`](#(nexus_workflow=0x0)_tool_registry_share)
-  [Function `slash_off_chain_tool`](#(nexus_workflow=0x0)_tool_registry_slash_off_chain_tool)
-  [Function `set_mist_collateral_to_lock`](#(nexus_workflow=0x0)_tool_registry_set_mist_collateral_to_lock)
-  [Function `set_lock_duration_ms`](#(nexus_workflow=0x0)_tool_registry_set_lock_duration_ms)
-  [Function `register_off_chain_tool_for_self`](#(nexus_workflow=0x0)_tool_registry_register_off_chain_tool_for_self)
    -  [Slashing](#@Slashing_1)
    -  [Owner Cap](#@Owner_Cap_2)
    -  [Gas Tickets](#@Gas_Tickets_3)
-  [Function `register_off_chain_tool`](#(nexus_workflow=0x0)_tool_registry_register_off_chain_tool)
-  [Function `unregister_off_chain_tool`](#(nexus_workflow=0x0)_tool_registry_unregister_off_chain_tool)
-  [Function `claim_collateral_for_self`](#(nexus_workflow=0x0)_tool_registry_claim_collateral_for_self)
-  [Function `claim_collateral_for_off_chain_tool`](#(nexus_workflow=0x0)_tool_registry_claim_collateral_for_off_chain_tool)
-  [Function `deescalate`](#(nexus_workflow=0x0)_tool_registry_deescalate)
-  [Function `did_unregister_period_pass`](#(nexus_workflow=0x0)_tool_registry_did_unregister_period_pass)
-  [Function `assert_tool_registered`](#(nexus_workflow=0x0)_tool_registry_assert_tool_registered)
-  [Function `assert_tool_owner`](#(nexus_workflow=0x0)_tool_registry_assert_tool_owner)
-  [Function `assert_tool_owner_unchecked_generic`](#(nexus_workflow=0x0)_tool_registry_assert_tool_owner_unchecked_generic)
-  [Function `register_off_chain_tool_`](#(nexus_workflow=0x0)_tool_registry_register_off_chain_tool_)
-  [Function `did_unregister_period_pass_`](#(nexus_workflow=0x0)_tool_registry_did_unregister_period_pass_)


<pre><code><b>use</b> (nexus_primitives=0x0)::event;
<b>use</b> (nexus_primitives=0x0)::owner_cap;
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
<b>use</b> <a href="../dependencies/sui/sui.md#sui_sui">sui::sui</a>;
<b>use</b> <a href="../dependencies/sui/table.md#sui_table">sui::table</a>;
<b>use</b> <a href="../dependencies/sui/transfer.md#sui_transfer">sui::transfer</a>;
<b>use</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context">sui::tx_context</a>;
<b>use</b> <a href="../dependencies/sui/types.md#sui_types">sui::types</a>;
<b>use</b> <a href="../dependencies/sui/url.md#sui_url">sui::url</a>;
<b>use</b> <a href="../dependencies/sui/vec_set.md#sui_vec_set">sui::vec_set</a>;
</code></pre>



<a name="(nexus_workflow=0x0)_tool_registry_ToolRegistry"></a>

## Struct `ToolRegistry`



<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">ToolRegistry</a> <b>has</b> key
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
<code>tools: <a href="../dependencies/sui/object_bag.md#sui_object_bag_ObjectBag">sui::object_bag::ObjectBag</a></code>
</dt>
<dd>
 Maps tool FQNs to their definitions.
</dd>
<dt>
<code>mist_collateral_to_lock: u64</code>
</dt>
<dd>
 How much [SUI] (in MIST) to lock to register a tool.
</dd>
<dt>
<code>lock_duration_ms: u64</code>
</dt>
<dd>
 How long is the collateral locked for in milliseconds after unregistering.
 Copied to tool upon registration.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_tool_registry_OffChainTool"></a>

## Struct `OffChainTool`

Dynamic object.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_OffChainTool">OffChainTool</a> <b>has</b> key, store
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
<code>url: vector&lt;u8&gt;</code>
</dt>
<dd>
 How can we reach this tool?
</dd>
<dt>
<code>input_schema: vector&lt;u8&gt;</code>
</dt>
<dd>
 Must follow our meta schema for input schemas.
</dd>
<dt>
<code>output_schema: vector&lt;u8&gt;</code>
</dt>
<dd>
 Must follow our meta schema for output schemas.
</dd>
<dt>
<code>vault: <a href="../dependencies/sui/balance.md#sui_balance_Balance">sui::balance::Balance</a>&lt;<a href="../dependencies/sui/sui.md#sui_sui_SUI">sui::sui::SUI</a>&gt;</code>
</dt>
<dd>
 The tool's vault holds the tool's locked minimum of collateral to
 register the tool;
 To register a tool one must lock [ToolRegistry::mist_collateral_to_lock]
 [SUI].
</dd>
<dt>
<code>lock_duration_ms: u64</code>
</dt>
<dd>
 How long is the collateral locked for in milliseconds after unregistering.
</dd>
<dt>
<code>was_unregistered_at_ms: <a href="../dependencies/std/option.md#std_option_Option">std::option::Option</a>&lt;u64&gt;</code>
</dt>
<dd>
 If the creator unregisters the tool, we keep track of when it happened.
 After some time we release the collateral back to the creator.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_tool_registry_OverSlashing"></a>

## Struct `OverSlashing`

Will identify admin cap for slashing permissions.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_OverSlashing">OverSlashing</a> <b>has</b> drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
</dl>


</details>

<a name="(nexus_workflow=0x0)_tool_registry_OverTool"></a>

## Struct `OverTool`

Will identify admin cap over a tool in this registry.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_OverTool">OverTool</a> <b>has</b> drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
</dl>


</details>

<a name="(nexus_workflow=0x0)_tool_registry_ToolRegistryCreatedEvent"></a>

## Struct `ToolRegistryCreatedEvent`



<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistryCreatedEvent">ToolRegistryCreatedEvent</a> <b>has</b> <b>copy</b>, drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>registry: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
<dt>
<code>slashing_cap: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_tool_registry_OffChainToolRegisteredEvent"></a>

## Struct `OffChainToolRegisteredEvent`



<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_OffChainToolRegisteredEvent">OffChainToolRegisteredEvent</a> <b>has</b> <b>copy</b>, drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>registry: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
 [ID] of [ToolRegistry].
</dd>
<dt>
<code>tool: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
 New [ID] of the [OffChainTool].
</dd>
<dt>
<code>fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a></code>
</dt>
<dd>
 The unique identifier for this tool.
</dd>
<dt>
<code>url: vector&lt;u8&gt;</code>
</dt>
<dd>
 How can we reach this tool?
</dd>
<dt>
<code>input_schema: vector&lt;u8&gt;</code>
</dt>
<dd>
 Must follow our meta schema for input schemas.
</dd>
<dt>
<code>output_schema: vector&lt;u8&gt;</code>
</dt>
<dd>
 Must follow our meta schema for output schemas.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_tool_registry_ToolUnregisteredEvent"></a>

## Struct `ToolUnregisteredEvent`



<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolUnregisteredEvent">ToolUnregisteredEvent</a> <b>has</b> <b>copy</b>, drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>tool: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
<dt>
<code>fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a></code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_tool_registry_ToolSlashedEvent"></a>

## Struct `ToolSlashedEvent`

The admin has slashed some collateral from a tool.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolSlashedEvent">ToolSlashedEvent</a> <b>has</b> <b>copy</b>, drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>tool: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
<dt>
<code>fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a></code>
</dt>
<dd>
</dd>
<dt>
<code>amount: u64</code>
</dt>
<dd>
 Amount of (MIST) collateral slashed.
</dd>
</dl>


</details>

<a name="@Constants_0"></a>

## Constants


<a name="(nexus_workflow=0x0)_tool_registry_ENotEnoughSuiToLock"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ENotEnoughSuiToLock">ENotEnoughSuiToLock</a>: vector&lt;u8&gt; = b"Not enough SUI to lock collateral";
</code></pre>



<a name="(nexus_workflow=0x0)_tool_registry_ECollateralNotReadyToClaim"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ECollateralNotReadyToClaim">ECollateralNotReadyToClaim</a>: vector&lt;u8&gt; = b"Collateral not ready to reclaim";
</code></pre>



<a name="(nexus_workflow=0x0)_tool_registry_EFqnNotFound"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_EFqnNotFound">EFqnNotFound</a>: vector&lt;u8&gt; = b"FQN not found";
</code></pre>



<a name="(nexus_workflow=0x0)_tool_registry_EUnauthorized"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_EUnauthorized">EUnauthorized</a>: vector&lt;u8&gt; = b"Only the creator can unregister a tool";
</code></pre>



<a name="(nexus_workflow=0x0)_tool_registry_EToolUnregistered"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_EToolUnregistered">EToolUnregistered</a>: vector&lt;u8&gt; = b"Tool <b>has</b> been unregistered";
</code></pre>



<a name="(nexus_workflow=0x0)_tool_registry_EFqnAlreadyExists"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_EFqnAlreadyExists">EFqnAlreadyExists</a>: vector&lt;u8&gt; = b"FQN already exists";
</code></pre>



<a name="(nexus_workflow=0x0)_tool_registry_DEFAULT_MIST_COLLATERAL_TO_LOCK"></a>

How much [SUI] (in MIST) to lock to register a tool.

TODO: This is only a testing value.


<pre><code><b>const</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_DEFAULT_MIST_COLLATERAL_TO_LOCK">DEFAULT_MIST_COLLATERAL_TO_LOCK</a>: u64 = 1;
</code></pre>



<a name="(nexus_workflow=0x0)_tool_registry_DEFAULT_LOCK_DURATION_MS"></a>

How long is the collateral locked for in milliseconds after unregistering.

TODO: This is only a testing value.


<pre><code><b>const</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_DEFAULT_LOCK_DURATION_MS">DEFAULT_LOCK_DURATION_MS</a>: u64 = 1;
</code></pre>



<a name="(nexus_workflow=0x0)_tool_registry_new"></a>

## Function `new`



<pre><code><b>public</b>(package) <b>fun</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_new">new</a>(ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): ((nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, (nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_OverSlashing">tool_registry::OverSlashing</a>&gt;)
</code></pre>





<a name="(nexus_workflow=0x0)_tool_registry_share"></a>

## Function `share`



<pre><code><b>public</b>(package) <b>fun</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_share">share</a>(self: (nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_tool_registry_slash_off_chain_tool"></a>

## Function `slash_off_chain_tool`

Takes given amount of collateral from a tool.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_slash_off_chain_tool">slash_off_chain_tool</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, _: &(nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_OverSlashing">tool_registry::OverSlashing</a>&gt;, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, amount: u64, clock: &<a href="../dependencies/sui/clock.md#sui_clock_Clock">sui::clock::Clock</a>): <a href="../dependencies/sui/balance.md#sui_balance_Balance">sui::balance::Balance</a>&lt;<a href="../dependencies/sui/sui.md#sui_sui_SUI">sui::sui::SUI</a>&gt;
</code></pre>





<a name="(nexus_workflow=0x0)_tool_registry_set_mist_collateral_to_lock"></a>

## Function `set_mist_collateral_to_lock`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_set_mist_collateral_to_lock">set_mist_collateral_to_lock</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, _: &(nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_OverSlashing">tool_registry::OverSlashing</a>&gt;, new_mist_collateral_to_lock: u64)
</code></pre>





<a name="(nexus_workflow=0x0)_tool_registry_set_lock_duration_ms"></a>

## Function `set_lock_duration_ms`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_set_lock_duration_ms">set_lock_duration_ms</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, _: &(nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_OverSlashing">tool_registry::OverSlashing</a>&gt;, new_duration_ms: u64)
</code></pre>





<a name="(nexus_workflow=0x0)_tool_registry_register_off_chain_tool_for_self"></a>

## Function `register_off_chain_tool_for_self`

Register a new off-chain tool.

To prevent spamming, we lock [ToolRegistry.mist_collateral_to_lock]
[SUI] as collateral.
If the tool is unregistered, the collateral is available after
[ToolRegistry.lock_duration_ms] milliseconds.

See <https://github.com/Talus-Network/nexus-next/wiki/Tool#tool-definitions>
to learn about the expected format of the input and output schemas and the
expected format of the FQN and URL.


<a name="@Slashing_1"></a>

### Slashing


If the tool does not uphold its contract defined by off-chain process the
admin has access to [slash_off_chain_tool] to slash collateral.


<a name="@Owner_Cap_2"></a>

### Owner Cap


Is transferred to the sender of this tx.


<a name="@Gas_Tickets_3"></a>

### Gas Tickets


By default the tool does not require gas for its invocations.
Gas needs to be configured, see the <code><a href="../nexus_workflow/gas.md#(nexus_workflow=0x0)_gas">nexus_workflow::gas</a></code> module.


<pre><code><b>public</b> <b>entry</b> <b>fun</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_register_off_chain_tool_for_self">register_off_chain_tool_for_self</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, url: vector&lt;u8&gt;, input_schema: vector&lt;u8&gt;, output_schema: vector&lt;u8&gt;, pay_with: &<b>mut</b> <a href="../dependencies/sui/coin.md#sui_coin_Coin">sui::coin::Coin</a>&lt;<a href="../dependencies/sui/sui.md#sui_sui_SUI">sui::sui::SUI</a>&gt;, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_tool_registry_register_off_chain_tool"></a>

## Function `register_off_chain_tool`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_register_off_chain_tool">register_off_chain_tool</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, url: vector&lt;u8&gt;, input_schema: vector&lt;u8&gt;, output_schema: vector&lt;u8&gt;, pay_with: &<b>mut</b> <a href="../dependencies/sui/coin.md#sui_coin_Coin">sui::coin::Coin</a>&lt;<a href="../dependencies/sui/sui.md#sui_sui_SUI">sui::sui::SUI</a>&gt;, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): (nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_OverTool">tool_registry::OverTool</a>&gt;
</code></pre>





<a name="(nexus_workflow=0x0)_tool_registry_unregister_off_chain_tool"></a>

## Function `unregister_off_chain_tool`

Permissioned way to unregister a tool.

Soon after this point all DAGs that use this tool will stop working.


<pre><code><b>public</b> <b>entry</b> <b>fun</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_unregister_off_chain_tool">unregister_off_chain_tool</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, owner_cap: &(nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_OverTool">tool_registry::OverTool</a>&gt;, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, clock: &<a href="../dependencies/sui/clock.md#sui_clock_Clock">sui::clock::Clock</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_tool_registry_claim_collateral_for_self"></a>

## Function `claim_collateral_for_self`

Same as [claim_collateral_for_off_chain_tool] but transfers the collateral
to the sender of this tx.


<pre><code><b>public</b> <b>entry</b> <b>fun</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_claim_collateral_for_self">claim_collateral_for_self</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, owner_cap: &(nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_OverTool">tool_registry::OverTool</a>&gt;, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, clock: &<a href="../dependencies/sui/clock.md#sui_clock_Clock">sui::clock::Clock</a>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_tool_registry_claim_collateral_for_off_chain_tool"></a>

## Function `claim_collateral_for_off_chain_tool`

Return collateral to a tool owner.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_claim_collateral_for_off_chain_tool">claim_collateral_for_off_chain_tool</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, owner_cap: &(nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_OverTool">tool_registry::OverTool</a>&gt;, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, clock: &<a href="../dependencies/sui/clock.md#sui_clock_Clock">sui::clock::Clock</a>): <a href="../dependencies/sui/balance.md#sui_balance_Balance">sui::balance::Balance</a>&lt;<a href="../dependencies/sui/sui.md#sui_sui_SUI">sui::sui::SUI</a>&gt;
</code></pre>





<a name="(nexus_workflow=0x0)_tool_registry_deescalate"></a>

## Function `deescalate`

Returns a new [CloneableOwnerCap] for the given tool but with the given
generic type that doesn't have any permissions within this module.

See also [assert_tool_owner_unchecked_generic].


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_deescalate">deescalate</a>&lt;T: drop&gt;(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, owner_cap: &(nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_OverTool">tool_registry::OverTool</a>&gt;, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, witness: T, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): (nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;T&gt;
</code></pre>





<a name="(nexus_workflow=0x0)_tool_registry_did_unregister_period_pass"></a>

## Function `did_unregister_period_pass`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_did_unregister_period_pass">did_unregister_period_pass</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, clock: &<a href="../dependencies/sui/clock.md#sui_clock_Clock">sui::clock::Clock</a>): bool
</code></pre>





<a name="(nexus_workflow=0x0)_tool_registry_assert_tool_registered"></a>

## Function `assert_tool_registered`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_assert_tool_registered">assert_tool_registered</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_tool_registry_assert_tool_owner"></a>

## Function `assert_tool_owner`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_assert_tool_owner">assert_tool_owner</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, owner_cap: &(nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_OverTool">tool_registry::OverTool</a>&gt;, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_tool_registry_assert_tool_owner_unchecked_generic"></a>

## Function `assert_tool_owner_unchecked_generic`

Assert that the owner cap is for the given tool but allows any generic
type to be used.

See also [deescalate].


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_assert_tool_owner_unchecked_generic">assert_tool_owner_unchecked_generic</a>&lt;T&gt;(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, owner_cap: &(nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;T&gt;, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_tool_registry_register_off_chain_tool_"></a>

## Function `register_off_chain_tool_`



<pre><code><b>fun</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_register_off_chain_tool_">register_off_chain_tool_</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, url: vector&lt;u8&gt;, input_schema: vector&lt;u8&gt;, output_schema: vector&lt;u8&gt;, vault: <a href="../dependencies/sui/balance.md#sui_balance_Balance">sui::balance::Balance</a>&lt;<a href="../dependencies/sui/sui.md#sui_sui_SUI">sui::sui::SUI</a>&gt;, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): (nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_OverTool">tool_registry::OverTool</a>&gt;
</code></pre>





<a name="(nexus_workflow=0x0)_tool_registry_did_unregister_period_pass_"></a>

## Function `did_unregister_period_pass_`

Has the tool been unregistered for longer than the lock duration?


<pre><code><b>fun</b> <a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_did_unregister_period_pass_">did_unregister_period_pass_</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_OffChainTool">tool_registry::OffChainTool</a>, clock: &<a href="../dependencies/sui/clock.md#sui_clock_Clock">sui::clock::Clock</a>): bool
</code></pre>




