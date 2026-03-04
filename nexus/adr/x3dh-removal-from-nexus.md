# ADR-1: Removal of X3DH+ Encryption from Nexus

**Status:** Proposed
**Date:** 2025-02-17
**Authors:** David ([@davidrotari19](https://github.com/davidrotari19))
**Deciders:** Pavel ([@kouks](https://github.com/kouks)), David ([@davidrotari19](https://github.com/davidrotari19)), Isaac, Augusto
**Consulted:** Stephen, Christos
**Informed:** Engineering Team

**Constraint Tags:** Technical | Architectural | Timeline

---

## Context

### What problem are we solving?

The current X3DH+ encryption implementation places decryption authority in the Leader. This design conflicts with our eventual goal of a permissionless leader network, where tools—not the Leader—should hold authority over secrets.

The encryption was intended to protect secrets (API keys) and sensitive data (prompts, chat completions) in Leader-Tool communication. However, the current design where Leader manages encryption context:

1. **Does not align with target architecture** - Authority should reside in tools, not Leader
1. **Requires complete redesign** - Stephen's intended design places encryption responsibility in tools, which is incompatible with current implementation
1. **Is not achievable within timeline** - Proper redesign cannot be completed before March mainnet

For the AvA Gaming use case specifically, the identified encryption needs are solvable without X3DH+:

- **API keys**: Solvable with "fat tools" that manage their own keys and charge per invocation
- **Prompts/completions**: Product decision—plaintext on-chain (via Walrus) is acceptable since all users have equal access to the same information, maintaining fair market dynamics

### Relevant Constraints

**Architectural:** Current encryption places authority in Leader; target architecture requires authority in tools. These are fundamentally incompatible approaches.

**Timeline:** March mainnet deadline does not permit the complete redesign required to implement encryption correctly.

**Product:** For AvA Gaming, on-chain visibility of game state data is acceptable—tech-savvy users having seconds of advantage is fair given equal access to information.

### Architectural Position

This decision affects the **Capability Layer** (Leader-Tool communication protocol). Rather than implement an ad-hoc solution that contradicts our architectural direction, we remove encryption entirely and solve the underlying needs through alternative mechanisms.

---

## Decision

### What are we doing?

We will remove X3DH+ encryption from Nexus entirely. The needs it was intended to address will be solved through alternative mechanisms:

- **API key protection**: Tools manage their own keys internally ("fat tools") and charge users per invocation
- **Sensitive data (prompts/completions)**: Stored in Walrus; plaintext is acceptable given equal access for all users

### Why this approach?

Implementing encryption properly requires authority to reside in tools, not Leader. The current implementation inverts this, and correcting it requires a complete redesign we cannot complete before March mainnet. Rather than ship an ad-hoc solution that contradicts our architectural direction, we remove encryption and solve the actual requirements (API key security, fair game dynamics) through simpler mechanisms that align with our target architecture.

---

## Alternatives Considered

### Alternative 1: Continue with current Leader-based encryption

**Description:** Complete David's in-progress changes to the existing encryption design.

**Why not:** The design fundamentally places authority in the wrong component (Leader instead of tools). Completing it would ship something incompatible with our eventual permissionless leader network goal.

### Alternative 2: Redesign encryption with tool-based authority

**Description:** Implement Stephen's design where tools manage their own encryption context.

**Why not:** Requires complete redesign incompatible with current implementation. Timeline to March mainnet does not permit this scope of work.

### Alternative 3: Do Nothing (keep partial implementation)

**Description:** Leave encryption code in place but incomplete.

**Why not:** Adds complexity without benefit. Encryption is a prerequisite for leader distribution, so incomplete implementation blocks other work while providing no security value.

---

## Consequences

### Positive Consequences

- Development effort redirected to agents and other critical path items
- Avoids shipping architecture that contradicts long-term direction
- Simplifies Leader implementation ahead of distribution work
- Existing encryption code may be reusable in Nexus SDK for tool developers implementing DTP

### Negative Consequences

- Prompts and chat completions visible in plaintext on Walrus (mitigated: equal access maintains fairness)
- API keys must be managed within tools rather than passed through workflows
- Time invested in X3DH+ implementation is sunk cost

### Neutral Consequences

- Tools become "fatter" with more responsibility for managing their own authority and secrets
- Tool pricing must account for resource usage (e.g., OpenAI token costs)

### Reversibility Assessment

- **Reversibility:** Moderate
- **Reversal cost:** Future encryption implementation should follow tool-based authority design, not resurrect Leader-based approach
- **Point of no return:** None—this decision explicitly defers proper encryption to post-mainnet

---

## Context Evolution Tracking

### Review Schedule

- **Next review:** Post-mainnet, when designing tool-based encryption for permissionless leader network
- **Review criteria:** New use cases requiring encrypted data that cannot be solved with fat tools; move toward permissionless leader network

---
