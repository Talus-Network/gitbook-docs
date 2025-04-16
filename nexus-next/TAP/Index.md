# Agent Development

Nexus, as the implementation of the Talus Agentic Framework (TAF),  provides a useful set of abstractions and, both onchain and offchain components that orchestrate the development, registration and discovery of tools, the composition of those tools in workflows and finally the workflow execution. Find the definitions of these terms in the [glossary][glossary] in case they are unfamiliar.

As a result, Nexus greatly facilitates building Talus Agents for [agent developers][actors]. 

<!-- Gitbook syntax -->
{% hint style="info" %} A Talus agent is an onchain identity associated with one or more onchain assets and workflow services {% endhint %}

## Development Requirements

There's a number of ways an agent developer could build their agents, with varying levels of complexity:

- Construct the workflow(s) (DAGs) AND write a Sui Move "Talus Agent Package" (TAP) that holds the workflows(s) as well as some custom business logic related to it. This is the most complex as it requires the agent developer to develop a custom TAP package.


- Only construct the workflow(s) (DAGs) and use the [_default TAP_][default-tap] to hold the workflow DAG and provide the functionality to execute it. The default TAP provides a template TAP implementation and reduces the development work to the configuration of the workflow DAG(s).

- Write a Sui Move TAP that uses existing workflows in a _plug-and-play_ manner. There could be additional business logic added to the TAP. This is an intermediate level of complexity.

<!-- Gitbook Syntax -->
{% hint style="success" %} How to choose the way to build?

The choice of how to build the agent will be determined by weighing: 

- familiarity with Sui Move, 
- the need for custom logic to govern workflow execution, payment etc. 
- the availability of existing workflows that meet the application's needs {% endhint %}

## Explore further

Continue learning about agent development with the following sections:

- the [Nexus interface for TAPs][interface] section, outlining what interface the TAP must comply with
- the reference [default TAP][default-tap] implemenation, that serves as an example for a bare-bones TAP

<!-- List of references -->

[actors]: ../index.md#actors
[glossary]: ../Glossary.md
[interface]: ../packages/Nexus-Interface.md
[default-tap]: ./Default-TAP.md