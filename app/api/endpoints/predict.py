import pandas as pd
import pickle
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import logging
from logging import FileHandler, StreamHandler
from logging import INFO
from app.healthinsurance import HealthInsurance
from ..models.dataframe import DataFrame


logging.basicConfig(
    level=INFO,
    format='%(levelname)s:%(asctime)s:%(message)s',
    handlers=[FileHandler('app/logs/logs.txt', 'w'), StreamHandler()]
)


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

    df = pd.DataFrame(data.dict())

    if isinstance(df, pd.DataFrame):
        logging.info("DataFrame -- read")
    else:
        logging.error(
            "Error on turn the data into a Pandas DataFrame object")

    df_response = make_prediction(df)
    return df_response


def make_prediction(data):
    """Make the prediction pipeline."""
    path = ("/home/marcos/Documentos/Projetos/HI_Cross_sell"
            "/app/models/model.pkl")
    with open(path, 'rb') as file:
        model = pickle.load(file)
    # Instantiate Rossmann class
    pipeline = HealthInsurance()

    # data cleaning
    df1 = pipeline.data_selection(data)
    if isinstance(data, pd.DataFrame):
        logging.info("Data Selection -- done")
    else:
        logging.error(
            "Error on data_selection")

    # feature engineering
    df2 = pipeline.feature_engineering(df1)
    if isinstance(data, pd.DataFrame):
        logging.info("Feature engineering -- done")
    else:
        logging.error(
            "Error on feature_engineering")

    # data preparation
    df3 = pipeline.data_preparation(df2)
    if isinstance(data, pd.DataFrame):
        logging.info("Data Preparation -- done")
    else:
        logging.error(
            "Error on feature_engineering")

    # prediction
    df_response = pipeline.get_predictions(model, data, df3)
    if isinstance(data, pd.DataFrame):
        logging.info("Get Predictions -- done")
    else:
        logging.error(
            "Error on get_predictions")

    return df_response
