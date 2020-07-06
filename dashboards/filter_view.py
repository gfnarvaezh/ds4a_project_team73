import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

from dashboards.variables_info import *

def filter_function(df_2019, var_to_filter, filter):
    return df_2019[df_2019[var_to_filter] == filter]

def test_update_filter(df_2019, var_to_filter):
    return [{'label': i, 'value': i} for i in sorted(df_2019[var_to_filter].unique())]

def test_update_graph(df_2019, var_to_filter, filter, var_to_see, score_to_see):
    df = filter_function(df_2019, var_to_filter, filter)
    df.sort_values(var_to_see, inplace=True)
    return px.violin(df, x=var_to_see, y=score_to_see, box=True)

def get_filter_view(columns_to_choose, filter_list, numeric_cols):
    return html.Div([
              
        html.H1(children='ThisIsJustATest'),

        html.Div([
            html.P('var_to_filter'),

            html.Div([
                dcc.Dropdown(
                    id='var_to_filter',
                    options=[{'label': i, 'value': i} for i in columns_to_choose],
                    value='ESTU_DEPTO_RESIDE'
                )
            ],
            style={'width': '48%', 'display': 'inline-block'}),

            html.P('Filter'),
            html.Div([
                dcc.Dropdown(
                    id='filter',
                    options=[{'label': i, 'value': i} for i in filter_list],
                    value='SANTANDER'
                )
            ],
            style={'width': '48%', 'display': 'inline-block'}),

            html.P('var_to_see'),
            html.Div([
                dcc.Dropdown(
                    id='var_to_see',
                    options=[{'label': i, 'value': i} for i in columns_to_choose],
                    value='FAMI_ESTRATOVIVIENDA'
                )
            ],
            style={'width': '48%', 'display': 'inline-block'}),

            html.P('score_to_see'),
            html.Div([
                dcc.Dropdown(
                    id='score_to_see',
                    options=[{'label': i, 'value': i} for i in numeric_cols],
                    value='PUNT_GLOBAL'
                )
            ],
            style={'width': '48%', 'display': 'inline-block'})
        ]),

        dcc.Graph(id='indicator-graphic')
    ])