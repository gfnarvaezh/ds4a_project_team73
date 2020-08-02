import dash
import dash_core_components as dcc
import dash_html_components as html
import json

from dashboards.variables_info import get_variables_predictive

from dashboards.translator import translator_class

with open('list_variables_plotly.json') as json_file:
    list_variables_plotly = json.load(json_file)

variables_predictive = get_variables_predictive()

translator = translator_class()

style_dropdown = {'width': 'calc(14% - 10px)', 'display': 'inline-block', 'font-size': '60%', 'padding': '0px 5px 0px 5px'}
style_dropdown_text = {'width': 'calc(18% - 10px)', 'display': 'inline-block', 'font-size': '60%', 'padding': '0px 5px 0px 5px'}



def get_dropdowns():

    dropdowns = []

    for variable in variables_predictive:
        div = html.Div([
                    dcc.Dropdown(
                        id='filter_' + variable,
                        options=[{'label': i, 'value': i} for i in translator.translate_list(list_variables_plotly[variable][0])],
                        value=translator.translate(list_variables_plotly[variable][1]),
                        clearable=False
                    )
                ],
                style=style_dropdown)

        
        dropdowns.append(html.P(translator.translate(variable), style=style_dropdown_text))
        dropdowns.append(div)

    return html.Div([
        html.Div(dropdowns)
        ])