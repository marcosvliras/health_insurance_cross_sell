from fastapi.testclient import TestClient
from app.run import app

client = TestClient(app)


def test_fetch():
    payload = {
        "k": 20
    }
    r = client.get('/v2/fetch', json=payload)
    assert r.status_code == 200
