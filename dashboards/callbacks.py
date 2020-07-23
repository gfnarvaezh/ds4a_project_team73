from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import json

from dashboards.filter_view import *
from dashboards.simulator import update_result
from dashboards.prescriptive import *

from dashboards.tabs import *
from dashboards.dash_test import build_analytics_tab
from dashboards.analytics.main import update_state_dash, update_country_dash

prescriptive_object = prescriptive_class()

with open('list_variables_plotly.json') as json_file:
    list_variables_plotly = json.load(json_file)

inputs = [Input('filter_' + str(variable), 'value') for variable in list_variables_plotly]

def call_callbacks_tabs(app, df_2019, columns_to_choose, numeric_cols):
    @app.callback(
        Output("app-content", "children"),
        [Input("tabs", "value")])
    def update_content(tab_name):
        return build_content_for_tab(tab_name, columns_to_choose, numeric_cols)

def call_callbacks_tabs_analytics(app):
    @app.callback(
        Output("content_analytics", "children"),
        [Input("tabs_analytics", "value")])
    def update_analytics_tab(tabs_analytics):
        return build_analytics_tab(tabs_analytics)

def call_callback_simulator(app):
    @app.callback(
        Output("result_simulation", "children"),
        inputs)
    def update_content(*args):
        return update_result(locals())


def call_callbacks_prescriptive_filter(app, df_2019):
    @app.callback(
        Output('prescriptive_filter', 'children'), 
        [Input('prescriptive_variables', 'value')])
    def update_list_prescriptive(prescriptive_variables):
        return prescriptive_object.get_list_prescriptive(df_2019, prescriptive_variables)

def call_callbacks_prescriptive_update(app, df_2019):
    @app.callback(
        Output('prescriptive_result', 'figure'),
        [Input('calculate_button', 'n_clicks')],
        [State('prescriptive_variables', 'value')] + 
        [State('prescriptive_sample_size', 'value')] + 
        [State('prescriptive_id_' + str(i), 'value') for i in range(0,100)]
    )
    def update_result(*args):
        return prescriptive_object.update_prediction(df_2019, locals())

def call_callback_data_country(app):
    @app.callback([
        Output('country_card_max', 'children'),
        Output('country_card_min', 'children'),
        Output('country_map', 'figure'),
        ],
        [Input('analytics_country_filter_period_box', 'value')]
    )
    def update_data_country(period):
        return update_country_dash()

def call_callback_data_state(app):
    @app.callback([
        Output('state_card_max', 'children'),
        Output('state_gauge', 'children'),
        Output('state_card_min', 'children'),
        Output('state_map', 'figure'),
        ],
        [Input('analytics_state_filter_state', 'value')]
    )
    def update_data_state(state):
        return update_state_dash(state)