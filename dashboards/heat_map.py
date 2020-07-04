import dash_core_components as dcc
import dash_html_components as html

def get_heat_map(categories):

    return html.Div(children=[
                      html.Div(className='six rows',  # Define the row element
                               children=[html.Div(className='three columns div-user-controls',
                                            children = [
                                                html.H2(' Saber11 Analytics project'),
                                                html.P('''Visualizing the contigency table amongst different dimensions '''),
                                                html.P('''Select two categories to visualize the heat map'''),
                                                html.H5('Valor Vertical'),
                                                html.Div([
                                                    dcc.Dropdown(id="selected-vertical",
                                                                 options=[{"label": i, "value": i} for i in categories],
                                                                 value='FAMI_EDUCACIONPADRE',
                                                                 searchable=True,
                                                                 style={"display": "block", "width": "80%"})
                                                ]),
                                                html.H5('Valor Horizontal'),
                                                html.Div([
                                                    dcc.Dropdown(id="selected-horizontal",
                                                                 options=[{"label": i, "value": i} for i in categories],
                                                                 value='FAMI_EDUCACIONMADRE',
                                                                 style={"display": "block", "width": "80%"})
                                                ]),
                                                ]
                                           ),
                                  html.Div(className='nine columns div-for-charts bg-grey',
                                           children=[
                                               html.Div([dcc.Graph(id="ru-my-heatmap",
                                                                   style={"margin-right": "auto",
                                                                             "margin-left": "auto",
                                                                             "width": "100%",
                                                                             "height":"800px"})
                                           ])  # Define the right element
                                  ])
                                ])
                            ])