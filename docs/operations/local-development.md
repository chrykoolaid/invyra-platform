# Local Development

## Current Sprint Scope

PF2 Sprint 1 provides a backend skeleton only.

Implemented:

- FastAPI app shell
- Health endpoints
- Configuration layer
- SQLAlchemy database foundation
- Alembic migration foundation
- Pytest harness
- Docker Compose foundation
- CI skeleton

Not implemented yet:

- Real login
- Real users
- Real organisations
- Real licensing
- Real device validation
- Real environment switching
- Real Inventory launch
- CRM
- POS
- Inventory operations

## Setup

```bash
cp .env.example .env.local
make install
make db-up
make migrate
make dev
```

## Test

```bash
make test
make lint
make typecheck
```

## Health Checks

```text
GET /health
GET /api/v1/health
```

## Environment Rule

Only `.env.example` is committed.

Do not commit:

```text
.env
.env.local
.env.test
.env.production
```

## Future Module Lock

The following must remain disabled by default:

```text
ALLOW_CRM=false
ALLOW_POS=false
ALLOW_PAYROLL=false
ALLOW_WORKFORCE_MANAGEMENT=false
ALLOW_FORECASTING=false
ALLOW_PURCHASING_EXTENSIONS=false
```
