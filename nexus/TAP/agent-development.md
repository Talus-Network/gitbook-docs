# Agent Development

Nexus, as an agentic framework, provides a useful set of abstractions and, both onchain and offchain components that orchestrate the development, registration and discovery of tools, the composition of those tools in workflows and finally the workflow execution. Find the definitions of these terms in the [glossary](../glossary.md) in case they are unfamiliar.

As a result, Nexus greatly facilitates building Talus Agents for [agent developers](../index.md#actors).

{% hint style="info" %}
A Talus agent is an onchain identity associated with one or more onchain assets and workflow services
{% endhint %}

## Development Requirements

There's a number of ways an agent developer could build their agents, with varying levels of complexity and customization:

* **Custom TAP + custom workflow (hard)**: Construct the workflow(s) (DAGs) AND write a Sui Move "Talus Agent Package" (TAP) that holds the workflows(s) as well as some custom business logic related to it. This is the most complex as it requires the agent developer to develop a custom TAP package and define the DAG. In return you get the highest amount of customization.

* **Custom TAP + existing workflow (medium)**: Write a Sui Move TAP that uses existing workflows in a _plug-and-play_ manner. There could be additional business logic added to the TAP. This is an intermediate level of complexity that gives a sufficient amount of customization provided there are workflows available that satisfy requirements.

* **Default TAP + custom workflow (easy)**: Only construct the workflow(s) (DAGs) and use the [_default TAP_](default-tap.md) to execute it and call the workflow engine. The default TAP provides a template TAP implementation and reduces the development work to the configuration of the workflow DAG(s). This simplifies development considerably at the cost of flexibility in adding business logic to trigger DAG execution.

{% hint style="success" %}
How to choose the way to build?

The choice of how to build the agent will be determined by weighing:

* familiarity with Sui Move,
* the need for custom logic to govern workflow execution, payment etc.
* the availability of existing workflows that meet the application's needs
{% endhint %}

## Explore further

Continue learning about agent development with the following sections:

* the [Nexus interface for TAPs](../packages/nexus-interface.md) section, outlining what interface the TAP must comply with
* the reference [default TAP](default-tap.md) implementation, that serves as an example for a bare-bones TAP