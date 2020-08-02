import dash_bootstrap_components as dbc
import dash_html_components as html
import dash
import dash_html_components as html
import dash_core_components as dcc

from dashboards.analytics.load_dataframes import get_df_from_state

from dashboards.analytics.headers import get_header_state, get_header_country, get_header_city, get_df_city
from dashboards.analytics.tables import get_table_city
from dashboards.analytics.maps import maps
from dashboards.analytics.bar_charts import plot_country_ranks, draw_onedim_bar_by_state, draw_onedim_bar_by_city

from dashboards.translator import translator_class

df_city = get_df_city()
list_dptos = df_city['ESTU_DEPTO_RESIDE'].unique()
maps_object = maps()

translator = translator_class()

list_options = ['Top 5 states', 'Top 10 states', 'Bottom 5 states', 'Bottom 10 states']
list_scores = ['PUNT_LECTURA_CRITICA', 'PUNT_MATEMATICAS', 'PUNT_C_NATURALES', 'PUNT_SOCIALES_CIUDADANAS', 'PUNT_INGLES', 'PUNT_GLOBAL']

def get_country_dash():
    dashboard =  html.Div(
    [
        dbc.Row(
            [   
                dbc.Col(
                    html.Div([
                        html.P('Period: ', id = 'country_period_filter_text', className = 'title_dropdown_header'),
                        dcc.Dropdown(
                        id='analytics_country_filter_period',
                        options=[{'label': i, 'value': i} for i in ['2019-2']],
                        value='2019-2',
                        clearable=False
                )
                    ]),width=3, id='analytics_country_filter_period_box', className = 'title_dropdown_header_box'),
                dbc.Col(' ',width=3, id = 'country_card_max'),
                dbc.Col(' ',width=1),
                dbc.Col(' ',width=3, id = 'country_card_min'),
                dbc.Col(' ',width=1),
            ],
            className="mb-4 header_analytics"
        ),
        html.Div([
            html.Div(
                [
                dcc.Dropdown(
                    id='analytics_country_filter_option_bar_chart',
                    options=[{'label': i, 'value': i} for i in list_options],
                    value=list_options[0],
                    clearable=False
                ),
                #html.Div('Score: ', id = 'country_score_filter_text'),
                dcc.Dropdown(
                        id='analytics_country_filter_score_bar_chart',
                        options=[{'label': i, 'value': i} for i in translator.translate_list(list_scores)],
                        value=translator.translate(list_scores[-1]),
                        clearable=False
                    ),
                dcc.Loading(
                            id="loading_country_bar_chart",
                            children=dcc.Graph(id = 'country_bar_char'),
                            type="circle"
                        ),
                ], id = 'country_bar_char_box'
            ), 
            html.Div([
                dcc.Loading(
                        id="loading_country_map",
                        children=dcc.Graph(id = 'country_map'),
                        type="circle"
                    )
            ], id = 'country_map_box')
        ]),
         ]
    )
    return dashboard

def get_state_dash(columns_to_choose):
    dashboard = html.Div(
    [
        dbc.Row(
            [   
                dbc.Col(html.Div([
                    html.P('State: ', id = 'state_state_filter_text', className = 'title_dropdown_header'),
                    dcc.Dropdown(
                    id='analytics_state_filter_state',
                    options=[{'label': i, 'value': i} for i in list_dptos],
                    value='CORDOBA',
                    clearable=False)
                ], className = 'title_dropdown_header_box'), width = 2, className = 'title_dropdown_header_box'),
                dbc.Col(' ',width=3, id = 'state_card_max'),
                dbc.Col(' ',width=4, id = 'state_gauge'),
                dbc.Col(' ',width=3, id = 'state_card_min'),

            ],
            className="mb-4 header_analytics",
        ),
        html.Div([
            html.Div([
            dcc.Dropdown(
                    id='analytics_state_filter_variable_bar_chart',
                    options=[{'label': i, 'value': i} for i in translator.translate_list(columns_to_choose)],
                    value=translator.translate(columns_to_choose[-1]),
                    clearable=False
                ),
            dcc.Loading(
                        id="loading_state_bar_chart",
                        children=dcc.Graph(id = 'state_bar_char'),
                        type="circle"
                    ),
            ], id = 'state_bar_char_box'),
            html.Div([
            dcc.Loading(
                        id="loading_state_map",
                        children=dcc.Graph(id = 'state_map'),
                        type="circle"
                    )
            ], id = 'state_map_box')
        ]),
        ],
        id = 'state_dashboard'
    )

    return dashboard

#City

def get_city_dash(columns_to_choose):
    dashboard = html.Div(
    [
        dbc.Row(
            [   dbc.Col([
                    html.P('State: ', id = 'city_state_filter_text', className = 'title_dropdown_header'),
                    dcc.Dropdown(
                    id='analytics_city_filter_state',
                    options=[{'label': i, 'value': i} for i in list_dptos],
                    value='BOYACA',
                    clearable=False),
                    html.P('city: ', id = 'city_city_filter_text', className = 'title_dropdown_header'),
                    dcc.Dropdown(
                    id='analytics_city_filter_city',
                    value = 'TUNJA',
                    clearable=False),
                    
                    ], width = 2, className = 'title_dropdown_header_box'),
                dbc.Col(' ',width=3, id = 'city_card_max'),
                dbc.Col(' ',width=4, id = 'city_gauge'),
                dbc.Col(' ',width=3, id = 'city_card_min'),

            ],
            className="mb-4 header_analytics",
        ),
        html.Div([
        dcc.Dropdown(
                id='analytics_city_filter_variable_bar_chart',
                options=[{'label': i, 'value': i} for i in translator.translate_list(columns_to_choose)],
                value=translator.translate(columns_to_choose[-1]),
                clearable=False
            ),
        dcc.Loading(
                    id="loading_city_bar_chart",
                    children=dcc.Graph(id = 'city_bar_char'),
                    type="circle"
                ),
        ], id = 'city_bar_char_box'),
        html.Div([
            dcc.Loading(
                        id="loading_city_table",
                        children=dcc.Graph(id = 'city_table'),
                        type="circle"
                    )
            ], id = 'city_table_box')
        ],
        id = 'city_dashboard'
    )

    return dashboard

def update_state_dash(state):
    returnable = get_header_state(state)
    print(len(returnable))
    return get_header_state(state) + (maps_object.draw_state_map(state),)

def update_country_dash():
    return get_header_country() + (maps_object.draw_colombian_map(),)

def update_city_dash(state, city):
    return get_header_city(state, city) + (get_table_city(state, city),)

def update_city_dropdown(state):
    list_cities = df_city[df_city['ESTU_DEPTO_RESIDE'] == state]['ESTU_MCPIO_RESIDE']
    return [{'label': i, 'value': i} for i in list_cities]

def update_country_bar_chart(option, score):
    return plot_country_ranks(option, translator.to_original(score))

def update_onedim_bar_by_state(state, category):
    return draw_onedim_bar_by_state(state, category=translator.to_original(category))

def update_onedim_bar_by_city(state, city, category):
    return draw_onedim_bar_by_city(state,city,translator.to_original(category))