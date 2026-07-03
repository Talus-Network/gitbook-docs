# Tool

A Tool is an off-chain HTTP service or an on-chain smart contract. These are invoked by [Leader nodes](crates/leader.md) based on instructions provided by the on-chain [Workflow](packages/workflow.md).

## Tool definitions

Each Tool must provide a standardized definition, telling us where and how to interact with it. This definition is stored in the Tool Registry onchain and should be retrievable publicly. Definition should be a JSON file in the following format:

```json
{
  "fqn": "{domain}.{name}@{version}",
  "type": "onchain/offchain",
  "url": "{url/move_ident}",
  "description": "A UTF-8 string",
  "input_schema": "draft-2020-12 JSON schema",
  "output_schema": "draft-2020-12 JSON schema"
}
```

1. `fqn`

Uniform resource name. Tool `fqn` consists of 3 parts - `domain`, `name` and `version`. When registering a tool, this structure should be checked.

```
xyz.taluslabs.llm.openai-chat-completion@1
```

2. `type`

Straightforward, and enum with `offchain` and `onchain` values.

3. `url`

This will determine _how_ the Leader contacts the Tool. For offchain Tools, this field will be an actual URL. This can point to the server directly or to a load balancer.

For onchain Tools, the `url` field is replaced by specific fields in the tool registry: `package_address` (the published package address), `module_name` (the Move module name), and an implicit `execute` function name. The Leader constructs the Move call as `{package_address}::{module_name}::execute` when invoking the tool.

4. `description`

A description of what the tool does. Currently we do not enforce a maximum length but this is
subject to change. In addition we assume a UTF-8 representation.

5. `input_schema` and `output_schema`

These will be `draft-2020-12` JSON schema definitions of the Tool inputs and outputs. This lets the Leader parse and verify data going in and coming out of the Tool.

Note that for `output_schema`, top level `oneOf` has to be enforced by the Tool deployment process to adhere to the `OutputVariant` DAG definition.

For onchain tools, both of these schemas will be generated automatically during tool registration.

## Off-chain Tool interface

Off-chain Tools will expose 3 HTTP endpoints:

1. `GET /health` - operational health, should return `200` if and only if the Tool is ready to be invoked
2. `GET /meta` - returns the Tool definition JSON
3. `POST /invoke` - this endpoint invokes the Tool logic; it accepts data in its `input_schema` format and outputs data in its `output_schema` format

For the full transport/security contract (HTTPS/TLS and signed HTTP), see:

- [Tool communication (HTTPS + signed HTTP)](guides/tool-communication.md)

## Onchain Tool interface

Onchain Tools are published as separate Move modules on Sui. They must adhere to specific interface requirements to be compatible with the Nexus framework.

### Required Interface

Every onchain tool must provide an `execute` entry function with the following signature:

```move
entry fun execute(
    worksheet: ProofOfUID,
    result: &mut OnchainToolResult,
    // ... tool specific parameters ...
    ctx: &mut TxContext,
)
```

#### Key Requirements execute function

1. **Workflow Worksheet**: The tool receives `worksheet: ProofOfUID`, stamps it, and passes it into `onchain_tool_result::finalize`.

2. **Witness Stamping**: The tool must stamp the worksheet with its witness ID to prove it was executed:

   ```move
   worksheet.stamp_with_data(&witness.id, b"tool_executed");
   ```

3. **Result Handling**: The function must not return values. It must write the final `TaggedOutput` into `result: &mut OnchainToolResult`; the leader shares that result object after `execute`.

4. **Tool Witness**: Each tool must maintain a witness object that uniquely identifies it. This is typically stored in the tool's shared state object.

#### Output enum

The module must also provide an `Output` enum in which the output variants and fields are specified. This is similar to the offchain tool template. This enum is not used directly during execution. It provides the output schema that is automatically generated during tool registration. All output variants and fields are up to the tool developer to specify. This `Output` enum may look like this:

```move
public enum Output {
    Success {
        old_count: u64,
        new_count: u64,
        increment: u64,
    },
    Error {
        reason: AsciiString,
    },
    LargeIncrement {
        old_count: u64,
        new_count: u64,
        increment: u64,
        warning: AsciiString,
    },
}
```

### TaggedOutput Usage

Tools build different output variants using `TaggedOutput`, then finalize that output into the mutable `OnchainToolResult` input. Fields must be typed using constructor functions to ensure proper JSON formatting:

```move
// Success case with typed fields
let output = tagged_output::new(b"ok")
    .with_named_payload(b"result", data::inline_one(value.to_string().into_bytes()).as_string())
    .with_named_payload(b"count", data::inline_one(count.to_string().into_bytes()).as_number())
    .with_named_payload(b"active", data::inline_one(b"true").as_bool())
    .with_named_payload(b"owner", data::inline_one(owner_address.to_string().into_bytes()).as_address());

// Error case
let output = tagged_output::new(b"err")
    .with_named_payload(b"reason", data::inline_one(b"Something went wrong").as_string());

// Custom variant with mixed types
let output = tagged_output::new(b"timeout")
    .with_named_payload(b"elapsed_ms", data::inline_one(elapsed.to_string().into_bytes()).as_number())
    .with_named_payload(b"retry_after", data::inline_one(retry_delay.to_string().into_bytes()).as_number())
    .with_named_payload(b"message", data::inline_one(b"Operation timed out").as_string());

onchain_tool_result::finalize_and_share(result, worksheet, output, ctx);
```

#### Field Value Types

The `data::inline_one(bytes)` helper provides typed constructors for different value types:

- `.as_number()`: For numeric values (u8, u16, u32, u64, u128, u256)
- `.as_string()`: For string values
- `.as_bool()`: For boolean values
- `.as_address()`: For address values

These constructors ensure proper JSON formatting when outputs are processed by the Nexus framework.

## Tool registration

Tools should be registered in the Tool Registry using our [CLI](../nexus-sdk/cli.md#nexus-tool).

### Offchain tools

The CLI leverages functions in module `tool_registry` in the `nexus_workflow` Sui package.

The registration locks `SUI` tokens as collateral to combat spam. The creator can at any point unregister the tool again, which starts a timer defined by the `tool_registry` module. After the timer expires, the collateral can be reclaimed.

### Onchain tools

Onchain tools are registered using the same CLI, but with additional parameters specific to the onchain tool Move module:

```bash
nexus tool register-onchain \
  --package-address <PACKAGE_ID> \
  --module-name <MODULE_NAME> \
  --fqn <DOMAIN.NAME@VERSION> \
  --description "<DESCRIPTION>" \
  --witness-id <WITNESS_OBJECT_ID>
```

The CLI automatically:

- Introspects the Move module's `execute` function to generate the input schema
- Generates the output schema based on the `Output` enum
- Allows for optional customization of input and output schemas
- Registers the tool in the Tool Registry with the appropriate data

## Tool authentication and key discovery (Network Auth)

Off-chain Tools are invoked by Nexus Leader nodes. Tools and Leader nodes need a way to authenticate signed messages and discover which public key is currently valid for an identity (with support for rotation and revocation).

Nexus uses the on-chain `nexus_workflow::network_auth` module as a trusted binding registry from identity → Ed25519 public keys. Any verifier can read the binding state on-chain to obtain the active public key for an identity and verify signed messages offline.

Network Auth is protocol-agnostic: it does not define a transport or wire format. It only defines identities, proofs, and key lifecycle.

Reference:

- [`nexus_workflow::network_auth`](packages/reference/nexus_workflow/network_auth.md)
