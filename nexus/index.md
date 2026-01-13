# 🫀 Nexus Core

This section aims to document the technical side of all core Nexus components. We will split the documentation into several parts that, albeit distinct projects, work together to form Nexus as a whole.

## Actors

For the purposes of this documentation we make distinction between different user roles within the ecosystem:

- **Nexus maintainer.** Core team member that maintains the Nexus codebase.
- **Tool developer.** Outside contributor that develops Tools to be used by Agents.
- **Agent developer.** Outside contributor that creates DAGs and subsequently deploys the Agent smart contract.
- **Agent user.** End-user that interacts with the ecosystem through clients built by us or outside contributors.

## [Glossary][glossary]

Ubiqutously used terms. Often these terms reference specific parts of the project so it is crucial that they be clearly defined.

## Onchain Nexus

The onchain part of Nexus. Holds the workflow state and requests [Tool][tool] execution from the [Leader][leader].

Docs:

- [Workflow package][workflow]
- [Primitives package][primitives]
- [Nexus interface package][nexus-interface]
- [Policy DFA][policy]

{% hint style="info" %}
The Nexus core onchain packages are currently not open sourced. To find all of the function signatures and data structs, please refer to [the reference API documentation][ref-api]
{% endhint %}

### [Sui Move Conventions][sui-move-conventions]

We established a [set of conventions for writing Move code][sui-move-conventions], which may not be universally known and adopted among Sui Move developers. Skim through them before diving into the Move codebase.

## Offchain Nexus

The main offchain service. Consumes events produced by the onchain Workflow, invokes Tools and notifies the Workflow about the outcome of Tool invocations. This service is provided by the Talus Labs team for now, with plans to decentralize in the future.

Docs:

- [Leader][leader]
- [Checkpoint clock][leader-clock]

## [Tools][tool]

Tools are Vertices in the Nexus workflow DAG. They are services with [Nexus-defined interface][tool] schema that perform specific tasks. These Tools are what Agent Developers orchestrate in a workflow DAG to create an Agent.

There are a few standard Nexus tools, they can be found in the [Nexus SDK repository's tools][nexus-sdk-tools] folder.

Some examples of what a Tool is:

- getting a chat completion from OpenAI
- posting a Tweet
- storing data on an external storage

Docs:

- [Tool][tool]

## Flow Controls

Nexus provides a set of tools to support branching, conditionals and looping for more complex workflows.

Docs:

- [Branching & Conditionals][branching_and_conditionals]
- [Looping][looping]

## [Agent Development][agent-development]

The components referenced above (onchain Nexus, offchain Nexus and tools) provide the infrastructure and building blocks for [agent developers][actors] to build Talus agents.

Docs:

- [Agent development][agent-development]
- [Default TAP template][default-tap]

## Nexus SDK

Nexus offers [tool and agent developers][actors] an easy-to-use SDK consisting of a CLI and Toolkit to streamline their development. The codebase resides in [this repository][nexus-sdk-repo] and is the main entry point for developers to interact with Nexus. It has a separate section in the developer docs dedicated to it.

Docs:

- [Nexus SDK documentation][nexus-sdk-gitbook]

<!-- List of references -->

[glossary]: glossary.md
[workflow]: packages/workflow.md
[primitives]: packages/primitives.md
[nexus-interface]: packages/nexus-interface.md
[policy]: policy/index.md
[ref-api]: ../developer-docs/index/nexus-core-api-docs/README.md
[sui-move-conventions]: conventions/sui-move.md
[tool]: tool.md
[leader]: crates/leader.md
[leader-clock]: crates/leader-checkpoint-clock.md
[actors]: #actors
[branching_and_conditionals]: ./flow-controls/branching_and_conditionals.md
[looping]: ./flow-controls/looping.md
[agent-development]: ./TAP/agent-development.md
[default-tap]: ./TAP/default-tap.md
[nexus-sdk-repo]: https://github.com/Talus-Network/nexus-sdk
[nexus-sdk-tools]: https://github.com/Talus-Network/nexus-sdk/tree/main/tools
[nexus-sdk-gitbook]: ../nexus-sdk/index.md
