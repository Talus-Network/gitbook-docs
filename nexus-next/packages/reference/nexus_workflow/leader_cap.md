
<a name="(nexus_workflow=0x0)_leader_cap"></a>

# Module `(nexus_workflow=0x0)::leader_cap`



-  [Struct `OverNetwork`](#(nexus_workflow=0x0)_leader_cap_OverNetwork)
-  [Struct `FoundingLeaderCapCreatedEvent`](#(nexus_workflow=0x0)_leader_cap_FoundingLeaderCapCreatedEvent)
-  [Function `new`](#(nexus_workflow=0x0)_leader_cap_new)
-  [Function `create_for_self_and_addresses`](#(nexus_workflow=0x0)_leader_cap_create_for_self_and_addresses)


<pre><code><b>use</b> (nexus_primitives=0x0)::event;
<b>use</b> (nexus_primitives=0x0)::owner_cap;
<b>use</b> <a href="../dependencies/std/ascii.md#std_ascii">std::ascii</a>;
<b>use</b> <a href="../dependencies/std/bcs.md#std_bcs">std::bcs</a>;
<b>use</b> <a href="../dependencies/std/option.md#std_option">std::option</a>;
<b>use</b> <a href="../dependencies/std/string.md#std_string">std::string</a>;
<b>use</b> <a href="../dependencies/std/vector.md#std_vector">std::vector</a>;
<b>use</b> <a href="../dependencies/sui/address.md#sui_address">sui::address</a>;
<b>use</b> <a href="../dependencies/sui/event.md#sui_event">sui::event</a>;
<b>use</b> <a href="../dependencies/sui/hex.md#sui_hex">sui::hex</a>;
<b>use</b> <a href="../dependencies/sui/object.md#sui_object">sui::object</a>;
<b>use</b> <a href="../dependencies/sui/transfer.md#sui_transfer">sui::transfer</a>;
<b>use</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context">sui::tx_context</a>;
</code></pre>



<a name="(nexus_workflow=0x0)_leader_cap_OverNetwork"></a>

## Struct `OverNetwork`

Type of [OwnerCap] that can be held by the leader of an off-chain network.
An off-chain network has one or more equally trusted leaders.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/leader_cap.md#(nexus_workflow=0x0)_leader_cap_OverNetwork">OverNetwork</a> <b>has</b> drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
</dl>


</details>

<a name="(nexus_workflow=0x0)_leader_cap_FoundingLeaderCapCreatedEvent"></a>

## Struct `FoundingLeaderCapCreatedEvent`



<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/leader_cap.md#(nexus_workflow=0x0)_leader_cap_FoundingLeaderCapCreatedEvent">FoundingLeaderCapCreatedEvent</a> <b>has</b> <b>copy</b>, drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code><a href="../nexus_workflow/leader_cap.md#(nexus_workflow=0x0)_leader_cap">leader_cap</a>: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
<dt>
<code>network: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_leader_cap_new"></a>

## Function `new`

Creates a founding [CloneableOwnerCap] with a random network ID.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/leader_cap.md#(nexus_workflow=0x0)_leader_cap_new">new</a>(ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): (nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/leader_cap.md#(nexus_workflow=0x0)_leader_cap_OverNetwork">leader_cap::OverNetwork</a>&gt;
</code></pre>





<a name="(nexus_workflow=0x0)_leader_cap_create_for_self_and_addresses"></a>

## Function `create_for_self_and_addresses`



<pre><code><b>public</b> <b>entry</b> <b>fun</b> <a href="../nexus_workflow/leader_cap.md#(nexus_workflow=0x0)_leader_cap_create_for_self_and_addresses">create_for_self_and_addresses</a>(n_per_address: u64, addresses: vector&lt;<b>address</b>&gt;, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>)
</code></pre>




