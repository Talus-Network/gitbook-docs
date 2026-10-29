# `xyz.taluslabs.templating.jinja@1`

Standard Nexus Tool that parses templates using the Jinja2 (MiniJinja) templating engine with flexible input options. Undefined variables are preserved as `{{placeholders}}` to support chaining with other tools.

## Input

**`template`: [`String`]**

The template string to render. Supports template syntax with variable substitution using double curly braces (e.g., `{{variable_name}}`). Undefined variables are preserved in the output (not an error), allowing partial rendering.

_opt_ **`args`: [`HashMap<String, String>`]** _default_: `{}`

Template arguments as a HashMap mapping variable names to their values. This parameter can be combined with `name`/`value` parameters to provide additional variables. At least one of `args` or the `name`/`value` pair must be provided.

_opt_ **`value`: [`Option<String>`]** _default_: [`None`]

Optional single value to substitute in the template. Must be used together with the `name` parameter. Can be combined with the `args` parameter to add an additional variable.

_opt_ **`name`: [`Option<String>`]** _default_: [`None`]

Optional name for the single variable. Must be used together with the `value` parameter. This allows you to specify an additional variable beyond those provided in `args`.

## Rendering limits

Expressions use all supplied arguments at once. Argument values are plain data and are never interpreted again as template source. Expressions containing missing variables remain unchanged for a later tool invocation.

Supported expressions are variables, scalar literals, concatenation with `~`, addition, repetition by a nonnegative integer literal, and these filters: `upper`, `lower`, `capitalize`, `title`, `trim`, `length`, `count`, `escape`, `e`, `tojson`, `default`, `d`, and `replace`. Only positional filter arguments are supported. Blocks, function calls, and other expressions or filters return an error. This restriction permits checking intermediate allocation sizes before running the expression.

The combined template and argument size is limited to 64 KiB, with at most 128 arguments and 256 expressions. Output and intermediate strings are limited to 1 MiB using conservative size estimates. Expressions also have depth and instruction budgets.

## Output Variants & Ports

**`ok`**

The template was rendered successfully.

- **`ok.result`: [`String`]** - The rendered template with all variables substituted

**`err`**

The template processing failed due to an error.

- **`err.reason`: [`String`]** - A detailed error message describing what went wrong. This could be:
  - `"Either 'args' or 'name'/'value' parameters must be provided"` - No parameters were provided or args is empty
  - `"name and value must both be provided or both be None"` - Only one of name/value was provided
  - `"Template syntax error: [error details]"` - Template has invalid syntax
  - `"Template rendering failed: [error details]"` - Rendering error

---

## Examples

### Example 1: Using args HashMap

```json
{
  "template": "Hello {{name}} from {{city}}!",
  "args": {
    "name": "Alice",
    "city": "Paris"
  }
}
```

**Output:**

```json
{
  "type": "ok",
  "result": "Hello Alice from Paris!"
}
```

### Example 2: Using name and value

```json
{
  "template": "Welcome, {{username}}!",
  "name": "username",
  "value": "Bob"
}
```

**Output:**

```json
{
  "type": "ok",
  "result": "Welcome, Bob!"
}
```

### Example 3: Combining args and name/value

```json
{
  "template": "{{greeting}} {{name}} from {{city}}!",
  "args": {
    "greeting": "Hello",
    "city": "Tokyo"
  },
  "name": "name",
  "value": "Dave"
}
```

**Output:**

```json
{
  "type": "ok",
  "result": "Hello Dave from Tokyo!"
}
```

### Example 4: Using empty args with name/value

```json
{
  "template": "{{message}}",
  "args": {},
  "name": "message",
  "value": "Test message"
}
```

**Output:**

```json
{
  "type": "ok",
  "result": "Test message"
}
```

### Example 5: Error - No parameters provided

```json
{
  "template": "Hello {{name}}!"
}
```

**Output:**

```json
{
  "type": "err",
  "reason": "Either 'args' or 'name'/'value' parameters must be provided"
}
```

### Example 6: Error - Only name provided

```json
{
  "template": "Hello {{name}}!",
  "name": "name"
}
```

**Output:**

```json
{
  "type": "err",
  "reason": "name and value must both be provided or both be None"
}
```

### Example 7: Undefined variables are preserved

```json
{
  "template": "Hi, this is {{name}}, from {{city}}",
  "args": {
    "name": "Alice"
  }
}
```

**Output:**

```json
{
  "type": "ok",
  "result": "Hi, this is Alice, from {{city}}"
}
```
