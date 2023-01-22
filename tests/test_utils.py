"""Test for help functions - TO DO"""
import inflection
from utils.utils import cramer_v, numeric_statistics, precision_at_k, \
    recall_at_k, cross_validation
import pandas as pd
import numpy as np
import pytest
from app.api.endpoints.predict import make_prediction
import pickle
from sklearn.model_selection import train_test_split
from app.healthinsurance import HealthInsurance


@pytest.fixture
def data():
    df = pd.read_csv('data/train.csv').head(10)
    col_response = df['Response']
    df_response = pd.read_json(make_prediction(df.drop('Response', axis=1)))
    df_response['Response'] = col_response

    return df_response


@pytest.mark.parametrize("var1, var2, expected", [
    [('Female', 'Male', 'Male', 'Female', 'Male'),
        ('Yes', 'No', 'No', 'Yes', 'Yes'), 0.1290994448735806],
    [('Female', 'Female', 'Female', 'Female', 'Male'),
        ('Yes', 'No', 'No', 'Yes', 'Yes'), 0.0]
])
def test_cramer_v(var1, var2, expected):
    cv = cramer_v(var1, var2)
    assert cv == expected


def test_numeric_statistics(data):
    columns = [
        'type',
        'Unique_Values',
        'Mean',
        'Median',
        'Std',
        'Min',
        'Max',
        'Range',
        'Skew',
        'Kurtosis'
    ]
    df = data.select_dtypes(include=[int, float])
    df_numeric_s = numeric_statistics(df)
    df_columns = df_numeric_s.columns.tolist()
    assert columns == df_columns


def test_precision_at_k(data):
    p_at_5, df = precision_at_k(data, 5, 'id', 'Response', 'score')
    assert p_at_5 == 0.3333333333333333
    assert isinstance(df, pd.DataFrame)


def test_recall_at_k(data):
    r_at_5, df = recall_at_k(data, 5, 'id', 'Response', 'score')
    assert r_at_5 == 0.6666666666666666
    assert isinstance(df, pd.DataFrame)


def test_cross_validation():
    path = ("/home/marcos/Documentos/Projetos/HI_Cross_sell"
            "/app/models/model.pkl")
    with open(path, 'rb') as file:
        model = pickle.load(file)

    data = pd.read_csv('data/train.csv')

    def snakecase(x):
        return inflection.underscore(x)
    new_columns = list(map(snakecase, data.columns.tolist()))

    data.columns = new_columns

    data = data.dropna()

    cols_selected = [
                     'vintage', 'annual_premium', 'age', 'region_code',
                     'previously_insured', 'policy_sales_channel']

    X = data.drop('response', axis=1)
    y = data['response']

    X_train, _, y_train, _ = train_test_split(
        X, y, test_size=0.2, random_state=1)

    cv = cross_validation(X_train, y_train, model, 5, cols_selected, 10, False)
    assert cv == 0.03636363636363636
