---
layout:
  width: default
  title:
    visible: true
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
---

# Step-by-step: My First Workflow

In this section, we’ll build a simple workflow together. We’ll recreate the example from the Nexus documentation (see the **Math Branching Quickstart** [guide](https://docs.talus.network/getting-started/math-branching-quickstart)) and observe how the JSON updates in real time.

This example takes a numeric input and performs the following sequence of operations:

1. Add **3** to the input value.
1. Evaluate the sign of the result and follow one of three branches:
   - **If the number is positive:** multiply it by **7**.
   - **If the number equals 0:** add **1**.
   - **If the number is negative:** multiply it by **–3**.

We will now construct the complete workflow step by step.

Initial state for the JSON editor:

````json
{
  "vertices": [],
  "edges": [],
  "default_values": []
}


```json
{
  "vertices": [],
  "edges": [],
  "default_values": []
}
````

## Step 1

The first node in this workflow performs the operation of adding **3** to the user’s input.

Under the **Math** category, the **Add** tool is designed for this purpose.  
From the **Tools** tab, navigate to **Math → Add**, then drag and drop the tool into the playground.

Rename the node to `add_input_and_default`.

Next, set **port B** as the default value and assign it the value **3**.

<figure>
  <img src="../assets/Screenshot 2025-11-11 at 13.10.47.png" alt="">
  <figcaption></figcaption>
</figure>

The JSON editor’s current state is:

```json
{
  "vertices": [
    {
      "entry_ports": [
        {
          "name": "a",
          "encrypted": false
        }
      ],
      "kind": {
        "variant": "off_chain",
        "tool_fqn": "xyz.taluslabs.math.i64.add@1"
      },
      "name": "add_input_and_default"
    }
  ],
  "edges": [],
  "default_values": [
    {
      "vertex": "add_input_and_default",
      "input_port": "b",
      "value": {
        "storage": "inline",
        "data": 3
      }
    }
  ]
}
```

### Step 2

In this step, we need to check whether the result from the first node is **negative**.

To do this, use the **Compare (cmp)** tool found under the **Math** category. This tool accepts two inputs and compares them, producing three outputs: **greater than**, **equal to**, and **less than** — exactly what is needed for branching logic.

1. Drag and drop the **Compare (cmp)** tool into the playground.
1. Rename the node to `is_negative`.
1. Set the second input (**port B**) to a **default value of 0**, which establishes the comparison target.
1. Connect the output of the `add_input_and_default` node to the **first input (port A)** of the `is_negative` node.

<figure>
<img src="../assets/Screenshot 2025-11-11 at 13.20.04.png" alt="">
<figcaption></figcaption>
</figure>

The JSON editor’s current state is:

```json
{
  "vertices": [
    {
      "entry_ports": [
        {
          "name": "a",
          "encrypted": false
        }
      ],
      "kind": {
        "variant": "off_chain",
        "tool_fqn": "xyz.taluslabs.math.i64.add@1"
      },
      "name": "add_input_and_default"
    },
    {
      "kind": {
        "variant": "off_chain",
        "tool_fqn": "xyz.taluslabs.math.i64.cmp@1"
      },
      "name": "is_negative"
    }
  ],
  "edges": [
    {
      "from": {
        "vertex": "add_input_and_default",
        "output_variant": "ok",
        "output_port": "result"
      },
      "to": {
        "vertex": "is_negative",
        "input_port": "a"
      }
    }
  ],
  "default_values": [
    {
      "vertex": "add_input_and_default",
      "input_port": "b",
      "value": {
        "storage": "inline",
        "data": 3
      }
    },
    {
      "vertex": "is_negative",
      "input_port": "b",
      "value": {
        "storage": "inline",
        "data": 0
      }
    }
  ]
}
```

### Step 3

In this step, we will generate new outputs based on the results from the **Compare (cmp)** node, following this logic:

- **If the number is greater than 0:** multiply it by 7
- **If the number equals 0:** add 1
- **If the number is less than 0:** multiply it by -3

To implement this logic, we will use:

- **Multiply (Mul)** tool (Math category) — for multiplying by 7 and -3
- **Add** tool (Math category) — for adding 1

## Steps to implement

1. Locate the tools in **Tools tab → Math category** and drag and drop them into the playground.

1. **Rename and configure each node** as follows:

   - **Multiply by 7 node**

     - Name: `mul_by_7`
     - Set input **B = 7**
     - Connect to the **gt** (greater than) output of the `is_negative` node

   - **Add 1 node**

     - Name: `add_1`
     - Set input **B = 1**
     - Connect to the **eq** (equal) output of the `is_negative` node

   - **Multiply by -3 node**
     - Name: `mul_by_neg_3`
     - Set input **B = -3**
     - Connect to the **lt** (less than) output of the `is_negative` node

<figure>
  <img src="../assets/Screenshot 2025-11-11 at 13.31.13.png" alt="">
  <figcaption></figcaption>
</figure>

The JSON editor's final state is:

```json
{
  "vertices": [
    {
      "entry_ports": [
        {
          "name": "a",
          "encrypted": false
        }
      ],
      "kind": {
        "variant": "off_chain",
        "tool_fqn": "xyz.taluslabs.math.i64.add@1"
      },
      "name": "add_input_and_default"
    },
    {
      "kind": {
        "variant": "off_chain",
        "tool_fqn": "xyz.taluslabs.math.i64.cmp@1"
      },
      "name": "is_negative"
    },
    {
      "kind": {
        "variant": "off_chain",
        "tool_fqn": "xyz.taluslabs.math.i64.mul@1"
      },
      "name": "mul_by_7"
    },
    {
      "kind": {
        "variant": "off_chain",
        "tool_fqn": "xyz.taluslabs.math.i64.add@1"
      },
      "name": "add_1"
    },
    {
      "kind": {
        "variant": "off_chain",
        "tool_fqn": "xyz.taluslabs.math.i64.mul@1"
      },
      "name": "mul_by_neg_3"
    }
  ],
  "edges": [
    {
      "from": {
        "vertex": "add_input_and_default",
        "output_variant": "ok",
        "output_port": "result"
      },
      "to": {
        "vertex": "is_negative",
        "input_port": "a"
      }
    },
    {
      "from": {
        "vertex": "is_negative",
        "output_variant": "gt",
        "output_port": "a"
      },
      "to": {
        "vertex": "mul_by_7",
        "input_port": "a"
      }
    },
    {
      "from": {
        "vertex": "is_negative",
        "output_variant": "eq",
        "output_port": "a"
      },
      "to": {
        "vertex": "add_1",
        "input_port": "a"
      }
    },
    {
      "from": {
        "vertex": "is_negative",
        "output_variant": "lt",
        "output_port": "a"
      },
      "to": {
        "vertex": "mul_by_neg_3",
        "input_port": "a"
      }
    }
  ],
  "default_values": [
    {
      "vertex": "add_input_and_default",
      "input_port": "b",
      "value": {
        "storage": "inline",
        "data": 3
      }
    },
    {
      "vertex": "is_negative",
      "input_port": "b",
      "value": {
        "storage": "inline",
        "data": 0
      }
    },
    {
      "vertex": "mul_by_7",
      "input_port": "b",
      "value": {
        "storage": "inline",
        "data": 7
      }
    },
    {
      "vertex": "add_1",
      "input_port": "b",
      "value": {
        "storage": "inline",
        "data": 1
      }
    },
    {
      "vertex": "mul_by_neg_3",
      "input_port": "b",
      "value": {
        "storage": "inline",
        "data": -3
      }
    }
  ]
}
```
