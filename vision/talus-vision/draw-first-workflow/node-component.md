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

# Node Component

Each tool added to the playground is transformed into a **node** within the workspace. These nodes are then converted into vertices following Nexus standards. Users can freely modify any node directly in the playground.

When examining a node, you will find the following features:

- **Editable names** — click the pencil icon to rename a node.
- **Quick deletion** — remove a node instantly from the playground.
- **Lockable positions** — use the anchor icon to lock a node in place during design.

<figure>
<img src="../assets/Screenshot 2025-11-11 at 12.35.00.png" alt="">
<figcaption></figcaption>
</figure>

Each node consists of two main sections:

## Inputs

The **Inputs** section allows users to configure all input parameters. For each input you can toggle:

- **Use as entry port** — expose the input as an entry point that receives a value at execution time.
- **Use as default value** — provide a fixed value baked into the workflow instead of an entry port.

Any change made here is immediately reflected in the DAG JSON within the JSON Editor.

<figure>
<img src="../assets/Screenshot 2025-11-11 at 12.47.24.png" alt="">
<figcaption></figcaption>
</figure>

Users can also create multiple entry groups by clicking **Add Entry Group**.

<figure>
<img src="../assets/Screenshot 2025-11-11 at 12.43.43.png" alt="">
<figcaption></figcaption>
</figure>

## Outputs

The **Outputs** section is used to create connections (edges) between nodes. When connecting an output to another node, users are prompted to select the appropriate port, ensuring a smooth and intuitive workflow-building experience.

<figure>
<img src="../assets/Screenshot 2025-11-11 at 12.43.56 (1).png" alt="">
<figcaption></figcaption>
</figure>

<figure>
<img src="../assets/Screenshot 2025-11-11 at 12.44.10.png" alt="">
<figcaption></figcaption>
</figure>
