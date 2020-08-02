import pandas as pd
import pickle
import joblib
import json

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler, OrdinalEncoder
from sklearn import set_config
from sklearn.pipeline import make_pipeline

from dashboards.variables_info import *


ordered_categorical_variables = get_ordered_variables()
scores = get_scores()

models = {}

for score in scores:
    with open('models/model_' + score + '.pkl', 'rb') as file:
        models[score] = pickle.load(file)

preprocessor = joblib.load('models/preprocessor.pkl')
regressor = joblib.load('models/regressor.pkl')

def predict_global_score(df):
    size = df.shape[0]
    output_series = pd.DataFrame(0, index=range(size), columns=range(1), dtype = 'float64')
    results = predict_all_models(df)
    for result in results:
        output_series += results[result][:, None]

    return output_series

def predict_all_models(df):
    result = {}
    for score in scores:
        result[score] = models[score].predict(transform_data(df)) + 50
    
    return result

def transform_data(df):
    #Este código reemplaza las categoricas ordinales por númericas
    for column in ordered_categorical_variables:
        for index, value in enumerate(ordered_categorical_variables[column]):
            mask = df[column] == value
            df.loc[mask, column] = str(index)
        df[column] = df[column].astype(int)
    
    return df


def predict_score(records: dict):
    with open('output.json', 'w') as outfile:
        json.dump(records, outfile, indent=4)
    X_prepared = prepare_data(records, preprocessor)
    
    return regressor.predict(X_prepared)

def prepare_data(records: dict,
                 preprocessor: object):
    X = pd.DataFrame.from_dict([records])
    X_prepared = preprocessor.transform(X)
    
    return X_prepared