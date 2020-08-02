
import plotly.express as px
import pandas as pd
from dashboards.translator import translator_class
from plotly.subplots import make_subplots
import plotly.graph_objects as go

#######################################
def get_country_summary():
    df_main = pd.read_excel('data/STATE_SUMMARY_SB11_20192.xlsx',sheet_name=0)
    return df_main

def read_state_category_agg(state,category):
    filename = 'data/' + category + '_STATE_CAT_SB11_20192.xlsx'
    df_main = pd.read_excel(filename ,sheet_name=0)
    df_main = df_main[df_main.ESTU_DEPTO_RESIDE == state]
    return df_main

def read_city_category_agg(state,city,category):
    filename = 'data/' + category + '_CITY_CAT_SB11_20192.xlsx'
    df_main = pd.read_excel(filename ,sheet_name=0)
    df_main = df_main[(df_main.ESTU_DEPTO_RESIDE == state)&(df_main.ESTU_MCPIO_RESIDE == city)]
    return df_main

def read_college_category_agg(state,city,college,category):
    filename = 'data/' + category + '_CITY_CAT_SB11_20192.xlsx'
    df_main = pd.read_excel(filename ,sheet_name=0)
    df_main = df_main[(df_main.ESTU_DEPTO_RESIDE == state)&(df_main.ESTU_MCPIO_RESIDE == city)&(df_main.COLE_NOMBRE_ESTABLECIMIENTO==college)]
    return df_main

def read_country_category_agg(category):
    filename = 'data/' + category + '_COUNTRY_CAT_SB11_20192.xlsx'
    df_main = pd.read_excel(filename ,sheet_name=0)
    return df_main
    
def draw_onedim_bar_by_state(state,category='FAMI_ESTRATOVIVIENDA',value='punt_global'):
    columns = ['ESTU_DEPTO_RESIDE','PERIODO','student_counter']
    measure = value.lower()+"_sum"
    columns.append(measure)
    columns.append(category)
    df = read_state_category_agg(state,category)[columns]
    Average = 'Average_'+measure
    df[Average] = round(df[measure]/df['student_counter'],2)
    #Translation 
    df.columns = get_label_from_list(df.columns)
    category = get_label_from_dimension(category)
    Average = Average.title()
    fig = px.bar(df, y=category, x='Student_Counter',
             hover_data=[Average], color=Average,
             orientation='h',
             color_continuous_scale='Viridis',
             labels={'Student_Counter':'Number of students of '+state.title()}, height=400)
    
    fig.update_layout(height=500, plot_bgcolor='rgb(255,255,255)')
    return fig

def draw_onedim_bar_by_city(state,city,category='FAMI_ESTRATOVIVIENDA',value='punt_global'):
    columns = ['ESTU_DEPTO_RESIDE','ESTU_MCPIO_RESIDE','PERIODO','student_counter']    
    measure = value.lower()+"_sum"
    columns.append(measure)
    columns.append(category)
    df = read_city_category_agg(state,city,category)[columns]
    Average = 'Average_'+measure
    df[Average] = round(df[measure]/df['student_counter'],2)
    #Translation 
    df.columns = get_label_from_list(df.columns)
    category = get_label_from_dimension(category)
    Average = Average.title()

    fig = px.bar(df, y=category, x='Student_Counter',
             hover_data=[Average], color=Average,
             orientation='h',
             color_continuous_scale='Viridis',
             labels={'Student_Counter':'Number of students of '+city.title()}, height=400)
    
    fig.update_layout(height=500, plot_bgcolor='rgb(255,255,255)')
    return fig     

def draw_top_rank_country(n_rank,ascending=False,value='punt_global'):
    measure = value.lower()+"_sum"
    columns = ['ESTU_DEPTO_RESIDE','PERIODO','student_counter']
    columns.append(measure)
    df = get_country_summary()[columns]
    Average = 'Average_'+measure  
    df[Average] = round(df[measure]/df['student_counter'],2)
    df.sort_values(by=Average, ascending=ascending, inplace=True)
    df = df[:n_rank]
    df.sort_values(by='student_counter', ascending=ascending, inplace=True)
    #Translation 
    df.columns = get_label_from_list(df.columns)
    category = get_label_from_dimension('ESTU_DEPTO_RESIDE')
    Average = Average.title()
    fig = px.bar(df, y=category, x='Student_Counter',
             hover_data=[Average], color=Average,
             orientation='h',
             color_continuous_scale='Viridis',
             labels={'Student_Counter':'Number of students by state'}, height=400)
    return fig

def draw_donut_for_onedim_in_country(category='FAMI_ESTRATOVIVIENDA',value='punt_global'):
    measure = value.lower()+"_sum"
    df = read_country_category_agg(category)
    Average = 'Average_'+measure  
    df[Average] = round(df[measure]/df['student_counter'],2)
    # Use `hole` to create a donut-like pie chart
    fig = px.pie(df,values='student_counter', names=category,hole=.4,color_discrete_sequence=px.colors.sequential.RdBu)
    return fig

def plot_country_ranks(option='Top 5 states',measure ='PUNT_GLOBAL'):
    """
    option can take the following values :
    1 : The Highest 5 states with the average displayed
    2 : The Highest 10 states with the average displayed
    3 : The Lowest 5 states with the average displayed
    1 : The Lowest 10 states with the average displayed
    Measure can take the following vairables :
    PUNT_LECTURA_CRITICA
    PUNT_MATEMATICAS
    PUNT_C_NATURALES
    PUNT_SOCIALES_CIUDADANAS
    PUNT_INGLES
    PUNT_GLOBAL

    """
    if option == 'Top 5 states':
        #Top Rank 5
        fig=draw_top_rank_country(5,ascending=False,value=measure)
    elif option == 'Top 10 states':
        #Top Rank 10
        fig=draw_top_rank_country(10,ascending=False,value=measure)
    elif option == 'Bottom 5 states':
        #Bottom Rank 5
        fig=draw_top_rank_country(5,ascending=True,value=measure)
    elif option == 'Bottom 10 states':
        #Bottom Rank 5
        fig=draw_top_rank_country(10,ascending=True,value=measure)
    return fig

def get_label_from_dimension(dim,language='english'):
    DIM = dim.upper()
    translator = translator_class()
    translatedDIM = translator.translate(DIM).title()
    return translatedDIM

def get_label_from_list(list,language='english'):
    translator = translator_class()
    translatedList = translator.translate_list(list)
    translatedList =[ i.title() for i in translatedList ]
    return translatedList