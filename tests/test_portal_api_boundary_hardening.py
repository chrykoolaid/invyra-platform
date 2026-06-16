"""Portal API boundary hardening tests."""

from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

from invyra_platform.app import create_app

PORTAL_ROUTE_CASES = [
    ("get", "/api/v1/portal/status", None),
    ("post", "/api/v1/portal/session", {}),
    (
        "post",
        "/api/v1/portal/navigation",
        {"user_id": "user-001", "organisation_id": "org-001", "environment": "LIVE"},
    ),
    (
        "post",
        "/api/v1/portal/entitlements",
        {"user_id": "user-001", "organisation_id": "org-001", "environment": "LIVE"},
    ),
    (
        "post",
        "/api/v1/portal/inventory-entry",
        {"user_id": "user-001", "organisation_id": "org-001", "environment": "LIVE"},
    ),
]

RUNTIME_DATA_KEYS = {
    "stock",
    "stock_on_hand",
    "orders",
    "purchase_orders",
    "receiving",
    "transfers",
    "stocktake",
    "wastage",
    "markdowns",
    "reports",
    "inventory_items",
    "item_id",
    "sku",
    "quantity",
}

TOKEN_AND_RUNTIME_SESSION_KEYS = {
    "access_token",
    "refresh_token",
    "reset_token",
    "launch_token",
    "launch_session_id",
    "inventory_launch_session_id",
}

FORBIDDEN_PORTAL_API_IMPORTS_OR_CALLS = {
    "from sqlalchemy",
    "import sqlalchemy",
    "from invyra_platform.db",
    "from invyra_platform.database",
    "from invyra_platform.models",
    "from invyra_platform.api.dependencies import",
    "get_auth_runtime_service",
    "get_inventory_access_gateway_service",
    "get_inventory_launch_service",
    "AuthRuntimeService",
    "InventoryAccessGatewayService",
    "InventoryLaunchService",
    "Depends(",
}


def _request(client: TestClient, method: str, path: str, payload: dict[str, Any] | None):
    if method == "post":
        return client.post(path, json=payload)
    return client.get(path)


def _iter_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        keys = set(value.keys())
        for nested in value.values():
            keys.update(_iter_keys(nested))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(_iter_keys(item))
        return keys
    return set()


def test_all_portal_routes_remain_api_response_skeletons() -> None:
    client = TestClient(create_app())

    for method, path, payload in PORTAL_ROUTE_CASES:
        response = _request(client, method, path, payload)

        assert response.status_code == 200
        body = response.json()
        assert set(body) == {"success", "code", "message", "data", "errors", "trace_id"}
        assert body["success"] is False
        assert body["code"] == "NOT_IMPLEMENTED"
        assert body["errors"][0]["code"] == "SERVICE_SKELETON_ONLY"


def test_portal_routes_do_not_expose_inventory_runtime_data() -> None:
    client = TestClient(create_app())

    for method, path, payload in PORTAL_ROUTE_CASES:
        response = _request(client, method, path, payload)

        assert response.status_code == 200
        data_keys = _iter_keys(response.json()["data"])
        assert data_keys.isdisjoint(RUNTIME_DATA_KEYS)


def test_portal_routes_do_not_create_tokens_or_runtime_sessions() -> None:
    client = TestClient(create_app())

    for method, path, payload in PORTAL_ROUTE_CASES:
        response = _request(client, method, path, payload)

        assert response.status_code == 200
        data = response.json()["data"]
        data_keys = _iter_keys(data)
        assert data_keys.isdisjoint(TOKEN_AND_RUNTIME_SESSION_KEYS)

        if isinstance(data, dict) and "session" in data:
            assert data["session"] is None

        if isinstance(data, dict) and "entry" in data:
            entry = data["entry"]
            assert entry["enabled"] is False
            assert entry["entry_allowed"] is False
            assert entry["availability"]["allowed"] is False


def test_portal_entitlements_keep_future_modules_unexposed() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/portal/entitlements",
        json={
            "user_id": "user-001",
            "organisation_id": "org-001",
            "environment": "LIVE",
            "include_future_modules": True,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == "NOT_IMPLEMENTED"
    assert body["data"]["groups"] == []


def test_portal_api_file_has_no_runtime_or_database_dependencies() -> None:
    portal_api_source = Path("src/invyra_platform/api/v1/portal.py").read_text(encoding="utf-8")

    for forbidden in FORBIDDEN_PORTAL_API_IMPORTS_OR_CALLS:
        assert forbidden not in portal_api_source


def test_portal_api_sprint_does_not_introduce_portal_migrations() -> None:
    migration_versions_path = Path("migrations/versions")

    if not migration_versions_path.exists():
        return

    portal_migration_files = [
        path for path in migration_versions_path.glob("*.py") if "portal" in path.name.lower()
    ]

    assert portal_migration_files == []
