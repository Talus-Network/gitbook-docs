
<a name="nexus_primitives_proof_of_uid"></a>

# Module `nexus_primitives::proof_of_uid`



-  [Struct `ProofOfUID`](#nexus_primitives_proof_of_uid_ProofOfUID)
-  [Function `new`](#nexus_primitives_proof_of_uid_new)
-  [Function `new_with_type`](#nexus_primitives_proof_of_uid_new_with_type)
-  [Function `consume`](#nexus_primitives_proof_of_uid_consume)
-  [Function `stamp_with_data`](#nexus_primitives_proof_of_uid_stamp_with_data)
-  [Function `stamp`](#nexus_primitives_proof_of_uid_stamp)
-  [Function `unstamp`](#nexus_primitives_proof_of_uid_unstamp)
-  [Function `stamps`](#nexus_primitives_proof_of_uid_stamps)
-  [Function `stamps_len`](#nexus_primitives_proof_of_uid_stamps_len)
-  [Function `has_stamp`](#nexus_primitives_proof_of_uid_has_stamp)
-  [Function `created_from`](#nexus_primitives_proof_of_uid_created_from)
-  [Function `type_name`](#nexus_primitives_proof_of_uid_type_name)


<pre><code><b>use</b> <a href="../dependencies/std/address.md#std_address">std::address</a>;
<b>use</b> <a href="../dependencies/std/ascii.md#std_ascii">std::ascii</a>;
<b>use</b> <a href="../dependencies/std/bcs.md#std_bcs">std::bcs</a>;
<b>use</b> <a href="../dependencies/std/option.md#std_option">std::option</a>;
<b>use</b> <a href="../dependencies/std/string.md#std_string">std::string</a>;
<b>use</b> <a href="../dependencies/std/type_name.md#std_type_name">std::type_name</a>;
<b>use</b> <a href="../dependencies/std/vector.md#std_vector">std::vector</a>;
<b>use</b> <a href="../dependencies/sui/address.md#sui_address">sui::address</a>;
<b>use</b> <a href="../dependencies/sui/hex.md#sui_hex">sui::hex</a>;
<b>use</b> <a href="../dependencies/sui/object.md#sui_object">sui::object</a>;
<b>use</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context">sui::tx_context</a>;
<b>use</b> <a href="../dependencies/sui/vec_map.md#sui_vec_map">sui::vec_map</a>;
</code></pre>



<a name="nexus_primitives_proof_of_uid_ProofOfUID"></a>

## Struct `ProofOfUID`

Hot potato that can collect stamps.

If [ProofOfUID] contains an [ID] stamp it means that the corresponding [UID]
has been referenced in [stamp] method.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">ProofOfUID</a>
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>from_uid: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
 Only the [UID] that created this proof in [new] constructor can consume it.
</dd>
<dt>
<code>from_type: <a href="../dependencies/std/option.md#std_option_Option">std::option::Option</a>&lt;<a href="../dependencies/std/type_name.md#std_type_name_TypeName">std::type_name::TypeName</a>&gt;</code>
</dt>
<dd>
 Optionally, the creator of the proof can also prove the type of the [UID].
 Some nexus components may require this information to be present.
</dd>
<dt>
<code><a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_stamps">stamps</a>: <a href="../dependencies/sui/vec_map.md#sui_vec_map_VecMap">sui::vec_map::VecMap</a>&lt;<a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a>, vector&lt;u8&gt;&gt;</code>
</dt>
<dd>
 Stampers can attach arbitrary data to their stamp.
</dd>
</dl>


</details>

<a name="nexus_primitives_proof_of_uid_new"></a>

## Function `new`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_new">new</a>(uid: &<a href="../dependencies/sui/object.md#sui_object_UID">sui::object::UID</a>): <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">nexus_primitives::proof_of_uid::ProofOfUID</a>
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_new">new</a>(uid: &UID): <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">ProofOfUID</a> {
    <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">ProofOfUID</a> {
        from_uid: object::uid_to_inner(uid),
        from_type: option::none(),
        <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_stamps">stamps</a>: vec_map::empty()
    }
}
</code></pre>



</details>

<a name="nexus_primitives_proof_of_uid_new_with_type"></a>

## Function `new_with_type`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_new_with_type">new_with_type</a>&lt;T: key&gt;(uid: &<a href="../dependencies/sui/object.md#sui_object_UID">sui::object::UID</a>, o: &T): <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">nexus_primitives::proof_of_uid::ProofOfUID</a>
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_new_with_type">new_with_type</a>&lt;T: key&gt;(uid: &UID, o: &T): <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">ProofOfUID</a> {
    <b>assert</b>!(object::uid_to_inner(uid) == object::id(o));
    <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">ProofOfUID</a> {
        from_uid: object::uid_to_inner(uid),
        from_type: option::some(type_name::get&lt;T&gt;()),
        <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_stamps">stamps</a>: vec_map::empty()
    }
}
</code></pre>



</details>

<a name="nexus_primitives_proof_of_uid_consume"></a>

## Function `consume`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_consume">consume</a>(self: <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">nexus_primitives::proof_of_uid::ProofOfUID</a>, uid: &<a href="../dependencies/sui/object.md#sui_object_UID">sui::object::UID</a>): <a href="../dependencies/sui/vec_map.md#sui_vec_map_VecMap">sui::vec_map::VecMap</a>&lt;<a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a>, vector&lt;u8&gt;&gt;
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_consume">consume</a>(self: <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">ProofOfUID</a>, uid: &UID): VecMap&lt;ID, vector&lt;u8&gt;&gt; {
    <b>let</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">ProofOfUID</a> { <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_stamps">stamps</a>, from_uid, .. } = self;
    <b>assert</b>!(object::uid_to_inner(uid) == from_uid);
    <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_stamps">stamps</a>
}
</code></pre>



</details>

<a name="nexus_primitives_proof_of_uid_stamp_with_data"></a>

## Function `stamp_with_data`

Add a stamp to the proof with some data.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_stamp_with_data">stamp_with_data</a>(self: &<b>mut</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">nexus_primitives::proof_of_uid::ProofOfUID</a>, uid: &<a href="../dependencies/sui/object.md#sui_object_UID">sui::object::UID</a>, <a href="../nexus_primitives/data.md#nexus_primitives_data">data</a>: vector&lt;u8&gt;)
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_stamp_with_data">stamp_with_data</a>(self: &<b>mut</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">ProofOfUID</a>, uid: &UID, <a href="../nexus_primitives/data.md#nexus_primitives_data">data</a>: vector&lt;u8&gt;) {
    self.<a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_stamps">stamps</a>.insert(object::uid_to_inner(uid), <a href="../nexus_primitives/data.md#nexus_primitives_data">data</a>)
}
</code></pre>



</details>

<a name="nexus_primitives_proof_of_uid_stamp"></a>

## Function `stamp`

Add a stamp to the proof.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_stamp">stamp</a>(self: &<b>mut</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">nexus_primitives::proof_of_uid::ProofOfUID</a>, uid: &<a href="../dependencies/sui/object.md#sui_object_UID">sui::object::UID</a>)
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_stamp">stamp</a>(self: &<b>mut</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">ProofOfUID</a>, uid: &UID) {
    self.<a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_stamp_with_data">stamp_with_data</a>(uid, vector::empty())
}
</code></pre>



</details>

<a name="nexus_primitives_proof_of_uid_unstamp"></a>

## Function `unstamp`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_unstamp">unstamp</a>(self: &<b>mut</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">nexus_primitives::proof_of_uid::ProofOfUID</a>, uid: &<a href="../dependencies/sui/object.md#sui_object_UID">sui::object::UID</a>)
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_unstamp">unstamp</a>(self: &<b>mut</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">ProofOfUID</a>, uid: &UID) {
    self.<a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_stamps">stamps</a>.remove(&object::uid_to_inner(uid));
}
</code></pre>



</details>

<a name="nexus_primitives_proof_of_uid_stamps"></a>

## Function `stamps`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_stamps">stamps</a>(self: &<a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">nexus_primitives::proof_of_uid::ProofOfUID</a>): &<a href="../dependencies/sui/vec_map.md#sui_vec_map_VecMap">sui::vec_map::VecMap</a>&lt;<a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a>, vector&lt;u8&gt;&gt;
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_stamps">stamps</a>(self: &<a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">ProofOfUID</a>): &VecMap&lt;ID, vector&lt;u8&gt;&gt; { &self.<a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_stamps">stamps</a> }
</code></pre>



</details>

<a name="nexus_primitives_proof_of_uid_stamps_len"></a>

## Function `stamps_len`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_stamps_len">stamps_len</a>(self: &<a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">nexus_primitives::proof_of_uid::ProofOfUID</a>): u64
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_stamps_len">stamps_len</a>(self: &<a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">ProofOfUID</a>): u64 { self.<a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_stamps">stamps</a>.size() }
</code></pre>



</details>

<a name="nexus_primitives_proof_of_uid_has_stamp"></a>

## Function `has_stamp`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_has_stamp">has_stamp</a>(self: &<a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">nexus_primitives::proof_of_uid::ProofOfUID</a>, of_uid: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a>): bool
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_has_stamp">has_stamp</a>(self: &<a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">ProofOfUID</a>, of_uid: ID): bool { self.<a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_stamps">stamps</a>.contains(&of_uid) }
</code></pre>



</details>

<a name="nexus_primitives_proof_of_uid_created_from"></a>

## Function `created_from`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_created_from">created_from</a>(self: &<a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">nexus_primitives::proof_of_uid::ProofOfUID</a>): <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a>
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_created_from">created_from</a>(self: &<a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">ProofOfUID</a>): ID { self.from_uid }
</code></pre>



</details>

<a name="nexus_primitives_proof_of_uid_type_name"></a>

## Function `type_name`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_type_name">type_name</a>(self: &<a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">nexus_primitives::proof_of_uid::ProofOfUID</a>): <a href="../dependencies/std/option.md#std_option_Option">std::option::Option</a>&lt;<a href="../dependencies/std/type_name.md#std_type_name_TypeName">std::type_name::TypeName</a>&gt;
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_type_name">type_name</a>(self: &<a href="../nexus_primitives/proof_of_uid.md#nexus_primitives_proof_of_uid_ProofOfUID">ProofOfUID</a>): Option&lt;TypeName&gt; { self.from_type }
</code></pre>



</details>
