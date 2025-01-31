# -*- coding: utf-8 -*-
# @Time    : 8/20/20 2:39 PM
# @Author  : Saptarshi
# @Email   : saptarshi.mitra@tum.de
# @File    : app.py
# @Project: group07
#
# ************************************
# Write all the callbacks in src/controllers for avoiding merge conflict, don't forget to import here!!
# *************************************

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np
from controllers.callbacks import register_callbacks
from dash_extensions.enrich import Dash
import pickle
import plotly.graph_objects as go

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')
df = pickle.load(open('dataset/Country_population_co2.pkl', 'rb'))
df['hover_text'] = df["Country"] + ": " + df['co2_percent'].apply(str)
fig = go.Figure(data=go.Choropleth(
    locations = df['CODE'],
    z = np.log(df['co2_percent']),
    text = df['hover_text'],
    hoverinfo="text",
    colorscale="Reds",marker={'line': {'color': 'rgb(180,180,180)','width': 0.5}},
    #colorbar={"thickness": 20, 'tickvals': [ 2, 10],'ticktext': ['100', '100,000']},
    autocolorscale=False,
    reversescale=False,
    showscale=False,
    # colorbar_tickprefix = '$',
    #colorbar_title = 'CO2 Percent<br>Contribution',
))

fig.update_layout(
    title_text='CO2 Emissions 2017(% of world)',
    autosize=True,
    geo=dict(
        showframe=True,
        showcoastlines=False,
        projection_type='equirectangular'
    ),

    height=400, width=650, margin=dict(l=50, r=50, b=50, t=50, pad=4)
)
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [
    "https://unpkg.com/tachyons@4.10.0/css/tachyons.min.css"]

app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=[
    {
        'name': 'PredictCarbon COVID',
        'content': 'This is a group project completed for the course Applied Machine Intelligence at the Technical University of Munich'
    },
    {
        'http-equiv': 'X-UA-Compatible',
        'content': 'IE=edge'
    },
    {
        'name': 'viewport',
        'content': 'width=device-width, initial-scale=1.0'
    }
], title='PredictCarbon COVID', update_title='Calculating')

country_names = np.array(pd.ExcelFile('dataset/features/Modified_Stringency_Data.xlsx').sheet_names)
country_list = [{'label': i, 'value': i} for i in country_names]

# Pie Diagram
# df = pickle.load(open('/dataset/Country_population_co2.pkl', 'rb'))
# df.loc[df['co2_percent'] < 1, 'Country'] = 'Other countries'
# fig = px.pie(df, values='co2_percent', names='Country', title='CO2 percent contribution of different Countries')
# fig.update_layout(height=400, width=700, margin=dict(l=50, r=50, b=100, t=100, pad=4))

#app.scripts.config.serve_locally = True

