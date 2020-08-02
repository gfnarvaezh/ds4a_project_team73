import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import json
import pandas as pd
import math
import numpy as np

import plotly.express as px

from dashboards.models_predict import predict_global_score
from dashboards.variables_info import get_order_variables_model
from dashboards.translator import translator_class

translator = translator_class()

with open('list_variables_plotly.json') as json_file:
    list_variables_ordered = json.load(json_file)

def get_prescriptive(columns_to_choose):
    columns_to_choose = translator.translate_list(columns_to_choose)
    output = get_prescriptive_filters(columns_to_choose)
    return output

def get_prescriptive_filters(columns_to_choose):
    return html.Div([
              
        html.Div([
            html.P(children='How to use this tool?', id='prescriptive_description_title'),
            html.P(children='In this section, you can simulate two scenarios and see how it would affect the score of the students. In the boxes below, select the variables you want to analyze and fill the percentages acordingly. The number of samples is just the number of students involved in the simulation (a bigger number is better, but the simulation takes longer). ', id='prescriptive_description'),
        ], id='prescriptive_description_box'),

        html.Div([
            html.P('Choose the variables to analyze'),

            html.Div([
                dcc.Dropdown(
                    id='prescriptive_variables',
                    options=[{'label': i, 'value': i} for i in columns_to_choose],
                    value=translator.translate('FAMI_ESTRATOVIVIENDA'),
                    multi=True
                )
            ]),

            html.P('Sample size: ', id = 'prescriptive_sample_size_text'),
            dcc.Input(id="prescriptive_sample_size", type="number", value = 1000),
            html.Button(id='calculate_button', n_clicks=0, children='Calculate'),
            html.Div(
                [html.Div(children = ' ', id="prescriptive_id_" + str(i)) for i in range(0,100)],
                id='prescriptive_filter'),
        ],
        id='prescriptive_filter_outer_box'
        ),
        html.Div([
            dcc.Loading(
                        id="loading-2",
                        children=dcc.Graph(id='prescriptive_result'),
                        type="circle"
                    ),
            html.Div([
                html.P('Case 1 average: '),
                html.Div( id = 'prescriptive_case_1_average')
            ], id = 'prescriptive_case_1_average_box', className = 'prescriptive_summary'),
            html.Div([
                html.P('Case 2 average: '),
                html.Div( id = 'prescriptive_case_2_average')
            ], id = 'prescriptive_case_2_average_box', className = 'prescriptive_summary'),
            html.Div([
                html.P('Difference: '),
                html.Div( id = 'prescriptive_p_value')
            ], id = 'prescriptive_p_value_box', className = 'prescriptive_summary')
        ],
        id = 'prescriptive_result_box'
        )
    ])

class prescriptive_class():
    def __init__(self):
        self.ids_number = 0
        self.variables_list = []

    def get_list_prescriptive(self, df, columns):
        self.ids_number = 0
        self.variables_list = []
        if type(columns) == str:
            columns = [translator.to_original(columns)]
        if type(columns) == list:
            columns = translator.to_original_list(columns)
            output = []
            for column in columns:
                output += self.get_list_prescriptive_one_column(df, column)

            for i in range(self.ids_number, 100):
                output.append(html.Div(children = ' ', id="prescriptive_id_" + str(i)))

            return output
        else:
            raise Exception('Getting incorrect data type from columns selection in filter')

    def get_list_prescriptive_one_column(self, df, column):
        output = [html.H4(translator.translate(column))]
        sorted_values = sorted(df[column].unique())

        if column in list_variables_ordered:
            temp_sorted_variables = []
            for value in list_variables_ordered[column][0]:
                if value in sorted_values:
                    temp_sorted_variables.append(value)
            sorted_values = temp_sorted_variables
            
        variables = []
        #Headers columns prescriptive
        output.append(html.P('Variable name', className = 'prescriptive_var_text prescriptive_var_title'))
        output.append(html.P('Case 1', className = 'prescriptive_var_box prescriptive_var_title'))
        output.append(html.P('Case 2', className = 'prescriptive_var_box prescriptive_var_title'))
        output.append(html.P('Variable name', className = 'prescriptive_var_text prescriptive_var_title'))
        output.append(html.P('Case 1', className = 'prescriptive_var_box prescriptive_var_title'))
        output.append(html.P('Case 2', className = 'prescriptive_var_box prescriptive_var_title'))

        for value in sorted_values:
            output.append(html.P(translator.translate(value), className = 'prescriptive_var_text'))
            output.append(dcc.Input(id="prescriptive_id_" + str(self.ids_number), type="number", value = 0, className = 'prescriptive_var_box prescriptive_case_1', persistence = True, min = 0, max = 100))
            self.ids_number += 1
            output.append(dcc.Input(id="prescriptive_id_" + str(self.ids_number), type="number", value = 0, className = 'prescriptive_var_box prescriptive_case_2', persistence = True, min = 0, max = 100))
            self.ids_number += 1
            variables.append(value)

        self.variables_list.append(variables)

        return output

    def get_variables_from_text_boxes(self):
        return self.variables_list

    def update_prediction(self, df, dic_entrada):
        try:
            values = self.allocate_variables_with_values(dic_entrada)
            print(values)
            df_sampled = df[get_order_variables_model()].sample(n=values['size'], replace = True)
            df_base = generate_prescriptive_dataset(values['percentages'], 'percentages_base', df_sampled)
            df_evaluation = generate_prescriptive_dataset(values['percentages'], 'percentages_evaluation', df_sampled)

            results_base = predict_global_score(df_base)
            results_evaluation = predict_global_score(df_evaluation)

            result = pd.concat([results_base, results_evaluation], axis=1)
            result.columns = ['Case 1', 'Case 2']

            average_case_1 = round(result['Case 1'].mean(), 1)
            average_case_2 = round(result['Case 2'].mean(), 1)
            difference = round(average_case_2 - average_case_1, 1)
            

            return average_case_1, average_case_2, difference, px.histogram(result, histnorm='probability density', barmode="overlay")
        except Exception as e:
            print(e)
            return 'Nothing yet', 'Nothing yet', 'Nothing yet', px.histogram(barmode="overlay")

    def allocate_variables_with_values(self, dic_entrada):
        values = {}
        values['percentages'] = {}
        values['columns'] = dic_entrada['args'][1]
        values['size'] = dic_entrada['args'][2]

        init = 3
        final = 3

        if type(values['columns']) == str:
            values['columns'] = [values['columns']]

        values['columns'] = translator.to_original_list(values['columns'] )

        for index, column in enumerate(values['columns']):
            values['percentages'][column] = {}
            values_column = self.variables_list[index]
            final += len(values_column)*2
            values['percentages'][column]['categories'] = values_column

            percentages_aggregated = dic_entrada['args'][init:final]

            percentages_base = []
            percentages_evaluation = []

            for index, value in enumerate(percentages_aggregated):
                if index%2 == 0:
                    percentages_base.append(value)
                else:
                    percentages_evaluation.append(value)

            values['percentages'][column]['percentages_base'] = percentages_base
            values['percentages'][column]['percentages_evaluation'] = percentages_evaluation
            
            init = final

        return values
            

def generate_prescriptive_dataset(prescriptive_columns, percentage_type, df):
    
    size = df.shape[0]
    df_output = df.copy()

    for column in prescriptive_columns:
        categories = prescriptive_columns[column]['categories']
        percentages = prescriptive_columns[column][percentage_type]
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