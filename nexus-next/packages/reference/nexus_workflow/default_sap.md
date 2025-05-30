
<a name="(nexus_workflow=0x0)_default_sap"></a>

# Module `(nexus_workflow=0x0)::default_sap`



-  [Struct `DefaultSAP`](#(nexus_workflow=0x0)_default_sap_DefaultSAP)
-  [Struct `DefaultSAPV1Witness`](#(nexus_workflow=0x0)_default_sap_DefaultSAPV1Witness)
-  [Function `new`](#(nexus_workflow=0x0)_default_sap_new)
-  [Function `begin_dag_execution`](#(nexus_workflow=0x0)_default_sap_begin_dag_execution)
-  [Function `worksheet`](#(nexus_workflow=0x0)_default_sap_worksheet)
-  [Function `confirm_tool_eval_for_walk`](#(nexus_workflow=0x0)_default_sap_confirm_tool_eval_for_walk)
-  [Function `get_witness`](#(nexus_workflow=0x0)_default_sap_get_witness)


<pre><code><b>use</b> (nexus_interface=0x0)::v1;
<b>use</b> (nexus_interface=0x0)::version;
<b>use</b> (nexus_primitives=0x0)::data;
<b>use</b> (nexus_primitives=0x0)::event;
<b>use</b> (nexus_primitives=0x0)::owner_cap;
<b>use</b> (nexus_primitives=0x0)::proof_of_uid;
<b>use</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>;
<b>use</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/leader_cap.md#(nexus_workflow=0x0)_leader_cap">leader_cap</a>;
<b>use</b> <a href="../dependencies/std/address.md#std_address">std::address</a>;
<b>use</b> <a href="../dependencies/std/ascii.md#std_ascii">std::ascii</a>;
<b>use</b> <a href="../dependencies/std/bcs.md#std_bcs">std::bcs</a>;
<b>use</b> <a href="../dependencies/std/option.md#std_option">std::option</a>;
<b>use</b> <a href="../dependencies/std/string.md#std_string">std::string</a>;
<b>use</b> <a href="../dependencies/std/type_name.md#std_type_name">std::type_name</a>;
<b>use</b> <a href="../dependencies/std/vector.md#std_vector">std::vector</a>;
<b>use</b> <a href="../dependencies/sui/address.md#sui_address">sui::address</a>;
<b>use</b> <a href="../dependencies/sui/bag.md#sui_bag">sui::bag</a>;
<b>use</b> <a href="../dependencies/sui/clock.md#sui_clock">sui::clock</a>;
<b>use</b> <a href="../dependencies/sui/dynamic_field.md#sui_dynamic_field">sui::dynamic_field</a>;
<b>use</b> <a href="../dependencies/sui/dynamic_object_field.md#sui_dynamic_object_field">sui::dynamic_object_field</a>;
<b>use</b> <a href="../dependencies/sui/event.md#sui_event">sui::event</a>;
<b>use</b> <a href="../dependencies/sui/hex.md#sui_hex">sui::hex</a>;
<b>use</b> <a href="../dependencies/sui/object.md#sui_object">sui::object</a>;
<b>use</b> <a href="../dependencies/sui/object_table.md#sui_object_table">sui::object_table</a>;
<b>use</b> <a href="../dependencies/sui/table.md#sui_table">sui::table</a>;
<b>use</b> <a href="../dependencies/sui/transfer.md#sui_transfer">sui::transfer</a>;
<b>use</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context">sui::tx_context</a>;
<b>use</b> <a href="../dependencies/sui/vec_map.md#sui_vec_map">sui::vec_map</a>;
<b>use</b> <a href="../dependencies/sui/vec_set.md#sui_vec_set">sui::vec_set</a>;
</code></pre>



<a name="(nexus_workflow=0x0)_default_sap_DefaultSAP"></a>

## Struct `DefaultSAP`

Shared object.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_DefaultSAP">DefaultSAP</a> <b>has</b> key
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
<code>witness: <a href="../dependencies/sui/bag.md#sui_bag_Bag">sui::bag::Bag</a></code>
</dt>
<dd>
 On package upgrade, we'll want to replace the previous witness with a
 new one that identifies the new package.
 This is because as of now Sui doesn't give us access to the package ID
 so we need to always create a new type and query it from the type via
 its type name.
</dd>
<dt>
<code>iv: (nexus_interface=0x0)::version::InterfaceVersion</code>
</dt>
<dd>
 Clients can search the smart agent shared object for this type to
 determine what interface to expect.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_default_sap_DefaultSAPV1Witness"></a>

## Struct `DefaultSAPV1Witness`

Used to identify the package::module deployment.

Will also serve as authorization token to change list of shared objects for
nexus interface v1.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_DefaultSAPV1Witness">DefaultSAPV1Witness</a> <b>has</b> key, store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>id: <a href="../dependencies/sui/object.md#sui_object_UID">sui::object::UID</a></code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_default_sap_new"></a>

## Function `new`



<pre><code><b>public</b>(package) <b>fun</b> <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_new">new</a>(ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>)
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b>(package) <b>fun</b> <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_new">new</a>(ctx: &<b>mut</b> TxContext) {
    <b>let</b> <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap">default_sap</a> = <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_DefaultSAP">DefaultSAP</a> {
        id: object::new(ctx),
        witness: {
            <b>let</b> <b>mut</b> b = bag::new(ctx);
            b.add(b"witness", <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_DefaultSAPV1Witness">DefaultSAPV1Witness</a> { id: object::new(ctx) });
            b
        },
        iv: <a href="../dependencies/nexus_workflow/version.md#(nexus_interface=0x0)_version_v">nexus_interface::version::v</a>(1),
    };
    <a href="../dependencies/nexus_workflow/v1.md#(nexus_interface=0x0)_v1_announce_interface_package">nexus_interface::v1::announce_interface_package</a>(
        <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap">default_sap</a>.<a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_get_witness">get_witness</a>(),
        vector[object::id(&<a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap">default_sap</a>)],
    );
    share_object(<a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap">default_sap</a>);
}
</code></pre>



</details>

<a name="(nexus_workflow=0x0)_default_sap_begin_dag_execution"></a>

## Function `begin_dag_execution`

Invokes the provided entry vertex on a DAG with the provided input data for
each input port.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_begin_dag_execution">begin_dag_execution</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_DefaultSAP">default_sap::DefaultSAP</a>, <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>, network: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a>, entry_group: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EntryGroup">dag::EntryGroup</a>, with_vertex_inputs: <a href="../dependencies/sui/vec_map.md#sui_vec_map_VecMap">sui::vec_map::VecMap</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>, <a href="../dependencies/sui/vec_map.md#sui_vec_map_VecMap">sui::vec_map::VecMap</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_InputPort">dag::InputPort</a>, (nexus_primitives=0x0)::data::NexusData&gt;&gt;, clock: &<a href="../dependencies/sui/clock.md#sui_clock_Clock">sui::clock::Clock</a>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>)
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_begin_dag_execution">begin_dag_execution</a>(
    self: &<b>mut</b> <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_DefaultSAP">DefaultSAP</a>,
    <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>: &DAG,
    network: ID,
    entry_group: EntryGroup,
    with_vertex_inputs: VecMap&lt;Vertex, VecMap&lt;InputPort, NexusData&gt;&gt;,
    clock: &Clock,
    ctx: &<b>mut</b> TxContext,
) {
    self.iv.expect_v(1);
    <b>let</b> <b>mut</b> <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_worksheet">worksheet</a> = self.<a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_worksheet">worksheet</a>();
    <b>let</b> (<b>mut</b> execution, ticket) = <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>.begin_execution_of_entry_group(
        &<b>mut</b> <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_worksheet">worksheet</a>,
        network,
        entry_group,
        with_vertex_inputs,
        clock,
        ctx
    );
    <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_worksheet">worksheet</a>.consume(&self.<a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_get_witness">get_witness</a>().id);
    <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>.request_network_to_execute_walks(&<b>mut</b> execution, ticket, ctx);
    public_share_object(execution);
}
</code></pre>



</details>

<a name="(nexus_workflow=0x0)_default_sap_worksheet"></a>

## Function `worksheet`

Nexus resources can prove that they did a thing.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_worksheet">worksheet</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_DefaultSAP">default_sap::DefaultSAP</a>): (nexus_primitives=0x0)::proof_of_uid::ProofOfUID
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_worksheet">worksheet</a>(self: &<a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_DefaultSAP">DefaultSAP</a>): ProofOfUID {
    self.iv.expect_v(1);
    proof_of_uid::new_with_type(&self.<a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_get_witness">get_witness</a>().id, self.<a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_get_witness">get_witness</a>())
}
</code></pre>



</details>

<a name="(nexus_workflow=0x0)_default_sap_confirm_tool_eval_for_walk"></a>

## Function `confirm_tool_eval_for_walk`

One calls this after workflow contract is done with advancing the DAG.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_confirm_tool_eval_for_walk">confirm_tool_eval_for_walk</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_DefaultSAP">default_sap::DefaultSAP</a>, <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_worksheet">worksheet</a>: (nexus_primitives=0x0)::proof_of_uid::ProofOfUID)
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_confirm_tool_eval_for_walk">confirm_tool_eval_for_walk</a>(
    self: &<b>mut</b> <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_DefaultSAP">DefaultSAP</a>,
    <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_worksheet">worksheet</a>: ProofOfUID,
) {
    self.iv.expect_v(1);
    <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_worksheet">worksheet</a>.consume(&self.<a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_get_witness">get_witness</a>().id);
}
</code></pre>



</details>

<a name="(nexus_workflow=0x0)_default_sap_get_witness"></a>

## Function `get_witness`



<pre><code><b>fun</b> <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_get_witness">get_witness</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_DefaultSAP">default_sap::DefaultSAP</a>): &(nexus_workflow=0x0)::<a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_DefaultSAPV1Witness">default_sap::DefaultSAPV1Witness</a>
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>fun</b> <a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_get_witness">get_witness</a>(self: &<a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_DefaultSAP">DefaultSAP</a>): &<a href="../nexus_workflow/default_sap.md#(nexus_workflow=0x0)_default_sap_DefaultSAPV1Witness">DefaultSAPV1Witness</a> {
    self.witness.borrow(b"witness")
}
</code></pre>



</details>
