import numpy as np
import pandas as np
import math

from dashboards.variables_info import *

ordered_variables_model = get_order_variables_model()

def fill_column_given_percentages(size, categories, percentages):
    final_size = 0
    sizes = []
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

def fill_column_randomly(size, categories, percentages):
    return list(np.random.choice(categories, size=size, p=percentages))

def generate_prescriptive_dataset(size, prescriptive_columns, df):

    df_output = df.sample(n=size)
    
    for column in prescriptive_columns:
        categories = prescriptive_columns[column]['categories']
        percentages = prescriptive_columns[column]['percentages']
        column_data = fill_column_given_percentages(size, categories, percentages)
        df_output['temp_column'] = column_data
        df_output[column] = df_output['temp_column']
        df_output.drop('temp_column', axis = 1, inplace = True)    
    
    return df_output