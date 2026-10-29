# Trading decisions

`xyz.taluslabs.trading.decide@<version>` chooses one trading action from a strategy, token pair,
and account snapshot. It returns a proposed action.

## Inputs

| Port | Type | Meaning |
| --- | --- | --- |
| `strategy` | string enum | Decision logic, selected from the table below. |
| `token_pair` | string | Binance spot symbol, checked against the supported markets. |
| `snapshot` | string | JSON text describing the settled account and its current decision window. |

The current supported pair is `SUIUSDT`. It must match `market_symbol` in the snapshot.

| Strategy | Decision logic |
| --- | --- |
| `hold` | Makes no trade and leaves existing positions unchanged. This is the cash baseline. |
| `time_aware_returns` | Predicts returns from price history and time features, then applies an entry threshold and holding period. |
| `volatility_scaled_returns` | Predicts returns from price changes scaled by volatility, then applies an entry threshold and holding period. |
| `price_direction` | Uses predicted price direction and account features to select a legal action with a saved policy. |
| `return_distribution` | Uses predicted ranges of returns and account features to select a legal action with a saved policy. |

The adapter uses the account balance, positions, leverage cap, settlement prices, and turn timing.
It estimates position ages from scheduled turn lengths and reconstructs risk relative to an initial
capital of 10,000. Card prose and preferences are not model features. Additional snapshot fields
are accepted, while required fields, numeric bounds, and account consistency are validated.

## Outputs

The [output schema] has `ok` and `err` variants. An `ok` result contains:

| Port | Meaning |
| --- | --- |
| `action` | `0` hold, `1` open long, `2` open short, or `3` close a position. |
| `size` | Opening notional in millionths of USDC. Zero for hold and close. |
| `leverage` | Opening leverage, bounded by the account's cap. Zero for hold and close. |
| `position_ix` | Position index to close. Zero for hold and open. |
| `reasoning` | Public explanation, at most 500 characters. |

The tool permits at most three positions, a minimum opening notional of 100, and an opening margin
of at most half the available capital. The bundled policies open at one times leverage. These
bounds match the saved models' account contract.

Invalid input returns `err` with a reason. The toolkit rejects an unknown strategy or missing port
before invocation. A closed decision window, stale market data, an incomplete market window, or a
model failure returns hold. Hold does not close existing positions. The caller remains responsible
for its authorization, final rule checks, and execution price.

## Configuration

| Variable | Meaning |
| --- | --- |
| `TRADING_MARKET_URL` | Required URL of the indexer's observation endpoint. |
| `TRADING_POLICY_SEED` | Actor checkpoint for both policy strategies, one of `7`, `19`, or `31`. Default `7`. |
| `TRADING_DRAWDOWN_LIMIT` | Policy risk limit in `(0, 1]`. Default `0.2`. |
| `TRADING_LATENCY_PROFILE` | Model execution delay profile from `0` to `2`. Default `1`. |
| `BIND_ADDR` | Toolkit listen address. Default `127.0.0.1:8080`. |

Our deployment sets `TRADING_MARKET_URL` in `tools.json` to
`https://trading-market-service.fly.dev/v1/market`, served by
[trading-market-service](https://github.com/Talus-Network/trading-market-service).

The binary embeds all four model artifacts. Startup loads the models and creates an HTTP client.
Model invocations and health checks fetch an observation. Health requires a current observation,
at most ten seconds old, and ignores quote age, so a quiet market stays healthy. The process
retains no market history or account state.

## Indexer contract

The indexer must provide complete, current observations of the Binance `SUIUSDT` spot market.
It must run independently of tool instances, maintain persistent market history, and be reachable
from every tool region. Its location must permit access to the required Binance market data.

The endpoint must accept `GET <TRADING_MARKET_URL>?token_pair=SUIUSDT`. Requests contain no account
data. A successful response must use HTTP 200 and contain a JSON object matching this schema
exactly. The complete response must arrive within three seconds. The response body after
decompression must not exceed 2,000,000 bytes. The endpoint must respond directly, without a redirect.

| Field | Requirement |
| --- | --- |
| `token_pair` | Must be the string `SUIUSDT`. |
| `quote.price_e8` | Must be the last trade price strictly before `market.timestamp`. |
| `quote.age_seconds` | Must be the elapsed seconds from that trade to `market.timestamp`. |
| `market.timestamp` | Must be an integer Unix timestamp in seconds. |
| `market.bars` | Must contain exactly 17,640 rows of two float32 values, oldest first. |
| `market.bar_quote_age_seconds` | Must measure quote age at the final completed bar boundary. |
| `market.minute_prices` | Must contain exactly 31 prices, newest first, at 60 second intervals. |

The observation timestamp must be within `1_600_000_000..=4_102_444_800`. Minute prices must use
the last trade strictly before `t`, `t - 60`, through `t - 1800`, where `t = market.timestamp`.
Bar quote age must use the last trade strictly before the final completed five second boundary,
measured at that boundary.

All prices must be integers in hundred millionths of USDT, greater than zero and less than
3,000,000,000. `market.minute_prices[0]` must equal `quote.price_e8`. Bar values and quote ages must
be finite float32 values. Ranges and ages must be nonnegative. JSON serialization must preserve
these values when decoded as float32.

Bar construction must satisfy these requirements:

1. Bars must cover `[end - 88200, end)`, where `end = floor(t / 5) * 5`, on UTC boundaries.
1. The source must contain consecutive raw trades with microsecond timestamps and a quote before
   the first bar. Trades at a closing boundary must belong to the next interval.
1. Each one second interval must contribute its actual high and low. An interval without trades
   must contribute its preceding close and must retain the actual age of the last trade.
1. Each five second bar must use the maximum of those highs, the minimum of those lows, and its
   last close. Its row must be `[ln(close / previous_close), ln(high / low)]`, computed in
   float64 and then rounded to float32.

The indexer must verify continuous retrieval through `t` before publishing an observation. It
must return HTTP 503 only when it cannot vouch for the window, because history is incomplete or
retrieval is more than ten seconds behind. A quiet market is not an error: the indexer returns
HTTP 200 with the actual quote age, which may exceed ten seconds. A usable observation must not be
in the future, must be no older than ten seconds, and must reach the account's current turn
opening time. Quote age plus elapsed time since `t` must not exceed ten seconds when the tool
finishes retrieval. The tool returns hold when retrieval, observation validation, or this
freshness check fails.

## Validation

```bash
cargo test --locked -p trading --all-targets
cargo clippy --locked -p trading --all-targets -- -D warnings
```

The suite covers the saved prediction references for every model and actor checkpoint, strategy
selection, pair validation, independent account requests, action limits, indexer validation,
request timeouts, account features, and the binary's public input contract.

<!-- List of references -->

[output schema]: output.schema.json
