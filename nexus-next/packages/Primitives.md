# Primitives Package

> concerns [`sui/primitives` package][repo-primitives-package]

Exports types that allow two Sui packages, A and B, to communicate with each other in an authenticated way without using explicit Move dependencies. Instead, A and B have a shared dependency on this package, `nexus_primitives`.

## Why is this useful?

Avoiding explicit dependencies shifts complexity from the Move code to the off-chain realm.
It is the off-chain realm's responsibility to craft programmable transaction blocks (PTBs) such that the expectations of the on-chain realm are met.

Thanks to this trade-off the system is more friendly to plug-and-play components.

Payments, workflows, verifications, those can have on-chain design that minimizes the need for explicit dependencies between each other.
Therefore, upgrading components is less likely to require changes to other components.

## Core Modules

### 1. ProofOfUID

`UID` (Unique Identifier) proves that an object exist on-chain and its unique. By requiring passing a UID reference as the input and keeping a record of the ID of the UID that was passed as argument we can prove that only the module that defined that object did that operation. As only that module can access the UID.

This is achieved with the [hot potato pattern][move-hot-potato].

{% hint style="info" %}
This is a step away from explicitness and towards conventions.
Prior similar work includes [Originbyte's `request` module][ob-request-module] and [Mysten's `transfer_policy` module][sui-transfer-policy].
{% endhint %}

A hot potato struct that enables authenticated communication between different packages without explicit dependencies. The `ProofOfUID` is created by one package and subsequently utilized across (potentially) multiple calls inside a PTB, allowing different participating packages to add their unique stamps.

```rust
module module_a {
    use nexus_primitives::proof_of_uid::{ProofOfUID};

    struct OwnerObject has key {
        id: UID,
    }

    public entry fun initiate_action(owner: &mut OwnerObject, ctx: &mut TxContext) {
        // Create a ProofOfUID tied to the OwnerObject
        let mut proof = ProofOfUID::create(&owner.id, ctx);

        // Pass the ProofOfUID to module B for stamping
        module_b::perform_action(&mut proof);

        // Consume the ProofOfUID after stamping
        proof.consume(&owner.id);
    }
}
```
```rust
module module_b {
    use nexus_primitives::proof_of_uid::{ProofOfUID};

    public fun perform_action(proof: &mut ProofOfUID) {
        // Perform some operation and stamp the ProofOfUID
        proof.stamp();
    }
}
```
Explanation of the Code
1. Module A:
    - Creates a `ProofOfUID` tied to its OwnerObject.
    - Passes the `ProofOfUID` to module B for stamping.
    - Consumes the `ProofOfUID` after it has been stamped, ensuring it is used only once.

2. Module B:
    - Accepts the `ProofOfUID` as input.
    - Performs an operation (e.g., stamping the proof) to authenticate its involvement.

**Key Features of the Pattern**

- **Authentication**: The `ProofOfUID` ensures that only the module owning the UID (module A) can create and consume the proof.
- **Cross-Module Communication**: Module B can interact with the proof (by stamping) within the same PTB without requiring explicit dependencies on module A.
- **Single Use**: The `ProofOfUID` is consumed after use, so that it's used exactly once, preventing duplication or misuse.

This pattern allows modules to communicate securely and verifiably while maintaining modularity and avoiding tight coupling.1

### 2. OwnerCap

Implements ownership capabilities with both cloneable and non-cloneable variants. Used to manage control and access rights over resources.

**Key Structs:**
- `OwnerCap<T>`: Simple ownership capability (non-cloneable)
- `CloneableOwnerCap<T>`: Ownership capability that can be cloned for multiple addresses or concurrent transactions

**Real-World Usage Example (from agent):**
```rust
// During initialization
let owner_cap_over_agent = owner_cap::new_cloneable_drop(
    OverAgent {},  // Witness
    &agent.id,     // What is it for
    ctx
);

// Transfer to admin address
public_transfer(owner_cap_over_agent, AGENT_ADMIN);
```

