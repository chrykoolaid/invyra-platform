"""Portal route-to-adapter refactor tests."""

from pathlib import Path

from fastapi.testclient import TestClient

from invyra_platform.app import create_app


def test_portal_routes_still_return_existing_skeleton_contracts_after_adapter_refactor() -> None:
    client = TestClient(create_app())

    route_cases = [
        ("get", "/api/v1/portal/status", None, "Portal API boundary skeleton only."),
        ("post", "/api/v1/portal/session", {}, "Portal session boundary skeleton only."),
        (
            "post",
            "/api/v1/portal/navigation",
            {"user_id": "user-001", "organisation_id": "org-001", "environment": "LIVE"},
            "Portal navigation boundary skeleton only.",
        ),
        (
            "post",
            "/api/v1/portal/entitlements",
            {"user_id": "user-001", "organisation_id": "org-001", "environment": "LIVE"},
            "Portal entitlement boundary skeleton only.",
        ),
        (
            "post",
            "/api/v1/portal/inventory-entry",
            {"user_id": "user-001", "organisation_id": "org-001", "environment": "LIVE"},
            "Portal Inventory entry boundary skeleton only.",
        ),
    ]

    for method, path, payload, expected_message in route_cases:
        if method == "post":
            response = client.post(path, json=payload)
        else:
            response = client.get(path)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is False
        assert body["code"] == "NOT_IMPLEMENTED"
        assert body["message"] == expected_message
        assert body["errors"][0]["code"] == "SERVICE_SKELETON_ONLY"


def test_portal_route_layer_delegates_to_adapter_builders() -> None:
    route_source = Path("src/invyra_platform/api/v1/portal.py").read_text(encoding="utf-8")

    assert "from invyra_platform.api.v1.portal_adapters import" in route_source
    assert "build_portal_status_result()" in route_source
    assert "build_portal_session_result(request)" in route_source
    assert "build_portal_navigation_result(request)" in route_source
    assert "build_portal_entitlement_result(request)" in route_source
    assert "build_portal_inventory_entry_result(request)" in route_source


def test_portal_route_layer_no_longer_builds_response_dtos_directly() -> None:
    route_source = Path("src/invyra_platform/api/v1/portal.py").read_text(encoding="utf-8")

    assert "PortalSessionResponse(" not in route_source
    assert "PortalNavigationResponse(" not in route_source
    assert "PortalEntitlementResponse(" not in route_source
    assert "PortalInventoryEntryResponse(" not in route_source
    assert "PortalInventoryEntryDTO(" not in route_source
    assert "ServiceResult.not_implemented" not in route_source
