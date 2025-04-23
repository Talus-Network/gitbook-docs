# Sui Move Conventions

In Nexus and related packages we (to the best of our ability) follow these conventions.

## Enum's `_variant_name`

Each enumeration variant contains property `_variant_name: AsciiString` which will always be a static string of the variant name.
This helps clients to identify the variant because at the moment RPCs do not include the variant name in the response.
