# Invyra Platform

Production SaaS platform foundation for Invyra.

## Repository Purpose

`invyra-platform` owns the production platform control layer:

- Authentication foundation
- Organisations / tenant resolution
- Users, roles, and permissions
- Licensing and entitlements
- Devices
- LIVE / TRAINING / TEST environments
- Portal runtime
- Inventory launch control
- Audit
- Support

## Repository Boundaries

This repository does **not** own:

- Public marketing website pages
- GitHub Pages deployment
- CRM runtime
- POS runtime
- Inventory stock operations
- Receiving workflows
- Transfer workflows
- Stocktake workflows
- Wastage workflows
- Markdown workflows
- Purchase orders
- Supplier pricebooks
- Inventory reporting logic

Those belong in separate repositories:

- `invyra-website` — public website, documentation, support content, static previews
- `invyra-inventory` — inventory runtime and inventory operations

## Commercial Direction

Current commercial product:

- Invyra Inventory

Future modules remain unavailable until explicitly unlocked:

- CRM
- POS
- Payroll
- Workforce Management
- Forecasting
- Purchasing Extensions

## PF2 Sprint 1 Scope

This sprint creates the backend skeleton only:

- FastAPI app shell
- Versioned API router
- Health endpoint
- Configuration layer
- SQLAlchemy database foundation
- Alembic migration foundation
- Test harness
- Local Docker Compose foundation
- CI skeleton

No real authentication, licensing, device validation, inventory launch, CRM, POS, or website files are implemented in this sprint.

## Local Development

Planned local workflow:

```bash
cp .env.example .env.local
make install
make db-up
make migrate
make dev
make test
```

## Status

```text
PF2 Sprint 1 backend skeleton: in progress
Production deployment: not started
Authentication implementation: not started
Inventory launch implementation: not started
```
