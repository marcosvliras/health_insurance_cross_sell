from fastapi.testclient import TestClient
from run import app

client = TestClient(app)


def test_predict_one():
    payload = {
        "id": 1,
        "gender": "Male",
        "age": 44,
        "driving_license": 1,
        "region_code": 28.0,
        "previously_insured": 0,
        "vehicle_age": "> 2 anos",
        "vehicle_damage": "Yes",
        "annual_premium": 40454.0,
        "policy_sales_channel": 26.0,
        "vintage": 217,
    }

    response = client.post("/v2/predict/one", json=payload)
    assert response.status_code == 200


def test_predict_many():
    payload = [
        {
            "id": 1,
            "gender": "Male",
            "age": 44,
            "driving_license": 1,
            "region_code": 28.0,
            "previously_insured": 0,
            "vehicle_age": "> 2 anos",
            "vehicle_damage": "Yes",
            "annual_premium": 40454.0,
            "policy_sales_channel": 26.0,
            "vintage": 217,
        },
        {
            "id": 1,
            "gender": "Male",
            "age": 44,
            "driving_license": 0,
            "region_code": 28.0,
            "previously_insured": 0,
            "vehicle_age": "> 2 anos",
            "vehicle_damage": "Yes",
            "annual_premium": 40454.0,
            "policy_sales_channel": 26.0,
            "vintage": 256,
        },
    ]

    response = client.post("/v2/predict/many", json=payload)
    assert response.status_code == 200
