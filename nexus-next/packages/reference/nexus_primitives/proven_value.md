
<a name="nexus_primitives_proven_value"></a>

# Module `nexus_primitives::proven_value`



-  [Struct `ProvenValue`](#nexus_primitives_proven_value_ProvenValue)
-  [Constants](#@Constants_0)
-  [Function `wrap`](#nexus_primitives_proven_value_wrap)
-  [Function `wrap_for_recipient`](#nexus_primitives_proven_value_wrap_for_recipient)
-  [Function `unwrap`](#nexus_primitives_proven_value_unwrap)
-  [Function `unwrap_as_recipient`](#nexus_primitives_proven_value_unwrap_as_recipient)
-  [Function `drop`](#nexus_primitives_proven_value_drop)
-  [Function `by`](#nexus_primitives_proven_value_by)
-  [Function `recipient`](#nexus_primitives_proven_value_recipient)


<pre><code><b>use</b> <a href="../dependencies/std/ascii.md#std_ascii">std::ascii</a>;
<b>use</b> <a href="../dependencies/std/bcs.md#std_bcs">std::bcs</a>;
<b>use</b> <a href="../dependencies/std/option.md#std_option">std::option</a>;
<b>use</b> <a href="../dependencies/std/string.md#std_string">std::string</a>;
<b>use</b> <a href="../dependencies/std/vector.md#std_vector">std::vector</a>;
<b>use</b> <a href="../dependencies/sui/address.md#sui_address">sui::address</a>;
<b>use</b> <a href="../dependencies/sui/hex.md#sui_hex">sui::hex</a>;
<b>use</b> <a href="../dependencies/sui/object.md#sui_object">sui::object</a>;
<b>use</b> <a href="../dependencies/sui/tx_context.md#sui_tx_context">sui::tx_context</a>;
</code></pre>



<a name="nexus_primitives_proven_value_ProvenValue"></a>

## Struct `ProvenValue`

Value that can be trusted to have been created by a UID.
Optionally, the value can also be locked to be received only by a given
recipient.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_ProvenValue">ProvenValue</a>&lt;T&gt;
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>value: T</code>
</dt>
<dd>
</dd>
<dt>
<code><a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_by">by</a>: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a></code>
</dt>
<dd>
</dd>
<dt>
<code><a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_recipient">recipient</a>: <a href="../dependencies/std/option.md#std_option_Option">std::option::Option</a>&lt;<a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a>&gt;</code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="@Constants_0"></a>

## Constants


<a name="nexus_primitives_proven_value_ENotRecipient"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_ENotRecipient">ENotRecipient</a>: vector&lt;u8&gt; = b"Not the expected <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_recipient">recipient</a>";
</code></pre>



<a name="nexus_primitives_proven_value_wrap"></a>

## Function `wrap`

Proves that the value was wrapped by the given UID.
Anyone can unwrap the value.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_wrap">wrap</a>&lt;T&gt;(<a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_by">by</a>: &<a href="../dependencies/sui/object.md#sui_object_UID">sui::object::UID</a>, value: T): <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_ProvenValue">nexus_primitives::proven_value::ProvenValue</a>&lt;T&gt;
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_wrap">wrap</a>&lt;T&gt;(<a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_by">by</a>: &UID, value: T): <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_ProvenValue">ProvenValue</a>&lt;T&gt; {
    <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_ProvenValue">ProvenValue</a> { value, <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_by">by</a>: <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_by">by</a>.to_inner(), <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_recipient">recipient</a>: option::none() }
}
</code></pre>



</details>

<a name="nexus_primitives_proven_value_wrap_for_recipient"></a>

## Function `wrap_for_recipient`

Proves that the value was wrapped by the given UID.
Only the recipient UID can unwrap the value.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_wrap_for_recipient">wrap_for_recipient</a>&lt;T&gt;(<a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_by">by</a>: &<a href="../dependencies/sui/object.md#sui_object_UID">sui::object::UID</a>, value: T, <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_recipient">recipient</a>: <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a>): <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_ProvenValue">nexus_primitives::proven_value::ProvenValue</a>&lt;T&gt;
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_wrap_for_recipient">wrap_for_recipient</a>&lt;T&gt;(<a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_by">by</a>: &UID, value: T, <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_recipient">recipient</a>: ID): <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_ProvenValue">ProvenValue</a>&lt;T&gt; {
    <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_ProvenValue">ProvenValue</a> { value, <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_by">by</a>: <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_by">by</a>.to_inner(), <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_recipient">recipient</a>: option::some(<a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_recipient">recipient</a>) }
}
</code></pre>



</details>

<a name="nexus_primitives_proven_value_unwrap"></a>

## Function `unwrap`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_unwrap">unwrap</a>&lt;T&gt;(self: <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_ProvenValue">nexus_primitives::proven_value::ProvenValue</a>&lt;T&gt;): T
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_unwrap">unwrap</a>&lt;T&gt;(self: <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_ProvenValue">ProvenValue</a>&lt;T&gt;): T {
    <b>let</b> <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_ProvenValue">ProvenValue</a> { value, .. } = self;
    value
}
</code></pre>



</details>

<a name="nexus_primitives_proven_value_unwrap_as_recipient"></a>

## Function `unwrap_as_recipient`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_unwrap_as_recipient">unwrap_as_recipient</a>&lt;T&gt;(self: <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_ProvenValue">nexus_primitives::proven_value::ProvenValue</a>&lt;T&gt;, <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_recipient">recipient</a>: &<a href="../dependencies/sui/object.md#sui_object_UID">sui::object::UID</a>): T
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_unwrap_as_recipient">unwrap_as_recipient</a>&lt;T&gt;(self: <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_ProvenValue">ProvenValue</a>&lt;T&gt;, <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_recipient">recipient</a>: &UID): T {
    <b>let</b> <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_ProvenValue">ProvenValue</a> { value, <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_recipient">recipient</a>: expected_recipient, .. } = self;
    <b>if</b> (expected_recipient.is_some()) {
        <b>assert</b>!(expected_recipient.destroy_some() == <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_recipient">recipient</a>.to_inner(), <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_ENotRecipient">ENotRecipient</a>);
    };
    value
}
</code></pre>



</details>

<a name="nexus_primitives_proven_value_drop"></a>

## Function `drop`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_drop">drop</a>&lt;T: <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_drop">drop</a>&gt;(self: <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_ProvenValue">nexus_primitives::proven_value::ProvenValue</a>&lt;T&gt;)
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_drop">drop</a>&lt;T: <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_drop">drop</a>&gt;(self: <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_ProvenValue">ProvenValue</a>&lt;T&gt;) {
    <b>let</b> <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_ProvenValue">ProvenValue</a> { .. } = self;
}
</code></pre>



</details>

<a name="nexus_primitives_proven_value_by"></a>

## Function `by`

Who wrapped the value.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_by">by</a>&lt;T&gt;(self: &<a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_ProvenValue">nexus_primitives::proven_value::ProvenValue</a>&lt;T&gt;): <a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a>
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_by">by</a>&lt;T&gt;(self: &<a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_ProvenValue">ProvenValue</a>&lt;T&gt;): ID { self.<a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_by">by</a> }
</code></pre>



</details>

<a name="nexus_primitives_proven_value_recipient"></a>

## Function `recipient`

Who is the recipient of the value, if any.


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_recipient">recipient</a>&lt;T&gt;(self: &<a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_ProvenValue">nexus_primitives::proven_value::ProvenValue</a>&lt;T&gt;): <a href="../dependencies/std/option.md#std_option_Option">std::option::Option</a>&lt;<a href="../dependencies/sui/object.md#sui_object_ID">sui::object::ID</a>&gt;
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_recipient">recipient</a>&lt;T&gt;(self: &<a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_ProvenValue">ProvenValue</a>&lt;T&gt;): Option&lt;ID&gt; { self.<a href="../nexus_primitives/proven_value.md#nexus_primitives_proven_value_recipient">recipient</a> }
</code></pre>



</details>
