"""Apply Alembic migrations for local development."""

from alembic import command as alembic_command
from alembic.config import Config


def main() -> None:
    cfg = Config("alembic.ini")
    alembic_command.upgrade(cfg, "head")


if __name__ == "__main__":
    main()
