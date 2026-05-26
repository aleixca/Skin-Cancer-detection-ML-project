from fastapi.testclient import TestClient

from api import app


client = TestClient(app)


def test_health_endpoint_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_endpoint_reports_service_status_without_loading_models():
    response = client.get("/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "DermaScan ML API"
    assert payload["model_loaded"] is False
    assert payload["rag_loaded"] is False
