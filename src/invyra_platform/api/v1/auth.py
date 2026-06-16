"""Authentication API route skeletons."""

from typing import Annotated

from fastapi import APIRouter, Depends

from invyra_platform.api.adapters import map_service_result_to_api_response
from invyra_platform.api.contracts import ApiResponse
from invyra_platform.api.dependencies import get_auth_runtime_service
from invyra_platform.api.v1.auth_contracts import (
    LoginRequest,
    LogoutRequest,
    PasswordResetConfirmRequest,
    PasswordResetRequest,
    RefreshRequest,
)
from invyra_platform.auth.service import AuthRuntimeService

router = APIRouter(prefix="/auth", tags=["auth"])
AuthServiceDependency = Annotated[AuthRuntimeService, Depends(get_auth_runtime_service)]


@router.post("/login", response_model=ApiResponse)
def login(_: LoginRequest, service: AuthServiceDependency) -> ApiResponse:
    """Future login boundary."""
    return map_service_result_to_api_response(service.login(), message="Auth login skeleton only.")


@router.post("/logout", response_model=ApiResponse)
def logout(_: LogoutRequest, service: AuthServiceDependency) -> ApiResponse:
    """Future logout boundary."""
    return map_service_result_to_api_response(service.logout(), message="Auth logout skeleton only.")


@router.post("/refresh", response_model=ApiResponse)
def refresh(_: RefreshRequest, service: AuthServiceDependency) -> ApiResponse:
    """Future refresh-token/session refresh boundary."""
    return map_service_result_to_api_response(
        service.refresh_session(),
        message="Auth refresh skeleton only.",
    )


@router.post("/password-reset/request", response_model=ApiResponse)
def request_password_reset(_: PasswordResetRequest, service: AuthServiceDependency) -> ApiResponse:
    """Future password reset request boundary."""
    return map_service_result_to_api_response(
        service.request_password_reset(),
        message="Auth password reset request skeleton only.",
    )


@router.post("/password-reset/confirm", response_model=ApiResponse)
def confirm_password_reset(_: PasswordResetConfirmRequest, service: AuthServiceDependency) -> ApiResponse:
    """Future password reset consumption boundary."""
    return map_service_result_to_api_response(
        service.consume_password_reset(),
        message="Auth password reset confirm skeleton only.",
    )


@router.get("/session", response_model=ApiResponse)
def session(service: AuthServiceDependency) -> ApiResponse:
    """Future current-session boundary."""
    return map_service_result_to_api_response(
        service.record_auth_security_event(),
        message="Auth session skeleton only.",
    )
