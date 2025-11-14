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

# Step-by-step My first Workflow

Let's build our first workflow together. We'll reconstruct this example from the Nexus documentation step-by-step and monitor the changes in the JSON files in real time. [https://docs.talus.network/getting-started/math-branching-quickstart](https://docs.talus.network/getting-started/math-branching-quickstart)\
\
This example accepts a numeric input from the user and performs the following sequence of operations:

1. Add **3** to the input value.
2. Evaluate the sign of the resulting number and apply one of three branches:
   * **If the number is positive:** multiply it by **7**.
   * **If the number equals 0:** add **1** to it.
   * **If the number is negative:** multiply it by **-3**.

We will now construct the complete workflow step by step.\
\
Initial state for JSON editor :&#x20;

```json
{
"vertices": [
],
"edges": [
],
"default_values": [
]
}
```

Step -  1\
The first node we need in our workflow will perform the operation of **adding the number 3** to the user’s input.

Under the **Math** category, the **Add** tool is designed precisely for this purpose. From the **Tools tab**, navigate to the **Math** category, locate the **Add** tool, and **drag and drop** it into the playground.

For naming, set the node name to **`add_input_and_default`**.\
Then, assign **port B** as the **default value**, and set this value to **3**.

<figure><img src="../assets/Screenshot 2025-11-11 at 13.10.47.png" alt=""><figcaption></figcaption></figure>

JSON editor current state is :&#x20;

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

Step - 2

In this step, we need to check whether the result from the first node is negative.

The most suitable node for this task is the **Compare (cmp)** tool, located under the **Math** category. This tool takes **two inputs** and compares them, producing **three distinct outputs**: **greater than**, **equal to**, and **less than** — perfectly fitting our example’s logic.

Drag and drop the **Compare (cmp)** tool into the playground and rename it to **`is_negative`**.\
Next, set the **second input** as a **default value of 0** to establish the desired comparison logic.

Finally, connect the **result output** from the **`add_input_and_default`** node to the **first input** of the **`is_negative`** node.

<figure><img src="../assets/Screenshot 2025-11-11 at 13.20.04.png" alt=""><figcaption></figcaption></figure>

JSON editor current state is :&#x20;

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

Step - 3&#x20;

In this step, we will generate new outputs based on the results from the **Compare (cmp)** node, following the target logic:

* **If the number is greater than 0:** multiply it by **7**
* **If the number equals 0:** add **1**
* **If the number is less than 0:** multiply it by **-3**

Based on this logic, the required tools are:

* **Multiply (Mul) tool** from the **Math** category for multiplying by 7 and -3
* **Add tool** from the **Math** category for adding 1

#### Steps to implement:

1. **Locate the tools** in the **Tools tab → Math category** and **drag and drop** them into the playground.
2.  **Rename and configure the nodes** as follows:

    * **Multiply by 7 node:**
      * Name: **`mul_by_7`**
      * **B input:** 7
      * Connect to the **gt output** of the **`is_negative`** node
    * **Add 1 node:**
      * Name: **`add_1`**
      * **B input:** 1
      * Connect to the **eq output** of the **`is_negative`** node
    * **Multiply by -3 node:**
      * Name: **`mul_by_neg_3`**
      * **B input:** -3
      * Connect to the **lt output** of the **`is_negative`** node



    <figure><img src="../assets/Screenshot 2025-11-11 at 13.31.13.png" alt=""><figcaption></figcaption></figure>



Json editor final state is :&#x20;

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
