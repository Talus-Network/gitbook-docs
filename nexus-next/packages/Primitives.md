# Primitives Package

> concerns [`sui/primitives` package][repo-primitives-package]

Exports types that allow two Sui packages, A and B, to communicate with each other in an authenticated way without using explicit Move dependencies.
Instead, A and B have a shared dependency on this package, `nexus_primitives`.
As long as A knowns an ID of any object created by B, that object's ID serves as the authentication because only B can access the object's [UID] property.
This is achieved with the [hot potato pattern][move-hot-potato]

This is a step away from explicitness and towards conventions.
Prior similar work includes [Originbyte's `request` module][ob-request-module] and [Mysten's `transfer_policy` module][sui-transfer-policy].

## Why is this useful?

Avoiding explicit dependencies shifts complexity from the Move code to the off-chain realm.
It is the off-chain realm's responsibility to craft programmable transactions such that the expectations of the on-chain realm are met.

Thanks to this trade-off the system is more amiable to plug-and-play components.
Payments, workflows, verifications, those can have on-chain design that minimizes the need for explicit dependencies between each other.
Therefore, upgrading components is less likely to require changes to other components.

<!-- List of References -->

[repo-primitives-package]: https://github.com/Talus-Network/nexus-next/tree/main/sui/primitives
[move-hot-potato]: https://move-book.com/programmability/hot-potato-pattern.html
[ob-request-module]: https://github.com/Origin-Byte/nft-protocol/tree/main/contracts/request/sources/request
[sui-transfer-policy]: https://github.com/MystenLabs/sui/blob/main/crates/sui-framework/packages/sui-framework/sources/kiosk/transfer_policy.move
