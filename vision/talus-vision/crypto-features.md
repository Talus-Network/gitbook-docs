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

# Crypto Features

**Nexus Crypto Auth** is a **secure authentication system** required to execute **encrypted workflows**. On first use, a unique **master key** is generated in your browser and stored in encrypted form.

Subsequently, two operations are performed on the **Sui blockchain**:

1. A **PreKey (encryption key)** is requested on your behalf.
2. An **encrypted session** is initiated using the **X3DH protocol** and recorded on the blockchain.

The session data is stored locally in your browser and is used to **encrypt and decrypt your data** when executing encrypted workflows. All keys are stored **exclusively in your browser**, and all blockchain operations are **signed with your Sui wallet**.

After logging in with your wallet, if the **Nexus Crypto Auth** process has not been completed previously, you will need to perform it. A dedicated button for this action is available in the **application header**.

All you need to do is **sign the generated transactions**. Completing this step is required before you can perform any **Nexus operations**.\
\

<figure><img src="assets/Screenshot 2025-11-11 at 12.20.26.png" alt=""><figcaption></figcaption></figure>
