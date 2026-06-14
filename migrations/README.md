# Alembic Migrations

This directory owns Invyra Platform database migrations.

PF2 Sprint 1 creates the migration foundation only.

The first real business migration should be introduced later as:

```text
001_platform_base
```

Migration rules:

- SQLAlchemy models and Alembic revisions must be committed together.
- Migrations must be reviewed before production use.
- Manual production database edits are not allowed.
