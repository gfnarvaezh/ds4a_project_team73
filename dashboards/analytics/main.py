import dash_bootstrap_components as dbc
import dash_html_components as html
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

from dashboards.analytics.header_country import get_header_country, get_header_state, get_df_city
from dashboards.analytics.load_dataframes import get_df_from_state

df_city = get_df_city()
list_cities = df_city['ESTU_DEPTO_RESIDE'].unique()

def get_country_dash():
    dashboard =  html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dcc.Dropdown(
                    id='analytics_country_filter_period',
                    options=[{'label': i, 'value': i} for i in ['2019-2']],
                    value='2019-2',
                    clearable=False
                ),width=3, id='analytics_country_filter_period_box'),
                dbc.Col(' ',width=3, id = 'country_card_max'),
                dbc.Col(' ',width=1),
                dbc.Col(' ',width=3, id = 'country_card_min'),
                dbc.Col(' ',width=1),
            ],
            className="mb-4 header_analytics"
        ),  ]
    )
    return dashboard

def get_state_dash(state):
    dashboard = html.Div(
    [
        dbc.Row(
            [   dbc.Col(dcc.Dropdown(
                    id='analytics_state_filter_state',
                    options=[{'label': i, 'value': i} for i in list_cities],
                    value='BOYACA',
                    clearable=False), width = 2),
                dbc.Col(' ',width=2, id = 'state_card_max'),
                dbc.Col(' ',width=5, id = 'state_gauge'),
                dbc.Col(' ',width=2, id = 'state_card_min'),
                dbc.Col(' ',width=1),
            ],
            className="mb-4 header_analytics",
        ),  ],
        id = 'state_dashboard'
    )

    return dashboard