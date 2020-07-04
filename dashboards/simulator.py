import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import pickle
import json

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from dashboards.simulator_dropdowns import get_dropdowns

style_results = {'width': 'calc(25% - 20px)', 'display': 'inline-block', 'font-size': '60%', 'padding': '0px 5px 0px 5px'}

ordered_categorical_variables = {
        'FAMI_ESTRATOVIVIENDA':['No data', 'Sin Estrato', 'Estrato 1', 'Estrato 2', 'Estrato 3', 'Estrato 4', 'Estrato 5', 'Estrato 6'],
        'FAMI_PERSONASHOGAR':['No data', '1 a 2', '3 a 4', '5 a 6', '7 a 8', '9 o más'],
        'FAMI_CUARTOSHOGAR': ['No data','Uno', 'Dos', 'Tres', 'Cuatro', 'Cinco', 'Seis o mas'],
        'FAMI_EDUCACIONPADRE': ['No data', 'No Aplica', 'No sabe', 'Ninguno', 'Primaria incompleta', 'Primaria completa', 'Secundaria (Bachillerato) incompleta', 'Secundaria (Bachillerato) completa', 'Técnica o tecnológica incompleta', 'Técnica o tecnológica completa', 'Educación profesional incompleta', 'Educación profesional completa', 'Postgrado'],
        'FAMI_EDUCACIONMADRE': ['No data', 'No Aplica', 'No sabe', 'Ninguno', 'Primaria incompleta', 'Primaria completa', 'Secundaria (Bachillerato) incompleta', 'Secundaria (Bachillerato) completa', 'Técnica o tecnológica incompleta', 'Técnica o tecnológica completa', 'Educación profesional incompleta', 'Educación profesional completa', 'Postgrado'],
        'FAMI_NUMLIBROS': ['No data', '0 A 10 LIBROS', '11 A 25 LIBROS', '26 A 100 LIBROS', 'MÁS DE 100 LIBROS'],
        'FAMI_COMELECHEDERIVADOS': ['No data', 'Nunca o rara vez comemos eso', '1 o 2 veces por semana', '3 a 5 veces por semana', 'Todos o casi todos los días'],
        'FAMI_COMECARNEPESCADOHUEVO': ['No data', 'Nunca o rara vez comemos eso', '1 o 2 veces por semana', '3 a 5 veces por semana', 'Todos o casi todos los días'],
        'FAMI_COMECEREALFRUTOSLEGUMBRE': ['No data', 'Nunca o rara vez comemos eso', '1 o 2 veces por semana', '3 a 5 veces por semana', 'Todos o casi todos los días'],
        'FAMI_SITUACIONECONOMICA': ['No data', 'Peor', 'Igual', 'Mejor'],
        'ESTU_DEDICACIONLECTURADIARIA': ['No data', 'No leo por entretenimiento', '30 minutos o menos', 'Entre 30 y 60 minutos', 'Entre 1 y 2 horas', 'Más de 2 horas'],
        'ESTU_DEDICACIONINTERNET': ['No data', 'No Navega Internet', '30 minutos o menos', 'Entre 30 y 60 minutos', 'Entre 1 y 3 horas', 'Más de 3 horas'],
        'ESTU_HORASSEMANATRABAJA': ['No data', '0', 'Menos de 10 horas', 'Entre 11 y 20 horas', 'Entre 21 y 30 horas', 'Más de 30 horas']        
    }

scores = [
'PUNT_LECTURA_CRITICA',
'PUNT_MATEMATICAS',
'PUNT_C_NATURALES',
'PUNT_SOCIALES_CIUDADANAS',
'PUNT_INGLES'
]

models = {}

for score in scores:
    with open('models/model_' + score + '.pkl', 'rb') as file:
        models[score] = pickle.load(file)

with open('list_variables_plotly.json') as json_file:
    list_variables_plotly = json.load(json_file)

def get_simulator():
    return html.Div([
            get_dropdowns(),
            html.Div(id="result_simulation")
        ])

def update_result(dic_entrada):
    
    dic_fixed = {}
    dic_fixed['EDAD'] = -18*365
    i = 0

    for variable in list_variables_plotly:
        dic_fixed[variable] = dic_entrada['args'][i]
        i += 1

    df_X = transform_data(pd.DataFrame([dic_fixed]))

    output = []
    total = 250

    for score in scores:
        result = models[score].predict(df_X)
        output.append(html.H3(score, style = style_results))
        output.append(html.H5(str(result[0] + 50), style = style_results))
        total = total + result[0]
    
    output.append(html.H3('TOTAL SCORE', style = style_results))
    output.append(html.H5(str(total), style = style_results))

    return html.Div(output)


def transform_data(df):
    #Este código reemplaza las categoricas ordinales por númericas
    for column in ordered_categorical_variables:
        for index, value in enumerate(ordered_categorical_variables[column]):
            mask = df[column] == value
            df.loc[mask, column] = str(index)
        df[column] = df[column].astype(int)
        
    mask = (df['ESTU_NACIONALIDAD'] != 'COLOMBIA')
    df.loc[mask, 'ESTU_NACIONALIDAD'] = 'EXTRANJERO'
    
    return df