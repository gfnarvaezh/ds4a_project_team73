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
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"
FONT_GLYCOSE = "https://netdna.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"

stylesheets=[dbc.themes.CYBORG, FONT_AWESOME,FONT_GLYCOSE, 'style.css']

#< ---- End of code to be moved to assessment Library --->

app = dash.Dash(external_stylesheets = stylesheets)

app.config['suppress_callback_exceptions'] = True

app.layout = html.Div(
    [
        html.Div(
            [
                # title
                html.Div(
                    [
                        html.H3(
                            "Icfes analytics project",
                        ),
                    ],
                    id = 'general_title'
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
call_callbacks_tabs_analytics(app)
call_callback_data_state(app)
call_callback_data_country(app)

if __name__ == '__main__':
    app.run_server(debug=True)