"""Predict."""
import pandas as pd
import pickle
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import logging
from app.healthinsurance import HealthInsurance
from ..models.dataframe import DataFrame
import os


router = APIRouter(prefix='/predict')


@router.post(
    "",
    response_class=JSONResponse,
    summary="Return the pediction."
)
def health_insurance_predict(
    data: DataFrame
):
    """Turn back the prediction."""
    logging.info("Prediction: Starting...")
    df = pd.DataFrame(data.dict())
    df_response = make_prediction(df)
    logging.info("Prediction: End")

    return df_response


def make_prediction(data):
    """Make the prediction pipeline."""
    # path = ("/home/marcos/Documentos/Projetos/HI_Cross_sell"
    #         "/app/models/model.pkl")

    path = ("app/models/model.pkl")

    with open(path, 'rb') as file:
        model = pickle.load(file)

    logging.info("Prediction: Starting...")
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
    logging.info("Predictions: Done")

    return df_response
