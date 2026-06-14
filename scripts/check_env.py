"""Check local environment safety."""

from invyra_platform.core.config import get_settings


def main() -> None:
    settings = get_settings()
    settings.validate_production_safety()
    print(f"Environment OK: {settings.app_env}")


if __name__ == "__main__":
    main()
