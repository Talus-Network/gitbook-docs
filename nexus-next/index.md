# 🫀 Nexus Core

This section aims to document the technical side of all core Nexus components. We will split the documentation into several parts that, albeit distinct projects, work together to form Nexus as a whole.

## Actors

For the purposes of this documentation we make distinction between different user roles within the ecosystem:

* **Nexus maintainer.** Core team member that maintains the Nexus codebase.
* **Tool developer.** Outside contributor that develops Tools to be used by Agents.
* **Agent developer.** Outside contributor that creates DAGs and subsequently deploys the Agent smart contract.
* **Agent user.** End-user that interacts with the ecosystem through clients built by us or outside contributors.

## [Glossary](glossary.md)

Ubiqutously used terms. Often these terms reference specific parts of the project so it is crucial that they be clearly defined.

## Onchain Nexus

The onchain part of Nexus. Holds the workflow state and requests [Tool](#tools) execution from the [Leader](#offchain-nexus). 

Docs:

* [Workflow package](packages/workflow.md)
* [Primitives package](packages/wrimitives.md)
* [Nexus interface package](packages/nexus-interface.md)

{% hint style="info" %}
The Nexus core onchain packages are currently not open sourced. To find all of the function signatures and data structs, please refer to [the reference API documentation](../developer-docs/index/nexus-core-api-docs/README.md)
{% endhint %}

### [Sui Move Conventions](conventions/sui-move.md)

We established a [set of conventions for writing Move code](conventions/sui-move.md), which may not be universally known and adopted among Sui Move developers. Skim through them before diving into the Move codebase.

## Offchain Nexus

The main offchain service. Consumes events produced by the onchain Workflow, invokes Tools and notifies the Workflow about the outcome of Tool invocations. This service is provided by the Talus Labs team for now, with plans to decentralize in the future.

Docs:

* [Leader](crates/leader.md)

## [Tools](tool.md)

Tools are Vertices in the Nexus workflow DAG. They are services with [Nexus-defined interface](tool.md) schema that perform specific tasks. These Tools are what Agent Developers orchestrate in a workflow DAG to create an Agent.

There are a few standard Nexus tools, they can be found it the [Nexus SDK repository's tools](https://github.com/Talus-Network/nexus-sdk/tree/main/tools) folder.

Some examples of what a Tool is:

* getting a chat completion from OpenAI
* posting a Tweet
* storing data on an external storage

Docs:

* [Tool](tool.md)

## [Agent Development](./TAP/agent-development.md)

The components referenced above (onchain Nexus, offchain Nexus and tools) provide the infrastructure and building blocks for [agent developers](index.md#actors) to build Talus agents.

Docs:

* [Agent development](./TAP/agent-development.md)
* [Default TAP template](./TAP/default-tap.md)

## Nexus SDK

Nexus offers [tool and agent developers](index.md#actors) an easy-to-use SDK consisting of a CLI and Toolkit to streamline their development. The codebase resides in [this repository](https://github.com/Talus-Network/nexus-sdk) and is the main entry point for developers to interact with Nexus. It has a separate section in the developer docs dedicated to it.

Docs:

* [Nexus SDK documentation](../nexus-sdk/index.md)
