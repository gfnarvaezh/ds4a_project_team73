import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json

from dashboards.simulator_dropdowns import get_dropdowns
from dashboards.variables_info import get_scores, get_variables_predictive
from dashboards.models_predict import predict_score
from dashboards.draw_explainer import get_bars_for_descriptive
from dashboards.translator import translator_class

translator = translator_class()
scores = get_scores()
variables_predictive = get_variables_predictive()


with open('list_variables_plotly.json') as json_file:
    list_variables_plotly = json.load(json_file)

def get_simulator():
    return html.Div([
                html.Div([
                html.P(children='How to use this tool?', id='prescriptive_description_title'),
                html.P(children='In this section, you can simulate the results of an individual student, according to a simplified model using 10 variables. Below the result, it is possible to see how each variable affected the overall score. ', id='prescriptive_description'),
            ], id='prescriptive_description_box'),
            html.P('Modify the variables below to see the result'),
            get_dropdowns(),
            html.Div(id="result_simulation"),
            dcc.Loading(
                        id="loading-2",
                        children=html.Div(id = 'graph_simulation'),
                        type="circle"
                    ),
        ])

def update_result(dic_entrada):
    
    dic_fixed = {}
    i = 0

    for variable in variables_predictive:
        dic_fixed[variable.lower()] = translator.to_original(dic_entrada['args'][i])
        i += 1

    score = round(predict_score(dic_fixed)[0])

    output = []

    output.append(html.H3('Global Score', id = 'predictive_result_title'))
    output.append(html.H5(str(score), id = 'predictive_result_title'))

    return html.Div(output, id = 'predictive_result_numeric_box')

def update_graph_simulator(dic_entrada):
    listInput = translator.to_original_list(dic_entrada['args'])
    #print(listInput)
    #listInput = ['Estrato 2', 'Ninguna', 'Secundaria (bachillerato) completa', '0 A 10 LIBROS', '1 o 2 veces por semana', '30 minutos o menos', 'Entre 1 y 3 horas', '0']
    return get_bars_for_descriptive(listInput)