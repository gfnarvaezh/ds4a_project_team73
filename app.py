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


df_2019, columns_to_choose_raw, numeric_cols = load_file(file_name = 'SB11_20192.TXT')
columns_to_choose = item_list = [e for e in columns_to_choose_raw if e not in ('EDAD', 'ESTU_DEPTO_RESIDE')]
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
        html.Div(children=html.Div(id="app-content")),

        html.Hr(),

        html.Footer(children =html.Div(
                    [
                        'Created by the team 73 - Data science for All'
                    ]) )
    ]
)

call_callbacks_tabs(app, df_2019, columns_to_choose, numeric_cols)
call_callback_simulator(app)
call_callbacks_prescriptive_filter(app, df_2019)
call_callbacks_prescriptive_update(app, df_2019)
call_callbacks_tabs_analytics(app, columns_to_choose)
call_callback_data_state(app)
call_callback_data_country(app)
call_callback_data_city(app)
call_callback_city_dropdown(app)
call_callback_country_bar_chart(app)
call_callback_state_bar_chart(app)
call_callback_city_bar_chart(app)

if __name__ == '__main__':
    app.run_server(debug=True)