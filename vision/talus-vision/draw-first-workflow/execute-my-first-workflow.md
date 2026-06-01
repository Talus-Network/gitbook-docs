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

# Execute My First Workflow

Now that the workflow has been fully validated and deployed as an **on-chain object**, the next step is to execute it and observe the outputs.

Navigate to the **Execute Workflow** tab, enter the required inputs, and run the DAG **on-chain**.

In this example, the workflow requires a single numeric input at the **`add_input_and_default`** node. Since the playground is now in **View Mode**, only the necessary input fields are shown. After providing the input, the console will display the execution result.

For an input of **12**, the step-by-step evaluation is:

- **`add_input_and_default` output:** 12 + 3 = 15
- **`is_negative` output:** 15 compared to 0 → **greater than**, triggering the `gt` branch
- **Final result:** Execution proceeds to **`mul_by_7`**, which produces the final output

<figure><img src="../assets/Screenshot 2025-11-11 at 13.50.22.png" alt=""><figcaption></figcaption></figure>
