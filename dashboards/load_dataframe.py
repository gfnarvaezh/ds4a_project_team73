import pandas as pd
import datetime

from dashboards.variables_info import *

def load_file(file_name):

    #importing data
    df_2019 = pd.read_csv(file_name, sep='¬', header = None, skiprows= 0, nrows=50000, encoding='utf-8')
    new_header = df_2019.iloc[0] #grab the first row for the header
    df_2019 = df_2019[1:] #take the data less the header row
    df_2019.columns = new_header

    ordered_variables = get_ordered_variables()
    numeric_cols = get_numerical_variables()
    unused_variables = get_unused_variables()
    irrelevant_variables = get_irrelevant_variables()
    columns_model = get_order_variables_model()

    #df_2019 = df_2019[numeric_cols + columns_to_choose + ['ESTU_FECHANACIMIENTO']]
    df_2019 = df_2019.drop(irrelevant_variables + unused_variables, 1).fillna('No data')

    for col in df_2019.keys():
        if col in ordered_variables:
            df_2019[col] = pd.Categorical(df_2019[col], 
                        categories=ordered_variables[col],
                        ordered=True).astype(str)

    df_2019 = df_2019.fillna('No data').replace('nan', 'No data')

    df_2019['ESTU_FECHANACIMIENTO'] = pd.to_datetime(df_2019['ESTU_FECHANACIMIENTO'])
    df_2019['EDAD'] = (datetime.datetime(2020, 1, 1) - df_2019['ESTU_FECHANACIMIENTO']).dt.days/365
    df_2019['EDAD'] = df_2019['EDAD'].round(0)

    df_2019.drop('ESTU_FECHANACIMIENTO', 1, inplace = True)

    mask = (df_2019['ESTU_NACIONALIDAD'] != 'COLOMBIA')
    df_2019.loc[mask, 'ESTU_NACIONALIDAD'] = 'EXTRANJERO'

    for col in  numeric_cols:
        df_2019[col] = df_2019[col].astype(str).replace('No data', None).astype(float)

    return (df_2019, columns_model, numeric_cols)