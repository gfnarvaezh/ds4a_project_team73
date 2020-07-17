import pandas as pd

def get_df_from_state():
    """
    function can be replaced by a connection to db 
    and retrieve table of results by state only
    """
    #return pd.read_excel('data/STATE_SUMMARY_SB11_20192.xlsx',sheet_name=0)
    return pd.read_csv("data/STATE_SUMMARY_SB11_20192.csv",sep='¬', encoding='utf-8')

