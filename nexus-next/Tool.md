# Tool

A Tool is an off-chain HTTP service or an on-chain smart contract. These are invoked by the Leader based on instructions provided by the on-chain Workflow.

## Tool definitions

Each Tool must provide a standardized definition, telling us where and how to interact with it. This definition is stored in the Tool Registry on-chain and should be retrievable publicly. Definition should be a JSON file in the following format:

```json
{
  "fqn": "{domain}.{name}@{version}",
  "type": "onchain/offchain",
  "url": "{url/move_ident}",
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

Straighforward, and enum with `offchain` and `onchain` values.

3. `url`

This will determine _how_ the Leader contacts the Tool. For off-chain Tools, this field will be an actual URL. This can point to the server directly or to a load balancer.

On-chain Tools will require a similar `url` but it would likely be a move call definition in the format `pkg_id::module::fn` or similar. This topic is, however, unexplored and needs to be researched in depth.

4. `input_schema` and `output_schema`

These will be `draft-2020-12` JSON schema definitions of the Tool inputs and outputs. This lets the Leader parse and verify data going in and coming out of the Tool.

Note that for `output_schema`, top-level `oneOf` has to be enforced by the Tool deployment process to adhere to the `OutputVariant` DAG definition.

## Off-chain Tool interface

Off-chain Tools will expose 3 HTTP endpoints:

1. `GET /health` - operational health, should retfqn 200 if and only if the Tool is ready to be invoked
2. `GET /meta` - retfqns the Tool definition JSON
3. `POST /invoke` - this endpoints invokes the Tool logic, it accepts data in its `input_schema` format and outputs data in its `output_schema` format

## On-chain Tool interface

This topic has not yet been discussed in depth and needs addressing.

## Tool registration

Tools should be register in the Tool Registry using our [CLI][repo-nexus-sdk-cli].

### Off-chain tools

The CLI leverages functions in module `tool_registry` in the `nexus_workflow` Sui package.

The registration locks `SUI` tokens as collateral to combat spam.
The creator can at any point unregister the tool again, which starts a timer defined by the `tool_registry` module.
After the timer expires, the collateral can be reclaimed.

### On-chain tools

This is still in process of design.
Our initial focus are off-chain tools.

## Tool authorization

Once there are community Tools, we will need a way to authorize communication between the Leader and a Tool. This has been discussed superficially and it needs to be researched in depth in the future.

<!-- List of References -->

[repo-nexus-sdk-cli]: https://github.com/Talus-Network/nexus-sdk/tree/main/cli