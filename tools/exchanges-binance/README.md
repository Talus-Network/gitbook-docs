# `xyz.taluslabs.exchanges.binance.get-price@1`

Standard Nexus Tool that retrieves the most recent trades for a symbol from the Binance Spot API. Binance API [reference](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market#get-trades)

Each invocation makes one `GET /api/v3/trades` request, which costs 25 request weight against the Tool host's IP.

## Input

**`symbol`: [`String`]**

The Binance spot symbol to get trades for, e.g. `"BTCUSDT"` or `"ETHBTC"`. The symbol is trimmed and uppercased; it must be 1–20 characters of `A-Z`, `0-9`, `-`, `_` or `.`.

**`limit`: [`u16`] (optional)**

Number of trades to return, between `1` and `256`. Defaults to `100`.

Binance allows up to 1000, but a Nexus output port holds at most 256 values, so larger pages cannot be returned in a single invocation.

## Output Variants & Ports

**`ok`**

The trades were retrieved successfully.

- **`ok.symbol`: [`String`]** - The normalized symbol
- **`ok.trades`: [`Vec<Trade>`]** - Recent trades, oldest first. Each trade has:
  - **`id`: [`u64`]** - Binance trade ID
  - **`price`: [`String`]** - Trade price
  - **`qty`: [`String`]** - Traded quantity in the base asset
  - **`quote_qty`: [`String`]** - Traded quantity in the quote asset
  - **`time`: [`u64`]** - Trade time in milliseconds since the Unix epoch
  - **`is_buyer_maker`: [`bool`]** - Whether the buyer was the maker (i.e., the taker sold)
  - **`is_best_match`: [`bool`]** - Whether the trade was the best price match

Prices and quantities are decimal strings, exactly as Binance returns them, to keep their precision:

```json
{
  "id": 28457,
  "price": "4.00000100",
  "qty": "12.00000000",
  "quote_qty": "48.000012",
  "time": 1499865549590,
  "is_buyer_maker": true,
  "is_best_match": true
}
```

**`no_trades`**

The symbol exists but Binance returned no recent trades for it.

- **`no_trades.symbol`: [`String`]** - The normalized symbol

**`err`**

The request was rejected because of its input.

- **`err.reason`: [`String`]** - What was wrong with the input. Always written by the Tool, never text from Binance or the HTTP client
- **`err.kind`: [`String`]** - Type of error:
  - `invalid_request` - The input is invalid, or Binance rejected its parameters (HTTP 400)
  - `invalid_symbol` - The symbol is not listed on Binance (code `-1121`)

## Failures

Outputs are recorded on-chain, so failures on the operator's side are not returned as outputs. These are rate limits (HTTP 429), IP bans (418), WAF rejections (403), restricted locations (451), Binance outages (5XX), timeouts (8 seconds), network errors, and unexpected, malformed or oversized responses.

For these, the invocation fails with an unsigned HTTP 500 (`{"error": "tool_invocation_failed"}`). The response carries no Tool signature, so it is not a Tool result. The details are logged on the Tool host at `error` level and are not included in the response. The log also shows a panic for the same invocation; this is how the Tool fails the invocation, not a crash.

## Configuration

**`BINANCE_API_BASE_URL`** (optional)

Overrides the Binance API base URL, which defaults to `https://api.binance.com`. Use it to point at an alternative Binance endpoint such as `https://data-api.binance.vision` or `https://api1.binance.com`. Only HTTPS URLs are accepted, except plain HTTP for loopback hosts during local development. The service refuses to start when the value is invalid. `--meta` does not read it.

Binance blocks requests from restricted locations (HTTP 451) including the United States, so deploy the Tool in a region Binance serves. Our deployment sets `https://data-api.binance.vision` (market data only) in `tools.json` because the Tool runs in `us-east1`.
