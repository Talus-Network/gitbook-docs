# Default Talus Agent Package (TAP)

## Overview

The Default TAP is a useful helper component for Nexus agent developers. It serves as a template or base implementation of a Talus Agent Package (TAP) that can be used for examples, tests, or to run JSON-defined DAGs from the CLI.

## Interface Compliance

The Default TAP implements the [Nexus Interface V1][nexus-interface-v1]  specification, which defines the required functionality for any Talus Agent Package to integrate with the Nexus workflow engine. Key interface requirements include:

1. **Version Management**
   - Must declare and maintain interface version compatibility.
   - Must support version checking for backward compatibility.

2. **Workflow Management**
   - Must handle worksheet management and state tracking.
   - Must support tool evaluation confirmation.

3. **Authorization**
   - Must implement witness-based authorization.
   - Must support package upgrade mechanisms.

For detailed interface requirements, see the [Nexus Interface Documentation][nexus-interface] .

<!-- Gitbook syntax -->
{% hint style="info" %} In the code snippets below, we reference some Sui Move patterns (e.g. hot potato), please refer to the [primitives pakcage doc][packages-primitives] for more information on the approach taken here. {% endhint %}

### DefaultTAP Structure

The agent will be represented by the `DefaultTAP` struct, which is a shared object that contains:
- `id`: A unique identifier for the TAP instance.
- `witness`: A Bag containing authorization tokens for package identification and upgrade management.
- `iv`: The interface version (currently v1) that clients can use to determine compatibility.

```rust
use nexus_interface::version::InterfaceVersion;
use sui::bag::{Self, Bag};
use sui::object::UID;

/// Shared object implementing the Nexus Interface v1 specification.
public struct DefaultTAP has key {
    id: UID,
    /// On package upgrade, we'll want to replace the previous witness with a
    /// new one that identifies the new package.
    ///
    /// This is because as of now Sui doesn't give us access to the package ID
    /// so we need to always create a new type and query it from the type via
    /// its type name.
    witness: Bag,
    /// Clients can search the smart agent shared object for this type to
    /// determine what interface to expect.
    iv: InterfaceVersion,
}
```

### Constructor and Leader Registration

The DefaultTAP is created using the `new()` constructor function, which:
1. Creates a new DefaultTAP instance with a unique ID.
2. Initializes a witness token for package identification.
3. Sets the Nexus interface version to v1.
4. Registers the TAP with the Nexus leader.

```rust
use nexus_interface::version::{Self, InterfaceVersion};
use sui::bag::{Self, Bag};
use sui::object::UID;
use sui::transfer::share_object;

public(package) fun new(ctx: &mut TxContext) {
    let default_sap = DefaultSAP {
        id: object::new(ctx),
        witness: {
            let mut b = bag::new(ctx);
            b.add(b"witness", DefaultSAPV1Witness { id: object::new(ctx) });
            b
        },
        iv: version::v(1),
    };

    announce_interface_package(
        default_sap.get_witness(),
        vector[object::id(&default_sap)],
    );

    share_object(default_sap);
}

/// with...
public struct DefaultSAPV1Witness has key, store {
    id: UID,
}
```

### Worksheet

The worksheet function is a core requirement of the Nexus Interface V1 specification. It creates a proof of UID (Unique Identifier) that serves as a "stamp collector" for tracking workflow execution state. This proof:

1. Acts as a hot-potato object that collects execution confirmations from Nexus components like the DAG.
2. Must be constructed with a type defined in the same package and module that implements the interface.
3. Is used to verify that required operations have been performed in the correct sequence.

```rust
use nexus_interface::version::InterfaceVersion;
use nexus_primitives::proof_of_uid::{Self, ProofOfUID};

public fun worksheet(self: &DefaultSAP): ProofOfUID {
    self.iv.expect_v(1);
    proof_of_uid::new_with_type(&self.get_witness().id, self.get_witness())
}
```

### Tool Evaluation Confirmation

The `confirm_tool_eval_for_walk` function is another core requirement of the Nexus Interface V1 specification. It is invoked by the Nexus Leader after a workflow contract has advanced the DAG to:

1. Consume the worksheet hot-potato.
2. Verify that all required confirmations have been collected.
3. Complete the tool evaluation cycle for a specific walk in the workflow.

```rust
use nexus_interface::version::InterfaceVersion

public fun confirm_tool_eval_for_walk(
    self: &mut DefaultSAP,
    worksheet: ProofOfUID,
) {
    self.iv.expect_v(1);
    worksheet.consume(&self.get_witness().id);
}

/// with...
fun get_witness(self: &DefaultSAP): &DefaultSAPV1Witness {
    self.witness.borrow(b"witness")
}
```

## DAG Execution

The Default TAP works in conjunction with the Nexus workflow engine, which provides:

1. **DAG Implementation**
   - Directed Acyclic Graph data structure for modeling complex workflows.
   - Support for vertices, edges, and input/output ports.
   - Entry group management for workflow initiation.

2. **Tool Registry**
   - Registration and management of available tools.

3. **Tool Invocation**
   - Support for tool execution invocation, onchain or offchain.
   - Leader capability management.

Where the above steps effectively ensure interface compliance, the (default) TAP also needs to enable DAG execution.

### Begin DAG Execution

The DAG execution is initiated through the `begin_dag_execution` function.

This function:

1. Takes a DAG and entry vertices with their input data.
2. Creates a worksheet to track execution state.
3. Begins execution of the entry group through the DAG.
4. Requests the network to execute walks through the DAG.
5. Shares the execution object for tracking progress.

