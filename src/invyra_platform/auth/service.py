"""Authentication runtime service skeleton."""

from invyra_platform.core.service_results import ServiceResult


class AuthRuntimeService:
    """Service boundary for future authentication runtime behavior."""

    service_name = "AuthRuntimeService"

    def _skeleton(self, method: str) -> ServiceResult:
        return ServiceResult.not_implemented(data={"service": self.service_name, "method": method})

    def login(self) -> ServiceResult:
        """Future login flow boundary."""
        return self._skeleton("login")

    def logout(self) -> ServiceResult:
        """Future logout flow boundary."""
        return self._skeleton("logout")

    def refresh_session(self) -> ServiceResult:
        """Future refresh-token/session refresh boundary."""
        return self._skeleton("refresh_session")

    def request_password_reset(self) -> ServiceResult:
        """Future password reset request boundary."""
        return self._skeleton("request_password_reset")

    def consume_password_reset(self) -> ServiceResult:
        """Future password reset consumption boundary."""
        return self._skeleton("consume_password_reset")

    def record_auth_security_event(self) -> ServiceResult:
        """Future auth security event persistence boundary."""
        return self._skeleton("record_auth_security_event")
