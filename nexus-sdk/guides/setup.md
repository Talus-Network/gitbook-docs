# 🔌 Setup Guide

This guide will help you quickly set up your development environment and start using Nexus SDK, including initializing your wallet, funding it through a faucet, and accessing the `devnet` Sui explorer.

## Installation and Setup

Follow these steps to install the Nexus CLI and set up your environment:

### Prerequisites

Make sure you have installed:

- [Rust](https://rustup.rs/) (latest stable)
- [Cargo](https://doc.rust-lang.org/cargo/getting-started/installation.html)
- [Sui](https://docs.sui.io/guides/developer/getting-started)

### Install the Nexus CLI

#### Using Homebrew (macOS/Linux)

```bash
brew tap talus-network/tap
brew install nexus-cli
```

or in one step:

```bash
brew install talus-network/tap/nexus-cli
```

#### Arch Linux

The [nexus-cli](https://aur.archlinux.org/packages/nexus-cli) is also available in the AUR (Arch User Repository). You can install it using your preferred [AUR helper](https://wiki.archlinux.org/title/AUR_helpers):

```bash
yay -S nexus-cli
```

#### Using cargo-binstall (recommended for faster binaries)

If you prefer quicker binary installation, use [cargo-binstall](https://github.com/cargo-bins/cargo-binstall):

```bash
cargo binstall --git https://github.com/talus-network/nexus-sdk nexus-cli
```

#### Using Cargo

To install directly from the source using `cargo`, run:

```bash
cargo install nexus-cli \
  --git https://github.com/talus-network/nexus-sdk \
  --tag v0.1.0 \
  --locked
```

### Verify the installation

```bash
nexus --version
```

It should print:

```bash
nexus-cli 0.1.0
```

## Configure the Talus devnet

{% hint style="warning" %}
The Talus `devnet` is currently private and accessible only through approved\
credentials. To request access, please submit your details using the form\
provided in the navigation bar.
{% endhint %}

Once you receive your credentials, first set them as environment variables in your terminal.\
Replace `my-username` and `my-password` with your actual credentials:

```bash
export NEXUS_USERNAME="my-username"
export NEXUS_PASSWORD="my-password"
```

Then, configure your Nexus CLI to connect to the Talus `devnet` by running:

```bash
nexus conf --sui.net devnet \
  --sui.basic-auth-user "$NEXUS_USERNAME" \
  --sui.basic-auth-password "$NEXUS_PASSWORD" \
  --nexus.primitives-pkg-id "0xaa132473ac02f2782b549596f6c4f3b39d2d6427dab6654b92666950722a80b0" \
  --nexus.workflow-pkg-id "0x4177e80a8da5d45e55e16b8075bf02ec8695e6f6a78b2694bfe7762afc2f500e" \
  --nexus.default-sap-object-id "0x779a768a7b34d9737ae654c3064ba040efc90996d595c891d1862d81e4141d33" \
  --nexus.tool-registry-object-id "0xa3be0bae7afe2628b2a35e23b1b2ec82a6f10bb973c3f73cf9c17ec394be83ae" \
  --nexus.network_id "0xcee192504b48a1306aa00217fa2714908e417ac07d1056e224fd2a4e0aac6e89"
```

Next, create a `.envrc` file to conveniently store your RPC and faucet URLs:

```bash
echo "export SUI_RPC_URL=https://rpc.ssfn.devnet.production.taluslabs.dev" > .envrc
echo "export SUI_FAUCET_URL=https://$NEXUS_USERNAME:$NEXUS_PASSWORD@faucet.devnet.production.taluslabs.dev/gas" >> .envrc
```

Activate these environment variables using:

```bash
source .envrc
```

{% hint style="success" %}
To automatically load these variables every time you navigate to the project\
directory, consider using [direnv](https://direnv.net/). After installing it,\
run `direnv allow` within your project directory.
{% endhint %}

### Configure the Sui client

After installing the Sui binaries, configure and activate your Talus `devnet`\
environment:

```bash
sui client new-env --alias devnet --rpc $SUI_RPC_URL \
  --basic-auth "$NEXUS_USERNAME":"$NEXUS_PASSWORD"
sui client switch --env devnet
```

## Create a wallet and request funds from the faucet

Create a new wallet with the following command:

```bash
sui client new-address ed25519 tally
```

{% hint style="danger" %}
This command will output your wallet details, including your address and\
recovery phrase. Ensure you store this information securely.
{% endhint %}

To request funds from the faucet, run:

```bash
sui client faucet --address tally --url $SUI_FAUCET_URL
```

To check the balance, run:

```bash
sui client balance tally
```

## Access Devnet Sui Explorer

Open the [Talus Sui Explorer](https://explorer.devnet.taluslabs.dev/) and log in using the credentials provided earlier.

---

After completing these steps, you are ready to build and execute workflows using the Nexus SDK. To build your first workflow, check the [Dev Quickstart guide](math-branching-quickstart.md).
