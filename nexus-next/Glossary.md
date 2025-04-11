# Glossary

- **`Tool Registry`** - On-chain object that holds Tool definitions so that the Leader knows where and how to invoke them.
- **`Tool`** - HTTP service or a smart contract with a predefined interface, executing a specific task. It is a Vertex in the Nexus DAG.
- **`DAG`** - Directed acyclic graph describes how outputs from Tools flow into inputs of other Tools. This is a static definition.
- **`JSON DAG`** - JSON representation of a DAG with a Nexus provided schema.
- **`DAG Execution`** - When a static DAG is passed to the Workflow, a DAG Execution is instantiated.
- **`Workflow`** - The on-chain Nexus package, that takes a DAG and its inputs to create and drive a DAG execution. It keeps all state related to the DAG execution and emits events to the off-chain world with instructions on how to proceed with the DAG execution.
- **`Primitives`** - Exports types that allow two Sui packages, A and B, to communicate with each other in an authenticated way without using explicit Move dependencies.
- **`TAP`** - Talus Agent Package is a smart contract that can accept a DAG, execute it and verify its execution. It also holds custom logic that can be hooked into the DAG execution process.
- **`Default TAP`** - Nexus provided TAP that only executes a DAG and verifies its execution. It does not have any custom logic.
- **`Leader`** - The off-chain service that listens to Sui events and executes Tools as instructed by Worflow.
- **`Indexer`** - The off-chain database service as a job queue. All events emitted by the Workflow are stored here, along with their execution status.
- **`Toolkit`** - Library that provides interfaces and boilerplate for Tool development. Currently implemented in Rust.
- **`CLI`** - Nexus CLI that provides commands for Tool registration, JSON DAG static analysis, publishing and execution via the Default TAP.
- **`SDK`** - Nexus Rust SDK that exposes various types, logic and transaction templates useful both internally and externally.

## `DAG` Related Terms

- **`Vertex`** - Abstraction of a Tool in the DAG.
- **`Edge`** - Connection between one Tool's output and other Tool's input.
- **`Input Port`** - A single input of a Tool. This can be one and only one of:
  1. Port that has an edge leading to it
  2. Port with a `Default Value` statically defined on the DAG
  3. Port as an `Entry Input Port` that accepts a value at execution time from the triggerer
- **`Output Variant`** - Resulting _state_ of a Tool evaluation. A Tool can define N Output Variants but will always evaluate into exactly 1 at runtime.
- **`Output Port`** - A single output of a Tool within an Output Variant.
- **`Entry Group`** - A set of Vertices and their respective Entry Input Ports that need to be provided a value upon DAG execution.
