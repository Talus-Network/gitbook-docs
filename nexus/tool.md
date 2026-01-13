# Tool

A Tool is an offchain HTTP service or an onchain smart contract. These are invoked by the [Leader](crates/leader.md) based on instructions provided by the onchain [Workflow](packages/workflow.md).

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

Note that for `output_schema`, top-level `oneOf` has to be enforced by the Tool deployment process to adhere to the `OutputVariant` DAG definition.

For onchain tools, both of these schemas will be generated automatically during tool registration.

## Off-chain Tool interface

Off-chain Tools will expose 3 HTTP endpoints:

1. `GET /health` - operational health, should retfqn 200 if and only if the Tool is ready to be invoked
2. `GET /meta` - retfqns the Tool definition JSON
3. `POST /invoke` - this endpoints invokes the Tool logic, it accepts data in its `input_schema` format and outputs data in its `output_schema` format

## Onchain Tool interface

Onchain Tools are published as separate Move modules on Sui. They must adhere to specific interface requirements to be compatible with the Nexus framework.

### Required Interface

Every onchain tool must provide an `execute` function with the following signature:

```move
public fun execute(
    worksheet: &mut ProofOfUID,
    // ... tool-specific parameters ...
    ctx: &mut TxContext,
): ToolOutput
```

#### Key Requirements execute function

1. **First Parameter**: The first parameter must be `worksheet: &mut ProofOfUID`. This is a worksheet object that the tool must stamp to prove execution.

2. **Witness Stamping**: The tool must stamp the worksheet with its witness ID to prove it was executed:

   ```move
   worksheet.stamp_with_data(&witness.id, b"tool_executed");
   ```

3. **Return Type**: The function must return a `ToolOutput` object, which provides a standardized way to return structured outputs. This object must be populated with the exact same variant type and fields as specified in the output schema.

4. **Tool Witness**: Each tool must maintain a witness object that uniquely identifies it. This is typically stored in the tool's shared state object.

#### Output enum

The module must also provide an `Output` enum in which the output variants and fields are specified. This is similar to the offchain tool template. This enum however, unlike the `ToolOutput` object, is not being used during execution. It is merely used as a means to have a clear overview of the output schema of the onchain tool, and to automatically generate the output schema during tool registration. All output variants and fields are up to the tool developer to specify. This `Output` enum may like this:

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

### ToolOutput Usage

Tools can return different output variants using the `ToolOutput` system. Fields must be typed using constructor functions to ensure proper JSON formatting:

```move
// Success case with typed fields
tool_output::ok()
    .with_field(b"result", tool_output::string_value(value.to_string().into_bytes()))
    .with_field(b"count", tool_output::number_value(count.to_string().into_bytes()))
    .with_field(b"active", tool_output::bool_value(b"true"))
    .with_field(b"owner", tool_output::address_value(owner_address.to_string().into_bytes()))

// Error case
tool_output::err(b"Something went wrong")

// Custom variant with mixed types
tool_output::variant(b"timeout")
    .with_field(b"elapsed_ms", tool_output::number_value(elapsed.to_string().into_bytes()))
    .with_field(b"retry_after", tool_output::number_value(retry_delay.to_string().into_bytes()))
    .with_field(b"message", tool_output::string_value(b"Operation timed out"))
```

#### Field Value Types

The `tool_output` module provides typed constructors for different value types:

- `tool_output::number_value(bytes)`: For numeric values (u8, u16, u32, u64, u128, u256)
- `tool_output::string_value(bytes)`: For string values (will be wrapped in quotes)
- `tool_output::bool_value(bytes)`: For boolean values (true/false)
- `tool_output::address_value(bytes)`: For address values (will be prefixed with "0x" and quoted)

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

## Tool authorization

Once there are community Tools, we will need a way to authorize communication between the Leader and a Tool. This has been discussed superficially and it needs to be researched in depth in the future.
