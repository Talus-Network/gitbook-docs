---
description: Where are we now and where are we going?
---

# 💸 Towards an Agentic Economy

In the [previous section](products/introducing-nexus.md) we provided an overview of the Talus technical ecosystem, the technical components and the ecosystem actors. **Talus’ vision is that this ecosystem will evolve into a burgeoning double-sided marketplace of AI service providers (Tools) on the one hand and Talus agent builders on the other.** An application developer wanting to build with Talus agents does not have to build and run the AI tools themselves and vice versa, an AI tool provider is not tasked with building the applications leveraging their models.

Talus is the platform where counterparty discovery happens, creating added value for all. Furthermore, Initial Agent Offerings (IAO) allow for agents to be tokenized further enhancing the option for application developers to incentivize AI agent use cases within their application. All of this combined, this is what we call the _agentic economy_.

{% hint style="warning" %}
Bootstrapping phase

What is described above is the future vision of a thriving ecosystem and marketplace on Talus. At the moment, however, we are still bootstrapping our platform and framework, Nexus. What does that mean for teams willing to partner with Talus to build agents?
{% endhint %}

For now it means that as an application developer aiming to build an app enhanced with Talus agents, you’ll have to follow these steps:

1. Select the offchain AI tools that your agent will use. You can check the Tool registry for Nexus first to see if there are integrated Tools available to adopt.
2. If all of the offchain Tools are already available in the registry, you can move on. If not, you’ll have to use Nexus SDK to integrate and register the offchain service as a Tool.
3. Select the onchain Tools that your agent will use. You can check the Tool registry for Nexus first to see if there are packages onchain with Tool definitions available.
4. If all of the onchain Tool are already available in the registry, you can move on. If not, you’ll have to use Nexus SDK to integrate and register the onchain package as a Tool.
5. Design the agent by defining the onchain Workflow for the agent (this will include the offchain and onchain Tools from previous steps).
6. With the Workflow designed and all Tools registered, you can go on to publish the TAP (Talus Agent Package) to deploy the agent.
7. (Optional) Use the IAO (Initial Agent Offering) package (ask for more information) to tokenize your agent.
