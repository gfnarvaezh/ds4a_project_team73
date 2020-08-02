from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import json

from dashboards.filter_view import *
from dashboards.simulator import update_result, update_graph_simulator
from dashboards.prescriptive import *

from dashboards.tabs import *
from dashboards.dash_test import build_analytics_tab
from dashboards.analytics.main import update_state_dash, update_country_dash, update_city_dash, update_city_dropdown, update_country_bar_chart, update_onedim_bar_by_state, update_onedim_bar_by_city
from dashboards.variables_info import get_variables_predictive

prescriptive_object = prescriptive_class()

variables_predictive = get_variables_predictive()

inputs = [Input('filter_' + str(variable), 'value') for variable in variables_predictive]

def call_callbacks_tabs(app, df_2019, columns_to_choose, numeric_cols):
    @app.callback(
        Output("app-content", "children"),
        [Input("tabs", "value")])
    def update_content(tab_name):
        return build_content_for_tab(tab_name, columns_to_choose, numeric_cols)

def call_callbacks_tabs_analytics(app, columns_to_choose):
    @app.callback(
        Output("content_analytics", "children"),
        [Input("tabs_analytics", "value"),])
    def update_analytics_tab(tabs_analytics):
        return build_analytics_tab(tabs_analytics, columns_to_choose)

def call_callback_simulator(app):
    @app.callback([
        Output("result_simulation", "children"),
        Output("graph_simulation", "children"),],
        inputs)
    def update_content(*args):
        return (update_result(locals()),) + (update_graph_simulator(locals()), )


def call_callbacks_prescriptive_filter(app, df_2019):
    @app.callback(
        Output('prescriptive_filter', 'children'), 
        [Input('prescriptive_variables', 'value')])
    def update_list_prescriptive(prescriptive_variables):
        return prescriptive_object.get_list_prescriptive(df_2019, prescriptive_variables)

def call_callbacks_prescriptive_update(app, df_2019):
    @app.callback([
        Output('prescriptive_case_1_average', 'children'),
        Output('prescriptive_case_2_average', 'children'),
        Output('prescriptive_p_value', 'children'),
        Output('prescriptive_result', 'figure')],
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

def call_callback_data_city(app):
    @app.callback([
        Output('city_card_max', 'children'),
        Output('city_gauge', 'children'),
        Output('city_card_min', 'children'),
        Output('city_table', 'figure'),
        ],
        [Input('analytics_city_filter_city', 'value')],
        [State('analytics_city_filter_state', 'value')]
    )
    def update_data_city(city, state):
        return update_city_dash(state, city)

def call_callback_city_dropdown(app):
    @app.callback(
        Output('analytics_city_filter_city', 'options'),
        [Input('analytics_city_filter_state', 'value')]
    )
    def update_data_dropdown_city(state):
        return update_city_dropdown(state)
    

def call_callback_country_bar_chart(app):
    @app.callback(
        Output('country_bar_char', 'figure'), 
        [Input('analytics_country_filter_option_bar_chart', 'value'),
        Input('analytics_country_filter_score_bar_chart', 'value')])
    def update_country_data_bar_chart(option, score):
        return update_country_bar_chart(option, score)

def call_callback_state_bar_chart(app):
    @app.callback(
        Output('state_bar_char', 'figure'), 
        [Input('analytics_state_filter_state', 'value'),
        Input('analytics_state_filter_variable_bar_chart', 'value')])
    def update_state_data_bar_chart(state, category):
        return update_onedim_bar_by_state(state, category)

def call_callback_city_bar_chart(app):
    @app.callback(
        Output('city_bar_char', 'figure'), 
        [Input('analytics_city_filter_city', 'value'),
        Input('analytics_city_filter_variable_bar_chart', 'value')],
        [State('analytics_city_filter_state', 'value')])
    def update_state_data_bar_chart(city, category, state):
        return update_onedim_bar_by_city(state, city, category)