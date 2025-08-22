---
description: Removing the veil of ignorance about AI agents
---

# 🤖 AI Agent: What's in a Name?
Talus aims to build the premier decentralized platform **for deploying, coordinating, and monetizing autonomous systems.** But… what do we actually mean when we say that? In fact, what do we mean when we talk about AI agents? With the hype surrounding them increasing, so too has the confusion and even misinformation. So before continuing, let’s clearly outline how we at Talus think about agents.

## General AI Agent Definition

AI Agents have rapidly become a fairly well established narrative in the AI sector, evolving out of foundational models (LLMs) that were, while impressive in their own right, rather narrow in their utility. AI agents or ‘agentic systems’ are the next step in the AI evolution, removing constraints for the LLM to perform a wider range of complex tasks with more tools available to it. An exact definition might differ from source to source ([Wikipedia](https://en.wikipedia.org/wiki/Intelligent_agent), [IBM](https://www.ibm.com/think/topics/ai-agents), [Amazon](https://aws.amazon.com/what-is/ai-agents/?nc1=h_ls), …) but we can summarize as follows:

**AI agents are compound AI systems with the following characteristics**:

- they can automate one or multiple composable, complex tasks;
- their tasks usually originate from a human user input, but they are not bound to constant (human) inputs to operate, rather…;
- they can take actions autonomously to achieve goals;
- they can plan and devise strategies to split up tasks in smaller actions;
- they can perceive and interact with their own environment;
- they can interpret their own performance;
- they can improve their performance by learning from their results.

**Some additional terminology that will aid general AI agent understanding:**

- **`Workflow`**: a structured sequence of tasks or operations powered by tools that an AI agent or system of agents executes to achieve a specific goal. It's essentially the "playbook" that defines how agents should process information, make decisions, and take actions.
    
    A workflow typically includes:
    
    - The order and dependencies between tasks (what needs to happen before what)
    - Decision points where the agent evaluates conditions and chooses different paths
    - Input/output specifications for each step
    - Error handling and recovery procedures
    - Success criteria and completion conditions
- **`Tool`**: functions or capabilities that agents can use to interact with external systems or perform specific tasks. They're essentially the atomic building blocks that enable agents to take concrete actions.
    
    Key aspects:
    
    - Tools have well-defined inputs and outputs
    - They perform specific operations (like web searches, calculations, or API calls)
    - They often interface with external services or resources
    - They can be composed into more complex workflows
    - They typically include error handling and usage constraints
    
    Common examples include text processing tools, mathematical operations, web access functions, file handling utilities, and API integrators.
    

Based on the definition above, we could design agents and autonomous systems that are closed-source, hard to compose or interoperate with other agents or external resources, have limited autonomy due to owner-imposed barriers, lack access to financial rails and in general, only operate within the walled gardens their centralized owners allow them to operate in. This is NOT the future we envision. At Talus, we are **more opinionated about autonomous systems**. But then, how can we formalize our classification of the agents we’ll encounter to ensure we take the path towards decentralization with AI agents?

## **Agentic Frameworks: a Spectrum**

AI agents that allow for complex tasks to be solved or complex multi-agent interactions, while incredibly useful to application builders, also present a challenge to design, build and deploy. To ensure that builders of the next wave of user applications on the internet can maximally focus on their application, frameworks can abstract away complexity and make development easier by providing out-of-the-box libraries, tooling and standards. This is what we call agentic frameworks, they allow to streamline the development of AI agents of all sorts.

An agentic framework provides the building blocks, architecture and foundational structure for developing, deploying, and managing agents and multi-agent systems.

Given how recent the development of AI agents is, there is not yet a formal categorization of those agentic frameworks, which opens the door for confusion and misinformation. The team at Talus has been leading the charge towards a classification.

We believe agentic frameworks (and thus the agents they allow to build) exist on a spectrum (in order of increasing decentralization):

- **Type 0**: agents that “live” and operate completely on centralized servers.
- **Type 1**: agents that “live” and operate mainly on centralized servers, but as part of their execution flow, have access to a wallet and submit transactions to a blockchain.
- **Type 2**: agents that are defined onchain with execution workflows that are verifiable onchain, but, for the sake of performance and cost-effectiveness, outsource (a part of) their execution offchain to service providers.
- **Type 3**: agents that are defined and operate completely onchain.

![Agentic Frameworks as a Spectrum](attachment:f15a2950-504d-4e1f-9554-9bd2801bf464:image.png)

Agentic Frameworks as a Spectrum

At Talus, we believe that agentic frameworks should strive towards decentralization but within the bounds of the pragmatic. The emphasis should be on **verifiability onchain** (along with the agent’s workflow definition), rather than putting all agentic execution onchain at great cost/performance penalties.

**We are building Nexus** (decentralized automation protocol and developer framework to build Talus Agents) **to occupy the Type 2 domain of the spectrum** where we leverage the open, censorship resistant and verifiable nature of the blockchain while keeping the overall workflow performant through outsourcing computation to offchain service providers. This is the first step to identify how Talus Agents are different, but there’s more that we can specify to rigorously define them.

## **Talus Agentic Workflows**

Talus Agents put users in control, *satisfying user intents* while delegating the complex workload to efficient AI systems operating behind the scenes. By combining the cutting-edge technologies of AI and blockchain, Talus Agents create empowering and highly effective digital experiences through transparent, censorship-resistant, and secure execution of composable workflows.

Nexus provides developers with the core interface to build these agents, leveraging both onchain and offchain components within the **Talus Agentic Framework (TAF)**. The architecture has the following properties:

- **Onchain infrastructure as the value and identity layer.** Talus uses onchain modules (smart contracts) as the foundation for verifiable value transfer and secure delegation of permissions:
    - **Onchain Workflows** (Talus Workflows: ensure transparency, auditability, and composability across services.
    - **Onchain identity** for Talus agents allows them to hold assets and permissions directly, so they can autonomously execute workflows without requiring repeated user authorization.
    - **Composability** enables multi-agent cooperation, swamrs, and seamless interaction with onchain protocols and external APIs.
    - **Nativa access to financial rails** ensures that agents can transact, allocate, and govern assets under transparent rules.
- **Middleware for coordination and storage.** The middleware layer via the Leader Network and Walrus provides coordination between blockchain and offchain AI systems. This layer ensures workflows remain live, censorship-resistant, and economically accountable while bridging onchain verification with offchain AI computation:
    - **Leader Node** **Network**: acts as a trustless coordinator network, ensuring workflow steps are executed correctly without user intervention.
    - **Walrus** decentralized storage supports verifiable offchain storage of intermediate values, enabling scalability while maintaining integrity.
- **Offchain State-of-the-Art (SOTA) AI infrastructure as the computation layer.** For cost-performance reasons, compute-heavy AI tasks still leverage offchain infrastructure. Nexus integrates these services while ensuring:
    - **Configurable verifiability** through proofs or trust-based mechanisms.
    - **Cost-performance parity** with centralized frameworks while preserving transparent onchain coordination.
    - **Developer flexibility** to trade off decentralization and performance per use case.

This deliberately modular, layered architecture lets Talus Agents inherit many of the desirable properties of each layer, optimizing its position in the trade-off design space (along the decentralization versus cost/performance spectrum).