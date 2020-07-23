import dash_bootstrap_components as dbc
import dash_html_components as html
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd

def get_df_from_state():
    """
    function can be replaced by a connection to db 
    and retrieve table of results by state only
    """
    df = pd.read_excel('data/STATE_SUMMARY_SB11_20192.xlsx',sheet_name=0)
    #df = pd.read_csv('data/STATE_SUMMARY_SB11_20192.csv',sep='¬', encoding='utf-8')
    return df
    
def get_df_city():
    return pd.read_csv("data/CITY_SUMMARY_SB11_20192.csv",sep='¬', encoding='utf-8')

def get_df_city_from_state(state):
    """
    function can be replaced by a connection to db 
    and retrieve table of results by state only
    """
    df_city = get_df_city()
    df_city = df_city[df_city.ESTU_DEPTO_RESIDE == state]
    return df_city

def get_df_college_from_state(state,city):
    """
    function can be replaced by a connection to db 
    and retrieve table of results by state only
    """
    #df_college = pd.read_csv("data/SCHOOL_SUMMARY_SB11_20192.csv",sep='¬', encoding='utf-8')
    df_college = pd.read_excel("data/SCHOOL_SUMMARY_SB11_20192.xlsx",sheetname=0)
    df_college = df_college[(df_college.ESTU_DEPTO_RESIDE == state)&(df_college.ESTU_MCPIO_RESIDE == city)]
    return df_college

def get_average_from_country_period(level,state,city,period = 20194,feature = 'punt_global_sum'):
    if level == 'country':
        df = get_df_from_state()
    elif level == 'state':
        df = get_df_city_from_state(state)
    else:
        df = get_df_college_from_state(state,city)
    df_temp = df.groupby('PERIODO').agg(student_counter=('student_counter','sum'),sum_total=(feature,'sum')).reset_index()
    average_val = float(df_temp['sum_total']/df_temp['student_counter'].values[0])
    return average_val

def get_min_average_from_country_period(level,state={},city={},period = 20194,feature = 'punt_global_sum'):
    df_temp = get_df_state_summary_from_country_period(level,state,city,period,feature)
    min_row = df_temp[df_temp.AVERAGE==df_temp.AVERAGE.min()].reset_index(drop=True)
    return min_row

def get_max_average_from_country_period(level,state={},city={},period = 20194,feature = 'punt_global_sum'):
    df_temp = get_df_state_summary_from_country_period(level,state,city,period,feature)    
    max_row = df_temp[df_temp.AVERAGE==df_temp.AVERAGE.max()].reset_index(drop=True)
    return max_row

def get_df_state_summary_from_country_period(level,state,city,period = 20194,feature = 'punt_global_sum'):
    if level == 'country':
        df = get_df_from_state()
        df_temp = df.groupby(['PERIODO','ESTU_DEPTO_RESIDE']).agg(student_counter=('student_counter','sum'),sum_total=(feature,'sum')).reset_index()
    elif level == 'state':
        df = get_df_city_from_state(state)
        df_temp = df.groupby(['PERIODO','ESTU_DEPTO_RESIDE','ESTU_MCPIO_RESIDE']).agg(student_counter=('student_counter','sum'),sum_total=(feature,'sum')).reset_index()
    else:
        df = get_df_college_from_state(state,city)
        df_temp = df.groupby(['PERIODO','ESTU_DEPTO_RESIDE','ESTU_MCPIO_RESIDE','COLE_NOMBRE_SEDE']).agg(student_counter=('student_counter','sum'),sum_total=(feature,'sum')).reset_index()
    df_temp['AVERAGE'] = df_temp['sum_total']/df_temp['student_counter']
    return df_temp

def get_state_summary_from_state_period(level,state,city,period,feature):
    df = get_df_state_summary_from_country_period(level,state,city,period,feature) 
    if level == 'country':
        df = df[df.ESTU_DEPTO_RESIDE == state].reset_index(drop=True)
    elif level == 'state':
        df = df[df.ESTU_MCPIO_RESIDE == city].reset_index(drop=True)
    else:
        #df = df[df.COLE_NOMBRE_SEDE == state].reset_index(drop=True)
        a=1
    return df