**Common Use Cases:**
- Admin controls: Managing administrative rights over resources
- Access delegation: Allowing multiple entities to have controlled access
- Resource management: Controlling who can modify or interact with resources

### 3. ProvenValue

A container that proves a value was created by a specific UID, optionally restricting who can unwrap it.

**Key Features:**
- `wrap<T>`: Proves a value was created by a UID (anyone can unwrap)
- `wrap_for_recipient<T>`: Creates a value that only a specific recipient can unwrap
- `unwrap<T>`: Extracts the value (for unrestricted proven values)
- `unwrap_as_recipient<T>`: Extracts the value if the caller is the intended recipient

**Common Use Cases:**
- Secure data transfer between modules
- Implementing restricted access to values
- Creating trusted communication channels

### 4. NexusData

A flexible data representation format supporting both inline and remote storage.

**Key Constructors:**
- `inline_one/inline_many`: Store small data directly on-chain
- `remote_one/remote_many`: Reference data stored off-chain via keys

**Real-World Usage Example (from agent):**
```rust
// Storing input data in a DAG
.with_default_value(
    dag::vertex_from_string(b"hellox".to_ascii_string()),
    dag::input_port_from_string(b"prompt".to_ascii_string()),
    nexus_primitives::data::inline_many(vector[b"Lorem ipsum"]),
)
```

**Common Use Cases:**
- Flexible configuration storage
- Bridging on-chain and off-chain data
- Storage optimization for different data sizes

### 5. Event

A simple wrapper for standardizing and emitting events.

**Key Features:**
- `emit<T>`: Wraps and emits any type of event in a standardized format
- `EventWrapper<T>`: Makes events searchable by type in client applications

**Common Use Cases:**
- Standardized event emission
- Improved indexing and filtering of events
- Consistent event handling across packages

## Integration Patterns

These primitives are designed to work synergistically, enabling the construction of robust, verifiable on-chain systems. Here are common patterns:

1.  **Agent / Workflow Systems (e.g., `agent`):** This pattern combines agent logic with workflow execution.
    *   `OwnerCap` (often `CloneableOwnerCap`) grants administrative control over the agent.
    *   `ProofOfUID` serves as a verifiable "worksheet" to track and authenticate actions across transaction boundaries or different package interactions within a workflow.
    *   `NexusData` provides flexible storage for agent configuration, workflow inputs, and state, supporting both inline and remote data references.
    *   `Event` standardizes the emission of agent actions and workflow progress updates.

2.  **Access Control Systems:** Focuses on managing permissions and verifying actions.
    *   `OwnerCap` defines and delegates control privileges.
    *   `ProofOfUID` can authenticate specific actions performed under those privileges.
    *   `ProvenValue` securely transfers capability-related data or attests to permissions.
    *   `Event` logs access changes or granted permissions.

## Security Considerations

1. **Hot Potato Pattern Security**
   - `ProofOfUID` cannot be duplicated or transferred
   - Only the original creator can consume a `ProofOfUID`
   - Stamping is tracked to prevent double-counting

2. **Ownership Capabilities**
   - The phantom type parameter ensures type safety
   - Cloneable capabilities must be explicitly created
   - Object identity verification prevents spoofing

3. **Proven Values**
   - Source authentication guarantees origin
   - Optional recipient restriction adds targeted security
   - Clear verification of data provenance

<!-- List of References -->

[repo-primitives-package]: https://github.com/Talus-Network/nexus-next/tree/main/sui/primitives
[move-hot-potato]: https://move-book.com/programmability/hot-potato-pattern.html
[ob-request-module]: https://github.com/Origin-Byte/nft-protocol/tree/main/contracts/request/sources/request
[sui-transfer-policy]: https://github.com/MystenLabs/sui/blob/main/crates/sui-framework/packages/sui-framework/sources/kiosk/transfer_policy.move