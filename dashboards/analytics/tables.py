import plotly.express as px
import pandas as pd
from dashboards.translator import translator_class
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash_core_components as dcc

def get_table_from_state(state):
    df_main = pd.read_excel('data/CITY_SUMMARY_SB11_20192.xlsx',sheet_name=0)
    df_main = df_main[df_main.ESTU_DEPTO_RESIDE == state ]
    df_main.index = df_main.ESTU_MCPIO_RESIDE
    df_main = df_main[['student_counter','punt_global_sum']]
    df_main['Average Score'] =  round(df_main['punt_global_sum']/df_main['student_counter'],2)
    df_main.sort_values(by='Average Score', ascending=False,inplace=True)
    df_main = df_main[['student_counter','Average Score']]
    df_main['student_counter'] = round(df_main['student_counter'],0)
    df_main.columns = ['Number of Students','Average Score']
    return df_main


def get_table_from_city(state,city):
    df_main = pd.read_excel('data/SCHOOL_SUMMARY_SB11_20192.xlsx',sheet_name=0)
    df_main = df_main[(df_main.ESTU_DEPTO_RESIDE==state)&(df_main.ESTU_MCPIO_RESIDE==city)]
    df_main.index = df_main.COLE_NOMBRE_SEDE
    df_main = df_main[['student_counter','punt_global_sum']]
    df_main['Average Score'] =  round(df_main['punt_global_sum']/df_main['student_counter'],2)
    df_main.sort_values(by='Average Score', ascending=False,inplace=True)
    df_main = df_main[['student_counter','Average Score']]
    df_main['student_counter'] = round(df_main['student_counter'],0)
    df_main.columns = ['Number of Students','Average Score']
    return df_main

def draw_table_by_state(state):
    df = get_table_from_state(state)
    fig = ff.create_table(df, index=True)
    return fig

def draw_table_by_city(state,city):
    df = get_table_from_city(state,city)
    fig = ff.create_table(df, index=True)
    #fig.layout.width=1200
    for i in range(len(fig.layout.annotations)):
        fig.layout.annotations[i].font.size = 8
    return fig

def get_table_city(state, city):
    return draw_table_by_city('CAUCA','MIRANDA')