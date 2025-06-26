# Nexus Tokenomics

In blockchain systems, typically users pay a gas fee to submit transactions to account for the computational work provided by the validators running the chain.

In Nexus an agentic workflow is usually triggered by a user action, but the additional work on behalf of the user (or Talus Agent, TAP) during workflow execution is delegated to other parties. This includes:

- the gas fees the [Leader](../crates/leader.md) incurs when submitting the results of the tool invocations back onchain
- the fees for the service the tool provides

To manage payment for those fees, Nexus introduces a tokenomics model to manage payments for the agentic (AI) workflow services it provides.

{% hint style="success" %}
One of the value propositions for Nexus, is its positioning as _Market for Agents_ or _MFA_. It provides the ability for service providers (be it AI or not, offchain or onchain) to offer their service to Talus agent developers using blockchain infrastructure as a unified payment layer.

This creates a market for agents where users can benefit from blockchain's unique properties, like providing a global, transparent and censorship resistant payment layer and the ability to allow for micro-payments for otherwise inaccessible services.
{% endhint %}

## Relevant Actors

From a tokenomics perspective, consider the following actors:

- the user (human or TAP)
- the tool owner
- the Nexus Leader
- other actors with read access into tokenomics (e.g. explorers)

## Gas Service Concepts

The implementation of the `GasService`, a shared object that manages all gas-related operations, can be found in the [dedicated section](gas-service.md).

### Where to draw gas from?

Broadly speaking, there's two ways a user gets charged for workflow execution.

1. They can purchase **prepaid access** to tool invocations, through `GasTickets`.
1. They can add funds directed for gas payments as `GasBudget`

Tool owners can provide different flavors of gas tickets by using existing or creating custom _gas extensions_ that allow for different modes of operation for the tool to consume gas tickets. The tool owners can also set a cost per single invocation. If no gas tickets are present, tools will charge from a non-zero gas budget instead.

Both gas tickets and budgets have different _scopes_ to protect users against unintended use of their tickets or budget.

{% hint style="info" %}
The provision of gas tickets and budgets, gas extensions and different scopes allows for flexibility in handling gas fees for workflow execution.
{% endhint %}

#### Leader

The leader requires gas to submit tool invocation outputs onchain and will use gas budget of appropriate scope to do so.

### Library of gas extensions

The Talus Labs team will provide some gas exentsion Move packages that can will be able to make up the bulk of use cases, including gas tickets with expiry and limited number of invocations.

However, the tool developers are free to write custom gas extensions Move packages that correspond to custom mode of operation for their gas tickets.

For more information and details on the gas service, refer to the [dedicated section](gas-service.md).

## Nexus CLI

You'll be able to manage interaction with the gas service through the [Nexus CLI](../../nexus-sdk/cli.md). Please refer to the commands and inspect the gas-related arguments.

