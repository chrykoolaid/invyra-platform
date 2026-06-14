"""Platform constants."""

AVAILABLE_COMMERCIAL_PRODUCT = "inventory"

FUTURE_MODULE_CODES = frozenset(
    {
        "crm",
        "pos",
        "payroll",
        "workforce_management",
        "forecasting",
        "purchasing_extensions",
    }
)

SUPPORTED_ENVIRONMENT_CODES = frozenset({"LIVE", "TRAINING", "TEST"})
