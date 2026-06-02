# Memory Tools (MemWal)

A Nexus Tool bundle exposing seven memory operations backed by the
[MemWal](https://memwal.ai) relayer:

- `remember` / `remember_bulk` — store one or up to 20 memories
- `recall` — semantic search over stored memories
- `ask` — memory-augmented Q&A (LLM with retrieved context)
- `analyze` — extract facts from text and store each as a memory
- `forget` — delete every memory in a namespace
- `stats` — report memory count and storage bytes for a namespace

## Pinned MemWal release

Wire format pinned to
[`@mysten-incubation/memwal@0.0.4`](https://github.com/MystenLabs/MemWal/tree/%40mysten-incubation%2Fmemwal%400.0.4/services/server)
(server `Cargo.toml` v`0.1.0`). `health_check()` enforces the version at
runtime against `GET /health`. On a new relayer tag with a Cargo bump or
any change to `auth.rs` / `types.rs` / `routes.rs` / `rate_limit.rs`,
update `MEMWAL_API_VERSION` in `src/client.rs` and re-audit those four files.

## Build & Run

```sh
# Build (release)
cargo build --package memory-memwal --release

# Run locally — binds to 127.0.0.1:8080 by default
cargo run --package memory-memwal

# Override the bind address
BIND_ADDR=0.0.0.0:9000 cargo run --package memory-memwal
```

## Environment Variables

`.env` (cwd-only) is loaded at startup via [`dotenvy`](https://crates.io/crates/dotenvy);
existing exports win.

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `MEMWAL_DELEGATE_PRIVATE_KEY` | **yes** | — | Hex-encoded 32-byte Ed25519 (Elliptic Curve Digital Signature Algorithm) delegate private key |
| `MEMWAL_ACCOUNT_ID` | recommended | — | MemWal account object ID (`0x…`). Sent as `x-account-id` and signed into the canonical message. Unset → relayer falls back to a slower on-chain registry scan |
| `MEMWAL_SERVER_URL` | no | `https://relayer.staging.memwal.ai` (testnet) | Relayer base URL. Validated as `https://` (no path/query/fragment/userinfo). Mainnet: `https://relayer.memwal.ai` |
| `MEMWAL_ALLOW_INSECURE` | no | unset | Set to `1` to accept `http://` relayer URLs (dev/mockito only) |

## Server Endpoints

```sh
# List registered tool paths
GET /tools

# Liveness check (validates key + reaches the relayer)
GET /health

# Invoke a tool (POST, JSON body)
POST /<tool-path>/invoke
```

## Tools

All seven tools return `Err { reason: String }` on failure (`reason` is a
short, terse description; full upstream bodies are not inlined). Per-tool
sections below cover only the `Ok` variant unless a failure mode is
tool-specific.

---

# `xyz.taluslabs.memory.memwal.remember@1`

Store a single piece of text as a persistent memory. The call blocks until the
memory is durably written to Walrus and returns the resulting blob ID — the
next vertex in a Nexus DAG (Directed Acyclic Graph) will not activate until
the write is confirmed.

## Input

**`text`: `String`** *(required)*

The text to store as a memory.

**`namespace`: `String`** *(optional)*

Namespace used to scope this memory. Defaults to `"default"` on the server
when omitted.

## Output Variants & Ports

**`ok`**

The memory was durably stored.

- **`ok.blob_id`: `String`** — Walrus blob identifier for the stored memory.

## Example

```sh
curl -s -X POST http://127.0.0.1:8080/memory/remember/invoke \
  -H 'Content-Type: application/json' \
  -d '{"text": "Paris is the capital of France"}'
# {"ok":{"blob_id":"<walrus-blob-id>"}}

# With an explicit namespace
curl -s -X POST http://127.0.0.1:8080/memory/remember/invoke \
  -H 'Content-Type: application/json' \
  -d '{"text": "Alice works at ACME", "namespace": "people"}'
# {"ok":{"blob_id":"<walrus-blob-id>"}}
```

---

# `xyz.taluslabs.memory.memwal.recall@1`

Semantic search over stored memories. Returns the closest matches ranked by
cosine distance — lower distance means more relevant.

## Input

**`query`: `String`** *(required)*

Natural-language query to search for relevant memories.

**`limit`: `u32`** *(optional)*

Maximum number of results to return. Server default applies when omitted.

**`namespace`: `String`** *(optional)*

Namespace to search within. Searches the `"default"` namespace when omitted.

## Output Variants & Ports

**`ok`**

Search completed. The result list may be empty if nothing matched.

- **`ok.results`: `Array`** — Memories ranked by relevance, each containing:
  - **`text`: `String`** — The stored text of the memory.
  - **`blob_id`: `String`** — Walrus blob identifier.
  - **`distance`: `f64`** — Cosine distance from the query vector (lower = more relevant).
- **`ok.namespace`: `String`** — The namespace that was searched (one query = one namespace).

## Example

```sh
curl -s -X POST http://127.0.0.1:8080/memory/recall/invoke \
  -H 'Content-Type: application/json' \
  -d '{"query": "capital cities in Europe", "limit": 3}'
# {"ok":{"results":[{"text":"Paris is the capital of France","blob_id":"...","distance":0.12,"namespace":"default"}]}}

# Empty result when nothing matches
curl -s -X POST http://127.0.0.1:8080/memory/recall/invoke \
  -H 'Content-Type: application/json' \
  -d '{"query": "something completely unknown"}'
# {"ok":{"results":[]}}
```

---

# `xyz.taluslabs.memory.memwal.ask@1`

Memory-augmented question answering. The relayer retrieves the most relevant
stored memories for the question, injects them as context into an LLM (Large
Language Model) prompt, and returns the generated answer together with the
source memories that informed it.

## Input

**`question`: `String`** *(required)*

The question to answer using stored memories as context.

**`namespace`: `String`** *(optional)*

Namespace to retrieve memories from. Uses the `"default"` namespace when
omitted.

**`limit`: `u32`** *(optional)*

Maximum number of source memories to inject as context. Server default applies
when omitted.

## Output Variants & Ports

**`ok`**

Question answered successfully.

- **`ok.answer`: `String`** — LLM-generated answer.
- **`ok.sources`: `Array`** — Memories used as context, each containing:
  - **`blob_id`: `String`** — Walrus blob identifier.
  - **`text`: `String`** — The stored text of the memory.
  - **`distance`: `f64`** — Cosine distance from the question vector.

## Example

```sh
curl -s -X POST http://127.0.0.1:8080/memory/ask/invoke \
  -H 'Content-Type: application/json' \
  -d '{"question": "What is the capital of France?"}'
# {"ok":{"answer":"Paris","sources":[{"blob_id":"...","text":"Paris is the capital of France","distance":0.05}]}}

# No relevant memories → answer with empty sources
curl -s -X POST http://127.0.0.1:8080/memory/ask/invoke \
  -H 'Content-Type: application/json' \
  -d '{"question": "What is the speed of light?"}'
# {"ok":{"answer":"I don't know","sources":[]}}
```

---

# `xyz.taluslabs.memory.memwal.analyze@1`

Extract discrete facts from a text document and store each fact as an
individual memory. The relayer runs an LLM fact-extraction pass and enqueues
one memory-write job per fact found.

This tool returns immediately after the jobs are enqueued — it does **not**
block on individual Walrus writes. Use `job_count` for downstream monitoring;
use `remember` if you need a confirmed blob ID.

## Input

**`text`: `String`** *(required)*

The text from which to extract and store facts.

**`namespace`: `String`** *(optional)*

Namespace to store the extracted facts in. Uses the `"default"` namespace when
omitted.

## Output Variants & Ports

**`ok`**

Facts were submitted for storage.

- **`ok.job_count`: `u32`** — Number of individual memory-write jobs enqueued.
  Zero means no facts were extracted from the text.

## Example

```sh
curl -s -X POST http://127.0.0.1:8080/memory/analyze/invoke \
  -H 'Content-Type: application/json' \
  -d '{"text": "Alice lives in Paris. Bob works at ACME. Paris is in France."}'
# {"ok":{"job_count":3}}

# No facts extracted → job_count is 0
curl -s -X POST http://127.0.0.1:8080/memory/analyze/invoke \
  -H 'Content-Type: application/json' \
  -d '{"text": "..."}'
# {"ok":{"job_count":0}}
```

---

# `xyz.taluslabs.memory.memwal.remember_bulk@1`

Store up to 20 memories in a single batched call. The relayer rate-limits
`/api/remember` at weight 5 per call but `/api/remember/bulk` at weight 10 for
up to 20 items — a 10× efficiency gain when batching is feasible. The call
blocks until every item is durably written; a single failed item fails the
whole batch.

## Input

**`items`: `Array`** *(required, 1–20 entries)*

Each entry has:

- **`text`: `String`** *(required)* — the text to store.
- **`namespace`: `String`** *(optional)* — namespace for this item. A single
  bulk call can write to multiple namespaces.

## Output Variants & Ports

**`ok`**

Every item was durably stored.

- **`ok.blob_ids`: `Array<String>`** — Walrus blob identifiers, in the same
  order as the input `items`.

**`err`** — additionally: the whole batch fails if any individual item fails (no partial success).

## Example

```sh
curl -s -X POST http://127.0.0.1:8080/memory/remember_bulk/invoke \
  -H 'Content-Type: application/json' \
  -d '{
    "items": [
      {"text": "Paris is the capital of France"},
      {"text": "Tokyo is the capital of Japan"},
      {"text": "Madrid is the capital of Spain"}
    ]
  }'
# {"ok":{"blob_ids":["<blob1>","<blob2>","<blob3>"]}}
```

---

# `xyz.taluslabs.memory.memwal.forget@1`

Delete every memory in a namespace. Owner-scoped — only memories belonging to
the authenticated account are removed. Lifecycle complement to `remember`:
useful for clearing scratch namespaces at the end of a DAG run, or for
recovering quota before the 1 GB per-account cap is hit.

## Input

**`namespace`: `String`** *(optional)*

The namespace to clear. Defaults to `"default"` on the server when omitted.

## Output Variants & Ports

**`ok`**

Deletion completed.

- **`ok.deleted`: `u64`** — number of memories removed. Zero is a valid
  success (the namespace was empty or did not exist).

## Example

```sh
curl -s -X POST http://127.0.0.1:8080/memory/forget/invoke \
  -H 'Content-Type: application/json' \
  -d '{"namespace": "scratch-pad"}'
# {"ok":{"deleted":12}}

# Clearing an empty namespace is fine
curl -s -X POST http://127.0.0.1:8080/memory/forget/invoke \
  -H 'Content-Type: application/json' \
  -d '{"namespace": "never-used"}'
# {"ok":{"deleted":0}}
```

---

# `xyz.taluslabs.memory.memwal.stats@1`

Report the number of memories and total encrypted byte size stored in a
namespace for the authenticated account. Useful as a quota guard before
heavy writes — the relayer enforces 1 GB per-account storage and starts
returning HTTP 402 once that's exceeded.

## Input

**`namespace`: `String`** *(optional)*

Defaults to `"default"` on the server when omitted.

## Output Variants & Ports

**`ok`**

- **`ok.memory_count`: `i64`** — number of memories in the namespace.
- **`ok.storage_bytes`: `i64`** — total encrypted byte size on Walrus.
- **`ok.namespace`: `String`** — the resolved namespace (mirrors what the
  server interpreted; `"default"` when the input was omitted).

## Example

```sh
curl -s -X POST http://127.0.0.1:8080/memory/stats/invoke \
  -H 'Content-Type: application/json' \
  -d '{"namespace": "people"}'
# {"ok":{"memory_count":17,"storage_bytes":5242880,"namespace":"people"}}
```
