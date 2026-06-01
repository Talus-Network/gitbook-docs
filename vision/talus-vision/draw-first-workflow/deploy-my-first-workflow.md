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

# Deploy My First Workflow

On the previous page, we created a valid workflow. The next step is to deploy this workflow **on-chain**. Up to this point, all actions focused on creating a valid workflow, continuously validated by built-in checks. Now it’s time to deploy the workflow on **Sui** (the deployment targets whichever network—Testnet or Mainnet—is selected in the header).

Before deploying, make sure the following steps are completed:

1. **Gas Management:**  
   Go to the **Gas Management** tab and add a **SUI gas budget** large enough to cover deployment costs.

1. **Key Setup:**  
   If a key icon appears in the application header, click it and complete the one-time **Key Setup** (tool signing key generation). No wallet transaction is required for this step.

Once preparation is complete, navigate to the **Deployment** tab in the sidebar to deploy your workflow.

Since deployment happens **on-chain**, a transaction will be initiated through your **Sui wallet**, and you will be asked to approve it. After the transaction succeeds, the current diagram in the editor will automatically switch from **Edit Mode** to **View Mode**.

<figure>
  <img src="../assets/Screenshot 2025-11-11 at 13.44.29.png" alt="">
  <figcaption></figcaption>
</figure>

<figure>
  <img src="../assets/Screenshot 2025-11-11 at 13.44.41.png" alt="">
  <figcaption></figcaption>
</figure>
