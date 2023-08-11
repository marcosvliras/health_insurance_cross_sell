"""Predict."""
import json
from typing import Dict, List
import pandas as pd
import pickle
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import logging
from app.healthinsurance import HealthInsurance
from ..models.dataframe import (
    UniquePredictionRequest,
    UniquePredictionResponse,
)


router = APIRouter(prefix="/predict", tags=["PREDICTIONS"])


@router.post(
    "/many",
    response_class=JSONResponse,
    summary="Prediction for many customers",
)
def health_insurance_predict_many(
    data: List[UniquePredictionRequest],
) -> List[UniquePredictionResponse]:
    """Turn back the prediction."""
    list_of_unique_input = [data_input.dict() for data_input in data]
    df = pd.DataFrame(list_of_unique_input)
    df_response = make_prediction(df)

    data_list = json.loads(df_response)
    prediction_objects = [
        UniquePredictionResponse(**item) for item in data_list
    ]

    return prediction_objects


@router.post(
    "/one",
    response_class=JSONResponse,
    summary="Prediction for one customer",
)
def health_insurance_predict_one(
    data: UniquePredictionRequest,
) -> UniquePredictionResponse:
    """Turn back the prediction."""
    df = pd.DataFrame([data.dict()])
    df_response = make_prediction(df)

    data_list = json.loads(df_response)
    return UniquePredictionResponse(**data_list[0])


def make_prediction(data):
    """Make the prediction pipeline."""
    # path = ("/home/marcos/Documentos/Projetos/HI_Cross_sell"
    #         "/app/models/model.pkl")

    logging.info("Prediction: Starting...")

    path = "app/models/model.pkl"

    with open(path, "rb") as file:
        model = pickle.load(file)

    # Instantiate Rossmann class
    pipeline = HealthInsurance()

    # data cleaning
    df1 = pipeline.data_selection(data)
    logging.info("Data Selection...")

    # feature engineering
    df2 = pipeline.feature_engineering(df1)
    logging.info("Feature engineering...")

    # data preparation
    df3 = pipeline.data_preparation(df2)
    logging.info("Data Preparation...")

    # prediction
    df_response = pipeline.get_predictions(model, data, df3)
    logging.info("Get Predictions...")
    logging.info("Prediction: Done")

    return df_response
