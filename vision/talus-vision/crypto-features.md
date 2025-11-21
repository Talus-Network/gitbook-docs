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

Nexus Crypto Auth establishes a secure, Signal-like encrypted channel between you and Nexus. It is **not** an authentication system.

Nexus secures all sensitive data using a Signal-inspired cryptographic stack:

- A persistent master key protects secrets at rest.
- An X3DH identity key authenticates you to the network.
- A Double-Ratchet session derived from an on-chain pre-key encrypts all runtime traffic.

On first use, a unique 32-byte master key is generated in your browser. This key is used to encrypt and decrypt all local data—including your identity key, sessions, and credentials. Each session is encrypted with the master key before being saved, preventing unauthorized access.

After initialization, Nexus performs two operations on the Sui blockchain:

1. A PreKey (encryption key) is requested on your behalf.
1. A secure session is initiated using the X3DH protocol and recorded on-chain. X3DH is a handshake algorithm used to establish encrypted channels between two parties.

The master key encrypts the session before it is stored locally in your browser. This session then derives all encryption keys used for data passed through Nexus. These keys encrypt and decrypt your data when executing encrypted workflows. All keys remain exclusively in your browser, and all blockchain interactions are signed with your Sui wallet.

For more technical details, see the [Setup Guide](https://docs.talus.network/staging/getting-started/setup) and the [CLI Documentation](https://docs.talus.network/staging/developer-docs/index-1/cli).

After logging in with your wallet, if Nexus Crypto Auth has not been completed previously, the application will prompt you to complete it using a dedicated button in the header.

All you need to do is **sign the generated transactions**. Completing this step is required before performing any Nexus operations.

<figure><img src="assets/Screenshot 2025-11-11 at 12.20.26.png" alt=""><figcaption></figcaption></figure>
