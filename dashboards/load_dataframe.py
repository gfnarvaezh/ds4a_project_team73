import pandas as pd

from dashboards.ordered_variables import *

def load_file(file_name):

    #importing data
    df_2019 = pd.read_csv(file_name, sep='¬', header = None, skiprows= 0, nrows=50000, encoding='utf-8')
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
    
    ordered_variables = get_ordered_variables()

    for col in columns_to_choose:
        if col in ordered_variables:
            df_2019[col] = pd.Categorical(df_2019[col], 
                        categories=ordered_variables[col],
                        ordered=True).astype(str)


    for col in  numeric_cols:
        df_2019[col] = df_2019[col].astype(str).replace('No_data', None).astype(float)

    return (df_2019, columns_to_choose, numeric_cols)