```rust
use nexus_primitives::data::NexusData;
use nexus_primitives::proof_of_uid::{Self, ProofOfUID};
use nexus_workflow::dag::{DAG, Vertex, InputPort, EntryGroup};

/// Invokes the provided entry vertex on a DAG with the provided input data for
/// each input port.
public fun begin_dag_execution(
    self: &mut DefaultSAP,
    dag: &DAG,
    network: ID,
    entry_group: EntryGroup,
    mut with_vertex_inputs: VecMap<Vertex, VecMap<InputPort, NexusData>>,
    ctx: &mut TxContext,
) {
    self.iv.expect_v(1);

    let mut entry_vertices = vector[];
    let mut with_vertices_inputs = vector[];
    while (!with_vertex_inputs.is_empty()) {
        let (vertex, inputs) = with_vertex_inputs.pop();
        entry_vertices.push_back(vertex);
        with_vertices_inputs.push_back(inputs);
    };

    let mut worksheet = self.worksheet();

    let (mut execution, ticket) = dag.begin_execution_of_entry_group(
        &mut worksheet,
        network,
        entry_group,
        entry_vertices,
        with_vertices_inputs,
        ctx
    );

    worksheet.consume(&self.get_witness().id);

    dag.request_network_to_execute_walks(&mut execution, ticket, ctx);

    public_share_object(execution);
}
```

## Security Considerations

- The TAP uses witness tokens for authorization as required by the [Nexus Interface][nexus-interface].
- Interface version checking ensures compatibility.
- Worksheet proofs ensure state integrity.
- Tool execution is properly isolated.
<!-- TODO: refer to Security analysis after integrating Stephen's whitepaper section on it -->

## Full Module Code

Toggle to see the full module code for the default TAP:
<details>

<summary>Toggle code</summary>

```rust
module nexus_workflow::default_sap;

//! Module defining a default smart agent package with no added logic but
//! executing the provided DAG. This can be used for examples, tests or to run
//! JSON-defined DAGs from the CLI or via other means.

use nexus_interface::version::InterfaceVersion;
use nexus_primitives::data::NexusData;
use nexus_primitives::proof_of_uid::{Self, ProofOfUID};
use nexus_workflow::dag::{DAG, Vertex, InputPort, EntryGroup};

use sui::bag::{Self, Bag};
use sui::transfer::{share_object, public_share_object};
use sui::vec_map::{VecMap};

/// Shared object.
public struct DefaultSAP has key {
    id: UID,
    /// On package upgrade, we'll want to replace the previous witness with a
    /// new one that identifies the new package.
    ///
    /// This is because as of now Sui doesn't give us access to the package ID
    /// so we need to always create a new type and query it from the type via
    /// its type name.
    witness: Bag,
    /// Clients can search the smart agent shared object for this type to
    /// determine what interface to expect.
    iv: InterfaceVersion,
}

/// Used to identify the package::module deployment.
///
/// Will also serve as authorization token to change list of shared objects for
/// nexus interface v1.
public struct DefaultSAPV1Witness has key, store {
    id: UID,
}

public(package) fun new(ctx: &mut TxContext) {
    let default_sap = DefaultSAP {
        id: object::new(ctx),
        witness: {
            let mut b = bag::new(ctx);
            b.add(b"witness", DefaultSAPV1Witness { id: object::new(ctx) });
            b
        },
        iv: nexus_interface::version::v(1),
    };

    nexus_interface::v1::announce_interface_package(
        default_sap.get_witness(),
        vector[object::id(&default_sap)],
    );

    share_object(default_sap);
}

// === Client entry ===

/// Invokes the provided entry vertex on a DAG with the provided input data for
/// each input port.
#[allow(lint(share_owned))]
public fun begin_dag_execution(
    self: &mut DefaultSAP,
    dag: &DAG,
    network: ID,
    entry_group: EntryGroup,
    mut with_vertex_inputs: VecMap<Vertex, VecMap<InputPort, NexusData>>,
    ctx: &mut TxContext,
) {
    self.iv.expect_v(1);

    let mut entry_vertices = vector[];
    let mut with_vertices_inputs = vector[];
    while (!with_vertex_inputs.is_empty()) {
        let (vertex, inputs) = with_vertex_inputs.pop();
        entry_vertices.push_back(vertex);
        with_vertices_inputs.push_back(inputs);
    };

    let mut worksheet = self.worksheet();

    let (mut execution, ticket) = dag.begin_execution_of_entry_group(
        &mut worksheet,
        network,
        entry_group,
        entry_vertices,
        with_vertices_inputs,
        ctx
    );

    worksheet.consume(&self.get_witness().id);

    dag.request_network_to_execute_walks(&mut execution, ticket, ctx);

    public_share_object(execution);
}

// === Nexus interface v1 ===

/// Nexus resources can prove that they did a thing.
public fun worksheet(self: &DefaultSAP): ProofOfUID {
    self.iv.expect_v(1);

    proof_of_uid::new_with_type(&self.get_witness().id, self.get_witness())
}

/// One calls this after workflow contract is done with advancing the DAG.
public fun confirm_tool_eval_for_walk(
    self: &mut DefaultSAP,
    worksheet: ProofOfUID,
) {
    self.iv.expect_v(1);

    worksheet.consume(&self.get_witness().id);
}

fun get_witness(self: &DefaultSAP): &DefaultSAPV1Witness {
    self.witness.borrow(b"witness")
}

```

</details>

<!-- List of references -->

[nexus-interface]: ../packages/Nexus-Interface.md
[nexus-interface-v1]: ../packages/Nexus-Interface.md#v1
[packages-primitives]: ../packages/Primitives.md
