import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

#importing data
df_2019 = pd.read_csv('SB11_20191.TXT',sep='¬', header = None, skiprows= 0, nrows=50000, encoding='utf-8')
new_header = df_2019.iloc[0] #grab the first row for the header
df_2019 = df_2019[1:] #take the data less the header row
df_2019.columns = new_header

columns_to_choose = ['ESTU_DEPTO_RESIDE', 
'COLE_NATURALEZA', 
'ESTU_GENERO', 
'FAMI_ESTRATOVIVIENDA',
'FAMI_PERSONASHOGAR',
'FAMI_CUARTOSHOGAR',
'FAMI_EDUCACIONPADRE',
'FAMI_EDUCACIONMADRE',
'FAMI_NUMLIBROS',
'FAMI_COMELECHEDERIVADOS',
'FAMI_COMECARNEPESCADOHUEVO',
'FAMI_COMECEREALFRUTOSLEGUMBRE',
'FAMI_SITUACIONECONOMICA',
'ESTU_DEDICACIONLECTURADIARIA',
'ESTU_DEDICACIONINTERNET',
'ESTU_HORASSEMANATRABAJA']

numeric_cols = ['PUNT_LECTURA_CRITICA',
'PERCENTIL_LECTURA_CRITICA',
'DESEMP_LECTURA_CRITICA',
'PUNT_MATEMATICAS',
'PERCENTIL_MATEMATICAS',
'DESEMP_MATEMATICAS',
'PUNT_C_NATURALES',
'PERCENTIL_C_NATURALES',
'DESEMP_C_NATURALES',
'PUNT_SOCIALES_CIUDADANAS',
'PERCENTIL_SOCIALES_CIUDADANAS',
'DESEMP_SOCIALES_CIUDADANAS',
'PUNT_INGLES',
'PERCENTIL_INGLES',
#'DESEMP_INGLES',
'PUNT_GLOBAL',
'PERCENTIL_GLOBAL',
'ESTU_INSE_INDIVIDUAL',
'ESTU_NSE_ESTABLECIMIENTO',
'ESTU_NSE_INDIVIDUAL']

df_2019 = df_2019[numeric_cols + columns_to_choose].fillna('No_data')

for col in  numeric_cols:
    df_2019[col] = df_2019[col].astype(str).replace('No_data', None).astype(float)

var_to_filter_list = columns_to_choose
var_to_see_list = columns_to_choose
filter_list = []

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([

    
    html.H1(children='ThisIsJustATest'),

    html.Div([
        html.P('var_to_filter'),

        html.Div([
            dcc.Dropdown(
                id='var_to_filter',
                options=[{'label': i, 'value': i} for i in var_to_filter_list],
                value='ESTU_DEPTO_RESIDE'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.P('Filter'),
        html.Div([
            dcc.Dropdown(
                id='filter',
                options=[{'label': i, 'value': i} for i in filter_list],
                value='SANTANDER'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.P('var_to_see'),
        html.Div([
            dcc.Dropdown(
                id='var_to_see',
                options=[{'label': i, 'value': i} for i in var_to_see_list],
                value='FAMI_ESTRATOVIVIENDA'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.P('score_to_see'),
        html.Div([
            dcc.Dropdown(
                id='score_to_see',
                options=[{'label': i, 'value': i} for i in numeric_cols],
                value='PUNT_GLOBAL'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic')
])


def filter_function(df, var_to_filter, filter):
    return df_2019[df_2019[var_to_filter] == filter]

@app.callback(
    Output('filter', 'options'),
    [Input('var_to_filter', 'value')])
def update_filter(var_to_filter):
    return [{'label': i, 'value': i} for i in sorted(df_2019[var_to_filter].unique())]

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('var_to_filter', 'value'),
    Input('filter', 'value'),
    Input('var_to_see', 'value'),
    Input('score_to_see', 'value')])
def update_graph(var_to_filter, filter, var_to_see, score_to_see):
    df = filter_function(df_2019, var_to_filter, filter)
    return px.violin(df, x=var_to_see, y=score_to_see, box=True)
    

if __name__ == '__main__':
    app.run_server(debug=True)