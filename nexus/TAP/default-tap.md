# Default TAP Retirement

The legacy witness-based `nexus_workflow::default_tap` module has been
retired as an active runtime and public authoring path.

Use the standard TAP registry, standard endpoint object, and
`default_tap_target` metadata instead. New executions are routed through
standard Talus agent, skill, endpoint, payment, agent-vault, and authorization
context.

New standard Talus agents always receive a shared `AgentPaymentVault`. Default
target execution can still use invoker-funded payment, but agent-triggered or
scheduled flows can select agent-vault-backed payment when the endpoint policy
allows it.

Historical data that was emitted by older witness TAP deployments may still be
decoded by compatibility event parsers, but it is not an executable runtime
path for new leader, SDK, CLI, or deployment flows.
