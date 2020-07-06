import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State

from dashboards.tabs import *
from dashboards.filter_view import *
from dashboards.dash_test import *
from dashboards.callbacks import *
from dashboards.load_dataframe import load_file


df_2019, columns_to_choose, numeric_cols = load_file(file_name = 'SB11_20192.TXT')

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div(
    [
        html.Div(
            [
                # title
                html.Div(
                    [
                        html.H3(
                            "This is just a test",
                        ),
                    ],
                ),
                # tabs
                html.Div(
                    [
                        build_tabs()
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
        ),
        html.Div(children=html.Div(
                    [
                        get_filter_view(columns_to_choose, [], numeric_cols),
                        get_heat_map(columns_to_choose)
                    ], id="app-content"))
    ]
)

call_callbacks_tabs(app, df_2019, columns_to_choose, numeric_cols)
call_callbacks_view_filter(app, df_2019)
call_callback_heat_map(app, df_2019)
call_callback_simulator(app)
call_callbacks_prescriptive_filter(app, df_2019)
call_callbacks_prescriptive_update(app, df_2019)

if __name__ == '__main__':
    app.run_server(debug=True)