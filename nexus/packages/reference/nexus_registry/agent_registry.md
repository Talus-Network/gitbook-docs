<a name="nexus_registry_agent_registry"></a>

# `nexus_registry::agent_registry`

`agent_registry` stores Talus agent and skill records and provides the bridge between registered skills, workflow DAG execution, payment policy, agent payment vaults, and scheduler tasks.

Primary surfaces:

- `AgentRegistry`: shared registry object for agent records and default-agent executor state.
- `AgentRecord`: registry-side agent lifecycle and skill table state.
- `SkillRecord`: current skill contract, active flag, DAG binding, requirements, and revision metadata.
- `create_agent`, `attach_embedded_agent`: agent creation and registry binding.
- `create_skill`, `register_skill`, `register_skill_with_fixed_tools`: skill creation and compatibility registration helpers.
- `set_skill_active`, `set_agent_active`, `update_skill_description`, `update_dag`, `update_skill_policies`: lifecycle and revision management.
- `new_agent_skill_payment_for_execution`, `new_agent_skill_payment_from_vault_for_execution`, `new_default_dag_executor_payment_for_execution`: execution payment helpers.
- `schedule_skill_execution*`, `trigger_scheduled_skill_execution`, `create_scheduled_occurrence_payment`, `cancel_scheduled_skill_execution_from_agent_vault`: scheduler integration for address-funded and vault-funded skill execution.
- `default_dag_executor_*`: default agent executor inspection and payment helpers.

See [Talus agent development](../../../TAP/agent-development.md), [Default agent](../../../TAP/default-agent.md), and [Agent skills and vaults](../../../TAP/agent-skills-and-vaults.md) for the conceptual workflow.
