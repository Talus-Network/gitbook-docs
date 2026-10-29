# Social Tools (Elfa AI)

A Nexus Tool bundle exposing two operations backed by the
[Elfa AI](https://docs.elfa.ai) market-intelligence API:

- `chat` — one complete answer from Elfa's market-intelligence model: a
  free-form question, a macro or summary overview, a token or X-account analysis
- `paper-trading-decide` — one seat's decider for Doppel paper trading: the
  `decide` vertex between the game's view and act vertices, deciding long,
  short, close or hold from Elfa's read on the market and Elfa's model

`chat` wraps `POST /v2/chat`. `paper-trading-decide` composes it with four
v3 reads (`GET /v3/entities`, `GET /v3/calls/positioning`, `GET /v3/events`,
`GET /v3/market/{crypto|equity}/mindshare`); those four live in the crate as
building blocks (`src/tools/`) with their own tests, but are not registered
as tools of their own. Elfa returns links, counts and written analysis, never
post text.

## Plans and credits

Both tools need a **pay-as-you-go, Grow or Enterprise** Elfa key; a Free key
gets `err.kind = forbidden` from `chat` and a hold from the decider. `chat` is
priced by the work a turn does, within the speed's cap: on the test key `fast`
cost 3 to 8 credits per call and `expert` (the default) about 115. The v3
reads are free of credits until 31 October 2026 by Elfa's announcement, so a
decision costs one `fast` chat call; the `signals` strategy makes it free
and deterministic. The rate limit is 60 requests per minute per key (120 on
Grow), shared by both tools; a 429 surfaces as `err.kind = rate_limited`
with the retry delay in `err.reason`. The tool environment holds **one** key:
every DAG invocation spends that key's credits.

## Build & Run

```sh
# Build (release)
cargo build --package social-elfa --release

# Run locally — binds to 127.0.0.1:8080 by default
cargo run --package social-elfa

# Override the bind address
BIND_ADDR=0.0.0.0:9000 cargo run --package social-elfa

# Print tool metadata and exit (what CI feeds to `nexus tool register`); needs no env
./target/release/social-elfa --meta

# Offline tests (mockito + protocol checks), then the live ones against Elfa (spend credits)
cargo test --package social-elfa
just elfa live live_paper_trading_decide
```

## Environment Variables

`.env` (cwd-only) is loaded at startup via [`dotenvy`](https://crates.io/crates/dotenvy);
existing exports win. See `.env.example`.

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `ELFA_API_KEY` | **yes** | — | Elfa API key, sent as `x-elfa-api-key`. Unset: the server boots but `chat` answers `err.kind = missing_api_key`, the decider decides from the snapshot alone (no evidence, no model) and `/health` fails. Malformed (whitespace, non-printable): fatal exit at startup |
| `ELFA_API_BASE_URL` | no | `https://api.elfa.ai` | Base URL. Validated as `https://` with no path/query/fragment/userinfo |
| `ELFA_ALLOW_INSECURE` | no | unset | Set to `1` to accept `http://` base URLs (dev/mockito only) |
| `BIND_ADDR` | no | `127.0.0.1:8080` | Address the bundled HTTP server binds to |

The key is never a tool input: inputs flow through the Nexus DAG as on-chain
data. `--meta` runs without any of these variables.

## Server Endpoints

```sh
# List registered tool paths
GET /tools

# Liveness: key configured + Elfa `GET /v2/ping` reachable (no credits)
GET /health

# One tool's metadata
GET /<tool-path>/meta

# Invoke a tool (POST, JSON body). The reply is canonical BCS, not JSON.
POST /<tool-path>/invoke
```

## Tools

`chat` returns `err { reason, kind, status_code, elfa_code, request_id }` on
failure; `paper-trading-decide` returns `err { reason }` only for a snapshot
the game's view vertex would not write, and answers a hold on every failure
of its own. Every port of a variant is always present; a port marked
_nullable_ is `null` when Elfa did not supply it. The examples below show the
decoded reply (the wire carries BCS).

---

# `xyz.taluslabs.social.elfa.chat@1`

One complete answer from Elfa's market-intelligence model (`POST /v2/chat`).
Six modes: free-form `chat`, `macro` and `summary` market overviews,
`tokenIntro` / `tokenAnalysis` for an asset, `accountAnalysis` for an X
account. The model does its own research (news, events, positioning, price
action) and answers in Markdown. The research can take over a minute, so the
tool declares a 120 s timeout. Elfa API
[reference](https://docs.elfa.ai/api/v2/chat).

## Input

**`message`: `String`** _(required for `chat`, ignored otherwise)_

The question to answer.

**`analysis_type`: `String`** _(optional)_

`chat` (default), `macro`, `summary`, `tokenIntro`, `tokenAnalysis` or
`accountAnalysis`.

**`speed`: `String`** _(optional)_

`fast`, `expert` (default) or `adaptive`. `expert` reads more and costs
roughly fifteen times as much.

**`session_id`: `String`** _(optional)_

`ok.session_id` from a previous answer, to continue that conversation.

**`include_sources`: `bool`** _(optional)_

Also return the links the research read. Costs nothing extra.

**`symbol`: `String`** _(for `tokenIntro` / `tokenAnalysis`)_

The asset's ticker, e.g. `BTC` or `$ETH`.

**`chain`: `String`**, **`contract_address`: `String`** _(alternative to `symbol`)_

Identify the asset by its contract instead.

**`username`: `String`** _(required for `accountAnalysis`)_

The X username, with or without `@`.

## Output Variants & Ports

**`ok`**

The model answered.

- **`ok.answer`: `String`** — The answer, Markdown.
- **`ok.session_id`: `String`** — Pass back as `session_id` to continue the thread.
- **`ok.analysis_type`: `String`** — The mode that produced the answer.
- **`ok.credits_used`: `u64`** — What the call cost: Elfa's per-request credit (the `x-elfa-credits` header) plus the model's consumption (`creditsConsumed`); the sum is what the balance loses.
- **`ok.source_count`: `u64`** — Research links returned (0 unless `include_sources`).
- **`ok.source_urls`: `String`** — Those links, comma-separated; empty when none.

**`err`**

The request failed before or at Elfa.

- **`err.reason`: `String`** — Short description. For 4xx responses Elfa's `message` and `details` are forwarded; 5xx bodies are logged, not inlined.
- **`err.kind`: `String`** — `missing_api_key`, `invalid_input`, `invalid_request`, `unauthorized`, `forbidden`, `insufficient_credits`, `not_found`, `rate_limited`, `upstream_unavailable`, `upstream_error`, `network`, `timeout`, `parse` or `oversized_response` (a body above 2 MiB is refused, not buffered). `rate_limited`, `upstream_unavailable` and `timeout` are safe to retry unchanged.
- **`err.status_code`: `u16`** _(nullable)_ — HTTP status from Elfa.
- **`err.elfa_code`: `String`** _(nullable)_ — Elfa's stable code, e.g. `ERR_RATE_LIMIT_EXCEEDED`.
- **`err.request_id`: `String`** _(nullable)_ — Elfa request id for support.

## Example

```sh
curl -s -X POST http://127.0.0.1:8080/chat/invoke \
  -H 'Content-Type: application/json' \
  -d '{"message": "Why is BTC moving today?", "speed": "fast"}' -o chat.bcs
# decoded: {"ok":{"answer":"# TL;DR:\n\nI read today's BTC move as a macro-driven relief bounce ...","session_id":"e4ec6067-…","analysis_type":"chat","credits_used":4,"source_count":0,"source_urls":""}}

# Token analysis with the research links
curl -s -X POST http://127.0.0.1:8080/chat/invoke \
  -H 'Content-Type: application/json' \
  -d '{"analysis_type": "tokenAnalysis", "symbol": "SUI", "speed": "fast", "include_sources": true}' -o chat.bcs
# decoded: {"ok":{"answer":"...","session_id":"...","analysis_type":"tokenAnalysis","credits_used":7,"source_count":36,"source_urls":"https://...,https://..."}}
```

---

# `xyz.taluslabs.social.elfa.paper-trading-decide@1`

One seat's decider for Doppel paper
trading. It is the `decide` vertex of the seat's act walk: the game's view
vertex hands it the seat's reading of its match as one JSON string, and it
answers the four integers the act vertex takes, within the game's rule. It
takes `strategy` and `token_pair` as `xyz.taluslabs.trading.decide` does, so
the game's decider DAG (`players/decider/act.dag.json` in the Doppel
repository) serves it as it is: set the `decide` vertex's `tool_fqn` to this
FQN, keep both defaults, publish it, and seats register their act skill for
that DAG; the view and act vertices stay as they are.

The act walk is view (20 s) + decide + act (30 s). It must land inside the
tournament's `retrigger_after_ms`, and inside the seat's act window: a move
that lands after the snapshot's `act_until_ms` (the seat's first trigger in
the turn plus the host's `act_window_ms`, 60 s by default) is written as a
hold. The tool declares a 30 s timeout and budgets each decision to end 15 s
before `act_until_ms`, at most 25 s: about 25 s with the default window. A
decision whose window is already closing is answered at once from the
snapshot alone, without calling Elfa.

A move is decided in this order:

- **Evidence.** The pair's base asset (`SUI` of `SUIUSDT`) is resolved to
  Elfa's asset family, then positioning, the newest five events and the 24h
  mindshare row are read in parallel (10 s, or less when the window is
  tighter; one market's evidence is shared by every seat for 60 s).
- **Judgement.** Elfa's model (`POST /v2/chat`, at the strategy's speed)
  gets the persona, the card, the book, the prices, the evidence and the
  rules, and when the order fills (about `resolve_at_ms`, so it forecasts the
  price then), and is asked for one JSON object: action, margin percent,
  leverage, position to close, confidence, reasoning. An open below
  confidence 40 becomes a hold; a leverage above the card's cap is cut before
  the size is computed, so the margin the model named is what it puts up. The
  model is not asked when less than 8 s of the budget is left.
- **Fallback.** With the `signals` strategy, or when the model does not answer
  within the budget, fails or answers prose, a deterministic signal policy
  decides from the same evidence: crowd lean
  (followed, or inverted for a contrarian or mean-reversion card), event
  implications, attention change, the one-step price return and the card's
  long or short bias. The open threshold falls with `aggression`; size and
  leverage come from the card's risk band scaled by `confidence`; an open
  position is closed when the signal turns against it or it is halfway to
  liquidation.
- **The rule, last.** At most three positions, leverage 1 to 50 cut to the
  card's cap, margin at most half the free capital, at least 100 USDC after
  the cut, a close only of an index that exists. The act never refuses.

The same input (strategy, pair and snapshot text) answers the same move for
ten minutes, so a leader that repeats the call spends no second chat; two
seats never share one, their books differ in the snapshot.

## Input

**`strategy`: `String`** _(required)_

The decision logic for this call. The `hold` strategy is answered once the
pair is checked, before anything else is read.

| Strategy | Decision logic | Elfa cost |
| --- | --- | --- |
| `hold` | Makes no trade and leaves the positions as they are: the cash baseline. | none |
| `signals` | The deterministic signal policy on Elfa's market evidence. | the v3 reads |
| `elfa_fast` | Elfa's model at `fast` speed on that evidence; the signal policy when it does not answer in time. | the reads plus 3 to 8 credits |
| `elfa_expert` | Elfa's model at `expert` speed; it answers in 20 to 60 s and usually misses the act window, so the signal policy decides. | the reads plus about 115 credits |

**`token_pair`: `String`** _(required)_

The market, a Binance spot symbol such as `SUIUSDT`, quoted in FDUSD, USDT,
USDC, TUSD or BUSD; Elfa's evidence is read for its base asset. It must be
the snapshot's `market_symbol`. An unsupported pair is refused before the
account is read, for the `hold` strategy too.

**`snapshot`: `String`** _(required)_

The view vertex's JSON text (`paper_trading::snapshot` in the Doppel
repository): `in_match`, `market_symbol` (the market, which must be
`token_pair`; the view vertex up to `@11` wrote it as `coin_id`, which
reads too), the card (`risk`, `leverage_cap`, `bias`,
`aggression`, `confidence`, `persona`), and in a live match `seat_ix`,
`turn_count`, `round_limit`, `turn_open`, `turn_opened_at_ms`,
`resolve_at_ms`, `act_until_ms`, `observed_price_e8`, `observed_at_ms`,
`capital`, `peak_equity`, `max_drawdown`, `positions` and
`settled_prices_e8`. Fields the game adds later are skipped; a snapshot
without the turn's times (an older view vertex) gets the full budget and no
fill horizon.

## Output Variants & Ports

**`ok`**

The seat's move for the open turn; the act DAG wires the first four ports.

- **`ok.action`: `u8`** — 0 hold, 1 open long, 2 open short, 3 close.
- **`ok.size`: `u64`** — The notional in USDC with six decimals; 0 unless opening.
- **`ok.leverage`: `u8`** — 1 to 50 and at most the card's cap; 0 unless opening.
- **`ok.position_ix`: `u64`** — The index of the position to close; 0 unless closing.
- **`ok.reasoning`: `String`** — What decided and what the rule changed, at most 500 characters; recorded with the walk.
- **`ok.confidence`: `u8`** — 0 to 100.
- **`ok.source`: `String`** — `chat` (the model decided), `signals` (the policy decided) or `rule` (no decision was needed).
- **`ok.credits_used`: `u64`** — What the decision cost as Elfa reports it: the chat call's request credit plus its consumption, plus the v3 reads; a replayed decision reports what it cost when it was made.

**`err`**

A request the tool cannot evaluate: a `token_pair` it does not support or
that is not the snapshot's `market_symbol`, or a snapshot that is not what
the view vertex writes. Every other failure is an `ok` hold, because `err`
ends the walk without an act and the seat pays another occurrence.

- **`err.reason`: `String`** — What was refused.

## Example

```sh
# A fresh seat on SUI, turn 2 of 6, momentum card, no open position
curl -s -X POST http://127.0.0.1:8080/paper-trading-decide/invoke \
  -H 'Content-Type: application/json' \
  -d '{"strategy": "elfa_fast", "token_pair": "SUIUSDT", "snapshot": "{\"in_match\":true,\"market_symbol\":\"SUIUSDT\",\"risk\":60,\"leverage_cap\":10,\"bias\":1,\"aggression\":70,\"confidence\":60,\"persona\":\"momentum trader\",\"seat_ix\":1,\"turn_count\":1,\"round_limit\":6,\"turn_open\":true,\"observed_price_e8\":101500000,\"observed_at_ms\":1792410000000,\"capital\":10000000000,\"peak_equity\":10000000000,\"max_drawdown\":0,\"positions\":[],\"settled_prices_e8\":[100000000]}"}' -o decide.bcs
# decoded: {"ok":{"action":1,"size":2000000000,"leverage":2,"position_ix":0,"reasoning":"[chat] Price has risen from 1.0000 to 1.0150, favoring a small momentum long ...","confidence":60,"source":"chat","credits_used":2}}

# A seat whose table has not opened: no Elfa call, a hold
curl -s -X POST http://127.0.0.1:8080/paper-trading-decide/invoke \
  -H 'Content-Type: application/json' \
  -d '{"strategy": "elfa_fast", "token_pair": "SUIUSDT", "snapshot": "{\"in_match\":false,\"market_symbol\":\"SUIUSDT\",\"risk\":25,\"leverage_cap\":50,\"bias\":0,\"aggression\":50,\"confidence\":50,\"persona\":\"test seat\"}"}' -o decide.bcs
# decoded: {"ok":{"action":0,"size":0,"leverage":0,"position_ix":0,"reasoning":"[rule] hold: the seat is in no live match","confidence":0,"source":"rule","credits_used":0}}
```
