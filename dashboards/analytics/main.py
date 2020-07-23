import dash_bootstrap_components as dbc
import dash_html_components as html
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

from dashboards.analytics.load_dataframes import get_df_from_state

from dashboards.analytics.headers import get_header_state, get_header_country, get_df_city
from dashboards.analytics.maps import maps

df_city = get_df_city()
list_cities = df_city['ESTU_DEPTO_RESIDE'].unique()
maps_object = maps()

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
        ),
        html.Div([
            dcc.Loading(
                        id="loading_country_map",
                        children=dcc.Graph(id = 'country_map'),
                        type="circle"
                    )
        ]),
         ]
    )
    return dashboard

def get_state_dash(state):
    dashboard = html.Div(
    [
        dbc.Row(
            [   dbc.Col(dcc.Dropdown(
                    id='analytics_state_filter_state',
                    options=[{'label': i, 'value': i} for i in list_cities],
                    value='CORDOBA',
                    clearable=False), width = 2),
                dbc.Col(' ',width=2, id = 'state_card_max'),
                dbc.Col(' ',width=5, id = 'state_gauge'),
                dbc.Col(' ',width=2, id = 'state_card_min'),
                dbc.Col(' ',width=1),
            ],
            className="mb-4 header_analytics",
        ),
        html.Div([
            dcc.Loading(
                        id="loading_state_map",
                        children=dcc.Graph(id = 'state_map'),
                        type="circle"
                    )
        ]),
        ],
        id = 'state_dashboard'
    )

    return dashboard

def update_state_dash(state):
    returnable = get_header_state(state)
    print(len(returnable))
    return get_header_state(state) + (maps_object.draw_state_map(state),)

def update_country_dash():
    return get_header_country() + (maps_object.draw_colombian_map(),)