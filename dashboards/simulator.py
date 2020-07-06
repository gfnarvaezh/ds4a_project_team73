import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json

from dashboards.simulator_dropdowns import get_dropdowns
from dashboards.variables_info import get_scores
from dashboards.models_predict import predict_all_models

style_results = {'width': 'calc(25% - 20px)', 'display': 'inline-block', 'font-size': '60%', 'padding': '0px 5px 0px 5px'}

scores = get_scores()

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

    results = predict_all_models(pd.DataFrame([dic_fixed]))

    output = []
    total = 250

    for score in results:
        output.append(html.H3(score, style = style_results))
        output.append(html.H5(str(results[score][0] + 50), style = style_results))
        total = total + results[score][0]
    
    output.append(html.H3('TOTAL SCORE', style = style_results))
    output.append(html.H5(str(total), style = style_results))

    return html.Div(output)