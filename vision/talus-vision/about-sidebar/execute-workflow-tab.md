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

# Execute Workflow Tab

This tab allows users to run any workflow they have already deployed. After providing the required inputs in the playground, the workflow can be executed directly from here.

- **On-chain execution:** All operations run on-chain, ensuring transparent and verifiable results.
- **Execution output:** The console displays the full transaction output, making it easy to inspect execution details.
- **Entry group support:** If a workflow contains multiple entry groups, the tab validates inputs after the user selects which group to run, ensuring a smooth and error-free execution experience.

<figure><img src="../assets/10.png" alt=""><figcaption></figcaption></figure>

## Execution Settings

Before running, you can configure:

- **DAG to be executed** and **Entry port to be used** — select the deployed workflow and, when several exist, the entry group.
- **Gas budget** — defaults to **0.1 SUI**.
- **Priority fee per gas unit** — optional for immediate execution; used to prioritize the run.
- **Cost estimate** — for immediate execution, the tab estimates the run cost from the tools used and shows it against your gas budget balance.
- **Network** — read-only here; change it from the header network switcher and it applies app-wide.

After a run completes, an **Execution Payment Breakdown** card shows how the cost was charged, and your budget balance refreshes automatically.

## Execution Modes

The **Execution Mode** selector offers two ways to run a workflow:

- **Execute DAG (Immediate):** runs the workflow once, right away.
- **Create Task:** creates a scheduled task instead of running immediately. Choose a **Generator Type**:
  - **Queue** — after the task is created, you add occurrences manually (each occurrence triggers one run).
  - **Periodic** — after the task is created, you set a recurring schedule.

Created tasks can be reviewed at any time through the **My Tasks** button, where you can pause, resume, or cancel a task, add occurrences, view the queue, and inspect periodic schedules. Tasks are also visible network-wide in the [Explorer](../explorer.md).

## Walrus Remote Storage (Optional)

For immediate execution, an optional **Walrus remote storage** section lets you upload selected port data to Walrus and reference it by blob ID in the transaction instead of sending it inline. Provide a publisher URL, the target ports, and the number of epochs (1–53) to keep the data.
