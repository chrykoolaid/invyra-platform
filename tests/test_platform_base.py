"""Platform base foundation tests."""

from invyra_platform.core.constants import (
    AVAILABLE_COMMERCIAL_PRODUCT,
    FUTURE_MODULE_CODES,
    SUPPORTED_ENVIRONMENT_CODES,
)
from invyra_platform.organisations.models import Organisation
from invyra_platform.shared.enums import CommercialStatus, EnvironmentCode


def test_inventory_is_available_commercial_product() -> None:
    assert AVAILABLE_COMMERCIAL_PRODUCT == "inventory"


def test_future_modules_do_not_include_inventory() -> None:
    assert "inventory" not in FUTURE_MODULE_CODES
    assert "crm" in FUTURE_MODULE_CODES
    assert "pos" in FUTURE_MODULE_CODES


def test_supported_environment_codes_are_locked() -> None:
    assert SUPPORTED_ENVIRONMENT_CODES == {"LIVE", "TRAINING", "TEST"}
    assert EnvironmentCode.LIVE == "LIVE"
    assert EnvironmentCode.TRAINING == "TRAINING"
    assert EnvironmentCode.TEST == "TEST"


def test_commercial_status_values_are_locked() -> None:
    assert CommercialStatus.AVAILABLE == "available"
    assert CommercialStatus.COMING_LATER == "coming_later"
    assert CommercialStatus.INTERNAL_ONLY == "internal_only"
    assert CommercialStatus.DISABLED == "disabled"


def test_uuid_primary_key_column_shape() -> None:
    column = Organisation.__table__.columns["id"]

    assert column.primary_key is True
    assert column.nullable is False
    assert column.default is not None
