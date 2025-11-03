
<a name="nexus_primitives_event"></a>

# Module `nexus_primitives::event`



-  [Struct `EventWrapper`](#nexus_primitives_event_EventWrapper)
-  [Function `emit`](#nexus_primitives_event_emit)


<pre><code><b>use</b> <a href="../dependencies/sui/event.md#sui_event">sui::event</a>;
</code></pre>



<a name="nexus_primitives_event_EventWrapper"></a>

## Struct `EventWrapper`



<pre><code><b>public</b> <b>struct</b> <a href="../nexus_primitives/event.md#nexus_primitives_event_EventWrapper">EventWrapper</a>&lt;T&gt; <b>has</b> <b>copy</b>, drop
</code></pre>



<details>
<summary>Fields</summary>


<dl>
<dt>
<code><a href="../nexus_primitives/event.md#nexus_primitives_event">event</a>: T</code>
</dt>
<dd>
</dd>
</dl>


</details>

<a name="nexus_primitives_event_emit"></a>

## Function `emit`



<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/event.md#nexus_primitives_event_emit">emit</a>&lt;T: <b>copy</b>, drop&gt;(<a href="../nexus_primitives/event.md#nexus_primitives_event">event</a>: T)
</code></pre>



<details>
<summary>Implementation</summary>


<pre><code><b>public</b> <b>fun</b> <a href="../nexus_primitives/event.md#nexus_primitives_event_emit">emit</a>&lt;T: <b>copy</b> + drop&gt;(<a href="../nexus_primitives/event.md#nexus_primitives_event">event</a>: T) {
    <a href="../dependencies/sui/event.md#sui_event_emit">sui::event::emit</a>(<a href="../nexus_primitives/event.md#nexus_primitives_event_EventWrapper">EventWrapper</a> { <a href="../nexus_primitives/event.md#nexus_primitives_event">event</a> })
}
</code></pre>



</details>
