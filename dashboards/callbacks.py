from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import json

from dashboards.filter_view import *
from dashboards.simulator import update_result
from dashboards.prescriptive import *

from dashboards.tabs import *

def call_callbacks_tabs(app, df_2019, columns_to_choose, numeric_cols):
    @app.callback(
        Output("app-content", "children"),
        [Input("tabs", "value")])
    def update_content(tab_name):
        return build_content_for_tab(tab_name, columns_to_choose, numeric_cols)

def call_callbacks_view_filter(app, df_2019):
    @app.callback(
        Output('filter', 'options'),
        [Input('var_to_filter', 'value')])
    def update_filter(var_to_filter):
        return test_update_filter(df_2019, var_to_filter)

    @app.callback(
        Output('indicator-graphic', 'figure'),
        [Input('var_to_filter', 'value'),
        Input('filter', 'value'),
        Input('var_to_see', 'value'),
        Input('score_to_see', 'value')])
    def update_graph(var_to_filter, filter, var_to_see, score_to_see):
        return test_update_graph(df_2019, var_to_filter, filter, var_to_see, score_to_see)

def call_callback_heat_map(app, df_2019):
    @app.callback(
        Output("ru-my-heatmap", "figure"),
        [Input("selected-horizontal", "value"),
        Input("selected-vertical", "value")])
    def update_figure(horizontal, vertical):
        print(" selected horizotal is ", horizontal)
        print(" selected vertical is ", vertical)
        #horizontal = 'FAMI_EDUCACIONPADRE'
        #vertical = 'FAMI_EDUCACIONMADRE'
        cols = [horizontal, vertical, 'PERCENTIL_GLOBAL']
        dff = df_2019.groupby([horizontal, vertical])['PERCENTIL_GLOBAL'].mean().reset_index()
        heatmap1_data = pd.pivot_table(dff, values='PERCENTIL_GLOBAL',
                                    index=[vertical],
                                    columns=horizontal)
        trace = go.Heatmap(z=heatmap1_data.values.tolist()
                        , x=heatmap1_data.columns.tolist()
                        , y=heatmap1_data.index.tolist()
                        , colorscale='rdylgn', colorbar={"title": "Average", 'x': -.09}, showscale=True)
        return {"data": [trace]
            , "layout": {
                "xaxis": {"automargin": False}
                , "yaxis": {"automargin": True, 'side': "right"}
                , "margin": {"t": 10, "l": 30, "r": 100, "b": 230}
            }}


with open('list_variables_plotly.json') as json_file:
    list_variables_plotly = json.load(json_file)

inputs = [Input('filter_' + str(variable), 'value') for variable in list_variables_plotly]

def call_callback_simulator(app):
    @app.callback(
        Output("result_simulation", "children"),
        inputs)
    def update_content(*args):
        return update_result(locals())


def call_callbacks_prescriptive_filter(app, df_2019):
    @app.callback(
        Output('prescriptive_filter', 'children'), 
        [Input('prescriptive_variables', 'value')])
    def update_list_prescriptive(prescriptive_variables):
        return get_list_prescriptive(df_2019, prescriptive_variables)

def call_callbacks_prescriptive_update(app, df_2019):
    @app.callback(
        Output('prescriptive_result', 'figure'),
        [Input('calculate_button', 'n_clicks')],
        [State('prescriptive_variables', 'value')] + 
        [State('prescriptive_sample_size', 'value')] + 
        [State('prescriptive_id_' + str(i), 'value') for i in range(0,100)]
    )
    def update_result(*args):
        return update_prediction(df_2019, locals())
    