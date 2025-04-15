---
description: Vision, tech, community
---

# 💧 Why Sui Move?

In the section above, we outlined the motivation for building Talus (and Nexus) and introduced our system-level definitions of Talus AI agents as a specific subset of the AI agent space, along with a classification of agentic frameworks to build agents. Before diving into the (first) actual implementation of the Nexus framework and Talus agents, let’s first take a moment to consider why we picked Sui Move as the smart contract language to build Talus agents and why we’ll initially deploy Nexus on the Sui chain.

We can summarize the decision to partner with Sui for our initial deployment, based on three broad categories:

#### Vision Alignment

* Talus has a vision of AI agents powering a new age of user-centric internet. To this end, we provide a framework to build, and platform to deploy Talus agents that leverage _blockchain(s) as their coordination and value layer_, _decentralized storage solutions as their data layer_ while leveraging offchain (potentially centralized) _AI models and general web/mobile infrastructure as their computation and execution layer_.
* Sui on the other hand, aims to create the new generation of the decentralized internet. The Mysten Labs team (Sui’s main core contributor) has therefore built Sui as the coordination and value layer and Walrus as the decentralized storage layer, with additional innovations to come. Additionally, Sui aims to be a home for the next wave of decentralized AI builders.

It is clear that there is high alignment in the vision of both projects. Talus aims to bring our vision to the user as quickly as we can without compromising on our ideals and launching on Sui is the best immediate way to achieve this.

#### Best-in-Class Tech

The strategic decision to utilize Move as the smart contract language is underpinned by its high-performance characteristics, in addition to its security and program design properties. We elaborate on the performance advantages of Move and the corresponding MoveVM, and why it is an optimal choice for Talus Network:

1. **On-Chain Logic Security**: Move’s design inherently enhances security, simplifying the development of secure protocols for managing valuable resources, which is critical for on-chain logic.
2. **Flexible Object Model**: Its object model excellently abstracts resources, aiding Talus in securely managing and valuing intelligence outcomes with precision and adaptability, setting it apart in the web3 space.
3. **High-Performance:** MoveVM’s architecture supports efficient concurrency, enabling Talus to scale by processing multiple transactions simultaneously without losing security or integrity.

#### The Ecosystem

Sui has known an impressive start ever since their launch with an ever increasing number of impressive and competent teams building on it. The launch of Walrus will only further Sui adoption. We believe there are many synergies for Sui ecosystem teams to partner with Talus for AI enhanced applications.
