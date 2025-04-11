
<a name="(nexus_workflow=0x0)_dag"></a>

# Module `(nexus_workflow=0x0)::dag`



-  [Struct `Vertex`](#(nexus_workflow=0x0)_dag_Vertex)
-  [Struct `EntryGroup`](#(nexus_workflow=0x0)_dag_EntryGroup)
-  [Struct `VertexInfo`](#(nexus_workflow=0x0)_dag_VertexInfo)
-  [Struct `OutputVariant`](#(nexus_workflow=0x0)_dag_OutputVariant)
-  [Struct `OutputPort`](#(nexus_workflow=0x0)_dag_OutputPort)
    -  [Example](#@Example_0)
-  [Struct `OutputVariantPort`](#(nexus_workflow=0x0)_dag_OutputVariantPort)
-  [Struct `InputPort`](#(nexus_workflow=0x0)_dag_InputPort)
-  [Struct `VertexInputPort`](#(nexus_workflow=0x0)_dag_VertexInputPort)
-  [Struct `Edge`](#(nexus_workflow=0x0)_dag_Edge)
-  [Struct `DAG`](#(nexus_workflow=0x0)_dag_DAG)
-  [Struct `DAGExecution`](#(nexus_workflow=0x0)_dag_DAGExecution)
-  [Struct `VertexEvaluations`](#(nexus_workflow=0x0)_dag_VertexEvaluations)
-  [Struct `DAGWalk`](#(nexus_workflow=0x0)_dag_DAGWalk)
-  [Struct `RequestWalkExecution`](#(nexus_workflow=0x0)_dag_RequestWalkExecution)
-  [Struct `DAGCreatedEvent`](#(nexus_workflow=0x0)_dag_DAGCreatedEvent)
-  [Struct `DAGVertexAddedEvent`](#(nexus_workflow=0x0)_dag_DAGVertexAddedEvent)
-  [Struct `DAGEntryVertexInputPortAddedEvent`](#(nexus_workflow=0x0)_dag_DAGEntryVertexInputPortAddedEvent)
-  [Struct `DAGEdgeAddedEvent`](#(nexus_workflow=0x0)_dag_DAGEdgeAddedEvent)
-  [Struct `DAGDefaultValueAddedEvent`](#(nexus_workflow=0x0)_dag_DAGDefaultValueAddedEvent)
-  [Struct `RequestWalkExecutionEvent`](#(nexus_workflow=0x0)_dag_RequestWalkExecutionEvent)
-  [Struct `EndStateReachedEvent`](#(nexus_workflow=0x0)_dag_EndStateReachedEvent)
-  [Struct `WalkAdvancedEvent`](#(nexus_workflow=0x0)_dag_WalkAdvancedEvent)
-  [Struct `ExecutionFinishedEvent`](#(nexus_workflow=0x0)_dag_ExecutionFinishedEvent)
-  [Enum `VertexKind`](#(nexus_workflow=0x0)_dag_VertexKind)
-  [Enum `DAGWalkStatus`](#(nexus_workflow=0x0)_dag_DAGWalkStatus)
-  [Constants](#@Constants_1)
-  [Function `vertex_on_chain`](#(nexus_workflow=0x0)_dag_vertex_on_chain)
-  [Function `vertex_off_chain`](#(nexus_workflow=0x0)_dag_vertex_off_chain)
-  [Function `vertex_from_string`](#(nexus_workflow=0x0)_dag_vertex_from_string)
-  [Function `vertex_into_string`](#(nexus_workflow=0x0)_dag_vertex_into_string)
-  [Function `output_variant_from_string`](#(nexus_workflow=0x0)_dag_output_variant_from_string)
-  [Function `output_variant_into_string`](#(nexus_workflow=0x0)_dag_output_variant_into_string)
-  [Function `output_port_from_string`](#(nexus_workflow=0x0)_dag_output_port_from_string)
-  [Function `output_port_from_raw`](#(nexus_workflow=0x0)_dag_output_port_from_raw)
-  [Function `output_port_into_string`](#(nexus_workflow=0x0)_dag_output_port_into_string)
-  [Function `input_port_from_string`](#(nexus_workflow=0x0)_dag_input_port_from_string)
-  [Function `input_port_into_string`](#(nexus_workflow=0x0)_dag_input_port_into_string)
-  [Function `vertex_input_port`](#(nexus_workflow=0x0)_dag_vertex_input_port)
-  [Function `vertex_input_port_from_string`](#(nexus_workflow=0x0)_dag_vertex_input_port_from_string)
-  [Function `default_entry_group`](#(nexus_workflow=0x0)_dag_default_entry_group)
-  [Function `entry_group_from_string`](#(nexus_workflow=0x0)_dag_entry_group_from_string)
-  [Function `entry_group_into_string`](#(nexus_workflow=0x0)_dag_entry_group_into_string)
-  [Function `inputs_to_begin_execution`](#(nexus_workflow=0x0)_dag_inputs_to_begin_execution)
-  [Function `request_walk_execution`](#(nexus_workflow=0x0)_dag_request_walk_execution)
-  [Function `new`](#(nexus_workflow=0x0)_dag_new)
-  [Function `with_vertex`](#(nexus_workflow=0x0)_dag_with_vertex)
-  [Function `with_entry_port`](#(nexus_workflow=0x0)_dag_with_entry_port)
-  [Function `with_entry_port_in_group`](#(nexus_workflow=0x0)_dag_with_entry_port_in_group)
-  [Function `with_entry`](#(nexus_workflow=0x0)_dag_with_entry)
-  [Function `with_entry_in_group`](#(nexus_workflow=0x0)_dag_with_entry_in_group)
-  [Function `with_edge`](#(nexus_workflow=0x0)_dag_with_edge)
-  [Function `with_default_value`](#(nexus_workflow=0x0)_dag_with_default_value)
-  [Function `rebuild`](#(nexus_workflow=0x0)_dag_rebuild)
-  [Function `begin_execution`](#(nexus_workflow=0x0)_dag_begin_execution)
-  [Function `begin_execution_of_entry_group`](#(nexus_workflow=0x0)_dag_begin_execution_of_entry_group)
-  [Function `request_network_to_execute_walks`](#(nexus_workflow=0x0)_dag_request_network_to_execute_walks)
-  [Function `submit_off_chain_tool_eval_for_walk`](#(nexus_workflow=0x0)_dag_submit_off_chain_tool_eval_for_walk)
-  [Function `submit_on_chain_tool_eval_for_walk`](#(nexus_workflow=0x0)_dag_submit_on_chain_tool_eval_for_walk)
-  [Function `request_walk_execution_walks_indices`](#(nexus_workflow=0x0)_dag_request_walk_execution_walks_indices)
-  [Function `execution_created_at`](#(nexus_workflow=0x0)_dag_execution_created_at)
-  [Function `execution_entry_group`](#(nexus_workflow=0x0)_dag_execution_entry_group)
-  [Function `execution_worksheet_type_name`](#(nexus_workflow=0x0)_dag_execution_worksheet_type_name)
-  [Function `execution_invoker`](#(nexus_workflow=0x0)_dag_execution_invoker)
-  [Function `execution_network`](#(nexus_workflow=0x0)_dag_execution_network)
-  [Function `dag_vertex_tool_fqn`](#(nexus_workflow=0x0)_dag_dag_vertex_tool_fqn)
-  [Function `execution_is_vertex_invoked`](#(nexus_workflow=0x0)_dag_execution_is_vertex_invoked)
-  [Function `request_walk_execution_vertices`](#(nexus_workflow=0x0)_dag_request_walk_execution_vertices)
-  [Function `execution_is_finished`](#(nexus_workflow=0x0)_dag_execution_is_finished)
-  [Function `assert_execution_matches_leader_cap`](#(nexus_workflow=0x0)_dag_assert_execution_matches_leader_cap)
-  [Function `assert_request_walk_execution_is_for`](#(nexus_workflow=0x0)_dag_assert_request_walk_execution_is_for)
-  [Function `assert_execution_is_for`](#(nexus_workflow=0x0)_dag_assert_execution_is_for)
-  [Function `assert_matches_worksheet`](#(nexus_workflow=0x0)_dag_assert_matches_worksheet)
-  [Function `for_walk`](#(nexus_workflow=0x0)_dag_for_walk)
-  [Function `advance_walk`](#(nexus_workflow=0x0)_dag_advance_walk)
-  [Function `if_finished_emit_final_event`](#(nexus_workflow=0x0)_dag_if_finished_emit_final_event)


<pre><code><b>use</b> (nexus_primitives=0x0)::data;
<b>use</b> (nexus_primitives=0x0)::event;
<b>use</b> (nexus_primitives=0x0)::owner_cap;
<b>use</b> (nexus_primitives=0x0)::proof_of_uid;
<b>use</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/leader_cap.md#(nexus_workflow=0x0)_leader_cap">leader_cap</a>;
<b>use</b> <a href="../dependencies/std/address.md#std_address">std::address</a>;
<b>use</b> <a href="../dependencies/std/ascii.md#std_ascii">std::ascii</a>;
<b>use</b> <a href="../dependencies/std/bcs.md#std_bcs">std::bcs</a>;
<b>use</b> <a href="../dependencies/std/option.md#std_option">std::option</a>;
<b>use</b> <a href="../dependencies/std/string.md#std_string">std::string</a>;
<b>use</b> <a href="../dependencies/std/type_name.md#std_type_name">std::type_name</a>;
<b>use</b> <a href="../dependencies/std/vector.md#std_vector">std::vector</a>;
<b>use</b> <a href="../dependencies/sui/address.md#sui_address">sui::address</a>;
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



<a name="(nexus_workflow=0x0)_dag_Vertex"></a>

## Struct `Vertex`



<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">Vertex</a> <b>has</b> <b>copy</b>, drop, store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>name: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a></code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_EntryGroup"></a>

## Struct `EntryGroup`

DAGs can group several [Vertex]s into a single entry point.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EntryGroup">EntryGroup</a> <b>has</b> <b>copy</b>, drop, store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>name: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a></code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_VertexInfo"></a>

## Struct `VertexInfo`



<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_VertexInfo">VertexInfo</a> <b>has</b> <b>copy</b>, drop, store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>kind: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_VertexKind">dag::VertexKind</a></code>
</dt>
<dd>
</dd>
<dt>
<code>input_ports: <a href="../dependencies/sui/vec_set.md#sui_vec_set_VecSet">sui::vec_set::VecSet</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_InputPort">dag::InputPort</a>&gt;</code>
</dt>
<dd>
 We want to know when all input ports are evaluated so that we can start
 the execution of the vertex.
 To know when all are evaluated we need to know how many there are.
 Note that these DO NOT include input ports with default values, only
 those that need to be evaluated by tools.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_OutputVariant"></a>

## Struct `OutputVariant`

Each [Vertex] has a list of exclusive output states.
These could be as simple as "ok" and "err" to many variants.

[OutputVariant] names a variant, e.g. "ok".


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputVariant">OutputVariant</a> <b>has</b> <b>copy</b>, drop, store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>name: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a></code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_OutputPort"></a>

## Struct `OutputPort`

An [OutputVariant] is exclusive.
However, it can contain multiple ports if instantiated.

This models algebraic enumeration type of first degree.


<a name="@Example_0"></a>

### Example

Let's model computation that can fail, or it can succeed with some image
data and some JSON metadata.

There would be a [Vertex] which with two [OutputVariant]s: "ok" and "err".
The "err" [OutputVariant] has one [OutputPort]: "reason".
The "ok" [OutputVariant] has two [OutputPort]s: "img" and "metadata".


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputPort">OutputPort</a> <b>has</b> <b>copy</b>, drop, store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>name: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a></code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_OutputVariantPort"></a>

## Struct `OutputVariantPort`

A union of [OutputVariant], and [OutputPort]  identifies an output port of
a [Vertex].


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputVariantPort">OutputVariantPort</a> <b>has</b> <b>copy</b>, drop, store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>variant: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputVariant">dag::OutputVariant</a></code>
</dt>
<dd>
</dd>
<dt>
<code>port: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputPort">dag::OutputPort</a></code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_InputPort"></a>

## Struct `InputPort`

An input port is a named input to a vertex.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_InputPort">InputPort</a> <b>has</b> <b>copy</b>, drop, store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>name: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a></code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_VertexInputPort"></a>

## Struct `VertexInputPort`

A union of [Vertex] and [InputPort] uniquely identifies an input port within
an DAG graph.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_VertexInputPort">VertexInputPort</a> <b>has</b> <b>copy</b>, drop, store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a></code>
</dt>
<dd>
</dd>
<dt>
<code>port: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_InputPort">dag::InputPort</a></code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_Edge"></a>

## Struct `Edge`

Maps output from unique output port to an input of vertex B.
By storing it in a map with [Vertex] as key we have a unique identification
for a output port in the DAG.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Edge">Edge</a> <b>has</b> <b>copy</b>, drop, store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>from: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputVariantPort">dag::OutputVariantPort</a></code>
</dt>
<dd>
</dd>
<dt>
<code>to: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_VertexInputPort">dag::VertexInputPort</a></code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_DAG"></a>

## Struct `DAG`

A directed acyclic graph (DAG) is a collection of [Vertex]s and [Edge]s
that describe how to walk the graph.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">DAG</a> <b>has</b> key, store
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
<code>vertices: <a href="../dependencies/sui/table.md#sui_table_Table">sui::table::Table</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>, (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_VertexInfo">dag::VertexInfo</a>&gt;</code>
</dt>
<dd>
 Lists all vertices in the graph and maps them to their [VertexInfo].
</dd>
<dt>
<code>entry_groups: <a href="../dependencies/sui/vec_map.md#sui_vec_map_VecMap">sui::vec_map::VecMap</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EntryGroup">dag::EntryGroup</a>, <a href="../dependencies/sui/vec_map.md#sui_vec_map_VecMap">sui::vec_map::VecMap</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>, <a href="../dependencies/sui/vec_set.md#sui_vec_set_VecSet">sui::vec_set::VecSet</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_InputPort">dag::InputPort</a>&gt;&gt;&gt;</code>
</dt>
<dd>
 Defines entry points to the DAG.
 The outer map is a list of groups.
 Only one group can be used to start the execution.
 Those DAGs that don't care about entry groups can use the default one
 defined in [default_entry_group].
 Within a group, all vertex-port pairs are entry and must all be provided
 with a value when beginning an execution.
 For each vertex in the group the DAG will spawn a walk if all vertex
 input ports defined in the <code>vertices</code> map have a value.
 It is possible to provide entry values for vertices that will be
 executed at a later point and not when the execution begins.
 Default values cannot be overridden.
</dd>
<dt>
<code>edges: <a href="../dependencies/sui/table.md#sui_table_Table">sui::table::Table</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>, vector&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Edge">dag::Edge</a>&gt;&gt;</code>
</dt>
<dd>
 Maps the outputs of vertices to the inputs of other vertices.
 The value is never an empty vector.
</dd>
<dt>
<code>defaults_to_input_ports: <a href="../dependencies/sui/table.md#sui_table_Table">sui::table::Table</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_VertexInputPort">dag::VertexInputPort</a>, (nexus_primitives=0x0)::data::NexusData&gt;</code>
</dt>
<dd>
 Maps [VertexInputPort] to default values.
 No [Edge] may lead to this [VertexInputPort].
 We'll ignore any default value if there's an [Edge] leading to the port.
 Useful for configurations such as LLM system prompts.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_DAGExecution"></a>

## Struct `DAGExecution`

Runtime execution of [DAG] comprises walking the graph by evaluating
vertices and following the edges.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">DAGExecution</a> <b>has</b> key, store
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
<code><a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
 For which [DAG] this execution is.
</dd>
<dt>
<code>entry_group: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EntryGroup">dag::EntryGroup</a></code>
</dt>
<dd>
 One of the [DAG] entry groups has to be picked to start an execution.
</dd>
<dt>
<code>invoker: <b>address</b></code>
</dt>
<dd>
 The sender of the tx that invoked [DAG].
</dd>
<dt>
<code>created_at: u64</code>
</dt>
<dd>
 The state of the [Clock] when the execution started.
</dd>
<dt>
<code>worksheet_from_type: <a href="../dependencies/std/type_name.md#std_type_name_TypeName">std::type_name::TypeName</a></code>
</dt>
<dd>
 The off-chain realm can determine the Smart Agent Package to invoke
 thanks to the package address and module name from this field.
</dd>
<dt>
<code>last_request_for_execution_emitted_at_digest: vector&lt;u8&gt;</code>
</dt>
<dd>
 What's the digest of the latest tx in which we emitted an event
 requesting off-chain realm to execute next tool.
 Will be empty if no such event [RequestWalkExecutionEvent] was emitted yet.
 Helps us guarantee that when a tx is over it will have emitted only
 valid events, not ones that were superseded by a newer request for
 execution.
 This would happen if e.g. two on-chain tools were invoked in a single tx.
 It's still possible, but thanks to [RequestWalkExecution] and this field
 we can skip emitting events for all but the last tool(s).
</dd>
<dt>
<code>network: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
 Only those with [OwnerCap] with type [OverNetwork] for this network can
 walk the [DAG].
 This forms an agreement on where computation is executed when it's
 delegated to the off-chain realm.
</dd>
<dt>
<code>evaluations: <a href="../dependencies/sui/object_table.md#sui_object_table_ObjectTable">sui::object_table::ObjectTable</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>, (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_VertexEvaluations">dag::VertexEvaluations</a>&gt;</code>
</dt>
<dd>
 Submitted values that are fed to the relevant input ports.
 Dynamic object fields so that they can be queried.
</dd>
<dt>
<code>walks: vector&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGWalk">dag::DAGWalk</a>&gt;</code>
</dt>
<dd>
 List of concurrent [DAGWalk]s with their states.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_VertexEvaluations"></a>

## Struct `VertexEvaluations`

Holds information about evaluated vertices, concretely input values to ports.

TODO: misnomer


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_VertexEvaluations">VertexEvaluations</a> <b>has</b> key, store
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
<code>ports_to_data: <a href="../dependencies/sui/vec_map.md#sui_vec_map_VecMap">sui::vec_map::VecMap</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_InputPort">dag::InputPort</a>, (nexus_primitives=0x0)::data::NexusData&gt;</code>
</dt>
<dd>
 Contains ports their values.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_DAGWalk"></a>

## Struct `DAGWalk`

Each [DAGWalk] represents a unique path through the [DAG].


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGWalk">DAGWalk</a> <b>has</b> store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>invoked_vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a></code>
</dt>
<dd>
 What's the vertex that should be executed next.
</dd>
<dt>
<code>status: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGWalkStatus">dag::DAGWalkStatus</a></code>
</dt>
<dd>
 What's going on with the walk?
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_RequestWalkExecution"></a>

## Struct `RequestWalkExecution`

Hot-potato object that tracks what is the next thing the off-chain realm
should do which will be emitted with [RequestWalkExecutionEvent].

Having this object allows us to skip emitting events for tools that were
invoked atomically in a single tx.

E.g. if we have a pipeline workflow with on-chain tools A, B, C and
off-chain tool D (A -> B -> C -> D), then we can craft a PT such that A, B
and C are all invoked within in.
In this case we emit an event requesting the off-chain realm to execute D.
However, we could also craft a PT that invokes only A and B.
Then, we emit an event requesting the off-chain realm to execute C.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_RequestWalkExecution">RequestWalkExecution</a>
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>execution: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
 Which [DAGExecution] does this request belong to.
</dd>
<dt>
<code>for_walks_indices: vector&lt;u64&gt;</code>
</dt>
<dd>
 We'll emit an event requesting the off-chain realm to execute next
 vertex on these walks.
 Indices into [DAGExecution.walks].
 Use [request_walk_execution_for_walk] to add a walk.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_DAGCreatedEvent"></a>

## Struct `DAGCreatedEvent`



<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGCreatedEvent">DAGCreatedEvent</a> <b>has</b> <b>copy</b>, drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code><a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_DAGVertexAddedEvent"></a>

## Struct `DAGVertexAddedEvent`



<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGVertexAddedEvent">DAGVertexAddedEvent</a> <b>has</b> <b>copy</b>, drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code><a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
<dt>
<code>vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a></code>
</dt>
<dd>
</dd>
<dt>
<code>kind: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_VertexKind">dag::VertexKind</a></code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_DAGEntryVertexInputPortAddedEvent"></a>

## Struct `DAGEntryVertexInputPortAddedEvent`



<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGEntryVertexInputPortAddedEvent">DAGEntryVertexInputPortAddedEvent</a> <b>has</b> <b>copy</b>, drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code><a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
<dt>
<code>vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a></code>
</dt>
<dd>
</dd>
<dt>
<code>entry_port: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_InputPort">dag::InputPort</a></code>
</dt>
<dd>
</dd>
<dt>
<code>entry_group: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EntryGroup">dag::EntryGroup</a></code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_DAGEdgeAddedEvent"></a>

## Struct `DAGEdgeAddedEvent`



<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGEdgeAddedEvent">DAGEdgeAddedEvent</a> <b>has</b> <b>copy</b>, drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code><a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
<dt>
<code>from_vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a></code>
</dt>
<dd>
</dd>
<dt>
<code>edge: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Edge">dag::Edge</a></code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_DAGDefaultValueAddedEvent"></a>

## Struct `DAGDefaultValueAddedEvent`



<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGDefaultValueAddedEvent">DAGDefaultValueAddedEvent</a> <b>has</b> <b>copy</b>, drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code><a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
<dt>
<code>vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a></code>
</dt>
<dd>
</dd>
<dt>
<code>port: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_InputPort">dag::InputPort</a></code>
</dt>
<dd>
</dd>
<dt>
<code>value: (nexus_primitives=0x0)::data::NexusData</code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_RequestWalkExecutionEvent"></a>

## Struct `RequestWalkExecutionEvent`

See [RequestWalkExecution] and [DAGExecution.last_request_for_execution_emitted_at_digest]
for more information.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_RequestWalkExecutionEvent">RequestWalkExecutionEvent</a> <b>has</b> <b>copy</b>, drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code><a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
<dt>
<code>execution: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
<dt>
<code>walk_index: u64</code>
</dt>
<dd>
</dd>
<dt>
<code>next_vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a></code>
</dt>
<dd>
</dd>
<dt>
<code>evaluations: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
 Dynamic object field which contains [VertexEvaluations] for the next
 vertex.
 Note that this does not include default values which can be known from
 the DAG itself.
</dd>
<dt>
<code>worksheet_from_type: <a href="../dependencies/std/type_name.md#std_type_name_TypeName">std::type_name::TypeName</a></code>
</dt>
<dd>
 The off-chain realm can determine the Smart Agent Package to invoke
 thanks to the package address and module name from this field.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_EndStateReachedEvent"></a>

## Struct `EndStateReachedEvent`

Emitted when a walk reaches an end state, ie. a vertex that has no further
outgoing edges.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EndStateReachedEvent">EndStateReachedEvent</a> <b>has</b> <b>copy</b>, drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code><a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
<dt>
<code>execution: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
<dt>
<code>walk_index: u64</code>
</dt>
<dd>
</dd>
<dt>
<code>vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a></code>
</dt>
<dd>
 Which vertex was the end state.
</dd>
<dt>
<code>variant: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputVariant">dag::OutputVariant</a></code>
</dt>
<dd>
</dd>
<dt>
<code>variant_ports_to_data: <a href="../dependencies/sui/vec_map.md#sui_vec_map_VecMap">sui::vec_map::VecMap</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputPort">dag::OutputPort</a>, (nexus_primitives=0x0)::data::NexusData&gt;</code>
</dt>
<dd>
 We don't store the end state vertex evaluations anywhere, you can get
 them from here only.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_WalkAdvancedEvent"></a>

## Struct `WalkAdvancedEvent`

Emitted when a walk advances to next vertex/vertices.

Includes copy of the vertex evaluations for debugging purposes.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_WalkAdvancedEvent">WalkAdvancedEvent</a> <b>has</b> <b>copy</b>, drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code><a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
<dt>
<code>execution: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
<dt>
<code>walk_index: u64</code>
</dt>
<dd>
</dd>
<dt>
<code>vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a></code>
</dt>
<dd>
</dd>
<dt>
<code>variant: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputVariant">dag::OutputVariant</a></code>
</dt>
<dd>
</dd>
<dt>
<code>variant_ports_to_data: <a href="../dependencies/sui/vec_map.md#sui_vec_map_VecMap">sui::vec_map::VecMap</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputPort">dag::OutputPort</a>, (nexus_primitives=0x0)::data::NexusData&gt;</code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_ExecutionFinishedEvent"></a>

## Struct `ExecutionFinishedEvent`

Emitted when no more work needs to be done.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_ExecutionFinishedEvent">ExecutionFinishedEvent</a> <b>has</b> <b>copy</b>, drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code><a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
<dt>
<code>execution: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
<dt>
<code>has_any_walk_failed: bool</code>
</dt>
<dd>
</dd>
<dt>
<code>has_any_walk_succeeded: bool</code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_VertexKind"></a>

## Enum `VertexKind`



<pre><code><b>public</b> <b>enum</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_VertexKind">VertexKind</a> <b>has</b> <b>copy</b>, drop, store
</code></pre>



<details>
<summary>Variants</summary>


<dl>
<dt>
Variant <code>OnChain</code>
</dt>
<dd>
 Execution is verified with [ProofOfUID].
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
<code>tool: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
</dl>


<dl>
<dt>
<code>tool_fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a></code>
</dt>
<dd>
</dd>
</dl>

<dt>
Variant <code>OffChain</code>
</dt>
<dd>
 Scheduled to be executed off-chain.
 Output of the execution is expected in another tx.
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
<code>tool_fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a></code>
</dt>
<dd>
</dd>
</dl>

</dl>


</details>

<a name="(nexus_workflow=0x0)_dag_DAGWalkStatus"></a>

## Enum `DAGWalkStatus`



<pre><code><b>public</b> <b>enum</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGWalkStatus">DAGWalkStatus</a> <b>has</b> <b>copy</b>, drop, store
</code></pre>



<details>
<summary>Variants</summary>


<dl>
<dt>
Variant <code>Active</code>
</dt>
<dd>
</dd>
<dt>
Variant <code>Successful</code>
</dt>
<dd>
</dd>
<dt>
Variant <code>Failed</code>
</dt>
<dd>
</dd>
<dt>
Variant <code>Consumed</code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="@Constants_1"></a>

## Constants


<a name="(nexus_workflow=0x0)_dag_ENotAnEntryVertex"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_ENotAnEntryVertex">ENotAnEntryVertex</a>: vector&lt;u8&gt; = b"This vertex is not in the <b>entry</b> group";
</code></pre>



<a name="(nexus_workflow=0x0)_dag_ENotAnEntryVertexPort"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_ENotAnEntryVertexPort">ENotAnEntryVertexPort</a>: vector&lt;u8&gt; = b"This vertex-port pair is not in the <b>entry</b> group";
</code></pre>



<a name="(nexus_workflow=0x0)_dag_EAlreadyRequestedWalkExecutionInThisTx"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EAlreadyRequestedWalkExecutionInThisTx">EAlreadyRequestedWalkExecutionInThisTx</a>: vector&lt;u8&gt; = b"Already requested walk execution in this tx";
</code></pre>



<a name="(nexus_workflow=0x0)_dag_ENetworkMismatch"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_ENetworkMismatch">ENetworkMismatch</a>: vector&lt;u8&gt; = b"Provided network ID does not match expected network ID";
</code></pre>



<a name="(nexus_workflow=0x0)_dag_EExpectedOffchainTool"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EExpectedOffchainTool">EExpectedOffchainTool</a>: vector&lt;u8&gt; = b"Expected an off-chain tool";
</code></pre>



<a name="(nexus_workflow=0x0)_dag_EVertexNotFound"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EVertexNotFound">EVertexNotFound</a>: vector&lt;u8&gt; = b"Input vertex does not exist";
</code></pre>



<a name="(nexus_workflow=0x0)_dag_EWalkNotActive"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EWalkNotActive">EWalkNotActive</a>: vector&lt;u8&gt; = b"The walk must be active to do this";
</code></pre>



<a name="(nexus_workflow=0x0)_dag_EWalkDoesNotExpectThisVertex"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EWalkDoesNotExpectThisVertex">EWalkDoesNotExpectThisVertex</a>: vector&lt;u8&gt; = b"The client provided vertex that the walk does not expect";
</code></pre>



<a name="(nexus_workflow=0x0)_dag_EInvokedVertexNotEvaluated"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EInvokedVertexNotEvaluated">EInvokedVertexNotEvaluated</a>: vector&lt;u8&gt; = b"The invoked vertex <b>has</b> not been evaluated";
</code></pre>



<a name="(nexus_workflow=0x0)_dag_EEdgeAndDefaultValueAreMutuallyExclusive"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EEdgeAndDefaultValueAreMutuallyExclusive">EEdgeAndDefaultValueAreMutuallyExclusive</a>: vector&lt;u8&gt; = b"An edge and a default value are mutually exclusive";
</code></pre>



<a name="(nexus_workflow=0x0)_dag_EVertexInputPortAlreadyHasDefaultValue"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EVertexInputPortAlreadyHasDefaultValue">EVertexInputPortAlreadyHasDefaultValue</a>: vector&lt;u8&gt; = b"<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">Vertex</a> input port already <b>has</b> a default value";
</code></pre>



<a name="(nexus_workflow=0x0)_dag_EWorksheetMustBeConstructedWithType"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EWorksheetMustBeConstructedWithType">EWorksheetMustBeConstructedWithType</a>: vector&lt;u8&gt; = b"Worksheet must be constructed with a type";
</code></pre>



<a name="(nexus_workflow=0x0)_dag_EWorksheetTypeMismatch"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EWorksheetTypeMismatch">EWorksheetTypeMismatch</a>: vector&lt;u8&gt; = b"Worksheet was constructed without type or with a different type";
</code></pre>



<a name="(nexus_workflow=0x0)_dag_ENotEntryGroup"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_ENotEntryGroup">ENotEntryGroup</a>: vector&lt;u8&gt; = b"Provided <b>entry</b> group is not this <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">DAG</a>'s <b>entry</b> group";
</code></pre>



<a name="(nexus_workflow=0x0)_dag_EEntryGroupWrongNumberOfInputs"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EEntryGroupWrongNumberOfInputs">EEntryGroupWrongNumberOfInputs</a>: vector&lt;u8&gt; = b"Entry group input does not have the expected number of vertices";
</code></pre>



<a name="(nexus_workflow=0x0)_dag_EExecutionMismatch"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EExecutionMismatch">EExecutionMismatch</a>: vector&lt;u8&gt; = b"Provided execution ID does not match expected execution ID";
</code></pre>



<a name="(nexus_workflow=0x0)_dag_EDAGMismatch"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EDAGMismatch">EDAGMismatch</a>: vector&lt;u8&gt; = b"Provided <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">DAG</a> ID does not match expected <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">DAG</a> ID";
</code></pre>



<a name="(nexus_workflow=0x0)_dag_EDAGEntryGroupResultsInNoWork"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EDAGEntryGroupResultsInNoWork">EDAGEntryGroupResultsInNoWork</a>: vector&lt;u8&gt; = b"The <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">DAG</a> is likely misconfigured <b>as</b> there are no walks to spawn";
</code></pre>



<a name="(nexus_workflow=0x0)_dag_vertex_on_chain"></a>

## Function `vertex_on_chain`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_vertex_on_chain">vertex_on_chain</a>(tool_fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, tool: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_VertexKind">dag::VertexKind</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_vertex_off_chain"></a>

## Function `vertex_off_chain`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_vertex_off_chain">vertex_off_chain</a>(tool_fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_VertexKind">dag::VertexKind</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_vertex_from_string"></a>

## Function `vertex_from_string`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_vertex_from_string">vertex_from_string</a>(name: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_vertex_into_string"></a>

## Function `vertex_into_string`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_vertex_into_string">vertex_into_string</a>(vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>): <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_output_variant_from_string"></a>

## Function `output_variant_from_string`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_output_variant_from_string">output_variant_from_string</a>(name: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputVariant">dag::OutputVariant</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_output_variant_into_string"></a>

## Function `output_variant_into_string`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_output_variant_into_string">output_variant_into_string</a>(variant: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputVariant">dag::OutputVariant</a>): <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_output_port_from_string"></a>

## Function `output_port_from_string`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_output_port_from_string">output_port_from_string</a>(name: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputPort">dag::OutputPort</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_output_port_from_raw"></a>

## Function `output_port_from_raw`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_output_port_from_raw">output_port_from_raw</a>(name: vector&lt;u8&gt;): (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputPort">dag::OutputPort</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_output_port_into_string"></a>

## Function `output_port_into_string`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_output_port_into_string">output_port_into_string</a>(port: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputPort">dag::OutputPort</a>): <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_input_port_from_string"></a>

## Function `input_port_from_string`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_input_port_from_string">input_port_from_string</a>(name: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_InputPort">dag::InputPort</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_input_port_into_string"></a>

## Function `input_port_into_string`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_input_port_into_string">input_port_into_string</a>(port: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_InputPort">dag::InputPort</a>): <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_vertex_input_port"></a>

## Function `vertex_input_port`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_vertex_input_port">vertex_input_port</a>(vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>, port: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_InputPort">dag::InputPort</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_VertexInputPort">dag::VertexInputPort</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_vertex_input_port_from_string"></a>

## Function `vertex_input_port_from_string`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_vertex_input_port_from_string">vertex_input_port_from_string</a>(vertex: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>, port: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_VertexInputPort">dag::VertexInputPort</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_default_entry_group"></a>

## Function `default_entry_group`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_default_entry_group">default_entry_group</a>(): (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EntryGroup">dag::EntryGroup</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_entry_group_from_string"></a>

## Function `entry_group_from_string`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_entry_group_from_string">entry_group_from_string</a>(name: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EntryGroup">dag::EntryGroup</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_entry_group_into_string"></a>

## Function `entry_group_into_string`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_entry_group_into_string">entry_group_into_string</a>(group: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EntryGroup">dag::EntryGroup</a>): <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_inputs_to_begin_execution"></a>

## Function `inputs_to_begin_execution`

Helper to construct inputs for [begin_execution].
Creates a map from a row based input (ie. repeat vertex name for each row).


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_inputs_to_begin_execution">inputs_to_begin_execution</a>(vertices: vector&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>&gt;, ports: vector&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_InputPort">dag::InputPort</a>&gt;, data: vector&lt;(nexus_primitives=0x0)::data::NexusData&gt;): <a href="../dependencies/sui/vec_map.md#sui_vec_map_VecMap">sui::vec_map::VecMap</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>, <a href="../dependencies/sui/vec_map.md#sui_vec_map_VecMap">sui::vec_map::VecMap</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_InputPort">dag::InputPort</a>, (nexus_primitives=0x0)::data::NexusData&gt;&gt;
</code></pre>





<a name="(nexus_workflow=0x0)_dag_request_walk_execution"></a>

## Function `request_walk_execution`

Creates a hot potato object that can be destroyed with [request_network_to_execute_walks].


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_request_walk_execution">request_walk_execution</a>(execution: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_RequestWalkExecution">dag::RequestWalkExecution</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_new"></a>

## Function `new`

Creates an empty [DAG].

A [DAG] can be edited only while it's an owned object.
It becomes immutable once it's shared.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_new">new</a>(ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_with_vertex"></a>

## Function `with_vertex`

Adds a new vertex.

The list of entry ports is added to the default entry group.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_with_vertex">with_vertex</a>(self: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>, name: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>, kind: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_VertexKind">dag::VertexKind</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_with_entry_port"></a>

## Function `with_entry_port`

Add a new input port to the vertex which has to be provided by the client
when they begin execution with the default entry group.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_with_entry_port">with_entry_port</a>(self: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>, vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>, entry_port: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_InputPort">dag::InputPort</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_with_entry_port_in_group"></a>

## Function `with_entry_port_in_group`

Add a new input port to the vertex which has to be provided by the client
when they begin execution with the provided entry group.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_with_entry_port_in_group">with_entry_port_in_group</a>(self: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>, vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>, entry_port: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_InputPort">dag::InputPort</a>, entry_group: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EntryGroup">dag::EntryGroup</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_with_entry"></a>

## Function `with_entry`

Use this after [with_vertex] to add that vertex to the default entry group.

See also [with_entry_in_group]


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_with_entry">with_entry</a>(self: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>, vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_with_entry_in_group"></a>

## Function `with_entry_in_group`

Use this after [with_vertex] to add that vertex to the given entry group.

Special case for vertices that are meant to have no input ports and should
be executed as soon as the execution begins.

[begin_execution] will start execution of this vertex only if it has no
input ports.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_with_entry_in_group">with_entry_in_group</a>(self: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>, vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>, entry_group: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EntryGroup">dag::EntryGroup</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_with_edge"></a>

## Function `with_edge`

Adds a new edge to the DAG.
The caller must ensure all constraints required by the workflow engine are
upheld.
See README for more information.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_with_edge">with_edge</a>(self: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>, from_vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>, from_variant: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputVariant">dag::OutputVariant</a>, from_port: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputPort">dag::OutputPort</a>, to_vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>, to_port: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_InputPort">dag::InputPort</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_with_default_value"></a>

## Function `with_default_value`

This [InputPort] mustn't have any [Edge] leading to it.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_with_default_value">with_default_value</a>(self: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>, vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>, port: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_InputPort">dag::InputPort</a>, value: (nexus_primitives=0x0)::data::NexusData): (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_rebuild"></a>

## Function `rebuild`

Consumes the input [DAG] and returns a copy of it with a new ID.

This is useful if you want to build a [DAG] over multiple txs or ahead of
time.

The [DAG] can be an owned object only to be rebuilt and shared at a more
convenient time.

(On Sui an object can be shared only in the tx that created it.)


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_rebuild">rebuild</a>(self: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_begin_execution"></a>

## Function `begin_execution`

Permission-lessly creates a new [DAGExecution] object using the default
entry group.
This will fail if there isn't a default entry group.

See also [begin_execution_of_entry_group].


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_begin_execution">begin_execution</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>, worksheet: &<b>mut</b> (nexus_primitives=0x0)::proof_of_uid::ProofOfUID, network: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a>, with_inputs: <a href="../dependencies/sui/vec_map.md#sui_vec_map_VecMap">sui::vec_map::VecMap</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>, <a href="../dependencies/sui/vec_map.md#sui_vec_map_VecMap">sui::vec_map::VecMap</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_InputPort">dag::InputPort</a>, (nexus_primitives=0x0)::data::NexusData&gt;&gt;, clock: &<a href="../dependencies/sui/clock.md#sui_clock_Clock">sui::clock::Clock</a>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): ((nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>, (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_RequestWalkExecution">dag::RequestWalkExecution</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_dag_begin_execution_of_entry_group"></a>

## Function `begin_execution_of_entry_group`

Permission-lessly creates a new [DAGExecution] object.

This method stamps [ProofOfUID] with proof that the [DAG] created
this [DAGExecution].

The only way to form a valid tx is to eventually call
[request_network_to_execute_walks].


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_begin_execution_of_entry_group">begin_execution_of_entry_group</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>, worksheet: &<b>mut</b> (nexus_primitives=0x0)::proof_of_uid::ProofOfUID, network: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a>, entry_group: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EntryGroup">dag::EntryGroup</a>, with_inputs: <a href="../dependencies/sui/vec_map.md#sui_vec_map_VecMap">sui::vec_map::VecMap</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>, <a href="../dependencies/sui/vec_map.md#sui_vec_map_VecMap">sui::vec_map::VecMap</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_InputPort">dag::InputPort</a>, (nexus_primitives=0x0)::data::NexusData&gt;&gt;, clock: &<a href="../dependencies/sui/clock.md#sui_clock_Clock">sui::clock::Clock</a>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): ((nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>, (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_RequestWalkExecution">dag::RequestWalkExecution</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_dag_request_network_to_execute_walks"></a>

## Function `request_network_to_execute_walks`

Consumes [RequestWalkExecution] and emits [RequestWalkExecutionEvent] to
the off-chain realm to carry on with the execution in another tx.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_request_network_to_execute_walks">request_network_to_execute_walks</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>, execution: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>, request: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_RequestWalkExecution">dag::RequestWalkExecution</a>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_dag_submit_off_chain_tool_eval_for_walk"></a>

## Function `submit_off_chain_tool_eval_for_walk`

This is meant to be invoked by the off-chain network after it evaluated a
tool (which is represented by a vertex in DAG).

Which vertex to evaluate is derived from the walk index and then compared to
the provided sanity-check argument <code>expected_vertex</code>.

The [Worksheet] is must be created with a type that matches the worksheet
of [RequestWalkExecution].
This type will be emitted in the [RequestWalkExecutionEvent].


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_submit_off_chain_tool_eval_for_walk">submit_off_chain_tool_eval_for_walk</a>(<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>, execution: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>, worksheet: &<b>mut</b> (nexus_primitives=0x0)::proof_of_uid::ProofOfUID, <a href="../nexus_workflow/leader_cap.md#(nexus_workflow=0x0)_leader_cap">leader_cap</a>: &(nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/leader_cap.md#(nexus_workflow=0x0)_leader_cap_OverNetwork">leader_cap::OverNetwork</a>&gt;, <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_request_walk_execution">request_walk_execution</a>: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_RequestWalkExecution">dag::RequestWalkExecution</a>, walk_index: u64, expected_vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>, variant: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputVariant">dag::OutputVariant</a>, variant_ports_to_data: <a href="../dependencies/sui/vec_map.md#sui_vec_map_VecMap">sui::vec_map::VecMap</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputPort">dag::OutputPort</a>, (nexus_primitives=0x0)::data::NexusData&gt;, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_dag_submit_on_chain_tool_eval_for_walk"></a>

## Function `submit_on_chain_tool_eval_for_walk`

After invoking a tool on-chain, this function is called to submit the result
of the evaluation.

The [Worksheet] is must be created with a type that matches the worksheet
of [RequestWalkExecution].
This type will be emitted in the [RequestWalkExecutionEvent].


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_submit_on_chain_tool_eval_for_walk">submit_on_chain_tool_eval_for_walk</a>(<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>, execution: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>, worksheet: &<b>mut</b> (nexus_primitives=0x0)::proof_of_uid::ProofOfUID, <a href="../nexus_workflow/leader_cap.md#(nexus_workflow=0x0)_leader_cap">leader_cap</a>: &(nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/leader_cap.md#(nexus_workflow=0x0)_leader_cap_OverNetwork">leader_cap::OverNetwork</a>&gt;, <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_request_walk_execution">request_walk_execution</a>: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_RequestWalkExecution">dag::RequestWalkExecution</a>, walk_index: u64, expected_vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>, variant: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputVariant">dag::OutputVariant</a>, variant_ports_to_data: <a href="../dependencies/sui/vec_map.md#sui_vec_map_VecMap">sui::vec_map::VecMap</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputPort">dag::OutputPort</a>, (nexus_primitives=0x0)::data::NexusData&gt;, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_dag_request_walk_execution_walks_indices"></a>

## Function `request_walk_execution_walks_indices`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_request_walk_execution_walks_indices">request_walk_execution_walks_indices</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_RequestWalkExecution">dag::RequestWalkExecution</a>): &vector&lt;u64&gt;
</code></pre>





<a name="(nexus_workflow=0x0)_dag_execution_created_at"></a>

## Function `execution_created_at`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_execution_created_at">execution_created_at</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>): u64
</code></pre>





<a name="(nexus_workflow=0x0)_dag_execution_entry_group"></a>

## Function `execution_entry_group`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_execution_entry_group">execution_entry_group</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>): &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_EntryGroup">dag::EntryGroup</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_execution_worksheet_type_name"></a>

## Function `execution_worksheet_type_name`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_execution_worksheet_type_name">execution_worksheet_type_name</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>): &<a href="../dependencies/std/type_name.md#std_type_name_TypeName">std::type_name::TypeName</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_execution_invoker"></a>

## Function `execution_invoker`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_execution_invoker">execution_invoker</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>): <b>address</b>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_execution_network"></a>

## Function `execution_network`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_execution_network">execution_network</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>): <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_dag_vertex_tool_fqn"></a>

## Function `dag_vertex_tool_fqn`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_dag_vertex_tool_fqn">dag_vertex_tool_fqn</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>, vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>): <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>
</code></pre>





<a name="(nexus_workflow=0x0)_dag_execution_is_vertex_invoked"></a>

## Function `execution_is_vertex_invoked`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_execution_is_vertex_invoked">execution_is_vertex_invoked</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>, vertex: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>): bool
</code></pre>





<a name="(nexus_workflow=0x0)_dag_request_walk_execution_vertices"></a>

## Function `request_walk_execution_vertices`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_request_walk_execution_vertices">request_walk_execution_vertices</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_RequestWalkExecution">dag::RequestWalkExecution</a>, <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>, execution: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>): vector&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>&gt;
</code></pre>





<a name="(nexus_workflow=0x0)_dag_execution_is_finished"></a>

## Function `execution_is_finished`

Returns true if all walks are in a terminal state.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_execution_is_finished">execution_is_finished</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>): bool
</code></pre>





<a name="(nexus_workflow=0x0)_dag_assert_execution_matches_leader_cap"></a>

## Function `assert_execution_matches_leader_cap`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_assert_execution_matches_leader_cap">assert_execution_matches_leader_cap</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>, <a href="../nexus_workflow/leader_cap.md#(nexus_workflow=0x0)_leader_cap">leader_cap</a>: &(nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/leader_cap.md#(nexus_workflow=0x0)_leader_cap_OverNetwork">leader_cap::OverNetwork</a>&gt;)
</code></pre>





<a name="(nexus_workflow=0x0)_dag_assert_request_walk_execution_is_for"></a>

## Function `assert_request_walk_execution_is_for`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_assert_request_walk_execution_is_for">assert_request_walk_execution_is_for</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_RequestWalkExecution">dag::RequestWalkExecution</a>, execution: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_dag_assert_execution_is_for"></a>

## Function `assert_execution_is_for`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_assert_execution_is_for">assert_execution_is_for</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>, <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_dag_assert_matches_worksheet"></a>

## Function `assert_matches_worksheet`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_assert_matches_worksheet">assert_matches_worksheet</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>, worksheet: &(nexus_primitives=0x0)::proof_of_uid::ProofOfUID)
</code></pre>





<a name="(nexus_workflow=0x0)_dag_for_walk"></a>

## Function `for_walk`

Won't add the walk if it's already there.


<pre><code><b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_for_walk">for_walk</a>(self: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_RequestWalkExecution">dag::RequestWalkExecution</a>, walk_index: u64)
</code></pre>





<a name="(nexus_workflow=0x0)_dag_advance_walk"></a>

## Function `advance_walk`

Advances the walk by evaluating the vertex and following the edges if possible.


<pre><code><b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_advance_walk">advance_walk</a>(<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag">dag</a>: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAG">dag::DAG</a>, execution: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>, <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_request_walk_execution">request_walk_execution</a>: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_RequestWalkExecution">dag::RequestWalkExecution</a>, walk_index: u64, expected_vertex: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_Vertex">dag::Vertex</a>, variant: (nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputVariant">dag::OutputVariant</a>, variant_ports_to_data: <a href="../dependencies/sui/vec_map.md#sui_vec_map_VecMap">sui::vec_map::VecMap</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_OutputPort">dag::OutputPort</a>, (nexus_primitives=0x0)::data::NexusData&gt;, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>)
</code></pre>





<a name="(nexus_workflow=0x0)_dag_if_finished_emit_final_event"></a>

## Function `if_finished_emit_final_event`

Will emit an event if the execution is done.


<pre><code><b>fun</b> <a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_if_finished_emit_final_event">if_finished_emit_final_event</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/dag.md#(nexus_workflow=0x0)_dag_DAGExecution">dag::DAGExecution</a>)
</code></pre>




