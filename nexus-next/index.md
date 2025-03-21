# `nexus-next`

This wiki aims to document the technical side of all Nexus components. We will split the documentation into several parts that, albeit distinct projects, work together to form Nexus as a whole.

## Actors

For the purposes of this documentation we make distinction between different user roles within the ecosystem:

- **Nexus maintainer.** Core team member that maintains the Nexus codebase.
- **Tool developer.** Outside contributor that develops Tools to be used by Agents.
- **Agent developer.** Outside contributor that creates DAGs and subsequently deploys the Agent smart contract.
- **Agent user.** End-user that interacts with the ecosystem through clients built by us or outside contributors.

## SUI Transactions

The Leader will be assigned a wallet via the `SUI_SECRET_MNEMONIC` environment variable. This wallet will hold N `leader_cap`s. These are owned objects that are used to verify that the TX submission was done from the Leader. On Sui, to avoid equivocation, only one parallel TX can be sent per-`leader_cap`. The wallet is assigned N `Coin<Sui>` objects as gas (on mainnet) or Coin objects are poured from a faucet (on localnet and testnet).

> Important thing to note is that, upon a failed transaction, Sui will lock all objects associated with the transaction until the next epoch, which is 24 hours. That means that we need to "damage" a `leader_cap` if a transaction fails and not use it for the next 24 hours.

Initially, there will only be one transaction type from Leader back to Workflow. This transaction notifies the Workflow of the Tool invocation result. More details are available in the [[Crate: Leader]] documentation.

Once on-chain Tools are defined, the Leader will also have to send transactions to invoke these Tools. This is however as of now an unexplored topic.

## [Glossary][glossary]

Ubiqutously used terms. Often these terms reference specific parts of the project so it is crucial that they be clearly defined.

## Onchain Nexus

The on-chain part of Nexus.
Holds the workflow DAG state and requests Tool execution from the Leader. The codebase resides in [this repository](repo-nexus-sui).

Docs:
- [Workflow package][packages-workflow]
- [Primitives package][packages-primitives]

Epics:

- https://github.com/Talus-Network/nexus-next/issues/9
- https://github.com/Talus-Network/nexus-next/issues/16

### [Sui Move Conventions][conventions-sui-move]

We established a [set of conventions for writing Move code][conventions-sui-move], some of them unfamiliar outside of the Nexus team.
Skim through them before diving into the Move codebase.

## Offchain Nexus

The main off-chain service. Consumes events produced by the on-chain Workflow, invokes Tools and notifies Workflow about the outcome of Tool invocations. The codebase resides in [this repository](repo-nexus-rust).

Docs: 

- [Leader][crates-leader]

Epics:

- https://github.com/Talus-Network/nexus-next/issues/53

## [Tools][tool]

Tools are Vertices in the Nexus workflow DAG. They are services with [Nexus-defined interface][nexus-interface] schema that perform specific tasks. These Tools are what Agent Developers orchestrate in a workflow DAG to create an Agent.

There are currently no Tools yet implemented. It is, however, likely that Tools will have their own repository.

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

## Nexus SDK

Nexus offers tool and agent developers (refer to [Actors](#actors)) an easy-to-use SDK consisting of a CLI and Toolkit to streamline their development. The codebase resides in [this repository][repo-nexus-sdk].

<!-- TODO: add link to docs when they are live -->

<!-- List of References -->

[repo-nexus-sui]: https://github.com/Talus-Network/nexus-next/tree/main/sui
[repo-nexus-rust]: https://github.com/Talus-Network/nexus-next/tree/main/be
[repo-nexus-sdk]: https://github.com/Talus-Network/nexus-sdk

[glossary]: ./Glossary.md
[packages-primitives]: ./packages/Primitives.md
[packages-workflow]: ./packages/Workflow.md
[conventions-sui-move]: ./conventions/Sui-Move.md
[crates-leader]: ./crates/Leader.md
[nexus-interface]: ./Nexus-Interface.md
[tool]: ./Tool.md
