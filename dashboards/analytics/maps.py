import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import warnings
warnings.filterwarnings('ignore')

class maps():

    def __init__(self):
        self.get_state_map_geoson()
        self.get_city_map_geoson()
        self.get_dfs()
        self.get_colombiandf_from_file()
    
    def get_state_map_geoson(self): 
        with open('data/DptoGeo_FeaturesToJSON.json') as geo1:
            geodept = json.loads(geo1.read())
        for i, _ in enumerate(geodept["features"]):
            geodept["features"][i]['id'] = geodept["features"][i]['properties']['DPTO']

        self.geodept = geodept

    def get_city_map_geoson(self):
        with open('data/Mpio_geo_FeaturesToJSON.json') as geo2:
            geompio = json.loads(geo2.read())    
        for i, _ in enumerate(geompio['features']):
            geompio['features'][i]['id']=geompio['features'][i]['properties']['DPTO'] + geompio['features'][i]['properties']['MPIO']
        self.geompio = geompio

    def get_dfs(self):
        self.df_main = pd.read_excel('data/CITY_SUMMARY_SB11_20192.xlsx',sheet_name=0)
        self.df_code = pd.read_excel('data/STATE_CITY_MAPS_INFO.xlsx',sheet_name=0)
        self.df_lat_lon = pd.read_csv('data/df_departamentos.csv')

    def get_colombiandf_from_file(self):
        df_main = self.df_main.copy()
        df_code = self.df_code.copy()
        df_code = df_code[['ESTU_DEPTO_RESIDE','ESTU_COD_RESIDE_DEPTO']]
        df_main = df_main.merge(df_code,how='inner',  left_on='ESTU_DEPTO_RESIDE', right_on='ESTU_DEPTO_RESIDE')
        df_main = df_main.drop_duplicates().reset_index(drop=True)
        df_main['PUNT_GLOBAL'] = df_main.punt_global_sum / df_main.student_counter
        df_main = df_main.dropna()
        df_main['ESTU_COD_RESIDE_DEPTO_str'] = df_main['ESTU_COD_RESIDE_DEPTO'].apply(lambda x: str("%02d" % x))
        df_main = df_main[['ESTU_COD_RESIDE_DEPTO_str','PUNT_GLOBAL','student_counter','ESTU_COD_RESIDE_DEPTO']]
        self.colombia_df = df_main

    def get_statedf_from_file(self, state):
        #state = 'BOYACA'
        df_main = self.df_main.copy()
        df_main = df_main[df_main.ESTU_DEPTO_RESIDE == state ]
        df_code = self.df_code.copy()
        df_main = df_main.merge(df_code,how='inner',  left_on=['ESTU_DEPTO_RESIDE','ESTU_MCPIO_RESIDE'], right_on=['ESTU_DEPTO_RESIDE','ESTU_MCPIO_RESIDE'])
        df_main = df_main.drop_duplicates().reset_index(drop=True)
        df_main['PUNT_GLOBAL'] = df_main.punt_global_sum / df_main.student_counter
        df_main = df_main.dropna()
        df_main['ESTU_COD_RESIDE_DEPTO_str'] = df_main['ESTU_COD_RESIDE_DEPTO'].apply(lambda x: str("%02d" % x))
        df_main['ESTU_COD_RESIDE_MCPIO_str'] = df_main['ESTU_COD_RESIDE_DEPTO_str']+df_main.apply(lambda x: str.split(str(x['ESTU_COD_RESIDE_MCPIO']),sep=str(x['ESTU_COD_RESIDE_DEPTO']))[1],axis=1) 
        df_main = df_main[['ESTU_COD_RESIDE_MCPIO_str','PUNT_GLOBAL','student_counter','ESTU_COD_RESIDE_DEPTO']]
        dff = df_main
        dff.head()
        return df_main

    def get_state_center(self, state):
        df_lat_lon = self.df_lat_lon[self.df_lat_lon.Departamento == state]
        lat_center = float(df_lat_lon.Latitude)
        lon_center = float(df_lat_lon.Longitude)
        return lat_center, lon_center

    def draw_map(self, df, map_geoson,type):
        if type == 'Country':
            location_var = 'ESTU_COD_RESIDE_DEPTO_str'
            color_var = 'PUNT_GLOBAL'
            lat_center = 4.570868
            lon_center = -74.2973328
            zoom_val = 4
        else:
            location_var = 'ESTU_COD_RESIDE_MCPIO_str'
            color_var = 'PUNT_GLOBAL'
            zoom_val=6.5
            lat_center, lon_center = self.get_state_center(type)

        fig = go.Figure(go.Choroplethmapbox(geojson=map_geoson, 
                                            locations=df[location_var],
                                            z=df[color_var],
                                            colorscale="Viridis", 
                                            #colorscale=["red", "green"],
                                            zmin=df[color_var].min(),
                                            zmax=df[color_var].max(), 
                                            marker_opacity=0.95, 
                                            marker_line_width=0.1))

        fig.update_layout( mapbox_style="carto-positron",mapbox_zoom=zoom_val,mapbox_center = {"lat": lat_center, "lon": lon_center})
        fig.update_layout(margin={"r":10,"t":10,"l":10,"b":10})
        return fig

    def draw_colombian_map(self):
        fig = self.draw_map(self.colombia_df, self.geodept, 'Country')
        return fig

    def draw_state_map(self, state):
        df = self.get_statedf_from_file(state)
        fig = self.draw_map(df, self.geompio, state)
        return fig

if __name__ == "__main__":
    maps_obj = maps()
    print(maps_obj.draw_state_map('ARAUCA'))