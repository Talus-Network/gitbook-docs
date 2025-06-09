# Gas extensions example

Gas extensions provide the ability for tool owners to provide gas tickets to users for custom payment strategies.

Nexus considers two default modes of operation for gas tickets: expiry and limited invocations. The implementation in move code is provided below as an inspiration for custom gas extensions that leverage the `UponDiscretionOfTool` modus operandi.

## Implementation of default gas extension (expiry based)

Toggle to see the full module code for the default gas extension move module:
<details>

<summary>Toggle code</summary>

```rust
use nexus_workflow::gas;
use nexus_workflow::tool_registry::ToolRegistry;
use std::ascii::String as AsciiString;
use sui::clock::Clock;
use sui::coin::Coin;
use sui::sui::SUI;

// === Errors ===

#[error]
const EThisMethodIsNotEnabled: vector<u8> = b"This method is not enabled";

// === Expiry Extension ===

/// How many [SUI] tokens should be paid for each minute.
public struct ExpiryCostPerMinuteKey has copy, drop, store {}
/// Will hold the gas owner cap to do requests on behalf of the tool owner.
public struct ExpiryGasOwnerCapKey has copy, drop, store {}

public entry fun buy_expiry_gas_ticket(
    gas_service: &mut gas::GasService,
    tool_registry: &ToolRegistry,
    fqn: AsciiString,
    minutes: u64,
    pay_with: &mut Coin<SUI>,
    clock: &Clock,
    ctx: &mut TxContext,
) {
    let settings = gas_service.get_tool_gas_setting(fqn);

    assert!(settings.contains(ExpiryGasOwnerCapKey {}), EThisMethodIsNotEnabled);
    let owner_cap = settings
        .borrow<_, CloneableOwnerCap<gas::OverGas>>(ExpiryGasOwnerCapKey {})
        .clone(ctx);

    let cost_per_minute = *settings.borrow<_, u64>(ExpiryCostPerMinuteKey {});

    gas_service.add_gas_ticket(
        tool_registry,
        &owner_cap,
        fqn,
        gas::scope_invoker_address(ctx.sender()),
        gas::modus_operandi_expiry(minutes * 60 * 1000),
        clock,
        ctx,
    );
    owner_cap.destroy();

    gas_service.donate_to_tool(fqn, pay_with.balance_mut().split(cost_per_minute * minutes));
}

/// Enables buying gas tickets that expire after a certain time in token
/// [SUI] for [cost_per_minute] of those tokens.
///
/// To update the cost just call this function again with the new value.
public fun enable_expiry(
    gas_service: &mut gas::GasService,
    tool_registry: &ToolRegistry,
    owner_cap: &CloneableOwnerCap<gas::OverGas>,
    cost_per_minute: u64,
    fqn: AsciiString,
    ctx: &mut TxContext,
) {
    let owner_cap = owner_cap.clone(ctx);

    let settings = gas_service.get_tool_gas_setting_mut(
        tool_registry,
        &owner_cap,
        fqn,
        ctx,
    );

    if (!settings.contains(ExpiryGasOwnerCapKey {})) {
        settings.add(ExpiryGasOwnerCapKey {}, owner_cap);
    } else {
        owner_cap.destroy();
    };

    let cost_per_minute_key = ExpiryCostPerMinuteKey {};

    if (settings.contains(cost_per_minute_key)) {
        // already configured, let's reset it

        settings.remove<_, u64>(cost_per_minute_key);
    };

    settings.add(cost_per_minute_key, cost_per_minute);
}

/// Disables this extension.
public fun disable_expiry(
    gas_service: &mut gas::GasService,
    tool_registry: &ToolRegistry,
    owner_cap: &CloneableOwnerCap<gas::OverGas>,
    fqn: AsciiString,
    ctx: &mut TxContext,
) {
    let settings = gas_service.get_tool_gas_setting_mut(
        tool_registry,
        owner_cap,
        fqn,
        ctx,
    );

    if (settings.contains(ExpiryGasOwnerCapKey {})) {
        settings
            .remove<_, CloneableOwnerCap<gas::OverGas>>(ExpiryGasOwnerCapKey {})
            .destroy();
    };

    let cost_per_minute_key = ExpiryCostPerMinuteKey {};

    if (settings.contains(cost_per_minute_key)) {
        settings.remove<_, u64>(cost_per_minute_key);
    };
}
```

</details>
