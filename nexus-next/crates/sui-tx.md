# Leader SUI Transactions

The Leader will be assigned a wallet via the `SUI_SECRET_MNEMONIC` environment variable. This wallet will hold N `leader_cap`s. These are owned objects that are used to verify that the transaction (TX) submission was performed by the Leader and are created and transferred to the leader upon deploying the Nexus onchain packages. On Sui, to avoid [equivocation](https://docs.sui.io/guides/developer/sui-101/avoid-equivocation), only one parallel TX can be sent per-`leader_cap`. The wallet is assigned N `Coin<Sui>` objects as gas (on mainnet) or Coin objects are poured from a faucet (on localnet and testnet).

{% hint style="warning" %} Important thing to note is that, upon a failed transaction, Sui will lock all objects associated with the transaction until the next epoch, which is 24 hours. That means that we need to "damage" a `leader_cap` if a transaction fails and not use it for the next 24 hours. {% endhint %}

Initially, there will only be one transaction type from Leader back to Workflow. This transaction notifies the Workflow of the Tool invocation result. More details are available in the [Leader](leader.md) documentation.

Once onchain Tools are defined, the Leader will also have to send transactions to invoke these Tools. These are currently still in the design phase however.
