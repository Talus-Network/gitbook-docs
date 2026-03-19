
<a name="(nexus_workflow=0x0)_network_auth"></a>

# Module `(nexus_workflow=0x0)::network_auth`

## Identity and key bindings

`network_auth` is an on-chain registry that binds off-chain identities (Leader nodes and Tools) to Ed25519 public keys used for message signing and verification.

It acts as a trusted binding registry for:

- Key discovery: find the currently active public key for an identity.
- Key rotation: register multiple keys over time and switch which key is active.
- Key revocation: explicitly revoke keys that should no longer be accepted.

### Identities

Identities are represented by `IdentityKey`:

- `Leader { address }` identifies a Leader node by Sui address.
- `Tool { fqn }` identifies a Tool by its fully-qualified name (FQN).

### Proofs

Key registration uses two independent proofs:

- `ProofOfIdentity`: proves the transaction is authorized to act for the identity (via on-chain capabilities).
- `ProofOfKey`: proof-of-possession (PoP) that the registrant controls the private key for the public key being registered.

### Verification rule

Verifiers should accept signatures from the binding’s active key only (`KeyBinding::active_key_id`). Non-active keys are treated as invalid even if they have not been revoked.



-  [Struct `NetworkAuth`](#(nexus_workflow=0x0)_network_auth_NetworkAuth)
-  [Struct `KeyBinding`](#(nexus_workflow=0x0)_network_auth_KeyBinding)
-  [Struct `KeyRecord`](#(nexus_workflow=0x0)_network_auth_KeyRecord)
-  [Struct `ProofOfIdentity`](#(nexus_workflow=0x0)_network_auth_ProofOfIdentity)
-  [Struct `ProofOfKey`](#(nexus_workflow=0x0)_network_auth_ProofOfKey)
-  [Struct `NetworkAuthCreatedEvent`](#(nexus_workflow=0x0)_network_auth_NetworkAuthCreatedEvent)
-  [Struct `KeyBindingCreatedEvent`](#(nexus_workflow=0x0)_network_auth_KeyBindingCreatedEvent)
-  [Struct `KeyRegisteredEvent`](#(nexus_workflow=0x0)_network_auth_KeyRegisteredEvent)
-  [Struct `KeyRevokedEvent`](#(nexus_workflow=0x0)_network_auth_KeyRevokedEvent)
-  [Struct `ActiveKeyUpdatedEvent`](#(nexus_workflow=0x0)_network_auth_ActiveKeyUpdatedEvent)
-  [Enum `IdentityKey`](#(nexus_workflow=0x0)_network_auth_IdentityKey)
-  [Constants](#@Constants_0)
-  [Function `new`](#(nexus_workflow=0x0)_network_auth_new)
-  [Function `share`](#(nexus_workflow=0x0)_network_auth_share)
-  [Function `prove_leader`](#(nexus_workflow=0x0)_network_auth_prove_leader)
-  [Function `prove_offchain_tool`](#(nexus_workflow=0x0)_network_auth_prove_offchain_tool)
-  [Function `proof_identity`](#(nexus_workflow=0x0)_network_auth_proof_identity)
-  [Function `new_proof_of_key`](#(nexus_workflow=0x0)_network_auth_new_proof_of_key)
-  [Function `binding_address`](#(nexus_workflow=0x0)_network_auth_binding_address)
-  [Function `binding_exists`](#(nexus_workflow=0x0)_network_auth_binding_exists)
-  [Function `create_binding`](#(nexus_workflow=0x0)_network_auth_create_binding)
-  [Function `register_key`](#(nexus_workflow=0x0)_network_auth_register_key)
-  [Function `revoke_key`](#(nexus_workflow=0x0)_network_auth_revoke_key)
-  [Function `set_active_key`](#(nexus_workflow=0x0)_network_auth_set_active_key)
-  [Function `key_binding_identity`](#(nexus_workflow=0x0)_network_auth_key_binding_identity)
-  [Function `key_binding_active_key_id`](#(nexus_workflow=0x0)_network_auth_key_binding_active_key_id)
-  [Function `key_binding_next_key_id`](#(nexus_workflow=0x0)_network_auth_key_binding_next_key_id)
-  [Function `key_binding_key`](#(nexus_workflow=0x0)_network_auth_key_binding_key)
-  [Function `assert_identity`](#(nexus_workflow=0x0)_network_auth_assert_identity)
-  [Function `append_bytes`](#(nexus_workflow=0x0)_network_auth_append_bytes)
-  [Function `clone_bytes`](#(nexus_workflow=0x0)_network_auth_clone_bytes)


<pre><code><b>use</b> (nexus_primitives=0x0)::event;
<b>use</b> (nexus_primitives=0x0)::owner_cap;
<b>use</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/leader_cap.md#(nexus_workflow=0x0)_leader_cap">leader_cap</a>;
<b>use</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry">tool_registry</a>;
<b>use</b> <a href="../dependencies/std/address.md#std_address">std::address</a>;
<b>use</b> <a href="../dependencies/std/ascii.md#std_ascii">std::ascii</a>;
<b>use</b> <a href="../dependencies/std/bcs.md#std_bcs">std::bcs</a>;
<b>use</b> <a href="../dependencies/std/option.md#std_option">std::option</a>;
<b>use</b> <a href="../dependencies/std/string.md#std_string">std::string</a>;
<b>use</b> <a href="../dependencies/std/type_name.md#std_type_name">std::type_name</a>;
<b>use</b> <a href="../dependencies/std/vector.md#std_vector">std::vector</a>;
<b>use</b> <a href="../dependencies/sui/accumulator.md#sui_accumulator">sui::accumulator</a>;
<b>use</b> <a href="../dependencies/sui/accumulator_metadata.md#sui_accumulator_metadata">sui::accumulator_metadata</a>;
<b>use</b> <a href="../dependencies/sui/accumulator_settlement.md#sui_accumulator_settlement">sui::accumulator_settlement</a>;
<b>use</b> <a href="../dependencies/sui/address.md#sui_address">sui::address</a>;
<b>use</b> <a href="../dependencies/sui/bag.md#sui_bag">sui::bag</a>;
<b>use</b> <a href="../dependencies/sui/balance.md#sui_balance">sui::balance</a>;
<b>use</b> <a href="../dependencies/sui/bcs.md#sui_bcs">sui::bcs</a>;
<b>use</b> <a href="../dependencies/sui/clock.md#sui_clock">sui::clock</a>;
<b>use</b> <a href="../dependencies/sui/coin.md#sui_coin">sui::coin</a>;
<b>use</b> <a href="../dependencies/sui/config.md#sui_config">sui::config</a>;
<b>use</b> <a href="../dependencies/sui/deny_list.md#sui_deny_list">sui::deny_list</a>;
<b>use</b> <a href="../dependencies/sui/derived_object.md#sui_derived_object">sui::derived_object</a>;
<b>use</b> <a href="../dependencies/sui/dynamic_field.md#sui_dynamic_field">sui::dynamic_field</a>;
<b>use</b> <a href="../dependencies/sui/dynamic_object_field.md#sui_dynamic_object_field">sui::dynamic_object_field</a>;
<b>use</b> <a href="../dependencies/sui/ed25519.md#sui_ed25519">sui::ed25519</a>;
<b>use</b> <a href="../dependencies/sui/event.md#sui_event">sui::event</a>;
<b>use</b> <a href="../dependencies/sui/funds_accumulator.md#sui_funds_accumulator">sui::funds_accumulator</a>;
<b>use</b> <a href="../dependencies/sui/hash.md#sui_hash">sui::hash</a>;
<b>use</b> <a href="../dependencies/sui/hex.md#sui_hex">sui::hex</a>;
<b>use</b> <a href="../dependencies/sui/object.md#sui_object">sui::object</a>;
<b>use</b> <a href="../dependencies/sui/object_bag.md#sui_object_bag">sui::object_bag</a>;
<b>use</b> <a href="../dependencies/sui/party.md#sui_party">sui::party</a>;
<b>use</b> <a href="../dependencies/sui/sui.md#sui_sui">sui::sui</a>;
<b>use</b> <a href="../dependencies/sui/table.md#sui_table">sui::table</a>;
<b>use</b> <a href="../dependencies/sui/transfer.md#sui_transfer">sui::transfer</a>;
<b>use</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context">sui::tx_context</a>;
<b>use</b> <a href="../dependencies/sui/types.md#sui_types">sui::types</a>;
<b>use</b> <a href="../dependencies/sui/url.md#sui_url">sui::url</a>;
<b>use</b> <a href="../dependencies/sui/vec_map.md#sui_vec_map">sui::vec_map</a>;
<b>use</b> <a href="../dependencies/sui/vec_set.md#sui_vec_set">sui::vec_set</a>;
</code></pre>



<a name="(nexus_workflow=0x0)_network_auth_NetworkAuth"></a>

## Struct `NetworkAuth`

Shared registry for identity key bindings.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_NetworkAuth">NetworkAuth</a> <b>has</b> key
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>id: <a href="../dependencies/sui/object.md#sui_object_UID">sui::object::UID</a></code>
</dt>
<dd>
 Object ID of the registry.
</dd>
<dt>
<code>identities: <a href="../dependencies/sui/vec_set.md#sui_vec_set_VecSet">sui::vec_set::VecSet</a>&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_IdentityKey">network_auth::IdentityKey</a>&gt;</code>
</dt>
<dd>
 Discoverable set of identities that have a [KeyBinding].
 This enables indexers/tooling to enumerate which identities have created
 bindings, without needing to guess identities and derived addresses.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_network_auth_KeyBinding"></a>

## Struct `KeyBinding`

Per-identity key binding stored at a deterministic derived address.

This object holds the full key lifecycle state for one identity:
- key registration (with PoP),
- active key selection (the only key verifiers accept),
- revocations (for incident response / decommissioning).


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBinding">KeyBinding</a> <b>has</b> key, store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>id: <a href="../dependencies/sui/object.md#sui_object_UID">sui::object::UID</a></code>
</dt>
<dd>
 Object ID of the binding.
</dd>
<dt>
<code>identity: (nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_IdentityKey">network_auth::IdentityKey</a></code>
</dt>
<dd>
 Identity this binding belongs to.
</dd>
<dt>
<code>description: <a href="../dependencies/std/option.md#std_option_Option">std::option::Option</a>&lt;vector&lt;u8&gt;&gt;</code>
</dt>
<dd>
 Optional description for operators and tooling.
</dd>
<dt>
<code>next_key_id: u64</code>
</dt>
<dd>
 Monotonically increasing key identifier.
 This is used as the key id for the next registration and as the PoP
 nonce to prevent replay of PoP signatures.
</dd>
<dt>
<code>active_key_id: <a href="../dependencies/std/option.md#std_option_Option">std::option::Option</a>&lt;u64&gt;</code>
</dt>
<dd>
 Active key identifier for verification.
 Off-chain verifiers MUST accept signatures from this key only.
 This allows key rotation while keeping verification unambiguous.
</dd>
<dt>
<code>keys: <a href="../dependencies/sui/table.md#sui_table_Table">sui::table::Table</a>&lt;u64, (nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyRecord">network_auth::KeyRecord</a>&gt;</code>
</dt>
<dd>
 Key records indexed by key id.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_network_auth_KeyRecord"></a>

## Struct `KeyRecord`

Single key record stored in a binding.

Keys are append-only (registered under a new <code>key_id</code>) and can be revoked.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyRecord">KeyRecord</a> <b>has</b> store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>scheme: u8</code>
</dt>
<dd>
 Key scheme identifier (Ed25519 only).
</dd>
<dt>
<code>public_key: vector&lt;u8&gt;</code>
</dt>
<dd>
 Raw public key bytes.
</dd>
<dt>
<code>added_at_ms: u64</code>
</dt>
<dd>
 Timestamp when the key was registered.
</dd>
<dt>
<code>revoked_at_ms: <a href="../dependencies/std/option.md#std_option_Option">std::option::Option</a>&lt;u64&gt;</code>
</dt>
<dd>
 Timestamp when the key was revoked, if any.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_network_auth_ProofOfIdentity"></a>

## Struct `ProofOfIdentity`

Ephemeral proof that the caller is authorized to act for an identity.

This prevents unauthorized parties from creating bindings or registering keys
for identities they do not control.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfIdentity">ProofOfIdentity</a> <b>has</b> drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>identity: (nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_IdentityKey">network_auth::IdentityKey</a></code>
</dt>
<dd>
 Identity proven by on-chain capabilities.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_network_auth_ProofOfKey"></a>

## Struct `ProofOfKey`

Ephemeral proof that a key is controlled by the signer.

This proves possession of the private key corresponding to <code>public_key</code>
without revealing it, and is valid only for a single registration slot
(bound to [KeyBinding::next_key_id]).


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfKey">ProofOfKey</a> <b>has</b> drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>scheme: u8</code>
</dt>
<dd>
 Key scheme identifier (Ed25519 only).
</dd>
<dt>
<code>public_key: vector&lt;u8&gt;</code>
</dt>
<dd>
 Public key proven by proof-of-possession.
</dd>
<dt>
<code>key_id: u64</code>
</dt>
<dd>
 Key id this proof is valid for.
 This must match [KeyBinding::next_key_id] when registering the key.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_network_auth_NetworkAuthCreatedEvent"></a>

## Struct `NetworkAuthCreatedEvent`

Emitted when a new network auth registry is created.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_NetworkAuthCreatedEvent">NetworkAuthCreatedEvent</a> <b>has</b> <b>copy</b>, drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>registry: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
 Registry object ID.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_network_auth_KeyBindingCreatedEvent"></a>

## Struct `KeyBindingCreatedEvent`

Emitted when a new key binding is created.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBindingCreatedEvent">KeyBindingCreatedEvent</a> <b>has</b> <b>copy</b>, drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>binding: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
 Binding object ID.
</dd>
<dt>
<code>identity: (nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_IdentityKey">network_auth::IdentityKey</a></code>
</dt>
<dd>
 Identity associated with the binding.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_network_auth_KeyRegisteredEvent"></a>

## Struct `KeyRegisteredEvent`

Emitted when a key is registered.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyRegisteredEvent">KeyRegisteredEvent</a> <b>has</b> <b>copy</b>, drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>binding: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
 Binding object ID.
</dd>
<dt>
<code>key_id: u64</code>
</dt>
<dd>
 Registered key identifier.
</dd>
<dt>
<code>scheme: u8</code>
</dt>
<dd>
 Key scheme identifier.
</dd>
<dt>
<code>public_key: vector&lt;u8&gt;</code>
</dt>
<dd>
 Public key bytes.
</dd>
<dt>
<code>added_at_ms: u64</code>
</dt>
<dd>
 Timestamp when the key was registered.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_network_auth_KeyRevokedEvent"></a>

## Struct `KeyRevokedEvent`

Emitted when a key is revoked.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyRevokedEvent">KeyRevokedEvent</a> <b>has</b> <b>copy</b>, drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>binding: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
 Binding object ID.
</dd>
<dt>
<code>key_id: u64</code>
</dt>
<dd>
 Revoked key identifier.
</dd>
<dt>
<code>revoked_at_ms: u64</code>
</dt>
<dd>
 Timestamp when the key was revoked.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_network_auth_ActiveKeyUpdatedEvent"></a>

## Struct `ActiveKeyUpdatedEvent`

Emitted when the active key changes.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ActiveKeyUpdatedEvent">ActiveKeyUpdatedEvent</a> <b>has</b> <b>copy</b>, drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>binding: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
 Binding object ID.
</dd>
<dt>
<code>active_key_id: <a href="../dependencies/std/option.md#std_option_Option">std::option::Option</a>&lt;u64&gt;</code>
</dt>
<dd>
 New active key identifier, or none if cleared.
</dd>
</dl>


</details>

<a name="(nexus_workflow=0x0)_network_auth_IdentityKey"></a>

## Enum `IdentityKey`

Canonical identity key namespace for key bindings.

This value is used as:
- the key for the derived [KeyBinding] address, and
- the identity commitment inside PoP signatures (via <code>bcs(<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_IdentityKey">IdentityKey</a>)</code>).


<pre><code><b>public</b> <b>enum</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_IdentityKey">IdentityKey</a> <b>has</b> <b>copy</b>, drop, store
</code></pre>



<details>
<summary>Variants</summary>


<dl>
<dt>
Variant <code>Leader</code>
</dt>
<dd>
 Leader identity keyed by address.
</dd>

<dl>
<dt>
<code><b>address</b>: <b>address</b></code>
</dt>
<dd>
 Leader address.
</dd>
</dl>

<dt>
Variant <code>Tool</code>
</dt>
<dd>
 Tool identity keyed by FQN.
</dd>

<dl>
<dt>
<code>fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a></code>
</dt>
<dd>
 Fully qualified tool name.
</dd>
</dl>

</dl>


</details>

<a name="@Constants_0"></a>

## Constants


<a name="(nexus_workflow=0x0)_network_auth_KEY_SCHEME_ED25519"></a>

Identifier for Ed25519 keys.


<pre><code><b>const</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KEY_SCHEME_ED25519">KEY_SCHEME_ED25519</a>: u8 = 0;
</code></pre>



<a name="(nexus_workflow=0x0)_network_auth_ED25519_PUBLIC_KEY_LEN"></a>

Required byte length of an Ed25519 public key.


<pre><code><b>const</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ED25519_PUBLIC_KEY_LEN">ED25519_PUBLIC_KEY_LEN</a>: u64 = 32;
</code></pre>



<a name="(nexus_workflow=0x0)_network_auth_ED25519_SIGNATURE_LEN"></a>

Required byte length of an Ed25519 signature.


<pre><code><b>const</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ED25519_SIGNATURE_LEN">ED25519_SIGNATURE_LEN</a>: u64 = 64;
</code></pre>



<a name="(nexus_workflow=0x0)_network_auth_POP_DOMAIN"></a>

Default domain separator for proof-of-possession.


<pre><code><b>const</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_POP_DOMAIN">POP_DOMAIN</a>: vector&lt;u8&gt; = vector[110, 101, 120, 117, 115, 95, 119, 111, 114, 107, 102, 108, 111, 119, 46, 110, 101, 116, 119, 111, 114, 107, 95, 97, 117, 116, 104, 46, 112, 111, 112, 95, 118, 49];
</code></pre>



<a name="(nexus_workflow=0x0)_network_auth_EUnsupportedKeyScheme"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_EUnsupportedKeyScheme">EUnsupportedKeyScheme</a>: vector&lt;u8&gt; = b"Only Ed25519 keys are supported";
</code></pre>



<a name="(nexus_workflow=0x0)_network_auth_EInvalidPublicKey"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_EInvalidPublicKey">EInvalidPublicKey</a>: vector&lt;u8&gt; = b"Invalid Ed25519 <b>public</b> key length";
</code></pre>



<a name="(nexus_workflow=0x0)_network_auth_EInvalidSignature"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_EInvalidSignature">EInvalidSignature</a>: vector&lt;u8&gt; = b"Invalid Ed25519 signature length";
</code></pre>



<a name="(nexus_workflow=0x0)_network_auth_EInvalidProofOfPossession"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_EInvalidProofOfPossession">EInvalidProofOfPossession</a>: vector&lt;u8&gt; = b"Invalid proof of possession";
</code></pre>



<a name="(nexus_workflow=0x0)_network_auth_EBindingAlreadyExists"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_EBindingAlreadyExists">EBindingAlreadyExists</a>: vector&lt;u8&gt; = b"Key binding already exists";
</code></pre>



<a name="(nexus_workflow=0x0)_network_auth_EIdentityMismatch"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_EIdentityMismatch">EIdentityMismatch</a>: vector&lt;u8&gt; = b"Proof identity does not match key binding";
</code></pre>



<a name="(nexus_workflow=0x0)_network_auth_EKeyNotFound"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_EKeyNotFound">EKeyNotFound</a>: vector&lt;u8&gt; = b"Key not found";
</code></pre>



<a name="(nexus_workflow=0x0)_network_auth_EKeyAlreadyRevoked"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_EKeyAlreadyRevoked">EKeyAlreadyRevoked</a>: vector&lt;u8&gt; = b"Key already revoked";
</code></pre>



<a name="(nexus_workflow=0x0)_network_auth_EKeyIdMismatch"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_EKeyIdMismatch">EKeyIdMismatch</a>: vector&lt;u8&gt; = b"Proof key id does not match binding slot";
</code></pre>



<a name="(nexus_workflow=0x0)_network_auth_new"></a>

## Function `new`

Create a new registry with the empty identity set.


<pre><code><b>public</b>(package) <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_new">new</a>(ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_NetworkAuth">network_auth::NetworkAuth</a>
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b>(package) <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_new">new</a>(ctx: &<b>mut</b> TxContext): <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_NetworkAuth">NetworkAuth</a> {
    <b>let</b> registry = <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_NetworkAuth">NetworkAuth</a> {
        id: object::new(ctx),
        identities: vec_set::empty(),
    };
    event::emit(<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_NetworkAuthCreatedEvent">NetworkAuthCreatedEvent</a> {
        registry: object::id(&registry),
    });
    registry
}
</code></pre>



</details>

<a name="(nexus_workflow=0x0)_network_auth_share"></a>

## Function `share`

Share the registry as a shared object.


<pre><code><b>public</b>(package) <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_share">share</a>(self: (nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_NetworkAuth">network_auth::NetworkAuth</a>)
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b>(package) <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_share">share</a>(self: <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_NetworkAuth">NetworkAuth</a>) {
    share_object(self);
}
</code></pre>



</details>

<a name="(nexus_workflow=0x0)_network_auth_prove_leader"></a>

## Function `prove_leader`

Create proof for the leader (sender) using its leader capability.

The leader capability serves as the on-chain authorization to act as a
Leader identity and register/rotate keys for <code>IdentityKey::Leader { <b>address</b>:
ctx.sender() }</code>.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_prove_leader">prove_leader</a>(_leader_cap: &(nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/leader_cap.md#(nexus_workflow=0x0)_leader_cap_OverNetwork">leader_cap::OverNetwork</a>&gt;, ctx: &<a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfIdentity">network_auth::ProofOfIdentity</a>
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_prove_leader">prove_leader</a>(
    _leader_cap: &CloneableOwnerCap&lt;OverNetwork&gt;,
    ctx: &TxContext,
): <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfIdentity">ProofOfIdentity</a> {
    <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfIdentity">ProofOfIdentity</a> {
        identity: IdentityKey::Leader {
            <b>address</b>: ctx.sender(),
        }
    }
}
</code></pre>



</details>

<a name="(nexus_workflow=0x0)_network_auth_prove_offchain_tool"></a>

## Function `prove_offchain_tool`

Create proof for an off-chain tool using its owner cap.

This uses the off-chain tool registry and expects an off-chain tool FQN.
The owner cap is validated against the registry to bind the tool identity.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_prove_offchain_tool">prove_offchain_tool</a>(registry: &(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_ToolRegistry">tool_registry::ToolRegistry</a>, owner_cap: &(nexus_primitives=0x0)::owner_cap::CloneableOwnerCap&lt;(nexus_workflow=0x0)::<a href="../nexus_workflow/tool_registry.md#(nexus_workflow=0x0)_tool_registry_OverTool">tool_registry::OverTool</a>&gt;, fqn: <a href="../dependencies/std/ascii.md#std_ascii_String">std::ascii::String</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfIdentity">network_auth::ProofOfIdentity</a>
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_prove_offchain_tool">prove_offchain_tool</a>(
    registry: &ToolRegistry,
    owner_cap: &CloneableOwnerCap&lt;OverTool&gt;,
    fqn: AsciiString,
): <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfIdentity">ProofOfIdentity</a> {
    registry.assert_tool_owner(owner_cap, fqn);
    <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfIdentity">ProofOfIdentity</a> {
        identity: IdentityKey::Tool {
            fqn,
        }
    }
}
</code></pre>



</details>

<a name="(nexus_workflow=0x0)_network_auth_proof_identity"></a>

## Function `proof_identity`

Return the identity proven by the proof.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_proof_identity">proof_identity</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfIdentity">network_auth::ProofOfIdentity</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_IdentityKey">network_auth::IdentityKey</a>
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_proof_identity">proof_identity</a>(self: &<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfIdentity">ProofOfIdentity</a>): <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_IdentityKey">IdentityKey</a> {
    self.identity
}
</code></pre>



</details>

<a name="(nexus_workflow=0x0)_network_auth_new_proof_of_key"></a>

## Function `new_proof_of_key`

Create proof-of-possession for registering the given public key.
Only Ed25519 keys are supported.

The signature must verify over
<code><a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_POP_DOMAIN">POP_DOMAIN</a> || bcs(<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_IdentityKey">IdentityKey</a>) || bcs(key_id) || public_key</code>
using the same public key, proving control of the private key for this
specific identity and key-id slot.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_new_proof_of_key">new_proof_of_key</a>(binding: &(nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBinding">network_auth::KeyBinding</a>, identity: &(nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfIdentity">network_auth::ProofOfIdentity</a>, public_key: vector&lt;u8&gt;, signature: vector&lt;u8&gt;): (nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfKey">network_auth::ProofOfKey</a>
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_new_proof_of_key">new_proof_of_key</a>(
    binding: &<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBinding">KeyBinding</a>,
    identity: &<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfIdentity">ProofOfIdentity</a>,
    public_key: vector&lt;u8&gt;,
    signature: vector&lt;u8&gt;,
): <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfKey">ProofOfKey</a> {
    <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_assert_identity">assert_identity</a>(binding, identity);
    <b>assert</b>!(public_key.length() == <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ED25519_PUBLIC_KEY_LEN">ED25519_PUBLIC_KEY_LEN</a>, <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_EInvalidPublicKey">EInvalidPublicKey</a>);
    <b>assert</b>!(signature.length() == <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ED25519_SIGNATURE_LEN">ED25519_SIGNATURE_LEN</a>, <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_EInvalidSignature">EInvalidSignature</a>);
    <b>let</b> <b>mut</b> msg = <b>copy</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_POP_DOMAIN">POP_DOMAIN</a>;
    <b>let</b> identity_bytes = bcs::to_bytes(&identity.identity);
    <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_append_bytes">append_bytes</a>(&<b>mut</b> msg, &identity_bytes);
    <b>let</b> key_id = binding.next_key_id;
    <b>let</b> key_id_bytes = bcs::to_bytes(&key_id);
    <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_append_bytes">append_bytes</a>(&<b>mut</b> msg, &key_id_bytes);
    <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_append_bytes">append_bytes</a>(&<b>mut</b> msg, &public_key);
    <b>assert</b>!(
        ed25519::ed25519_verify(&signature, &public_key, &msg),
        <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_EInvalidProofOfPossession">EInvalidProofOfPossession</a>
    );
    <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfKey">ProofOfKey</a> {
        scheme: <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KEY_SCHEME_ED25519">KEY_SCHEME_ED25519</a>,
        public_key,
        key_id,
    }
}
</code></pre>



</details>

<a name="(nexus_workflow=0x0)_network_auth_binding_address"></a>

## Function `binding_address`

Deterministic derived address for the key binding.

Uses the registry object ID and the identity as the derivation key.

This allows any caller to deterministically compute where the [KeyBinding]
for an identity lives on-chain.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_binding_address">binding_address</a>(registry: &(nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_NetworkAuth">network_auth::NetworkAuth</a>, identity: (nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_IdentityKey">network_auth::IdentityKey</a>): <b>address</b>
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_binding_address">binding_address</a>(registry: &<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_NetworkAuth">NetworkAuth</a>, identity: <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_IdentityKey">IdentityKey</a>): <b>address</b> {
    derived_object::derive_address(object::id(registry), identity)
}
</code></pre>



</details>

<a name="(nexus_workflow=0x0)_network_auth_binding_exists"></a>

## Function `binding_exists`

Check whether a binding has been created for the given identity.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_binding_exists">binding_exists</a>(registry: &(nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_NetworkAuth">network_auth::NetworkAuth</a>, identity: (nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_IdentityKey">network_auth::IdentityKey</a>): bool
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_binding_exists">binding_exists</a>(registry: &<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_NetworkAuth">NetworkAuth</a>, identity: <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_IdentityKey">IdentityKey</a>): bool {
    derived_object::exists(&registry.id, identity)
}
</code></pre>



</details>

<a name="(nexus_workflow=0x0)_network_auth_create_binding"></a>

## Function `create_binding`

Create a new key binding for the given identity.

This claims the derived object ID, initializes the binding state, and
inserts the identity into the registry's discovery set.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_create_binding">create_binding</a>(registry: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_NetworkAuth">network_auth::NetworkAuth</a>, identity: (nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfIdentity">network_auth::ProofOfIdentity</a>, description: <a href="../dependencies/std/option.md#std_option_Option">std::option::Option</a>&lt;vector&lt;u8&gt;&gt;, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBinding">network_auth::KeyBinding</a>
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_create_binding">create_binding</a>(
    registry: &<b>mut</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_NetworkAuth">NetworkAuth</a>,
    identity: <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfIdentity">ProofOfIdentity</a>,
    description: Option&lt;vector&lt;u8&gt;&gt;,
    ctx: &<b>mut</b> TxContext,
): <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBinding">KeyBinding</a> {
    <b>let</b> identity_key = identity.identity;
    <b>assert</b>!(!derived_object::exists(&registry.id, identity_key), <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_EBindingAlreadyExists">EBindingAlreadyExists</a>);
    <b>let</b> binding_id = derived_object::claim(&<b>mut</b> registry.id, identity_key);
    <b>let</b> binding = <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBinding">KeyBinding</a> {
        id: binding_id,
        identity: identity_key,
        description,
        next_key_id: 0,
        active_key_id: option::none(),
        keys: table::new(ctx),
    };
    registry.identities.insert(identity_key);
    event::emit(<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBindingCreatedEvent">KeyBindingCreatedEvent</a> {
        binding: object::id(&binding),
        identity: identity_key,
    });
    binding
}
</code></pre>



</details>

<a name="(nexus_workflow=0x0)_network_auth_register_key"></a>

## Function `register_key`

Register a new key and set it as active.

This assigns a monotonically increasing key id, stores the key record, and
updates the active key pointer.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_register_key">register_key</a>(binding: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBinding">network_auth::KeyBinding</a>, identity: &(nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfIdentity">network_auth::ProofOfIdentity</a>, proof_of_key: (nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfKey">network_auth::ProofOfKey</a>, clock: &<a href="../dependencies/sui/clock.md#sui_clock_Clock">sui::clock::Clock</a>)
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_register_key">register_key</a>(
    binding: &<b>mut</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBinding">KeyBinding</a>,
    identity: &<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfIdentity">ProofOfIdentity</a>,
    proof_of_key: <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfKey">ProofOfKey</a>,
    clock: &Clock,
) {
    <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_assert_identity">assert_identity</a>(binding, identity);
    <b>assert</b>!(proof_of_key.scheme == <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KEY_SCHEME_ED25519">KEY_SCHEME_ED25519</a>, <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_EUnsupportedKeyScheme">EUnsupportedKeyScheme</a>);
    // PoP is one-time-<b>use</b> <b>for</b> the current slot.
    <b>assert</b>!(proof_of_key.key_id == binding.next_key_id, <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_EKeyIdMismatch">EKeyIdMismatch</a>);
    <b>let</b> key_id = binding.next_key_id;
    binding.next_key_id = key_id + 1;
    <b>let</b> added_at_ms = clock.timestamp_ms();
    <b>let</b> public_key_copy = <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_clone_bytes">clone_bytes</a>(&proof_of_key.public_key);
    binding.keys.add(key_id, <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyRecord">KeyRecord</a> {
        scheme: proof_of_key.scheme,
        public_key: proof_of_key.public_key,
        added_at_ms,
        revoked_at_ms: option::none(),
    });
    binding.active_key_id = option::some(key_id);
    event::emit(<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyRegisteredEvent">KeyRegisteredEvent</a> {
        binding: object::id(binding),
        key_id,
        scheme: <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KEY_SCHEME_ED25519">KEY_SCHEME_ED25519</a>,
        public_key: public_key_copy,
        added_at_ms,
    });
    event::emit(<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ActiveKeyUpdatedEvent">ActiveKeyUpdatedEvent</a> {
        binding: object::id(binding),
        active_key_id: option::some(key_id),
    });
}
</code></pre>



</details>

<a name="(nexus_workflow=0x0)_network_auth_revoke_key"></a>

## Function `revoke_key`

Revoke an existing key.

This sets the revocation timestamp and clears the active key if needed.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_revoke_key">revoke_key</a>(binding: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBinding">network_auth::KeyBinding</a>, identity: &(nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfIdentity">network_auth::ProofOfIdentity</a>, key_id: u64, clock: &<a href="../dependencies/sui/clock.md#sui_clock_Clock">sui::clock::Clock</a>)
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_revoke_key">revoke_key</a>(
    binding: &<b>mut</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBinding">KeyBinding</a>,
    identity: &<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfIdentity">ProofOfIdentity</a>,
    key_id: u64,
    clock: &Clock,
) {
    <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_assert_identity">assert_identity</a>(binding, identity);
    <b>assert</b>!(binding.keys.contains(key_id), <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_EKeyNotFound">EKeyNotFound</a>);
    <b>let</b> record = binding.keys.borrow_mut(key_id);
    <b>assert</b>!(record.revoked_at_ms.is_none(), <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_EKeyAlreadyRevoked">EKeyAlreadyRevoked</a>);
    <b>let</b> revoked_at_ms = clock.timestamp_ms();
    record.revoked_at_ms = option::some(revoked_at_ms);
    <b>if</b> (binding.active_key_id == option::some(key_id)) {
        binding.active_key_id = option::none();
        event::emit(<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ActiveKeyUpdatedEvent">ActiveKeyUpdatedEvent</a> {
            binding: object::id(binding),
            active_key_id: option::none(),
        });
    };
    event::emit(<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyRevokedEvent">KeyRevokedEvent</a> {
        binding: object::id(binding),
        key_id,
        revoked_at_ms,
    });
}
</code></pre>



</details>

<a name="(nexus_workflow=0x0)_network_auth_set_active_key"></a>

## Function `set_active_key`

Set the active key to an existing, non-revoked key.

This switches the active key pointer without altering key records.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_set_active_key">set_active_key</a>(binding: &<b>mut</b> (nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBinding">network_auth::KeyBinding</a>, identity: &(nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfIdentity">network_auth::ProofOfIdentity</a>, key_id: u64)
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_set_active_key">set_active_key</a>(
    binding: &<b>mut</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBinding">KeyBinding</a>,
    identity: &<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfIdentity">ProofOfIdentity</a>,
    key_id: u64,
) {
    <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_assert_identity">assert_identity</a>(binding, identity);
    <b>assert</b>!(binding.keys.contains(key_id), <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_EKeyNotFound">EKeyNotFound</a>);
    <b>let</b> record = binding.keys.borrow(key_id);
    <b>assert</b>!(record.revoked_at_ms.is_none(), <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_EKeyAlreadyRevoked">EKeyAlreadyRevoked</a>);
    binding.active_key_id = option::some(key_id);
    event::emit(<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ActiveKeyUpdatedEvent">ActiveKeyUpdatedEvent</a> {
        binding: object::id(binding),
        active_key_id: option::some(key_id),
    });
}
</code></pre>



</details>

<a name="(nexus_workflow=0x0)_network_auth_key_binding_identity"></a>

## Function `key_binding_identity`

Return the identity associated with a key binding.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_key_binding_identity">key_binding_identity</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBinding">network_auth::KeyBinding</a>): (nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_IdentityKey">network_auth::IdentityKey</a>
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_key_binding_identity">key_binding_identity</a>(self: &<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBinding">KeyBinding</a>): <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_IdentityKey">IdentityKey</a> { self.identity }
</code></pre>



</details>

<a name="(nexus_workflow=0x0)_network_auth_key_binding_active_key_id"></a>

## Function `key_binding_active_key_id`

Return the active key id for a binding.

Off-chain verifiers must accept signatures from this key only.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_key_binding_active_key_id">key_binding_active_key_id</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBinding">network_auth::KeyBinding</a>): <a href="../dependencies/std/option.md#std_option_Option">std::option::Option</a>&lt;u64&gt;
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_key_binding_active_key_id">key_binding_active_key_id</a>(self: &<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBinding">KeyBinding</a>): Option&lt;u64&gt; { self.active_key_id }
</code></pre>



</details>

<a name="(nexus_workflow=0x0)_network_auth_key_binding_next_key_id"></a>

## Function `key_binding_next_key_id`

Return the next key id that will be assigned on registration.

This value is also committed into PoP signatures to make them one-time-use.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_key_binding_next_key_id">key_binding_next_key_id</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBinding">network_auth::KeyBinding</a>): u64
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_key_binding_next_key_id">key_binding_next_key_id</a>(self: &<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBinding">KeyBinding</a>): u64 { self.next_key_id }
</code></pre>



</details>

<a name="(nexus_workflow=0x0)_network_auth_key_binding_key"></a>

## Function `key_binding_key`

Borrow a key record by id.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_key_binding_key">key_binding_key</a>(self: &(nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBinding">network_auth::KeyBinding</a>, key_id: u64): &(nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyRecord">network_auth::KeyRecord</a>
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_key_binding_key">key_binding_key</a>(self: &<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBinding">KeyBinding</a>, key_id: u64): &<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyRecord">KeyRecord</a> {
    &self.keys[key_id]
}
</code></pre>



</details>

<a name="(nexus_workflow=0x0)_network_auth_assert_identity"></a>

## Function `assert_identity`

Ensure the proof identity matches the binding identity.


<pre><code><b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_assert_identity">assert_identity</a>(binding: &(nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBinding">network_auth::KeyBinding</a>, identity: &(nexus_workflow=0x0)::<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfIdentity">network_auth::ProofOfIdentity</a>)
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_assert_identity">assert_identity</a>(binding: &<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_KeyBinding">KeyBinding</a>, identity: &<a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_ProofOfIdentity">ProofOfIdentity</a>) {
    <b>assert</b>!(binding.identity == identity.identity, <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_EIdentityMismatch">EIdentityMismatch</a>);
}
</code></pre>



</details>

<a name="(nexus_workflow=0x0)_network_auth_append_bytes"></a>

## Function `append_bytes`

Append bytes to a vector without reallocating intermediate vectors.


<pre><code><b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_append_bytes">append_bytes</a>(out: &<b>mut</b> vector&lt;u8&gt;, bytes: &vector&lt;u8&gt;)
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_append_bytes">append_bytes</a>(out: &<b>mut</b> vector&lt;u8&gt;, bytes: &vector&lt;u8&gt;) {
    <b>let</b> <b>mut</b> i = 0;
    <b>while</b> (i &lt; bytes.length()) {
        out.push_back(bytes[i]);
        i = i + 1;
    };
}
</code></pre>



</details>

<a name="(nexus_workflow=0x0)_network_auth_clone_bytes"></a>

## Function `clone_bytes`

Clone bytes into a new vector.


<pre><code><b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_clone_bytes">clone_bytes</a>(bytes: &vector&lt;u8&gt;): vector&lt;u8&gt;
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>fun</b> <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_clone_bytes">clone_bytes</a>(bytes: &vector&lt;u8&gt;): vector&lt;u8&gt; {
    <b>let</b> <b>mut</b> out = vector[];
    <a href="../nexus_workflow/network_auth.md#(nexus_workflow=0x0)_network_auth_append_bytes">append_bytes</a>(&<b>mut</b> out, bytes);
    out
}
</code></pre>



</details>
