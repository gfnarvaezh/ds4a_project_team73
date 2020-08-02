import dill
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import glob, os
import dash_html_components as html
import dash_bootstrap_components as dbc
import string
import random

#from components.translator import translator_class

# load pre-trained explainer
with open('models/explainer.pkl', 'rb') as f:
    explainer = dill.load(f)

# load pre-trained preprocessor and regressor
preprocessor = joblib.load('models/preprocessor.pkl')
regressor = joblib.load('models/regressor.pkl')


def prepare_data(records: dict,
                 preprocessor: object):
    X = pd.DataFrame.from_dict([records])
    X_prepared = preprocessor.transform(X)
    return X_prepared


def predict_score(records: dict,
                  preprocessor: object,
                  regressor: object):
                  
    X_prepared = prepare_data(records, preprocessor)

    return regressor.predict(X_prepared)


def get_explainer(records, preprocessor, regressor):
    X_prepared = prepare_data(records, preprocessor).ravel()
    exp = explainer.explain_instance(
        X_prepared, regressor.predict, num_features=8)
    #exp.show_in_notebook(show_all=False)
    return exp


def draw_explainer_from_input(inputList):
    records = {'fami_estratovivienda': inputList[0],
                'fami_educacionpadre': inputList[1],
                'fami_educacionmadre': inputList[2],
                'fami_numlibros'     : inputList[3].upper(),
                'fami_comelechederivados': inputList[4],
                'estu_dedicacionlecturadiaria': inputList[5],
                'estu_dedicacioninternet': inputList[6],
                'estu_horassemanatrabaja': inputList[7]}

    exp = get_explainer(records, preprocessor, regressor)
    remove_all_files_from_path('static/')
    filename = 'static/' + get_random_alphanumeric_string() +'.html'
    exp.save_to_file(filename,predict_proba=True,show_predicted_value=True)
    return filename

def remove_all_files_from_path(path):
    fullpath = path +  '*'
    r = glob.glob(fullpath)
    for i in r:
        os.remove(i)

def get_random_alphanumeric_string():
    length = 14
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

def get_bars_for_descriptive(listInput):
    filename = draw_explainer_from_input(listInput)

    print('full filename is ',filename)
    var = html.Div(
    [   dbc.Row(
            [
                dbc.Col(html.Iframe(id="predictor",src=filename,width='1000',height='400', style={'border':'none'}),width=8),

            ],
            className="mb-8",
        )
        
          ]
    )
    return var
    