
<a name="nexus_primitives_owner_cap"></a>

# Module `nexus_primitives::owner_cap`



-  [Struct `CloneableOwnerCap`](#nexus_primitives_owner_cap_CloneableOwnerCap)
    -  [Important](#@Important_0)
-  [Struct `OwnerCap`](#nexus_primitives_owner_cap_OwnerCap)
    -  [Important](#@Important_1)
-  [Constants](#@Constants_2)
-  [Function `new_uncloneable`](#nexus_primitives_owner_cap_new_uncloneable)
-  [Function `new_cloneable_drop`](#nexus_primitives_owner_cap_new_cloneable_drop)
-  [Function `new_cloneable_key`](#nexus_primitives_owner_cap_new_cloneable_key)
-  [Function `clone`](#nexus_primitives_owner_cap_clone)
-  [Function `clone_n`](#nexus_primitives_owner_cap_clone_n)
-  [Function `clone_for_receiver`](#nexus_primitives_owner_cap_clone_for_receiver)
-  [Function `destroy`](#nexus_primitives_owner_cap_destroy)
-  [Function `id`](#nexus_primitives_owner_cap_id)
-  [Function `what_for`](#nexus_primitives_owner_cap_what_for)
-  [Function `is_for`](#nexus_primitives_owner_cap_is_for)
-  [Function `is_for_id`](#nexus_primitives_owner_cap_is_for_id)
-  [Function `as_ref`](#nexus_primitives_owner_cap_as_ref)


<pre><code><b>use</b> <a href="../dependencies/std/ascii.md#std_ascii">std::ascii</a>;
<b>use</b> <a href="../dependencies/std/bcs.md#std_bcs">std::bcs</a>;
<b>use</b> <a href="../dependencies/std/option.md#std_option">std::option</a>;
<b>use</b> <a href="../dependencies/std/string.md#std_string">std::string</a>;
<b>use</b> <a href="../dependencies/std/vector.md#std_vector">std::vector</a>;
<b>use</b> <a href="../dependencies/sui/address.md#sui_address">sui::address</a>;
<b>use</b> <a href="../dependencies/sui/hex.md#sui_hex">sui::hex</a>;
<b>use</b> <a href="../dependencies/sui/object.md#sui_object">sui::object</a>;
<b>use</b> <a href="../dependencies/sui/transfer.md#sui_transfer">sui::transfer</a>;
<b>use</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context">sui::tx_context</a>;
</code></pre>



<a name="nexus_primitives_owner_cap_CloneableOwnerCap"></a>

## Struct `CloneableOwnerCap`

When you want to prove you own something.

The pattern of usage:
Authorize with <code><a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_what_for">what_for</a></code> UID value of the resource and assert <code><a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_what_for">what_for</a></code>
from the resource's module.
In this case [clone] is useful to allow multiple addresses or
multiple concurrent txs.


<a name="@Important_0"></a>

### Important

The generic parameter <code>T</code> is a phantom type that is used to distinguish
between different things that can be owned.

a. <code>T <b>has</b> drop</code> then [CloneableOwnerCap] can be created only by giving <code>T</code>
b. <code>T <b>has</b> store</code> then [CloneableOwnerCap] can be created by giving <code>&T</code>
and associated [UID].


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">CloneableOwnerCap</a>&lt;<b>phantom</b> T&gt; <b>has</b> key, store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code><a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_id">id</a>: <a href="../dependencies/sui/object.md#sui_object_UID">sui::object::UID</a></code>
</dt>
<dd>
</dd>
<dt>
<code><a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_what_for">what_for</a>: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
 What does this [CloneableOwnerCap] actually own?
</dd>
<dt>
<code>inner: <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_OwnerCap">nexus_primitives::owner_cap::OwnerCap</a>&lt;T&gt;</code>
</dt>
<dd>
 Some packages might not care about the <code><a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_what_for">what_for</a></code> field, so they accept
 [OwnerCap].
 This allows us to emulate Rust's <code>AsRef</code> trait.
 Similar pattern for [sui::coin] and [sui::balance].
</dd>
</dl>


</details>

<a name="nexus_primitives_owner_cap_OwnerCap"></a>

## Struct `OwnerCap`

When you want to prove you own something.

The pattern of usage:
Store the [OwnerCap] ID in a resource and assert from the resource's
module that the sender has the right [OwnerCap]'s ID.


<a name="@Important_1"></a>

### Important

The generic parameter <code>T</code> is a phantom type that is used to distinguish
between different things that can be owned.
Anyone with a reference to [T] can create an [OwnerCap] with its generic.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_OwnerCap">OwnerCap</a>&lt;<b>phantom</b> T&gt; <b>has</b> drop, store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>unique: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="@Constants_2"></a>

## Constants


<a name="nexus_primitives_owner_cap_EObjectUidMismatch"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_EObjectUidMismatch">EObjectUidMismatch</a>: vector&lt;u8&gt; = b"Object key must match provided UID";
</code></pre>



<a name="nexus_primitives_owner_cap_new_uncloneable"></a>

## Function `new_uncloneable`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_new_uncloneable">new_uncloneable</a>&lt;T&gt;(_: &T, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_OwnerCap">nexus_primitives::owner_cap::OwnerCap</a>&lt;T&gt;
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_new_uncloneable">new_uncloneable</a>&lt;T&gt;(_: &T, ctx: &<b>mut</b> TxContext): <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_OwnerCap">OwnerCap</a>&lt;T&gt; {
    <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_OwnerCap">OwnerCap</a> {
        unique: {
            <b>let</b> uid = object::new(ctx);
            <b>let</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_id">id</a> = uid.to_inner();
            object::delete(uid);
            <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_id">id</a>
        }
    }
}
</code></pre>



</details>

<a name="nexus_primitives_owner_cap_new_cloneable_drop"></a>

## Function `new_cloneable_drop`

Creates a new [CloneableOwnerCap] for a given _thing_.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_new_cloneable_drop">new_cloneable_drop</a>&lt;T: drop&gt;(witness: T, <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_what_for">what_for</a>: &<a href="../dependencies/sui/object.md#sui_object_UID">sui::object::UID</a>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">nexus_primitives::owner_cap::CloneableOwnerCap</a>&lt;T&gt;
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_new_cloneable_drop">new_cloneable_drop</a>&lt;T: drop&gt;(
    witness: T, <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_what_for">what_for</a>: &UID, ctx: &<b>mut</b> TxContext,
): <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">CloneableOwnerCap</a>&lt;T&gt; {
    <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">CloneableOwnerCap</a> {
        <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_id">id</a>: object::new(ctx),
        <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_what_for">what_for</a>: <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_what_for">what_for</a>.to_inner(),
        inner: <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_new_uncloneable">new_uncloneable</a>(&witness, ctx),
    }
}
</code></pre>



</details>

<a name="nexus_primitives_owner_cap_new_cloneable_key"></a>

## Function `new_cloneable_key`

Creates a new [CloneableOwnerCap] for a given _object_.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_new_cloneable_key">new_cloneable_key</a>&lt;T: key&gt;(object: &T, its_uid: &<a href="../dependencies/sui/object.md#sui_object_UID">sui::object::UID</a>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">nexus_primitives::owner_cap::CloneableOwnerCap</a>&lt;T&gt;
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_new_cloneable_key">new_cloneable_key</a>&lt;T: key&gt;(
    object: &T, its_uid: &UID, ctx: &<b>mut</b> TxContext,
): <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">CloneableOwnerCap</a>&lt;T&gt; {
    <b>assert</b>!(object::id(object) == its_uid.to_inner(), <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_EObjectUidMismatch">EObjectUidMismatch</a>);
    <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">CloneableOwnerCap</a> {
        <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_id">id</a>: object::new(ctx),
        <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_what_for">what_for</a>: object::id(object),
        inner: <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_new_uncloneable">new_uncloneable</a>(object, ctx),
    }
}
</code></pre>



</details>

<a name="nexus_primitives_owner_cap_clone"></a>

## Function `clone`

Creates a new [CloneableOwnerCap] with the same <code><a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_what_for">what_for</a></code>.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_clone">clone</a>&lt;T&gt;(cap: &<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">nexus_primitives::owner_cap::CloneableOwnerCap</a>&lt;T&gt;, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">nexus_primitives::owner_cap::CloneableOwnerCap</a>&lt;T&gt;
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_clone">clone</a>&lt;T&gt;(cap: &<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">CloneableOwnerCap</a>&lt;T&gt;, ctx: &<b>mut</b> TxContext): <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">CloneableOwnerCap</a>&lt;T&gt; {
    <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">CloneableOwnerCap</a> {
        <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_id">id</a>: object::new(ctx),
        <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_what_for">what_for</a>: cap.<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_what_for">what_for</a>,
        inner: <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_OwnerCap">OwnerCap</a> {
            unique: cap.inner.unique,
        },
    }
}
</code></pre>



</details>

<a name="nexus_primitives_owner_cap_clone_n"></a>

## Function `clone_n`

Creates N new [CloneableOwnerCap]s with the same <code><a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_what_for">what_for</a></code>.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_clone_n">clone_n</a>&lt;T&gt;(cap: &<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">nexus_primitives::owner_cap::CloneableOwnerCap</a>&lt;T&gt;, n: u64, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>): vector&lt;<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">nexus_primitives::owner_cap::CloneableOwnerCap</a>&lt;T&gt;&gt;
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_clone_n">clone_n</a>&lt;T&gt;(cap: &<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">CloneableOwnerCap</a>&lt;T&gt;, n: u64, ctx: &<b>mut</b> TxContext): vector&lt;<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">CloneableOwnerCap</a>&lt;T&gt;&gt; {
    <b>let</b> <b>mut</b> v = vector[];
    <b>let</b> <b>mut</b> i = 0;
    <b>while</b> (i &lt; n) {
        v.push_back(<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_clone">clone</a>(cap, ctx));
        i = i + 1;
    };
    v
}
</code></pre>



</details>

<a name="nexus_primitives_owner_cap_clone_for_receiver"></a>

## Function `clone_for_receiver`

Creates a new [CloneableOwnerCap] with the same <code><a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_what_for">what_for</a></code> and transfers it to the
given address.


<pre><code><b>public</b> <b>entry</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_clone_for_receiver">clone_for_receiver</a>&lt;T&gt;(cap: &<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">nexus_primitives::owner_cap::CloneableOwnerCap</a>&lt;T&gt;, receiver: <b>address</b>, ctx: &<b>mut</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context_TxContext">sui::tx_context::TxContext</a>)
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>entry</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_clone_for_receiver">clone_for_receiver</a>&lt;T&gt;(
    cap: &<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">CloneableOwnerCap</a>&lt;T&gt;,
    receiver: <b>address</b>,
    ctx: &<b>mut</b> TxContext,
) {
    public_transfer(<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_clone">clone</a>(cap, ctx), receiver);
}
</code></pre>



</details>

<a name="nexus_primitives_owner_cap_destroy"></a>

## Function `destroy`

Destroy existing [CloneableOwnerCap].

Inner [OwnerCap] will be dropped.


<pre><code><b>public</b> <b>entry</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_destroy">destroy</a>&lt;T&gt;(self: <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">nexus_primitives::owner_cap::CloneableOwnerCap</a>&lt;T&gt;)
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>entry</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_destroy">destroy</a>&lt;T&gt;(self: <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">CloneableOwnerCap</a>&lt;T&gt;) {
    <b>let</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">CloneableOwnerCap</a> { <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_id">id</a>, .. } = self;
    object::delete(<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_id">id</a>);
}
</code></pre>



</details>

<a name="nexus_primitives_owner_cap_id"></a>

## Function `id`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_id">id</a>&lt;T&gt;(self: &<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_OwnerCap">nexus_primitives::owner_cap::OwnerCap</a>&lt;T&gt;): <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a>
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_id">id</a>&lt;T&gt;(self: &<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_OwnerCap">OwnerCap</a>&lt;T&gt;): ID { self.unique }
</code></pre>



</details>

<a name="nexus_primitives_owner_cap_what_for"></a>

## Function `what_for`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_what_for">what_for</a>&lt;T&gt;(self: &<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">nexus_primitives::owner_cap::CloneableOwnerCap</a>&lt;T&gt;): <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a>
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_what_for">what_for</a>&lt;T&gt;(self: &<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">CloneableOwnerCap</a>&lt;T&gt;): ID { self.<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_what_for">what_for</a> }
</code></pre>



</details>

<a name="nexus_primitives_owner_cap_is_for"></a>

## Function `is_for`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_is_for">is_for</a>&lt;T, U: key&gt;(self: &<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">nexus_primitives::owner_cap::CloneableOwnerCap</a>&lt;T&gt;, what: &U): bool
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_is_for">is_for</a>&lt;T, U: key&gt;(self: &<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">CloneableOwnerCap</a>&lt;T&gt;, what: &U): bool { self.<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_what_for">what_for</a> == object::id(what) }
</code></pre>



</details>

<a name="nexus_primitives_owner_cap_is_for_id"></a>

## Function `is_for_id`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_is_for_id">is_for_id</a>&lt;T&gt;(self: &<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">nexus_primitives::owner_cap::CloneableOwnerCap</a>&lt;T&gt;, what_id: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a>): bool
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_is_for_id">is_for_id</a>&lt;T&gt;(self: &<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">CloneableOwnerCap</a>&lt;T&gt;, what_id: ID): bool { self.<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_what_for">what_for</a> == what_id }
</code></pre>



</details>

<a name="nexus_primitives_owner_cap_as_ref"></a>

## Function `as_ref`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_as_ref">as_ref</a>&lt;T&gt;(self: &<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">nexus_primitives::owner_cap::CloneableOwnerCap</a>&lt;T&gt;): &<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_OwnerCap">nexus_primitives::owner_cap::OwnerCap</a>&lt;T&gt;
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_as_ref">as_ref</a>&lt;T&gt;(self: &<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_CloneableOwnerCap">CloneableOwnerCap</a>&lt;T&gt;): &<a href="../nexus_primitives/owner_cap.md#nexus_primitives_owner_cap_OwnerCap">OwnerCap</a>&lt;T&gt; { &self.inner }
</code></pre>



</details>
