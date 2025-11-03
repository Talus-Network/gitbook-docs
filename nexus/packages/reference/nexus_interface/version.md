
<a name="(nexus_interface=0x0)_version"></a>

# Module `(nexus_interface=0x0)::version`



-  [Struct `InterfaceVersion`](#(nexus_interface=0x0)_version_InterfaceVersion)
-  [Constants](#@Constants_0)
-  [Function `v`](#(nexus_interface=0x0)_version_v)
-  [Function `number`](#(nexus_interface=0x0)_version_number)
-  [Function `expect_v`](#(nexus_interface=0x0)_version_expect_v)


<pre><code></code></pre>



<a name="(nexus_interface=0x0)_version_InterfaceVersion"></a>

## Struct `InterfaceVersion`



<pre><code><b>public</b> <b>struct</b> <a href="../nexus_primitives/version.md#(nexus_interface=0x0)_version_InterfaceVersion">InterfaceVersion</a> <b>has</b> <b>copy</b>, drop, store
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code>inner: u64</code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="@Constants_0"></a>

## Constants


<a name="(nexus_interface=0x0)_version_EInterfaceVersionMismatch"></a>



<pre><code>#[error]
<b>const</b> <a href="../nexus_primitives/version.md#(nexus_interface=0x0)_version_EInterfaceVersionMismatch">EInterfaceVersionMismatch</a>: vector&lt;u8&gt; = b"Interface <a href="../nexus_primitives/version.md#(nexus_interface=0x0)_version">version</a> mismatch";
</code></pre>



<a name="(nexus_interface=0x0)_version_v"></a>

## Function `v`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/version.md#(nexus_interface=0x0)_version_v">v</a>(<a href="../nexus_primitives/version.md#(nexus_interface=0x0)_version">version</a>: u64): (nexus_interface=0x0)::<a href="../nexus_primitives/version.md#(nexus_interface=0x0)_version_InterfaceVersion">version::InterfaceVersion</a>
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/version.md#(nexus_interface=0x0)_version_v">v</a>(<a href="../nexus_primitives/version.md#(nexus_interface=0x0)_version">version</a>: u64): <a href="../nexus_primitives/version.md#(nexus_interface=0x0)_version_InterfaceVersion">InterfaceVersion</a> {
    <a href="../nexus_primitives/version.md#(nexus_interface=0x0)_version_InterfaceVersion">InterfaceVersion</a> { inner: <a href="../nexus_primitives/version.md#(nexus_interface=0x0)_version">version</a> }
}
</code></pre>



</details>

<a name="(nexus_interface=0x0)_version_number"></a>

## Function `number`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/version.md#(nexus_interface=0x0)_version_number">number</a>(self: &(nexus_interface=0x0)::<a href="../nexus_primitives/version.md#(nexus_interface=0x0)_version_InterfaceVersion">version::InterfaceVersion</a>): u64
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/version.md#(nexus_interface=0x0)_version_number">number</a>(self: &<a href="../nexus_primitives/version.md#(nexus_interface=0x0)_version_InterfaceVersion">InterfaceVersion</a>): u64 {
    self.inner
}
</code></pre>



</details>

<a name="(nexus_interface=0x0)_version_expect_v"></a>

## Function `expect_v`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/version.md#(nexus_interface=0x0)_version_expect_v">expect_v</a>(self: &(nexus_interface=0x0)::<a href="../nexus_primitives/version.md#(nexus_interface=0x0)_version_InterfaceVersion">version::InterfaceVersion</a>, expected: u64)
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/version.md#(nexus_interface=0x0)_version_expect_v">expect_v</a>(self: &<a href="../nexus_primitives/version.md#(nexus_interface=0x0)_version_InterfaceVersion">InterfaceVersion</a>, expected: u64) {
    <b>assert</b>!(self.inner == expected, <a href="../nexus_primitives/version.md#(nexus_interface=0x0)_version_EInterfaceVersionMismatch">EInterfaceVersionMismatch</a>)
}
</code></pre>



</details>
