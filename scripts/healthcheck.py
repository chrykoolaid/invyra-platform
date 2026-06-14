"""Simple local application healthcheck."""

from fastapi.testclient import TestClient

from invyra_platform.app import create_app


def main() -> None:
    client = TestClient(create_app())
    response = client.get("/health")
    response.raise_for_status()
    print(response.json())


if __name__ == "__main__":
    main()