app.layout = html.Div(
    children=[
        html.Div(className='app-ui',
                 children=[
                     html.Div(className='top-area',
                              children=[
                                  html.H1('Carbon Emissions Prediction by Policy Decisions'),
                              ]
                              ),
                     html.Div(className='input-area',
                              children=[
                                  html.Div(className='left',
                                           children=[
                                              html.Label('Select the countries for analysis:',
                                                         style={'margin-left': 20, 'color': 'white'}),
                                              dcc.Dropdown(className='dropdown', id='country-dropdown',
                                                           options=country_list,
                                                           value=[],
                                                           multi=True
                                                           ),

                                              daq.ToggleSwitch(
                                                  id='input-switch',
                                                  value=False,
                                                  size=50,
                                                  color='#004BA0',
                                                  label={'style':{'color': 'white'} , 'label': 'Click here to toggle between Social Indicators and Stringency Index'},
                                                  labelPosition= 'top'
                                              ),
                                              html.Div(className='card card-1', id='social-indicators-scroll',
                                                       style={"maxHeight": "250px", "overflow": "scroll", 'display': 'block'},
                                                       # block this div by toggle button
                                                       children=[
                                                           html.Label('Social Indicators:',
                                                                      style={'margin-left': 20, 'color': 'black'}),
                                                           html.Label('1. School Closing:',
                                                                      style={'margin-left': 20, 'color': 'black'}),
                                                           dcc.RadioItems(className='checkboxes', id='school-closing',
                                                                          options=[
                                                                              {'label': 'No measures ', 'value': '0'},
                                                                              {'label': 'Recommend closing', 'value': '1'},
                                                                              {'label': 'Require closing (on some levels)',
                                                                               'value': '2'},
                                                                              {'label': 'Require closing (on all levels)',
                                                                               'value': '3'}
                                                                          ],
                                                                          value='0'
                                                                          ),
                                                           html.Label('2. Workplace Closing:',
                                                                      style={'margin-left': 20, 'color': 'black'}),
                                                           dcc.RadioItems(className='checkboxes', id='workplace-closing',
                                                                          options=[
                                                                              {'label': 'No measures ', 'value': '0'},
                                                                              {'label': 'Recommend closing', 'value': '1'},
                                                                              {'label': 'Require closing (for some sectors)',
                                                                               'value': '2'},
                                                                              {'label': 'Require closing (for all sectors)',
                                                                               'value': '3'}
                                                                          ],
                                                                          value='0'
                                                                          ),
                                                           html.Label('3. Cancel public events:',
                                                                      style={'margin-left': 20, 'color': 'black'}),
                                                           dcc.RadioItems(className='checkboxes', id='public-events',
                                                                          options=[
                                                                              {'label': 'No measures ', 'value': '0'},
                                                                              {'label': 'Recommend cancelling', 'value': '1'},
                                                                              {'label': 'Require cancelling', 'value': '2'}
                                                                          ],
                                                                          value='0'
                                                                          ),
                                                           html.Label('4. Restrictions on gatherings:',
                                                                      style={'margin-left': 20, 'color': 'black'}),
                                                           dcc.RadioItems(className='checkboxes', id='gatherings',
                                                                          options=[
                                                                              {'label': 'No restrictions', 'value': '0'},
                                                                              {
                                                                                  'label': 'Restrictions on very large gatherings (the limit is above 1000 people)',
                                                                                  'value': '1'},
                                                                              {
                                                                                  'label': 'Restrictions on gatherings between 101-1000 people',
                                                                                  'value': '2'},
                                                                              {
                                                                                  'label': 'Restrictions on gatherings between 11-100 people',
                                                                                  'value': '3'},
                                                                              {
                                                                                  'label': 'Restrictions on gatherings of 10 people or less',
                                                                                  'value': '4'}
                                                                          ],
                                                                          value='0'
                                                                          ),
                                                           html.Label('5. Close public transport:',
                                                                      style={'margin-left': 20, 'color': 'black'}),
                                                           dcc.RadioItems(className='checkboxes', id='public-transport',
                                                                          options=[
                                                                              {'label': 'No measures ', 'value': '0'},
                                                                              {
                                                                                  'label': 'Recommend closing (or significantly reduce volume/route/means)',
                                                                                  'value': '1'},
                                                                              {
                                                                                  'label': 'Require closing (or prohibit most citizens from using it)',
                                                                                  'value': '2'}
                                                                          ],
                                                                          value='0'
                                                                          ),
                                                           html.Label('6. Stay at home requirements:',
                                                                      style={'margin-left': 20, 'color': 'black'}),
                                                           dcc.RadioItems(className='checkboxes', id='stay-home',
                                                                          options=[
                                                                              {'label': 'No measures ', 'value': '0'},
                                                                              {'label': 'Recommend not leaving house',
                                                                               'value': '1'},
                                                                              {
                                                                                  'label': 'Require not leaving house with exceptions for daily exercise, grocery shopping, ...',
                                                                                  'value': '2'},
                                                                              {
                                                                                  'label': 'Require not leaving house with minimal exceptions',
                                                                                  'value': '3'}
                                                                          ],
                                                                          value='0'
                                                                          ),
                                                           html.Label('7. Restrictions on internal movement:',
                                                                      style={'margin-left': 20, 'color': 'black'}),
                                                           dcc.RadioItems(className='checkboxes', id='internal-movement',
                                                                          options=[
                                                                              {'label': 'No measures ', 'value': '0'},
                                                                              {
                                                                                  'label': 'Recommend not to travel between regions/cities',
                                                                                  'value': '1'},
                                                                              {'label': 'Internal movement restrictions in place',
                                                                               'value': '2'},
                                                                          ],
                                                                          value='0'
                                                                          ),
                                                           html.Label('8. International travel controls:',
                                                                      style={'margin-left': 20, 'color': 'black'}),
                                                           dcc.RadioItems(className='checkboxes', id='international-travel',
                                                                          options=[
                                                                              {'label': 'No measures ', 'value': '0'},
                                                                              {'label': 'Screening arrivals', 'value': '1'},
                                                                              {
                                                                                  'label': 'Quarantine arrivals from some or all regions',
                                                                                  'value': '2'},
                                                                              {'label': 'Ban arrivals from some regions',
                                                                               'value': '3'},
                                                                              {
                                                                                  'label': 'Ban on all regions or total border closure',
                                                                                  'value': '4'}
                                                                          ],
                                                                          value='0'
                                                                          ),

                                                       ]
                                                       ),

                                              # dcc.RadioItems(
                                              #     options=[
                                              #         {'label': 'Italy', 'value': 'ITA'},
                                              #         {'label': 'South Korea', 'value': 'KOR'},
                                              #         {'label': 'Finland', 'value': 'FIN'},
                                              #         {'label': 'Brazil', 'value': 'BRA'}
                                              #     ],
                                              #     value='ITA'
                                              # ),

                                              # html.Label('Text Input'),
                                              # dcc.Input(value='hi', type='text'),
                                              html.Div(className='slider-container slider-container-1', id='stringency-slider-container',
                                                        style={'display': 'block'},
                                                       # block this div by toggle button
                                                       children=[

                                                            html.Label('Stringency Index',
                                                                      style={'margin-left': 20, 'color': 'black'}),
                                                            dcc.Slider(
                                                               id='stringency_index',
                                                               min=0,
                                                               max=100,
                                                               marks={
                                                                   0: {'label': '0', 'style': {'color': '#77b0b1'}},
                                                                   25: {'label': '25'},
                                                                   50: {'label': '50'},
                                                                   75: {'label': '75'},
                                                                   100: {'label': '100', 'style': {'color': '#f50'}}
                                                               },
                                                               value=5,
                                                           ),
                                                           html.Div(className='slider-data', id='stringency_index_show',
                                                                    style={'margin-left': 20, 'color': 'black'}),

                                                       ]
                                              ),
                                           ]
                                  ),
                                  html.Div(className='right',
                                           children=[
                                               html.Div(className='map-container map-container-1',
                                                        children=[
                                                            dcc.Graph(id="my-graph", figure=fig)
                                                            # dcc.Graph(id='co2-percent-graph', figure=fig)
                                                            #html.Img(src='assets/map.png', height=400, width=700)
                                                        ]
                                               ),
                                           ]
                                  )
                                  #html.Img(src='assets/map.png', height=400, width=700)
                              ]#, style={'columnCount': 1}  # for two column view in HTML page
                              ),
                     html.Div(className='mid-area',style={'marginBottom': 50},
                              children=[
                                  html.Button('Submit', id='submit_policy_selection', n_clicks=0,
                                              className='pure-material-button-contained')
                              ]
                              ),
                     html.Div(className='output-area',
                              id='outputs',
                              children=[
                                  html.Div(className='left-graph',
                                           children=[
                                                dcc.Graph(id='absolute-graph')],
                                           id='left_co2'),
                                  html.Div(className='right-graph',
                                           children=[
                                                dcc.Graph(id='reduction-graph')],
                                           id='right_co2'),
                                  #html.Div(className='output_figure', id='div_output_graph'),
                                  html.Div(id='graph_dash-loading-callback'),
                                  dcc.Store(id='trigger')
                              ],
                              style={'display': 'block'}),
                     # dcc.Input(id="loading-input-1", value='Input triggers local spinner'),
                     # dcc.Loading(
                     #        id="loading-1",
                     #        type="default",
                     #        fullscreen=True,
                     #        children=html.Div(id="loading-output-1")
                     #        )
                 ]
                 )
    ]
)
# , style={'columnCount': 1}
# html.Label('Dropdown'),
# dcc.Dropdown(
#     options=[
#         {'label': 'Italy', 'value': 'ITA'},
#         {'label': 'South Korea', 'value': 'KOR'},
#         {'label': 'Finland', 'value': 'FIN'},
#         {'label': 'Brazil', 'value': 'BRA'}
#     ],
#     value='ITA'
# ),


register_callbacks(app, dcc)

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=True)
