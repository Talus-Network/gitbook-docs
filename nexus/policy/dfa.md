# DFA Module

## Overview
The `nexus_primitives::automaton` module is the on-chain, deterministic regex engine that powers policies. It stores the canonical DFA tuple `(States, Alphabet, Transition, Start, Accepting)`, enforces shape/uniqueness invariants at construction time, and exposes constant-cost evaluation (`delta`) plus richer config hooks via dynamic fields.

## Why
- On-chain workflows need a **regular language** over typed symbols (witness type names or UIDs).
- Move lacks runtime regex support; a DFA makes the accepted language explicit, deterministic, and cheap to evaluate.
- The automaton lives beside the guarded asset/process, so the allowed traces cannot drift off-chain.

## Core Types
- `DeterministicAutomaton<State, Symbol>`: `TableVec`-backed `states`, `alphabet`, transition matrix `|States| x |Alphabet|` (as nested `TableVec` of indices), accepting bitmap, and a start index.
- `ConfiguredAutomaton<State, Symbol>`: wraps a DFA with a UID so `(state?, symbol)` transition metadata can be stored as dynamic fields.
- `TransitionKey` / `TransitionConfigKey`: keys for configs; specific `(state, symbol)` overrides wildcard `(*, symbol)`.

## Data Layout & Invariants
- Backed by `TableVec` storage for states/alphabet/transition/accepting; creation requires a `TxContext`.
- States and alphabet entries must be unique; duplicates assert.
- The transition matrix is dense and validated to `|States| x |Alphabet|`; mismatched shapes assert.
- Start state must be in the basis; accepting set is converted to a bitmap aligned with `states`.
- Symbol/state lookups assert when outside the basis, preventing silent off-path behavior.

## Constructing a DFA
- `new(states, alphabet, start, accepting, transitions, ctx)`: takes `TableVec` inputs, canonicalizes the matrix by translating successor states to indices, and materializes `TableVec` storage.
- Mutators: `add_symbol` (append column), `add_state(..., ctx)` (append row), `set_transition`, `set_transition_indexed`, `set_accepting_state`.
- Helpers: `symbol_index_of` / `expect_symbol_index_of`, `expect_state_index_of` for safe membership checks.

## Evaluating
- `delta(state, symbol)` / `delta_indexed(state_idx, symbol_idx)`: single-step transition.
- `run(word: TableVec<Symbol>)` / `run_from(state, word)`: fold over a word; returns final state.
- `accepts(word: TableVec<Symbol>)`: true if the final state is accepting.
- `start_state`, `start_index`, `state_at`: introspection utilities.

## Transition Configs
- `register_symbol_config((* , symbol), config)` registers wildcard metadata.
- `register_transition_config((state, symbol), config)` registers a specific transition’s metadata.
- Lookup order: specific `(state, symbol)` first, then wildcard; missing configs assert when borrowed.
- Accessors: `has_symbol_config`, `borrow_symbol_config`, `borrow_transition_config` (+ mutable variants).

## Using with Policy
- The policy module fixes `State = u64` and `Symbol = Witness(TypeName) | Uid(object::ID)` and embeds a `ConfiguredAutomaton`.
- `advance_with_*` resolves a symbol to its alphabet index, asserts if absent, and applies `delta_indexed`.
- `new_linear` (in policy) builds a prefix-enforcing DFA where non-matching in-alphabet symbols self-loop; to hard-fail off-path symbols, omit them from the alphabet or route them to a non-accepting sink state you add via `add_state`.

## Mental Model
Think of `automaton.move` as the minimal, programmable regex backend: it gives you the deterministic state machine, lets you extend it with new symbols/states, and hangs typed configs off transitions. The policy module composes this with typed symbols to act as an on-chain dispatcher and filter.
