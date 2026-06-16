"""Portal session contract tests."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from invyra_platform.portal.contracts import (
    PortalDeviceDTO,
    PortalEnvironment,
    PortalEnvironmentDTO,
    PortalOrganisationDTO,
    PortalUserDTO,
)
from invyra_platform.portal.session_contracts import (
    PortalSessionContextDTO,
    PortalSessionDTO,
    PortalSessionRequest,
    PortalSessionResponse,
    PortalSessionStatus,
)


def test_portal_session_request_accepts_future_session_lookup_context() -> None:
    request = PortalSessionRequest(
        session_id="portal-session-001",
        auth_session_id="auth-session-001",
        user_id="user-001",
        organisation_id="org-001",
        device_id="device-001",
        environment=PortalEnvironment.LIVE,
        trace_id="trace-001",
    )

    assert request.session_id == "portal-session-001"
    assert request.environment == PortalEnvironment.LIVE
    assert request.trace_id == "trace-001"


def test_portal_session_request_restricts_environment_codes() -> None:
    with pytest.raises(ValidationError):
        PortalSessionRequest(environment="DEMO")


def test_active_portal_session_requires_identity_and_environment() -> None:
    with pytest.raises(ValidationError):
        PortalSessionDTO(status=PortalSessionStatus.ACTIVE, authenticated=True, session_id="portal-session-001")


def test_active_portal_session_accepts_complete_contract_shape() -> None:
    expires_at = datetime(2026, 1, 1, tzinfo=UTC)

    session = PortalSessionDTO(
        session_id="portal-session-001",
        auth_session_id="auth-session-001",
        status=PortalSessionStatus.ACTIVE,
        authenticated=True,
        user_id="user-001",
        organisation_id="org-001",
        environment=PortalEnvironment.TRAINING,
        expires_at=expires_at,
    )

    assert session.status == PortalSessionStatus.ACTIVE
    assert session.authenticated is True
    assert session.environment == PortalEnvironment.TRAINING
    assert session.expires_at == expires_at


def test_inactive_portal_session_cannot_be_authenticated() -> None:
    with pytest.raises(ValidationError):
        PortalSessionDTO(status=PortalSessionStatus.EXPIRED, authenticated=True)


def test_revoked_portal_session_requires_revoked_timestamp() -> None:
    with pytest.raises(ValidationError):
        PortalSessionDTO(status=PortalSessionStatus.REVOKED, authenticated=False)


def test_portal_session_context_accepts_safe_nested_dtos() -> None:
    context = PortalSessionContextDTO(
        user=PortalUserDTO(user_id="user-001", email="operator@example.com"),
        organisation=PortalOrganisationDTO(organisation_id="org-001", name="Invyra Demo"),
        environment=PortalEnvironmentDTO(environment=PortalEnvironment.TEST, is_selected=True),
        device=PortalDeviceDTO(device_id="device-001", trusted=True, registered=True),
    )

    assert context.user is not None
    assert context.user.user_id == "user-001"
    assert context.organisation is not None
    assert context.organisation.name == "Invyra Demo"
    assert context.environment is not None
    assert context.environment.environment == PortalEnvironment.TEST
    assert context.device is not None
    assert context.device.trusted is True


def test_authenticated_portal_response_requires_active_session() -> None:
    with pytest.raises(ValidationError):
        PortalSessionResponse(authenticated=True, session=PortalSessionDTO(status=PortalSessionStatus.UNKNOWN))


def test_authenticated_portal_response_requires_user_and_organisation_context() -> None:
    active_session = PortalSessionDTO(
        session_id="portal-session-001",
        status=PortalSessionStatus.ACTIVE,
        authenticated=True,
        user_id="user-001",
        organisation_id="org-001",
        environment=PortalEnvironment.LIVE,
    )

    with pytest.raises(ValidationError):
        PortalSessionResponse(authenticated=True, session=active_session)


def test_authenticated_portal_response_accepts_complete_contract_shape() -> None:
    active_session = PortalSessionDTO(
        session_id="portal-session-001",
        status=PortalSessionStatus.ACTIVE,
        authenticated=True,
        user_id="user-001",
        organisation_id="org-001",
        environment=PortalEnvironment.LIVE,
    )
    context = PortalSessionContextDTO(
        user=PortalUserDTO(user_id="user-001", email="operator@example.com"),
        organisation=PortalOrganisationDTO(organisation_id="org-001", name="Invyra Demo"),
    )

    response = PortalSessionResponse(authenticated=True, session=active_session, context=context)

    assert response.authenticated is True
    assert response.session is active_session
    assert response.context is context


def test_portal_session_contracts_forbid_runtime_credential_fields() -> None:
    with pytest.raises(ValidationError):
        PortalSessionDTO(
            session_id="portal-session-001",
            status=PortalSessionStatus.UNKNOWN,
            credential_value="not-allowed",
        )
