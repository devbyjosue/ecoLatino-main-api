from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_live() -> None:
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_ready() -> None:
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_v1_health_live() -> None:
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_v1_health_ready() -> None:
    response = client.get("/api/v1/health/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_v1_articles() -> None:
    response = client.get("/api/v1/articles")
    assert response.status_code == 200
    assert response.json() == []


def test_api_v1_sources() -> None:
    response = client.get("/api/v1/sources")
    assert response.status_code == 200
    assert response.json() == []


def test_api_v1_stories() -> None:
    response = client.get("/api/v1/stories")
    assert response.status_code == 200
    assert response.json() == []


def test_api_v1_analytics() -> None:
    response = client.get("/api/v1/analytics")
    assert response.status_code == 200
    assert response.json() == {}
