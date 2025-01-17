import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dashboards.dash_test import get_dash
from dashboards.filter_view import *
from dashboards.simulator import get_simulator
from dashboards.prescriptive import get_prescriptive

def build_tabs():
    return dcc.Tabs(
        id="tabs",
        value='Analytics',
        children=[
            dcc.Tab(label='Analytics', value='Analytics'),
            dcc.Tab(label='Simulator', value='Predictive'),
            dcc.Tab(label='Forecasting and testing', value='Prescriptive')
        ]
    )

def build_content_for_tab(tab_name, columns_to_choose, numeric_cols):
    if tab_name == 'Analytics':
        return get_dash(columns_to_choose, numeric_cols)
    elif tab_name == 'Predictive':
        return get_simulator()
    elif tab_name == 'Prescriptive':
        return get_prescriptive(columns_to_choose)