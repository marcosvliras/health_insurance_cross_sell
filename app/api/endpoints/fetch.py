"""Fetch."""
import os
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import pandas as pd
from .predict import make_prediction
import logging


router = APIRouter(prefix='/fetch')


@router.get(
    "",
    response_class=JSONResponse,
    summary="Return the top k people most likely to be predicted as class 1."
)
def fetch(k=10):
    """Fetch result from top k users."""
    path = os.getcwd() + '/data/test.csv'
    df = pd.read_csv(path)

    logging.info("Fetch: Starting...")
    json_response = make_prediction(df)
    df_response = pd.read_json(json_response)
    df_response = df_response.head(k)
    df_response_final = df_response.to_json(
        orient='records', date_format='iso')
    logging.info("Fetch: End")

    return df_response_final
