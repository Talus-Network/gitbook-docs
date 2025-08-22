---
description: Removing the veil of ignorance about AI agents
---

# 🤖 AI Agent: What's in a Name?

# **Agentic Frameworks: a Spectrum**

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

# **Talus Agentic Workflows**

Talus Agents put users in control, *satisfying user intents* while delegating the complex workload to efficient AI systems operating behind the scenes. By combining the cutting-edge technologies of AI and blockchain, Talus Agents create empowering and highly effective digital experiences through transparent, censorship-resistant, and secure execution of composable workflows.

Nexus provides developers with the core interface to build these agents, leveraging both onchain and offchain components within the **Talus Agentic Framework (TAF)**. The architecture has the following properties:

- **Onchain infrastructure as the value and identity layer.** Talus uses onchain modules (smart contracts) as the foundation for verifiable value transfer and secure delegation of permissions:
    - **Onchain Workflows** (Talus Workflows: ensure transparency, auditability, and composability across services.
    - **Onchain identity** for Talus agents allows them to hold assets and permissions directly, so they can autonomously execute workflows without requiring repeated user authorization.
    - **Composability** enables multi-agent cooperation, swamrs, and seamless interaction with onchain protocols and external APIs.
    - **Nativa access to financial rails** ensures that agents can transact, allocate, and govern assets under transparent rules.
- **Middleware for coordination and storage.** The middleware layer via the Leader Network and Walrus provides coordination between blockchain and offchain AI systems:
    - **Leader Node** **Network**: acts as a trustless coordinator network, ensuring workflow steps are executed correctly without user intervention.
    - **Walrus** decentralized storage supports verifiable offchain storage of intermediate values, enabling scalability while maintaining integrity.
    - This layer ensures workflows remain live, censorship-resistant, and economically accountable while bridging onchain verification with offchain AI computation.
- **Offchain State-of-the-Art (SOTA) AI infrastructure as the computation layer.** For cost-performance reasons, compute-heavy AI tasks still leverage offchain infrastructure. Nexus integrates these services while ensuring:
    - **Configurable verifiability** through proofs or trust-based mechanisms.
    - **Cost-performance parity** with centralized frameworks while preserving transparent onchain coordination.
    - **Developer flexibility** to trade off decentralization and performance per use case.

This deliberately modular, layered architecture lets Talus Agents inherit many of the desirable properties of each layer, optimizing its position in the trade-off design space (along the decentralization versus cost/performance spectrum).