import os
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import pandas as pd
from .predict import make_prediction


router = APIRouter(prefix='/fetch')


@router.get(
    "",
    response_class=JSONResponse,
    summary="Return the top 10 people most likely to be predicted as class 1."
)
def fetch():
    path = os.getcwd() + '/data/test.csv'
    df = pd.read_csv(path)

    json_response = make_prediction(df)
    df_response = pd.read_json(json_response)
    df_response = df_response.head(10)
    df_response_final = df_response.to_json(
        orient='records', date_format='iso')

    return df_response_final
