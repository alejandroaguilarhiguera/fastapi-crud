# tests/test_health.py
import pytest

@pytest.mark.anyio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.anyio
async def test_readiness_check(client):
    response = await client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}