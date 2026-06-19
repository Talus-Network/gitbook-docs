# Agent Development

Nexus, as an agentic framework, provides on-chain and off-chain components for developing agents, registering skills, discovering endpoints, composing tools into workflows, and executing those workflows. Find the definitions of these terms in the [glossary](../glossary.md) if they are unfamiliar.

{% hint style="info" %}
A Talus agent is a standard TAP `Agent` identity registered in the TAP registry and associated with one or more workflow services, endpoint revisions, payment policies, and on-chain assets.
{% endhint %}

## Standard TAP Model

New TAP development uses the standard TAP registry and endpoint model in `nexus_interface::tap`. The legacy witness-based default TAP runtime is retired for active authoring; see [Default TAP Retirement](default-tap.md) for compatibility context.

The standard model has these core objects:

* `Agent`: the keyed on-chain identity for the agent.
* `AgentSkill`: an agent-owned skill child addressed by an agent-local `SkillId` (`u64`).
* endpoint revisions: versioned execution metadata for a skill, including endpoint object metadata, shared object requirements, and activation state.
* `DefaultDagExecutor`: the registry-backed default runtime-selected DAG target used by default DAG execution flows.
* `AgentPaymentVault`: the agent-owned vault created for every standard Talus agent.
* `ExecutionPayment`: the execution-bound payment child used for immediate and scheduled TAP execution.

## Development Paths

* **Registered agent skill**: Create an `Agent`, publish or select a DAG, register a skill with `register_skill`, and activate endpoint revisions through the TAP registry. This is the default path for application agents.
* **Default runtime DAG executor**: Use the deployment-provided default DAG executor for runtime-selected DAG execution when no app-specific TAP business logic is needed.
* **Custom TAP package + standard registry**: Publish a package with custom endpoint objects or business logic, but still register the agent, skills, endpoint revisions, authorization schema, and payments through the standard TAP registry and interface.

{% hint style="success" %}
Choose the simplest path that preserves the authorization and payment behavior your agent needs. Most agents should start with a standard registered skill and add custom TAP package logic only when endpoint state or business rules require it.
{% endhint %}

## Standard Procedure

1. Publish the workflow DAG or choose runtime-selected default DAG execution.
2. Define the skill requirements: input schema hash, workflow hash, metadata hash, `TapPaymentPolicy`, `TapSchedulePolicy`, and `TapVertexAuthorizationSchema`.
3. Create the agent through the TAP registry. Agent creation also creates the agent's `AgentPaymentVault`.
4. Register the skill with the owning `Agent`. `register_skill` allocates the next agent-local `SkillId`, stores the `AgentSkill` child under the agent, stores registry records, and writes the initial endpoint revision.
5. Publish or provide the endpoint object for the TAP package when the skill needs endpoint-local state. The endpoint object ID, version, digest, shared object references, interface revision, and requirements are committed through the endpoint config digest.
6. Announce later endpoint revisions with `announce_endpoint_revision` and activate the revision intended for new executions with `set_active_endpoint_revision`.
7. Publish discovery metadata by relying on standard TAP events and registry records. Leaders and SDK clients resolve active runtime state by `(agent_id, skill_id, interface_revision)`.
8. Execute through the registered agent path or the default runtime DAG executor path. A worksheet pins the `Agent`, `SkillId`, endpoint revision, endpoint object, and execution ID so later payment and authorization checks use the same revision.
9. Create payment using the endpoint policy. Invoker-funded execution supplies a payment coin; agent-funded execution uses the `AgentPaymentVault`. Both paths create an execution-bound `ExecutionPayment` child under the `DAGExecution`.
10. Finalize payment after execution. Successful executions accomplish the payment; failed or rejected executions refund it. Scheduled occurrences finalize against the occurrence payment and then update the scheduled task state.

## Default Runtime DAG Execution

The current default path is a registry-owned default agent target, not the old witness `nexus_workflow::default_tap` module. Deployment bootstraps a runtime-selected default skill and stores a `DefaultDagExecutor` in the TAP registry. Default DAG execution and scheduler-triggered default execution resolve that target, create the same TAP worksheet/payment context, and pin the runtime-selected DAG in execution evidence.

Use this path when the agent does not need package-specific endpoint logic. Use a registered skill when the agent needs a stable agent-owned skill with its own endpoint revisions, payment policy, schedule policy, or authorization schema.

## Payment Vaults

Every standard Talus agent receives an `AgentPaymentVault` when the agent is created. The vault is the canonical on-chain balance holder for agent-funded explicit agent execution.

Anyone can deposit SUI into an agent vault. Withdrawals are restricted to the agent owner or operator through the standard TAP registry authorization path. When an endpoint policy selects agent-funded execution, TAP payment creation locks the requested budget from the agent vault into an `ExecutionPayment`. Consumption is tracked on the payment, and finalization either charges the consumed amount on accomplish or releases the lock on refund.

This does not force every TAP endpoint to use agent funds. `TapPaymentPolicy` determines whether execution is invoker-funded or agent-funded, and scheduled execution can use address-funded reserve or agent-vault-funded reserve depending on the selected agent path.

## Scheduling and Authorization

Scheduled agent execution creates a `ScheduledSkillTask` tied to the agent, skill, endpoint revision, payment source, reserve, and occurrence policy. Each triggered occurrence converts prepaid reserve into a normal execution-bound payment, then completion records whether that occurrence accomplished or refunded and whether the task may continue recurring.

Fixed on-chain tool authorization uses `TapVertexAuthorizationSchema` and per-vertex authorization grants. Endpoint revisions commit to the allowed fixed tools and payment requirement. Leaders verify the grant against the pinned worksheet before a one-use `VertexAuthorizationCheckCap` can authorize the fixed tool call.

## Explore Further

Continue learning about agent development with:

* the [Nexus interface for TAPs](../packages/nexus-interface.md), which summarizes the active standard TAP interface surface
* [Default TAP Retirement](default-tap.md), which explains the retired witness path and the standard default DAG executor replacement