def get_average_state_gauge(level='country',state={},city={},period = 20194,feature = 'punt_global_sum'):
    minRow = get_min_average_from_country_period(level,state,city,period)
    maxRow = get_max_average_from_country_period(level,state,city,period)
    maxAverage = float(maxRow.AVERAGE) 
    minAverage = float(minRow.AVERAGE)
    average = get_average_from_country_period(level,state,city,period,feature)
    sumState = get_state_summary_from_state_period(level,state,city,period,feature)
    if level == 'country':
        Name = sumState.ESTU_DEPTO_RESIDE[0]    
    elif level == 'state':
        Name = sumState.ESTU_MCPIO_RESIDE[0]
    else:
        Name = sumState.COLE_NOMBRE_SEDE[0]

    Average = float(sumState.AVERAGE)
    layout = go.Layout(
      autosize=False,
      width=400,
      height=170,
      margin=dict(l=10, r=10, t=40, b=10))
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = Average,
        mode = "gauge+number+delta",
        title = {'text': "Average Result for "+Name.title()},
        delta = {'reference': average},
        gauge = {'axis': {'range': [None, 500]},
                'steps' : [
                    {'range': [0, minAverage], 'color': "lightgray"},
                    {'range': [minAverage, average], 'color': "red"},                 
                    {'range': [average, maxAverage], 'color': "lightgreen"}],
                'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 500}})
                ,layout=layout)
    fig.update_layout(width=400, height=170
    , font = {'color': "darkblue", 'family': "Arial"},
    )

    return fig            

def get_indicator_card(type,level='country',state={},city={}):
    """
    get_indicator_card 
    type : min, max. 
        'min':to get the lowest value
        'max':to get the highest value
    level : 'country', 'state', 'city'
    state : Name of the state in uppercase, or empty
    city :  Name of the city in uppercase or empty
    """
    if type == 'min':
        cardHeaderTitle = "Lowest Average Score"
        colorType = "danger"
        iconGly = "glyphicon glyphicon-triangle-bottom"
        if level == 'country':
            Row = get_min_average_from_country_period(level,feature = 'punt_global_sum')
            #location ='temp'
            location = Row.ESTU_DEPTO_RESIDE[0] 
        elif level == 'state':
            Row = get_min_average_from_country_period(level,state,feature = 'punt_global_sum')
            location = Row.ESTU_MCPIO_RESIDE[0]
        else:
            Row = get_min_average_from_country_period(level,state,city,feature = 'punt_global_sum')
            location = Row.COLE_NOMBRE_SEDE[0]   
            #location ='temp'
    else:
        cardHeaderTitle = "Highest Average Score"
        colorType = "success"
        iconGly = "glyphicon glyphicon-triangle-top"
        if level == 'country':
            Row = get_max_average_from_country_period(level,feature = 'punt_global_sum')
            location = Row.ESTU_DEPTO_RESIDE[0]
            print( Row ) 
        elif level == 'state':
            Row = get_max_average_from_country_period(level,state,feature = 'punt_global_sum')
            location = Row.ESTU_MCPIO_RESIDE[0]            
        else:
            Row = get_max_average_from_country_period(level,state,city,feature = 'punt_global_sum')
            location = Row.COLE_NOMBRE_SEDE[0]
            
    
    students = "Students : "+Row.student_counter[0].astype(str)
    stateAverage = round(float(Row.AVERAGE),0) 
    card_content = [
    dbc.CardHeader(cardHeaderTitle),
    dbc.CardBody(
        [
            html.H5(location.title()+', '+students, className="card-title"),
            
            html.Div(children=[
            html.Table([
                html.Tr( [html.Th(html.H1(stateAverage)),
                          html.Th(html.H1(html.I(className=iconGly)))])  ]) 
            ])
        ],
        style={"width": "40rem"},
    ),]
    var = dbc.Card(card_content, color=colorType, inverse=True)
    return var

def get_header_country():

    card_max_country = get_indicator_card('max', level='country')
    card_min_country = get_indicator_card('min', level='country')

    return card_max_country, card_min_country

def get_dash_country():
    return get_header_country()

def get_header_state(state='BOYACA'):
    state = 'BOYACA'
    card_max_state = get_indicator_card(type='max',level='state',state=state)
    gauge_state = dcc.Graph(figure=get_average_state_gauge(level='state',state=state,city='BERBEO'))
    card_min_state = get_indicator_card(type='min',level='state',state=state)
    return card_max_state, gauge_state, card_min_state

def get_dash_state(state = 'BOYACA'):
    state = 'BOYACA'
    print(state)
    return get_header_state(state)

if __name__ == "__main__":
    print(get_average_state_gauge(level='state',state='ARAUCA',city='BERBEO'))