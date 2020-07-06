import dash
import dash_core_components as dcc
import dash_html_components as html
import json
import pandas as pd
import math
import numpy as np

import plotly.express as px

from dashboards.models_predict import predict_global_score
from dashboards.variables_info import get_order_variables_model

style_box = {'width': 'calc(15% - 25px)', 'display': 'inline-block', 'font-size': '80%', 'padding': '0px 10px 0px 0px', 'margin': '0'}
style_text = {'width': 'calc(35% - 25px)', 'display': 'inline-block', 'font-size': '80%', 'padding': '0px 0px 0px 10px', 'margin': '0'}

ids_number = []
variables_list = []

with open('list_variables_plotly.json') as json_file:
    list_variables_ordered = json.load(json_file)

def get_prescriptive(columns_to_choose):
    output = get_prescriptive_filters(columns_to_choose)
    return output

def get_prescriptive_filters(columns_to_choose):
    return html.Div([
              
        html.H1(children='ThisIsJustATest'),

        html.Div([
            html.P('var_to_filter'),

            html.Div([
                dcc.Dropdown(
                    id='prescriptive_variables',
                    options=[{'label': i, 'value': i} for i in columns_to_choose],
                    value='FAMI_ESTRATOVIVIENDA',
                    multi=True
                )
            ],
            style={'width': '100%', 'display': 'inline-block'}),
            dcc.Input(id="prescriptive_sample_size", type="number", value = 1000),
            html.Button(id='calculate_button', n_clicks=0, children='Calculate'),
            html.Div(
                [html.Div(children = ' ', id="prescriptive_id_" + str(i)) for i in range(0,100)],
                id='prescriptive_filter', style={'width': '100%', 'display': 'inline-block'}),
        ],
        style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'top'}
        ),

        dcc.Graph(id='prescriptive_result', style={'width': '45%', 'display': 'inline-block'})

    ])

def get_list_prescriptive(df, columns):
    global ids_number, variables_list
    ids_number = 0
    variables_list = []
    if type(columns) == str:
        output = get_list_prescriptive_one_column(df, columns)
        for i in range(ids_number, 100):
            output.append(html.Div(children = ' ', id="prescriptive_id_" + str(i)))
        return output
    elif type(columns) == list:
        output = []
        for column in columns:
            output += get_list_prescriptive_one_column(df, column)

        for i in range(ids_number, 100):
            output.append(html.Div(children = ' ', id="prescriptive_id_" + str(i)))

        return output
    else:
        raise Exception('Getting incorrect data type from columns selection in filter')

def get_list_prescriptive_one_column(df, column):
    output = [html.H3(column)]
    sorted_values = sorted(df[column].unique())

    if column in list_variables_ordered:
        temp_sorted_variables = []
        for value in list_variables_ordered[column][0]:
            if value in sorted_values:
                temp_sorted_variables.append(value)
        sorted_values = temp_sorted_variables
        
    variables = []

    for value in sorted_values:
        output.append(html.P(value, style=style_text))
        global ids_number
        output.append(dcc.Input(id="prescriptive_id_" + str(ids_number), type="number", value = 0, style=style_box, persistence = True, min = 0))
        ids_number += 1
        variables.append(value)

    global variables_list
    variables_list.append(variables)

    return output

def get_variables_from_text_boxes():
    return variables_list

def update_prediction(df, dic_entrada):
    try:
        values = allocate_variables_with_values(dic_entrada)
        df_sampled = df[get_order_variables_model()].sample(n=values['size'])
        df_prescriptive = generate_prescriptive_dataset(values['percentages'], df_sampled)

        results_sampled = predict_global_score(df_sampled)
        results_prescriptive = predict_global_score(df_prescriptive)

        result = pd.concat([results_sampled, results_prescriptive], axis=1)
        result.columns = ['Base', 'Simulation']

        return px.histogram(result + 250, barmode="overlay")
    except:
        return px.histogram(barmode="overlay")

def allocate_variables_with_values(dic_entrada):
    values = {}
    values['percentages'] = {}
    values['columns'] = dic_entrada['args'][1]
    values['size'] = dic_entrada['args'][2]

    init = 3
    final = 3

    if type(values['columns']) == str:
        values['columns'] = [values['columns']]

    for index, column in enumerate(values['columns']):
        values['percentages'][column] = {}
        values_column = variables_list[index]
        final += len(values_column)
        values['percentages'][column]['categories'] = values_column
        values['percentages'][column]['percentages'] = dic_entrada['args'][init:final]
        init = final

    return values
        

def generate_prescriptive_dataset(prescriptive_columns, df):
    
    size = df.shape[0]
    df_output = df.copy()

    for column in prescriptive_columns:
        categories = prescriptive_columns[column]['categories']
        percentages = prescriptive_columns[column]['percentages']
        column_data = fill_column_given_percentages(size, categories, percentages)
        df_output['temp_column'] = column_data
        df_output[column] = df_output['temp_column']
        df_output.drop('temp_column', axis = 1, inplace = True)    
    
    return df_output

def fill_column_given_percentages(size, categories, percentages_raw):
    final_size = 0
    sizes = []

    percentages = fit_percentages(percentages_raw)

    for percentage in percentages:
        sizes.append(math.ceil(percentage*size))
        final_size += math.ceil(percentage*size)
    
    output = np.empty(final_size, dtype = '<U128')
    
    initial = 0
    final = 0
    
    for category, size_category in zip(categories, sizes):
        final += size_category
        output[initial:final] = category
        initial = final
    
    return list(np.random.choice(output, size, replace=False))


def fit_percentages(percentages_raw):
    sum_percentages = sum(percentages_raw)

    if sum_percentages != 0:
        return [percentage_raw/sum_percentages for percentage_raw in percentages_raw]
    else:
        return [1/len(percentages_raw) for i in percentages_raw]