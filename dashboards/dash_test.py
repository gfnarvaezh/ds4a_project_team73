import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State

from dashboards.analytics.main import get_country_dash, get_state_dash, get_city_dash

def get_dash(columns_to_choose, numeric_cols):
    return html.Div([
        dcc.Tabs(
            id="tabs_analytics",
            value='Country',
            children=[
                dcc.Tab(label='Country', value='Country'),
                dcc.Tab(label='State', value='State'),
                dcc.Tab(label='City', value='City')
            ]
        ),
        html.Div(id='content_analytics')
        ])

def build_analytics_tab(tab_name, columns_to_choose):
    if tab_name == 'Country':
        return get_country_dash()
    elif tab_name == 'State':
        return get_state_dash(columns_to_choose)
    else:
        return get_city_dash(columns_to_choose)