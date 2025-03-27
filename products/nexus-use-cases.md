---
description: So what can you build?
---

# Nexus Use Cases

To make matters a bit more concrete, let’s walk through a hypothetical use case that showcases the potential of Nexus to build Talus AI agents.

### Example Use Case: In-game Soundtrack Agent

#### The business idea

Imagine a scenario where a game developer is building a game that has some functionality that interacts with the blockchain. At the very least there is an **in-game currency that is a token deployed onchain**.

Additionally, there is an **onchain music marketplace** that offers songs by paying a (small) fee, either to own the rights to play the song or the capability to play it only once.

We would like to develop a Talus AI Agent, an onchain workflow designed to autonomously purchase and curate background soundtracks for gaming. Instead of requiring players to manually select songs, the AI Agent intelligently recommends and acquires tracks based on user preferences and contextual factors, such as time of day, season, and in-game events (e.g., boss battles or exploration sequences).

The AI dynamically analyzes gameplay and environmental cues to select the most immersive soundtracks. Over time, the agent optimizes its recommendations through reinforcement learning, continuously improving its ability to match music with gameplay moments for a more engaging and personalized experience.

Now, we would like to create a Talus AI agent (defined as a workflow onchain) that enables the purchase of songs to be used as background soundtracks while playing the game. The AI element comes into play when the agent is using the preferences of the user and some other contextual data (time of the day, time of the year, game context e.g. boss battle) to recommend which songs to purchase and play, the user does not actively need to pick them. The agent's performance is optimized through reinforcement learning.

#### Dependencies

* There exists an onchain marketplace for music tracks to purchase songs from.
  * Ideally with low fees through transaction batching or something of the sort.
* The onchain marketplace offering can be queried with price and metadata information available.
* There exists an AI service that allows to output song recommendations based on contextual data with reinforcement learning capabilities.
* The contextual metadata from the game’s backend is available.
* Wallet integration for Sui (should be present given the in-game currency already exists)

#### Developer Journey

Let’s walk through the steps from the previous section that outline what development work needs to be done to implement this Talus agent:

1. We are using 1 offchain Tool. The AI song recommendation service. This service is not yet registered in the Nexus Tool registry.
2. We need to integrate the AI song recommendation service as a Tool. This means we’ll need to create a Tool definition to comply with the Tool interface expected by Nexus. This will allow the Nexus offchain components to invoke the Tool when the onchain workflow requests it. Additionally you’ll register the Tool to the Nexus onchain Tool registry. All of the above is facilitated by the Nexus SDK.
3. We are also using 1 onchain Tool, the online music marketplace dApp. This service is not yet registered in the Nexus Tool registry.
4. We need to write a proxy contract onchain that will hold the Tool definition. Again this is to comply with the Tool interface set by Nexus, but this time for onchain Tools. The Tool then needs to be registered in the Nexus Tool registry. Once more, Nexus SDK can automate part of your development work.
5. This step can happen in parallel with previous steps and involves designing the agent Workflow, i.e. formalizing the desired functionality in terms of Tools and the control flow between them. For each Tool you’ll need to specify what inputs it is taking, what outputs are possible and what to do next based on those outputs. \
   In our case, we’ll need to trigger the workflow by some event from the game (for example, some new contextual metadata is added) which will then take some inputs (user ID etc.) and the onchain workflow should emit an event to request the AI Song recommendation tool to return a list of songs to purchase. This will be the major output of the Tool. The list of songs to purchase will then serve as input for the next Tool, which is the onchain Tool that can purchase the songs using the funds it has at its disposal. The output here could be some metadata referencing an NFT transfer of the songs to the user’s wallet. This then completes the workflow.&#x20;
6. When the workflow is designed as part of the TAP, we can publish the package and instantiate the agent.

{% hint style="info" %}
**Fat Agent or multi-agent workflows?**

One design question to consider is whether to put all of your application logic into a single “fat” agent, or whether to split up functionality into smaller agents (that could be used by others, potentially with some royalty fee going to the original builder) that interact, i.e. multi-agent workflows. This is still an open design space at the moment.
{% endhint %}

### Examples: Tools

To further get the creative juices flowing, here is a non-exhaustive list of potential AI services that could serve as offchain Tools:

<details>

<summary>Information Retrieval &#x26; Analysis</summary>

* Web search APIs (Google Custom Search, Bing Web Search)
* Academic paper databases (Semantic Scholar, arXiv)

- Knowledge bases (Wikidata, DBpedia)

* News APIs (NewsAPI, The Guardian)

</details>

<details>

<summary>Text Processing</summary>

* Language models (GPT models, Claude, PaLM)

- Translation APIs (DeepL, Google Translate)

* Sentiment analysis tools (VADER, TextBlob)

- Text-to-speech/Speech-to-text (Whisper, Azure Speech)

</details>

<details>

<summary>Data &#x26; Computation</summary>

* Wolfram Alpha API for computations

- Database interfaces (SQL, MongoDB)

* Spreadsheet manipulation tools

- Data visualization libraries (Plotly, D3.js)

</details>

<details>

<summary>Media Processing</summary>

* Image generation (DALL-E, Stable Diffusion)

- Image analysis (Google Cloud Vision, Azure Computer Vision)

* Video processing (OpenCV)

- Audio processing (Librosa)

</details>

<details>

<summary>Productivity &#x26; Communication</summary>

* Email APIs (Gmail, SendGrid)

- Calendar management (Google Calendar API)

* Document processing (DocParser, Textract)

- Task management (Trello API, Asana API)

</details>

<details>

<summary>Development &#x26; Coding</summary>

* GitHub API for code management

- Code completion tools (GitHub Copilot)

* Code analysis tools

- Testing frameworks

</details>

<details>

<summary>Social Media Posting</summary>

* Automated X Posting

- Automated TikTok Video Uploads

* Automated Instagram Posts

</details>



