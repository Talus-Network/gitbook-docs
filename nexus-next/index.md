# `nexus-next`

This wiki aims to document the technical side of all Nexus components. We will split the documentation into several parts that, albeit distinct projects, work together to form Nexus as a whole.

## Actors

For the purposes of this documentation we make distinction between different user roles within the ecosystem:

- **Nexus maintainer.** Core team member that maintains the Nexus codebase.
- **Tool developer.** Outside contributor that develops Tools to be used by Agents.
- **Agent developer.** Outside contributor that creates DAGs and subsequently deploys the Agent smart contract.
- **Agent user.** End-user that interacts with the ecosystem through clients built by us or outside contributors.

## [Glossary][glossary]

Ubiqutously used terms. Often these terms reference specific parts of the project so it is crucial that they be clearly defined.

## Onchain Nexus

The on-chain part of Nexus.
Holds the workflow DAG state and requests Tool execution from the Leader. The codebase resides in [this repository][repo-nexus-sui].

Docs:
- [Workflow package][packages-workflow]
- [Primitives package][packages-primitives]
- [Nexus interface package][packages-interface]

Epics:

- https://github.com/Talus-Network/nexus-next/issues/9
- https://github.com/Talus-Network/nexus-next/issues/16

### [Sui Move Conventions][conventions-sui-move]

We established a [set of conventions for writing Move code][conventions-sui-move], some of them unfamiliar outside of the Nexus team.
Skim through them before diving into the Move codebase.

## Offchain Nexus

The main off-chain service. Consumes events produced by the on-chain Workflow, invokes Tools and notifies Workflow about the outcome of Tool invocations. The codebase resides in [this repository][repo-nexus-rust].

Docs: 

- [Leader][crates-leader]

Epics:

- https://github.com/Talus-Network/nexus-next/issues/53

## [Tools][tool]

Tools are Vertices in the Nexus workflow DAG. They are services with [Nexus-defined interface][tool] schema that perform specific tasks. These Tools are what Agent Developers orchestrate in a workflow DAG to create an Agent.

There are a few standard Nexus tools, they can be found it the [Nexus SDK repository's tools][repo-tools] folder.

Some examples of what a Tool is:

- getting a chat completion from OpenAI
- posting a Tweet
- storing data on an external storage

Docs:

- [Tool][tool]

Epics:

- https://github.com/Talus-Network/nexus-next/issues/69
- https://github.com/Talus-Network/nexus-next/issues/30
- https://github.com/Talus-Network/nexus-next/issues/31

## [Agent Development][agent-development]

The components referenced above (onchain Nexus, offchain Nexus and tools) provide the infrastructure and building blocks for [agent developers](#actors) to build Talus agents.

Docs:

- [Agent development][agent-development]
- [Default SAP template][default-sap]

## Nexus SDK

Nexus offers tool and [agent developers](#actors) an easy-to-use SDK consisting of a CLI and Toolkit to streamline their development. The codebase resides in [this repository][repo-nexus-sdk].

Docs:

- [Nexus SDK documentation](../nexus-sdk/index.md)

<!-- List of References -->

[repo-nexus-sui]: https://github.com/Talus-Network/nexus-next/tree/main/sui
[repo-nexus-rust]: https://github.com/Talus-Network/nexus-next/tree/main/be
[repo-nexus-sdk]: https://github.com/Talus-Network/nexus-sdk
[repo-tools]: https://github.com/Talus-Network/nexus-sdk/tree/main/tools

[glossary]: ./Glossary.md
[packages-primitives]: ./packages/Primitives.md
[packages-workflow]: ./packages/Workflow.md
[packages-interface]: ./packages/Nexus-Interface.md
[conventions-sui-move]: ./conventions/Sui-Move.md
[crates-leader]: ./crates/Leader.md
[tool]: ./Tool.md
[agent-development]: ./SAP/Index.md
[default-sap]: ./SAP/Default-SAP.md

