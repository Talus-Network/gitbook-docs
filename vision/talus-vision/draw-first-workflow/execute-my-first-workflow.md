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

# Execute My first Workflow

So far, we have successfully built a workflow according to our desired logic. After passing all **validation steps**, we deployed this workflow, turning it into an **on-chain object**. The next step is to **execute it and observe the results**.

Navigate to the **Execute Workflow tab**, fill in the required inputs, and execute the DAG **on-chain**.

In this example, the workflow expects **one numeric input** at the **`add_input_and_default`** node. At this point, the playground is in **View Mode**, and only the necessary input fields are visible. Once the input is provided, we can monitor the **output in the console**.

I chose **12** as the input, and the expected step-by-step results are as follows:

* **`add_input_and_default` output:** 12 + 3 = **15**
* **`is_negative` output:** 15 compared to 0 → **greater than**, so the **gt output** is triggered
* **Final result:** The workflow ends at the **`mul_by_7`** node

<figure><img src="../assets/Screenshot 2025-11-11 at 13.50.22.png" alt=""><figcaption></figcaption></figure>
