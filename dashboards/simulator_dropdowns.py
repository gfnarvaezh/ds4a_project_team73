import dash
import dash_core_components as dcc
import dash_html_components as html
import json

with open('list_variables_plotly.json') as json_file:
    list_variables_plotly = json.load(json_file)

style_dropdown = {'width': 'calc(14% - 20px)', 'display': 'inline-block', 'font-size': '60%', 'padding': '0px 5px 0px 5px'}
style_dropdown_text = {'width': 'calc(18% - 20px)', 'display': 'inline-block', 'font-size': '60%', 'padding': '0px 5px 0px 5px'}

dropdowns = []

for variable in list_variables_plotly:
    div = html.Div([
                dcc.Dropdown(
                    id='filter_' + variable,
                    options=[{'label': i, 'value': i} for i in list_variables_plotly[variable][0]],
                    value=list_variables_plotly[variable][1],
                    clearable=False
                )
            ],
            style=style_dropdown)
    dropdowns.append(html.P(variable, style=style_dropdown_text))
    dropdowns.append(div)


def get_dropdowns():
    return html.Div([
              
        html.H1(children='Simulator test'),

        html.Div(dropdowns)
        ])