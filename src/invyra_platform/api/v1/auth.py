"""Authentication API route skeletons.

Routes in this module expose contract-only boundaries for future portal/UI
integration. They intentionally return AuthRuntimeService skeleton results and
must not perform real authentication, token issuance, email sending, or database
writes in PF2 Sprint 14.3.
"""

from fastapi import APIRouter

from invyra_platform.api.contracts import ApiResponse
from invyra_platform.api.v1.auth_contracts import (
    LoginRequest,
    LogoutRequest,
    PasswordResetConfirmRequest,
    PasswordResetRequest,
    RefreshRequest,
)
from invyra_platform.auth.service import AuthRuntimeService

router = APIRouter(prefix="/auth", tags=["auth"])


def _auth_service() -> AuthRuntimeService:
    return AuthRuntimeService()


@router.post("/login", response_model=ApiResponse)
def login(_: LoginRequest) -> ApiResponse:
    """Future login boundary."""
    return ApiResponse.from_service_result(_auth_service().login(), message="Auth login skeleton only.")


@router.post("/logout", response_model=ApiResponse)
def logout(_: LogoutRequest) -> ApiResponse:
    """Future logout boundary."""
    return ApiResponse.from_service_result(_auth_service().logout(), message="Auth logout skeleton only.")


@router.post("/refresh", response_model=ApiResponse)
def refresh(_: RefreshRequest) -> ApiResponse:
    """Future refresh-token/session refresh boundary."""
    return ApiResponse.from_service_result(
        _auth_service().refresh_session(),
        message="Auth refresh skeleton only.",
    )


@router.post("/password-reset/request", response_model=ApiResponse)
def request_password_reset(_: PasswordResetRequest) -> ApiResponse:
    """Future password reset request boundary."""
    return ApiResponse.from_service_result(
        _auth_service().request_password_reset(),
        message="Auth password reset request skeleton only.",
    )


@router.post("/password-reset/confirm", response_model=ApiResponse)
def confirm_password_reset(_: PasswordResetConfirmRequest) -> ApiResponse:
    """Future password reset consumption boundary."""
    return ApiResponse.from_service_result(
        _auth_service().consume_password_reset(),
        message="Auth password reset confirm skeleton only.",
    )


@router.get("/session", response_model=ApiResponse)
def session() -> ApiResponse:
    """Future current-session boundary."""
    return ApiResponse.from_service_result(
        _auth_service().record_auth_security_event(),
        message="Auth session skeleton only.",
    )
