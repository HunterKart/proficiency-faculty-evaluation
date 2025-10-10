def test_health_endpoint_returns_ok() -> None:
    from fastapi.testclient import TestClient

    from src.main import app

    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
