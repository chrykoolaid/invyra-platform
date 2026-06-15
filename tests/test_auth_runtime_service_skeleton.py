"""Auth runtime service skeleton tests."""

from invyra_platform.auth.service import AuthRuntimeService


AUTH_METHODS = [
    "login",
    "logout",
    "refresh_session",
    "request_password_reset",
    "consume_password_reset",
    "record_auth_security_event",
]


def test_auth_runtime_service_methods_return_skeleton_result() -> None:
    service = AuthRuntimeService()

    for method_name in AUTH_METHODS:
        method = getattr(service, method_name)
        result = method()

        assert result.success is False
        assert result.status == "NOT_IMPLEMENTED"
        assert result.reason == "SERVICE_SKELETON_ONLY"
        assert result.data == {"service": "AuthRuntimeService", "method": method_name}
