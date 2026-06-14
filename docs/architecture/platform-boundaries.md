# Platform Boundaries

## Purpose

`invyra-platform` is the production SaaS control layer for Invyra.

It owns:

- Authentication foundation
- Organisations and tenant resolution
- Users, roles, and permissions
- Licensing and entitlements
- Devices
- LIVE / TRAINING / TEST environment control
- Portal runtime
- Inventory launch eligibility
- Audit
- Support

## Explicit Non-Goals

This repository does not own:

- Marketing website pages
- Static GitHub Pages deployment
- CRM runtime
- POS runtime
- Inventory item master
- Stock movements
- Receiving
- Transfers
- Stocktakes
- Wastage
- Markdown
- Supplier pricebooks
- Inventory reports
- Inventory intelligence outputs

## Repository Split

```text
invyra-website
  Marketing, documentation, support content, roadmap pages, static previews.

invyra-platform
  Production SaaS control layer and Inventory launch gate.

invyra-inventory
  Inventory runtime and operational workflows.
```

## Commercial Lock

Inventory is the first commercial product.

CRM, POS, Payroll, Workforce Management, Forecasting, and Purchasing Extensions remain future modules until explicitly unlocked.
