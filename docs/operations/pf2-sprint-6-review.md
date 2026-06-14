# PF2 Sprint 6 Review

## Status

```text
PF2 Sprint 6: COMPLETED
Repository: invyra-platform
Scope: Licensing and Inventory entitlement data foundation
```

## Completed

- Added licensing module package.
- Added `LicenseProduct` model.
- Added `License` model.
- Added `LicenseEntitlement` model.
- Added `LicenseSeat` model.
- Added `LicenseEvent` model.
- Registered licensing models in Alembic environment.
- Added migration `005_licensing_entitlements_foundation`.
- Added licensing foundation tests.

## Migration Added

```text
migrations/versions/005_licensing_entitlements_foundation.py
```

Creates:

```text
license_products
licenses
license_entitlements
license_seats
license_events
```

## Commercial Lock

Inventory remains the only available commercial product path.

Future modules remain blocked:

```text
CRM
POS
Payroll
Workforce Management
Forecasting
Purchasing Extensions
```

They may exist as future product codes later, but they must not receive production launch entitlement until explicitly unlocked.

## Preserved Boundaries

No website files were added.

No CRM or POS runtime was added.

No Inventory operation logic was added.

No login endpoint, password reset endpoint, token issuance, device validation, environment switching, portal runtime, support workflow, or Inventory launch was added.

## Important Lock

Licensing controls commercial access.

It does not perform Inventory operations.

Inventory launch eligibility will later check licensing, but stock movements, receiving, transfers, stocktakes, wastage, markdowns, suppliers, and reports remain in `invyra-inventory`.

## Next Recommended Phase

```text
PF2 Sprint 7 — Devices Foundation
```

Sprint 7 should add device registration and device assignment data structures only.
