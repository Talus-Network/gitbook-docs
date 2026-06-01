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

# Deploy Workflows Tab

In the sidebar this panel is labeled **Deployment**. It allows users to **deploy any workflow created in the playground with a single click**. It works alongside the JSON Editor, which continuously monitors validation status to ensure the workflow is ready for on-chain deployment via the Sui wallet.

Before deploying, the tab lets you configure a few fields:

- **Choose workflow** — select which open draft to deploy.
- **Gas budget** — a **default of 0.1 SUI**, which users may increase if needed.
- **Name (optional)** and **Description (optional, up to 300 characters)** — metadata stored with the deployment.
- **Validation output** — a live panel that reflects the current validation status; the **Deploy** button stays disabled until the workflow is valid and a wallet is connected.

Key points:

- After a successful deployment, the playground automatically switches from **Edit Mode** to **View Mode**.
- The system displays the resulting **on-chain object ID**, confirming that the workflow is now deployed.

<figure><img src="../assets/7.png" alt=""><figcaption></figcaption></figure>
