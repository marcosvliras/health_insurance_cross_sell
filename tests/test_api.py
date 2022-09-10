import pytest
import pandas as pd
import sys
import os

try:
 from heroku_files.healthinsurance import HealthInsurance   
except ModuleNotFoundError:
    pdir = os.path.dirname(os.getcwd())
    sys.path.insert(0, pdir)

from heroku_files.healthinsurance import HealthInsurance

@pytest.fixture
def data():

    data = """[{"id":312628,"Gender":"Female","Age":23,"Driving_License":1,
    "Region_Code":29.0,"Previously_Insured":1,"Vehicle_Age":"< 1 Year",
    "Vehicle_Damage":"No","Annual_Premium":31271.0,
    "Policy_Sales_Channel":152.0,"Vintage":273},
    {"id":74843,"Gender":"Male","Age":39,"Driving_License":1,
    "Region_Code":28.0,"Previously_Insured":1,"Vehicle_Age":"1-2 Year",
    "Vehicle_Damage":"No","Annual_Premium":2630.0,
    "Policy_Sales_Channel":154.0,"Vintage":178}]"""

    data = pd.read_json(data, orient="records", dtype=False)

    return data

@pytest.fixture
def data2():

    data = """[{"id":277146,"gender":"Male","age":54,"driving_license":1,
    "region_code":28.0,"previously_insured":0,"vehicle_age":"1-2 Year",
    "vehicle_damage":"Yes","annual_premium":38441.0,
    "policy_sales_channel":26.0,"vintage":39},
    {"id":136111,"gender":"Male","age":64,"driving_license":1,
    "region_code":28.0,"previously_insured":0,"vehicle_age":"1-2 Year",
    "vehicle_damage":"Yes","annual_premium":32159.0,
    "policy_sales_channel":122.0,"vintage":249}]"""

    data = pd.read_json(data, orient="records", dtype=False)

    return data

def test_columns(data):
    new_data = HealthInsurance()
    new_data = new_data.data_selection(df1=data)
    assert new_data.columns.tolist() == ['id',
                                        'gender',
                                        'age',
                                        'driving_license',
                                        'region_code',
                                        'previously_insured',
                                        'vehicle_age',
                                        'vehicle_damage',
                                        'annual_premium',
                                        'policy_sales_channel',
                                        'vintage'
                                        ]

def test_feature_engineering(data2):
    new_data = HealthInsurance()
    new_data = new_data.feature_engineering(data2)
    assert isinstance(new_data, pd.DataFrame)

def test_data_preparation(data2):
    new_data = HealthInsurance()
    new_data = new_data.data_preparation(data2)
    assert isinstance(new_data, pd.DataFrame)
