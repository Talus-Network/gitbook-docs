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

**Nexus Crypto Auth** generates an secure Signal like **Session** /Channel between an user and **nexus**. Its not an authentication system.

Nexus encrypts every sensitive value using a Signal-inspired stack: a persistent master key protects secrets at rest, an X3DH identity key authenticates you to the network, and a Double-Ratchet session derived from an on-chain pre-key encrypts runtime traffic.

On first use, a unique master key is generated in your browser. The master key is a 32-byte key that is used to encrypt and decrypt stored data (identity key, sessions, credentials) in your browser. The session is encrypted with the master key before being stored locally to prevent unauthorized access.

Subsequently, two operations are performed on the Sui blockchain:

1. A PreKey (encryption key) is requested on your behalf.
1. An encrypted session is initiated using the X3DH protocol and recorded on the blockchain. X3DH is a handshake algorithm used to establish a secure session between two parties.

The master key is used to encrypt the session before it is saved locally in your browser. The session is used to generate encryption keys for data passed through Nexus. This encrypted session data is then used to encrypt and decrypt your data when executing encrypted workflows. All keys are stored exclusively in your browser, and all blockchain operations are signed with your Sui wallet.

For more technical details, see the [Setup Guide](https://docs.talus.network/staging/getting-started/setup) and [CLI Documentation](https://docs.talus.network/staging/developer-docs/index-1/cli).

After logging in with your wallet, if the Nexus Crypto Auth process has not been completed previously, you will need to perform it. A dedicated button for this action is available in the application header.

All you need to do is **sign the generated transactions**. Completing this step is required before you can perform any **Nexus operations**.

<figure><img src="assets/Screenshot 2025-11-11 at 12.20.26.png" alt=""><figcaption></figcaption></figure>
