# Table of contents

- [🏠 Home](README.md)

## 🔮 Talus Overview

- [🐸 Introduction to Talus](talus-overview/readme.md)
- [🤖 AI Agent: What's in a Name?](talus-overview/ai-agent-whats-in-a-name.md)
- [🔬 Writings](talus-overview/writings.md)

## 🚀 Getting Started

- [🔌 Setup Guide](nexus-sdk/guides/setup.md)
- [💨 Dev Quickstart](nexus-sdk/guides/math-branching-quickstart.md)
- [📓 Dev Guides](getting-started/dev-guides/README.md)
  - [Build the Quickstart](nexus-sdk/guides/math-branching-dag-builder.md)
  - [Add Flexibility with Entry Groups](nexus-sdk/guides/math-branching-dag-entry.md)
  - [Build the Missing Tool](nexus-sdk/guides/llm-openai-chat-prep-tool.md)
  - [Add an LLM to your DAG](nexus-sdk/guides/math-branching-with-chat.md)
  - [Protect your Tool](nexus-sdk/guides/tool-firewall.md)

## 🌟 Product Docs

- [👋 Introducing Nexus](products/introducing-nexus.md)
- [💧 Why Sui Move?](talus-overview/why-sui-move.md)
- [💸 Towards an Agentic Economy](products/towards-an-agentic-economy.md)
- [🎨 Nexus Use Cases](products/nexus-use-cases.md)

## 💻 Developer Docs

- [🫀 Nexus Core](nexus/index.md)
  - [Onchain Nexus](developer-docs/index/onchain-nexus/README.md)
    - [Workflow](nexus/packages/workflow.md)
      - [On-chain Scheduler](nexus/scheduler/index.md)
    - [Primitives](nexus/packages/primitives.md)
      - [Policy](nexus/policy/index.md)
        - [DFA module](nexus/policy/dfa.md)
    - [Nexus Interface](nexus/packages/nexus-interface.md)
    - [Sui Move Conventions](nexus/conventions/sui-move.md)
  - [Offchain Nexus](developer-docs/index/offchain-nexus/README.md)
    - [Leader](nexus/crates/leader.md)
      - [Checkpoint clock](nexus/crates/leader-checkpoint-clock.md)
    - [Leader Sui TXs](nexus/crates/sui-tx.md)
  - [Agent Development](nexus/TAP/agent-development.md)
  - [Flow Controls]
    - [Branching & Conditionals](nexus/flow-controls/branching_and_conditionals.md)
    - [Looping](nexus/flow-controls/looping.md)
  - [Default TAP](nexus/TAP/default-tap.md)
  - [Tool](nexus/tool.md)
  - [Tool Communication](nexus/guides/tool-communication.md)
  - [Tokenomics](nexus/tokenomics/tokenomics.md)
    - [Gas Service](nexus/tokenomics/gas-service.md)
    - [Default Gas Extension](nexus/tokenomics/default-gas-extension.md)
  - [Nexus Core API docs](developer-docs/index/nexus-core-api-docs/README.md)
    - [nexus_interface/v1](nexus/packages/reference/nexus_interface/v1.md)
    - [nexus_interface/version](nexus/packages/reference/nexus_interface/version.md)
    - [nexus_primitives/data](nexus/packages/reference/nexus_primitives/data.md)
    - [nexus_primitives/event](nexus/packages/reference/nexus_primitives/event.md)
    - [nexus_primitives/owner_cap](nexus/packages/reference/nexus_primitives/owner_cap.md)
    - [nexus_primitives/proof_of_uid](nexus/packages/reference/nexus_primitives/proof_of_uid.md)
    - [nexus_primitives/proven_value](nexus/packages/reference/nexus_primitives/proven_value.md)
    - [nexus_workflow/dag](nexus/packages/reference/nexus_workflow/dag.md)
    - [nexus_workflow/default_gas_extension](nexus/packages/reference/nexus_workflow/default_gas_extension.md)
    - [nexus_workflow/default_tap](nexus/packages/reference/nexus_workflow/default_tap.md)
    - [nexus_workflow/gas](nexus/packages/reference/nexus_workflow/gas.md)
    - [nexus_workflow/leader_cap](nexus/packages/reference/nexus_workflow/leader_cap.md)
    - [nexus_workflow/main](nexus/packages/reference/nexus_workflow/main.md)
    - [nexus_workflow/tool_registry](nexus/packages/reference/nexus_workflow/tool_registry.md)
- [🧰 Nexus SDK](nexus-sdk/index.md)
  - [CLI](nexus-sdk/cli.md)
  - [Client](nexus-sdk/client.md)
  - [Tool Development](nexus-sdk/tool-development.md)
  - [Toolkit Rust](nexus-sdk/toolkit-rust.md)
  - [Tool Communication](nexus-sdk/guides/tool-communication.md)
  - [How to Build a DAG](nexus-sdk/guides/dag-construction.md)
- [🔮 Vision](vision/README.md)
  - [Welcome to Talus Vision](vision/talus-vision/welcome-to-talus-vision.md)
  - [Cryptographic Features](vision/talus-vision/crypto-features.md)
  - [Connect with Sui Wallet](vision/talus-vision/connect-with-sui-wallet.md)
  - [User Workflows and Profile](vision/talus-vision/user-workflows-and-profile.md)
  - [About Previously Deployed Workflows](vision/talus-vision/about-previously-deployed-workflows.md)
  - [Draw Your First Workflow](vision/talus-vision/draw-first-workflow/README.md)
    - [About Playground](vision/talus-vision/draw-first-workflow/about-playground.md)
    - [Node Component](vision/talus-vision/draw-first-workflow/node-component.md)
    - [Step by Step: My First Workflow](vision/talus-vision/draw-first-workflow/step-by-step-my-first-workflow.md)
    - [Deploy My First Workflow](vision/talus-vision/draw-first-workflow/deploy-my-first-workflow.md)
    - [Execute My First Workflow](vision/talus-vision/draw-first-workflow/execute-my-first-workflow.md)
    - [Summary](vision/talus-vision/draw-first-workflow/summary.md)
  - [About Sidebar](vision/talus-vision/about-sidebar/README.md)
    - [Workflow Discovery Tab](vision/talus-vision/about-sidebar/workflow-discovery-tab.md)
    - [Deploy Workflows Tab](vision/talus-vision/about-sidebar/deploy-workflows-tab.md)
    - [Execute Workflow Tab](vision/talus-vision/about-sidebar/execute-workflow-tab.md)
    - [Tools Tab](vision/talus-vision/about-sidebar/tools-tab.md)
    - [JSON Editor Tab](vision/talus-vision/about-sidebar/json-editor-tab.md)
    - [Gas Management Tab](vision/talus-vision/about-sidebar/gas-management-tab.md)
- [Technical Glossary](nexus/glossary.md)

## 🛠️ Tools

- [⚓ Nexus Standard Tools](tools/nexus-standard-tools.md)
  - [Math](tools/math/README.md)
  - [LLM: OpenAI Chat Completion](tools/llm-openai-chat-completion/README.md)
  - [Social: X](tools/social-twitter/README.md)
  - [Storage: Walrus](tools/storage-walrus/README.md)
  - [Echanges: Coinbase](tools/exchanges-coinbase/README.md)
  - [HTTP](tools/http/README.md)
  - [Templating: Jinja](tools/templating-jinja/README.md)

## ADRs

- [Encryption Removal](nexus/adr/x3dh-removal-from-nexus.md)

## Looking for a home

* [vision/talus-vision/explorer.md](vision/talus-vision/explorer.md)
* [nexus/adr/address-balance-gas-payment.md](nexus/adr/address-balance-gas-payment.md)
* [nexus/adr/auto-abort-expired-executions.md](nexus/adr/auto-abort-expired-executions.md)
* [nexus/adr/leader-status-ownership-versioning.md](nexus/adr/leader-status-ownership-versioning.md)
* [nexus/adr/multi-coin-gas-payment.md](nexus/adr/multi-coin-gas-payment.md)
* [nexus/packages/reference/nexus_registry/agent_registry.md](nexus/packages/reference/nexus_registry/agent_registry.md)
