from fastapi.testclient import TestClient
from app.run import app

client = TestClient(app)


def test_predict():
    payload = {
        "id": [40276],
        "gender": ["Female"],
        "age": [53],
        "driving_license": [1],
        "region_code": [28.0],
        "previously_insured": [0],
        "vehicle_age": ["between_1_2_years"],
        "vehicle_damage": [1],
        "annual_premium": [30595.0],
        "policy_sales_channel": [124.0],
        "vintage": [186]
    }

    response = client.post('/v2/predict', json=payload)
    assert response.status_code == 200
