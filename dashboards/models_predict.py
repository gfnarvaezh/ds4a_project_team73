import pandas as pd
import pickle

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from dashboards.variables_info import *

ordered_categorical_variables = get_ordered_variables()
scores = get_scores()

models = {}

for score in scores:
    with open('models/model_' + score + '.pkl', 'rb') as file:
        models[score] = pickle.load(file)

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
        result[score] = models[score].predict(transform_data(df))
    
    return result

def transform_data(df):
    #Este código reemplaza las categoricas ordinales por númericas
    for column in ordered_categorical_variables:
        for index, value in enumerate(ordered_categorical_variables[column]):
            mask = df[column] == value
            df.loc[mask, column] = str(index)
        df[column] = df[column].astype(int)
    
    return df

