import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State

from dashboards.filter_view import get_filter_view
from dashboards.heat_map import get_heat_map

def get_dash(columns_to_choose, numeric_cols):
    return html.Div([
        
        get_filter_view(columns_to_choose, [], numeric_cols),
        get_heat_map(columns_to_choose)
        
        ])