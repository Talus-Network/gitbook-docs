# 🫀 Nexus Core

This section aims to document the technical side of all core Nexus components. We will split the documentation into several parts that, albeit distinct projects, work together to form Nexus as a whole.

## Actors

For the purposes of this documentation we make distinction between different user roles within the ecosystem:

* **Nexus maintainer.** Core team member that maintains the Nexus codebase.
* **Tool developer.** Outside contributor that develops Tools to be used by Agents.
* **Agent developer.** Outside contributor that creates DAGs and subsequently deploys the Agent smart contract.
* **Agent user.** End-user that interacts with the ecosystem through clients built by us or outside contributors.

## [Glossary](Glossary.md)

Ubiqutously used terms. Often these terms reference specific parts of the project so it is crucial that they be clearly defined.

## Onchain Nexus

The on-chain part of Nexus. Holds the workflow DAG state and requests Tool execution from the Leader.

Docs:

* [Workflow package](../developer-docs/index/onchain-nexus/workflow.md)
* [Primitives package](../developer-docs/index/onchain-nexus/primitives.md)
* [Nexus interface package](../developer-docs/index/onchain-nexus/nexus-interface.md)

{% hint style="info" %}
The Nexus core onchain packages are currently not open sourced. To find all of the function signatures and data structs, please refer to [the reference API documentation](packages/reference/)
{% endhint %}

### [Sui Move Conventions](../developer-docs/index/onchain-nexus/sui-move.md)

We established a [set of conventions for writing Move code](../developer-docs/index/onchain-nexus/sui-move.md), some of them unfamiliar outside of the Nexus team. Skim through them before diving into the Move codebase.

## Offchain Nexus

The main off-chain service. Consumes events produced by the on-chain Workflow, invokes Tools and notifies Workflow about the outcome of Tool invocations. The codebase resides in [this repository](https://github.com/Talus-Network/nexus-next/tree/main/be).

Docs:

* [Leader](crates/Leader.md)

## [Tools](Tool.md)

Tools are Vertices in the Nexus workflow DAG. They are services with [Nexus-defined interface](Tool.md) schema that perform specific tasks. These Tools are what Agent Developers orchestrate in a workflow DAG to create an Agent.

There are a few standard Nexus tools, they can be found it the [Nexus SDK repository's tools](https://github.com/Talus-Network/nexus-sdk/tree/main/tools) folder.

Some examples of what a Tool is:

* getting a chat completion from OpenAI
* posting a Tweet
* storing data on an external storage

Docs:

* [Tool](Tool.md)

## [Agent Development](SAP/Index.md)

The components referenced above (onchain Nexus, offchain Nexus and tools) provide the infrastructure and building blocks for [agent developers](index.md#actors) to build Talus agents.

Docs:

* [Agent development](../developer-docs/index/index/)
* [Default TAP template](../developer-docs/index/index/default-tap.md)

## Nexus SDK

Nexus offers tool and [agent developers](index.md#actors) an easy-to-use SDK consisting of a CLI and Toolkit to streamline their development. The codebase resides in [this repository](https://github.com/Talus-Network/nexus-sdk).

Docs:

* [Nexus SDK documentation](../nexus-sdk/index.md)
