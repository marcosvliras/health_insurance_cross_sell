import pandas as pd
import pickle
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import logging
from logging import FileHandler, StreamHandler
from logging import INFO
from app.healthinsurance import HealthInsurance


logging.basicConfig(
    level=INFO,
    format='%(levelname)s:%(asctime)s:%(message)s',
    handlers=[FileHandler('app/logs/logs.txt', 'w'), StreamHandler()]
)

path = '/home/marcos/Documentos/Projetos/HI_Cross_sell/app/models/model.pkl'
model = pickle.load(open(path, 'rb'))

# with open(path, 'rb') as file:
#    model = pickle.load(file)
router = APIRouter(prefix='/predict')


@router.post(
    "", response_class=JSONResponse, summary="Return the pediction."
)
def health_insurance_predict(test_json: str):
    """Turn back the prediction.

    Parameters
    ----------
    test_json: str
        example for 1 register: '[{"id":40276,"gender":"Female","age":53,
        "driving_license":1,"region_code":28.0,"previously_insured":0,
        "vehicle_age":"between_1_2_years","vehicle_damage":1,
        "annual_premium":30595.0,"policy_sales_channel":124.0,"vintage":186}]'
    """
    if test_json:

        logging.info("File read")

        data = pd.read_json(test_json, orient='records', dtype=False)

        if isinstance(data, pd.DataFrame):
            logging.info("DataFrame -- read")
        else:
            logging.error(
                "Error on turn the data into a Pandas DataFrame object")

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
    else:
        raise TypeError("The string is empty")
