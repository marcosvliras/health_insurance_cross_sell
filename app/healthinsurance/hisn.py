"""HealhInsurance."""
import pickle
import pandas as pd
import inflection


class HealthInsurance(object):
    """HealthInsurance class."""

    def __init__(self):
        """Construct."""
        # self.home_path =
        # '/home/marcos/Documentos/Projetos/HI_Cross_sell/app/'

        def read_pickle(file):
            # home_path = '/home/marcos/Documentos/Projetos/HI_Cross_sell/app/'
            home_path = 'app/'
            folder = 'parameters'
            path = home_path + folder

            return pickle.load(open(path + file, 'rb'))

        self.age = read_pickle('/age_scaler.pkl')
        self.annual_premium = read_pickle('/annual_premium_scaler.pkl')
        self.gender = read_pickle('/gender_encoder.pkl')
        self.policy_channel = read_pickle('/policy_sales_channel_encoder.pkl')
        self.region = read_pickle('/region_encoder.pkl')
        self.vintage = read_pickle('/vintage.pkl')

    def data_selection(self, df1):
        """Rename columns."""
        old_columns = [
            'id', 'Gender', 'Age', 'Driving_License',
            'Region_Code', 'Previously_Insured', 'Vehicle_Age',
            'Vehicle_Damage', 'Annual_Premium', 'Policy_Sales_Channel',
            'Vintage']

        def snakecase(x):
            return inflection.underscore(x)
        new_columns = list(map(snakecase, old_columns))

        df1.columns = new_columns

        df1 = df1.dropna()
        return df1

    def feature_engineering(self, df2):
        """Feature engineering.

        Change the values in the columns vehicle_age and vehicle_damage.
        """
        df2['vehicle_age'] = df2['vehicle_age'].apply(
            lambda x: 'over_2_years' if x == '> 2 Years'
            else 'between_1_2_years' if x == '1-2 Year' else 'below_1_year')

        # vehicle damage
        df2['vehicle_damage'] = df2['vehicle_damage'].apply(
            lambda x: 1 if x == 'Yes' else 0)

        return df2

    def data_preparation(self, df5):
        """Prepare data to be scored.

        This method apply on data the transformations needed to be done.
        """
        df5['annual_premium'] = self.annual_premium.transform(
            df5[['annual_premium']].values)

        df5['age'] = self.age.transform(df5[['age']].values)

        df5['vintage'] = self.vintage.transform(df5[['vintage']].values)

        df5['gender'] = df5['gender'].map(self.gender)

        df5['region_code'] = df5['region_code'].map(self.region)

        df5 = pd.get_dummies(
            df5, prefix='vehicle_age', columns=['vehicle_age'])

        # TO DO
        # investigar, aqui esta gerando valores nulos, talvez o map dessa var
        # nao esteja mapeando todas
        df5['policy_sales_channel'] = df5['policy_sales_channel'].map(
            self.policy_channel)

        cols_selected = [
            'vintage', 'annual_premium', 'age', 'region_code',
            'vehicle_damage', 'previously_insured', 'policy_sales_channel']

        df5 = df5[cols_selected]
        df5 = df5.dropna()
        return df5

    def get_predictions(self, model, original_data, test_data):
        """Score the data."""
        pred = pd.DataFrame(model.predict_proba(test_data))[1]

        original_data['score'] = pred
        original_data = original_data.sort_values('score', ascending=False)

        return original_data.to_json(orient='records', date_format='iso')
