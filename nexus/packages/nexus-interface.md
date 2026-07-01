# Nexus Interface

Nexus TAP execution now uses the standard TAP registry and endpoint model in
`nexus_interface::tap`.

The standard TAP interface also creates an `AgentPaymentVault` for every new
agent. The vault holds agent-funded execution balances, tracks locked budget,
and is used by vault-backed `ExecutionPayment` settlement. Deposits are open;
withdrawals are authorized by the agent owner or operator through the TAP
registry. Payment finalization records source kind, source identity, locked
budget, consumed amount, and final state.

The old v1 witness announcement flow is retired for active package authoring.
`nexus_interface::v1` remains only for non-witness shared-object reference and
configuration helpers that are still consumed by verifier compatibility and
historical decoding.
