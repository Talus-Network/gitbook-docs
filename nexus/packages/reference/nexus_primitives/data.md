
<a name="nexus_primitives_data"></a>

# Module `nexus_primitives::data`



-  [Struct `NexusData`](#nexus_primitives_data_NexusData)
-  [Constants](#@Constants_0)
-  [Function `inline_many`](#nexus_primitives_data_inline_many)
-  [Function `inline_one`](#nexus_primitives_data_inline_one)
-  [Function `remote_many`](#nexus_primitives_data_remote_many)
-  [Function `remote_one`](#nexus_primitives_data_remote_one)


<pre><code></code></pre>



<a name="nexus_primitives_data_NexusData"></a>

## Struct `NexusData`

References some some specific data.

Serialization conventions are agreed on by the off-chain realm.


<pre><code><b>public</b> <b>struct</b> <a href="../nexus_primitives/data.md#nexus_primitives_data_NexusData">NexusData</a> <b>has</b> <b>copy</b>, drop, store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>storage: vector&lt;u8&gt;</code>
</dt>
<dd>
 Will be b"inline" if stored on chain, or an identifier of the storage.
 Inline data are useful for short data that can be stored on-chain such
 as configurations.
</dd>
<dt>
<code><a href="../nexus_primitives/data.md#nexus_primitives_data">data</a>: vector&lt;vector&lt;u8&gt;&gt;</code>
</dt>
<dd>
 If storage is not inline then use these keys to fetch the data from
 the storage.
 For array types there might be more than one element.
 None is an empty vector which is a useful representation.
</dd>
</dl>


</details>

<a name="@Constants_0"></a>

## Constants


<a name="nexus_primitives_data_INLINE_STORAGE_KEY"></a>



<pre><code><b>const</b> <a href="../nexus_primitives/data.md#nexus_primitives_data_INLINE_STORAGE_KEY">INLINE_STORAGE_KEY</a>: vector&lt;u8&gt; = vector[105, 110, 108, 105, 110, 101];
</code></pre>



<a name="nexus_primitives_data_inline_many"></a>

## Function `inline_many`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/data.md#nexus_primitives_data_inline_many">inline_many</a>(<a href="../nexus_primitives/data.md#nexus_primitives_data">data</a>: vector&lt;vector&lt;u8&gt;&gt;): <a href="../nexus_primitives/data.md#nexus_primitives_data_NexusData">nexus_primitives::data::NexusData</a>
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/data.md#nexus_primitives_data_inline_many">inline_many</a>(<a href="../nexus_primitives/data.md#nexus_primitives_data">data</a>: vector&lt;vector&lt;u8&gt;&gt;): <a href="../nexus_primitives/data.md#nexus_primitives_data_NexusData">NexusData</a> {
    <a href="../nexus_primitives/data.md#nexus_primitives_data_NexusData">NexusData</a> { storage: <a href="../nexus_primitives/data.md#nexus_primitives_data_INLINE_STORAGE_KEY">INLINE_STORAGE_KEY</a>, <a href="../nexus_primitives/data.md#nexus_primitives_data">data</a> }
}
</code></pre>



</details>

<a name="nexus_primitives_data_inline_one"></a>

## Function `inline_one`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/data.md#nexus_primitives_data_inline_one">inline_one</a>(<a href="../nexus_primitives/data.md#nexus_primitives_data">data</a>: vector&lt;u8&gt;): <a href="../nexus_primitives/data.md#nexus_primitives_data_NexusData">nexus_primitives::data::NexusData</a>
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/data.md#nexus_primitives_data_inline_one">inline_one</a>(<a href="../nexus_primitives/data.md#nexus_primitives_data">data</a>: vector&lt;u8&gt;): <a href="../nexus_primitives/data.md#nexus_primitives_data_NexusData">NexusData</a> {
    <a href="../nexus_primitives/data.md#nexus_primitives_data_NexusData">NexusData</a> { storage: <a href="../nexus_primitives/data.md#nexus_primitives_data_INLINE_STORAGE_KEY">INLINE_STORAGE_KEY</a>, <a href="../nexus_primitives/data.md#nexus_primitives_data">data</a>: vector[<a href="../nexus_primitives/data.md#nexus_primitives_data">data</a>] }
}
</code></pre>



</details>

<a name="nexus_primitives_data_remote_many"></a>

## Function `remote_many`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/data.md#nexus_primitives_data_remote_many">remote_many</a>(storage: vector&lt;u8&gt;, keys: vector&lt;vector&lt;u8&gt;&gt;): <a href="../nexus_primitives/data.md#nexus_primitives_data_NexusData">nexus_primitives::data::NexusData</a>
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/data.md#nexus_primitives_data_remote_many">remote_many</a>(storage: vector&lt;u8&gt;, keys: vector&lt;vector&lt;u8&gt;&gt;): <a href="../nexus_primitives/data.md#nexus_primitives_data_NexusData">NexusData</a> {
    <a href="../nexus_primitives/data.md#nexus_primitives_data_NexusData">NexusData</a> { storage, <a href="../nexus_primitives/data.md#nexus_primitives_data">data</a>: keys }
}
</code></pre>



</details>

<a name="nexus_primitives_data_remote_one"></a>

## Function `remote_one`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/data.md#nexus_primitives_data_remote_one">remote_one</a>(storage: vector&lt;u8&gt;, key: vector&lt;u8&gt;): <a href="../nexus_primitives/data.md#nexus_primitives_data_NexusData">nexus_primitives::data::NexusData</a>
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/data.md#nexus_primitives_data_remote_one">remote_one</a>(storage: vector&lt;u8&gt;, key: vector&lt;u8&gt;): <a href="../nexus_primitives/data.md#nexus_primitives_data_NexusData">NexusData</a> {
    <a href="../nexus_primitives/data.md#nexus_primitives_data_NexusData">NexusData</a> { storage, <a href="../nexus_primitives/data.md#nexus_primitives_data">data</a>: vector[key] }
}
</code></pre>



</details>
