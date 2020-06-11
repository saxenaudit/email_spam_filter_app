from app import app
from app import server
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from datetime import datetime
import dash_table
import pandas as pd
import folium
from decouple import config
import plotly.express as px
import dash_auth

colors = {
    'background': '#111111',
    'background2': '#FF0',
    'text': 'yellow'
    }
tabs_styles = {
                       'height': '40px'
                      }
tab_style = {
                          'borderBottom': '1px solid #d6d6d6',
                          'padding': '2px',
                          'fontWeight': 'bold'
                      }

tab_selected_style = {
                          'borderTop': '1px solid #d6d6d6',
                          'borderBottom': '1px solid #d6d6d6',
                          'backgroundColor': 'black',
                          'color': 'grey',
                          'padding': '10px'
                      }
product_list = ['Bookcases', 'Chairs', 'Labels', 'Tables', 'Storage',
       'Furnishings', 'Art', 'Phones', 'Binders', 'Appliances', 'Paper',
       'Accessories', 'Envelopes', 'Fasteners', 'Supplies', 'Machines',
       'Copiers']
VALID_USERNAME_PASSWORD_PAIRS = [
    ['vanijya', 'technology']
]
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
#------------------------------------------------------------------------------------------
footer = html.Div(className='footer',
                  children=[html.Div([
                               html.Div([html.H2("Created by ",
                                        style={'display': 'inline-block',
                                               'margin': "0px",
                                               "color": 'navy',
                                               "line-height": "0.1"
                                               }
                                        ),
                                html.A(html.Img(src="Capture.JPG", alt="Vanijya Technology",
                                                style={
                                                    'height': "55%",
                                                    "width": "30.75%",
                                                    'display': 'inline-block',
                                                    "border-radius": "50%",
                                                    "margin": "10px"
                                                }
                                                ),
                                       href='https://vanijyasolutions.netlify.com/',
                                       style={'vertical-align': 'middle'}
                                       )
                                      ]),                          
                                      ]),
                    ],
                  style={'textAlign': "center"})
#------------------------------------------------------------------------------------------
app.layout = html.Div([            
                html.Div(html.H1('Vanijya Technology',
                               style={
                                      'textAlign': 'center',
                                      "background": "#ffffff"}),style={'color': 'navy', 'fontSize': 14}),
               html.Div(['Select Date here',
               dcc.DatePickerRange(
                   id='date-input',
                   stay_open_on_select=False,
                   min_date_allowed=datetime(2014, 1, 14),
                   max_date_allowed=datetime(2018,1,5),#.now(),
                   initial_visible_month=datetime(2018,1,5),
                   start_date=datetime(2014, 1, 14),
                   end_date=datetime(2018,1,5),
                   number_of_months_shown=1,
                   month_format='MMMM,YYYY',
                   display_format='YYYY-MM-DD',
                   style={
                          'color': '#ffffff',
                          'font-size': '18px',
                          'margin': 0,
                          'padding': '8px',
                          'background': '#ffffff',
                   }
               ),
               '      Select Product here',
               dcc.Dropdown(id='dropdown',
                            options=[{'label': i, 'value': i} for i in product_list],
                            value='Bookcases',
                            optionHeight=10,
                            style={
                                'height': '50px',
                                'font-weight': 100,
                                'font-size': '16px',
                                'line-height': '10px',
                                'color': 'gray',
                                'margin': 0,
                                'padding': '8px',
                                'background': '#ffffff',
                                'position': 'middle',
                                'display': 'inline-block',
                                'width': '150px',
                                'vertical-align': 'middle',
                                }
                            ),
                html.Div(id='date-output'),
                html.Div(id='intermediate-value', style={'display': 'none'}),
                               ], className="row ",
                    style={'marginTop': 0, 'marginBottom': 0, 'font-size': 30, 'color': 'navy',
                           'display': 'inline-block'}),

               dcc.Tabs(id="all-tabs-inline", value='tab-1', children=[
                                  dcc.Tab(label='Consumer', value='tab-1', style=tab_style, selected_style=tab_selected_style),
                                  dcc.Tab(label='Home Office', value='tab-2', style=tab_style, selected_style=tab_selected_style),
                                  dcc.Tab(label='Corporate', value='tab-3', style=tab_style, selected_style=tab_selected_style),
                                  dcc.Tab(label='All Combined', value='tab-4', style=tab_style, selected_style=tab_selected_style),
                                                           ], style=tabs_styles,
                                  colors={
                                  "border": "black",
                                  "primary": "red",
                                  "background": "blue"
                                  }),
               html.Div(id='graph-output'),
               #html.Div(footer),
               html.Div(children=[dcc.Markdown( 
                                    " © 2020 [Vanijya Technology](https://vanijyasolutions.netlify.com/)  All Rights Reserved.")], style={
                                    'textAlign': 'center',
                                    "background": "grey"}),
                         ],
              style={"background": "#ffffff"}
                            )
#------------------------------------------------------------------------------------------
from tt_data import get_data
@app.callback(Output('intermediate-value', 'children'),
              [Input('dropdown', 'value')])
def get_x_data(product): 
    df = get_data(product)
    return df.to_json(date_format='iso', orient='split')

from MapIndia import MapIndia
@app.callback(Output('graph-output', 'children'),
              [Input('all-tabs-inline', 'value'),
              Input('intermediate-value', 'children'),
              Input('date-input', 'start_date'),
              Input('date-input', 'end_date')
              ])
def render_content(tab,data,start_date,end_date):
    df = pd.read_json(data, orient='split')
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[(df.Date >= start_date) & (df.Date <= end_date)]
    if tab == 'tab-1':
        df = df[df['Segment']=='Consumer']
        bar1= dcc.Graph(
                           id='graph-1',
                           figure={
                               'data': [
                                   {'x': df['Date'], 'y': df['Sales'], 'type': 'bar', 'name': 'Sales'},
                                       ],
                               'layout': {
                                   'title': 'Sales V/s Date',

                           'xaxis': {
                                  'title': 'Date',
                                  'showspikes': True,
                                  'spikedash': 'dot',
                                  'spikemode': 'across',
                                  'spikesnap': 'cursor',
                                  },
                          'yaxis': {
                                  'title': 'Sales',
                                  'showspikes': True,
                                  'spikedash': 'dot',
                                  'spikemode': 'across',
                                  'spikesnap': 'cursor'
                                  },
                                     }
                                 } 
                            ),
        bar2 = dcc.Graph(
                           id='graph-1',
                           figure={
                               'data': [
                                   {'x': df['City'], 'y': df['Profit'], 'type': 'bar', 'name': 'Profit'},
                                       ],
                               'layout': {
                                   'title': 'Profit V/s City',

                           'xaxis': {
                                  'title': 'Date',
                                  'showspikes': True,
                                  'spikedash': 'dot',
                                  'spikemode': 'across',
                                  'spikesnap': 'cursor',
                                  },
                          'yaxis': {
                                  'title': 'Sales',
                                  'showspikes': True,
                                  'spikedash': 'dot',
                                  'spikemode': 'across',
                                  'spikesnap': 'cursor'
                                  },
                                     }
                                 } 
                            ),
        d_fig = px.sunburst(df, path=['State', 'City'],
                            values='Sales', color='State',
                            hover_data=["Sales", 'City']
                            )
        d_fig.update_layout(margin=dict(t=40, l=0, r=0, b=0),
                            title='Citywise Sales Distribution',
                            height=700,
                            # width=410,
                            paper_bgcolor='#ffffff',
                            font={'size': 16}
                            )
        d_fig.data[0].update(
            hovertemplate="Sales: ₹%{customdata[0]},<br>City: %{customdata[1]}"
        )
        map_ = MapIndia(df)
        return html.Div([html.Div(bar1, className='cum-cases', id='cum-cases', 
                              style={'display': 'inline-block'}),
                          html.Div(bar2, className='cum-cases-1', id='cum-cases-1', 
                              style={'display': 'inline-block'}),
                          html.Div(children=[dcc.Graph(id='dist-chart', figure=d_fig)],
                            style={'display': 'inline-block', 'textAlign': 'center'}),
                          html.Br(),
                          html.Br(),
                          html.Br(),
                          html.Div(children=[dcc.Graph(figure=map_)], className='India-map',
                              style={'display': 'inline-block', 'textAlign': 'center'})]
                               , className='tab1-graph', id="tab1-graph", style={'textAlign': 'center'}),

    elif tab == 'tab-2':
        df = df[df['Segment']=='Home Office']
        bar1= dcc.Graph(
                           id='graph-1',
                           figure={
                               'data': [
                                   {'x': df['Date'], 'y': df['Sales'], 'type': 'bar', 'name': 'Sales'},
                                       ],
                               'layout': {
                                   'title': 'Sales V/s Date',

                           'xaxis': {
                                  'title': 'Date',
                                  'showspikes': True,
                                  'spikedash': 'dot',
                                  'spikemode': 'across',
                                  'spikesnap': 'cursor',
                                  },
                          'yaxis': {
                                  'title': 'Sales',
                                  'showspikes': True,
                                  'spikedash': 'dot',
                                  'spikemode': 'across',
                                  'spikesnap': 'cursor'
                                  },
                                     }
                                 } 
                            ),
        bar2 = dcc.Graph(
                           id='graph-1',
                           figure={
                               'data': [
                                   {'x': df['City'], 'y': df['Profit'], 'type': 'bar', 'name': 'Profit'},
                                       ],
                               'layout': {
                                   'title': 'Profit V/s City',

                           'xaxis': {
                                  'title': 'Date',
                                  'showspikes': True,
                                  'spikedash': 'dot',
                                  'spikemode': 'across',
                                  'spikesnap': 'cursor',
                                  },
                          'yaxis': {
                                  'title': 'Sales',
                                  'showspikes': True,
                                  'spikedash': 'dot',
                                  'spikemode': 'across',
                                  'spikesnap': 'cursor'
                                  },
                                     }
                                 } 
                            ),
        d_fig = px.sunburst(df, path=['State', 'City'],
                            values='Sales', color='State',
                            hover_data=["Sales", 'City']
                            )
        d_fig.update_layout(margin=dict(t=40, l=0, r=0, b=0),
                            title='Citywise Sales Distribution',
                            height=700,
                            # width=410,
                            paper_bgcolor='#ffffff',
                            font={'size': 16}
                            )
        d_fig.data[0].update(
            hovertemplate="Sales: ₹%{customdata[0]},<br>City: %{customdata[1]}"
        )
        map_ = MapIndia(df)
        return html.Div([html.Div(bar1, className='cum-cases', id='cum-cases', 
                              style={'display': 'inline-block'}),
                          html.Div(bar2, className='cum-cases-1', id='cum-cases-1', 
                              style={'display': 'inline-block'}),
                          html.Div(children=[dcc.Graph(id='dist-chart', figure=d_fig)],
                            style={'display': 'inline-block', 'textAlign': 'center'}),
                          html.Br(),
                          html.Br(),
                          html.Br(),
                          html.Div(children=[dcc.Graph(figure=map_)], className='India-map',
                              style={'display': 'inline-block', 'textAlign': 'center'})]
                               , className='tab1-graph', id="tab1-graph", style={'textAlign': 'center'}),

    elif tab == 'tab-3':
        df = df[df['Segment']=='Corporate']
        bar1= dcc.Graph(
                           id='graph-1',
                           figure={
                               'data': [
                                   {'x': df['Date'], 'y': df['Sales'], 'type': 'bar', 'name': 'Sales'},
                                       ],
                               'layout': {
                                   'title': 'Sales V/s Date',

                           'xaxis': {
                                  'title': 'Date',
                                  'showspikes': True,
                                  'spikedash': 'dot',
                                  'spikemode': 'across',
                                  'spikesnap': 'cursor',
                                  },
                          'yaxis': {
                                  'title': 'Sales',
                                  'showspikes': True,
                                  'spikedash': 'dot',
                                  'spikemode': 'across',
                                  'spikesnap': 'cursor'
                                  },
                                     }
                                 } 
                            ),
        bar2 = dcc.Graph(
                           id='graph-1',
                           figure={
                               'data': [
                                   {'x': df['City'], 'y': df['Profit'], 'type': 'bar', 'name': 'Profit'},
                                       ],
                               'layout': {
                                   'title': 'Profit V/s City',

                           'xaxis': {
                                  'title': 'Date',
                                  'showspikes': True,
                                  'spikedash': 'dot',
                                  'spikemode': 'across',
                                  'spikesnap': 'cursor',
                                  },
                          'yaxis': {
                                  'title': 'Sales',
                                  'showspikes': True,
                                  'spikedash': 'dot',
                                  'spikemode': 'across',
                                  'spikesnap': 'cursor'
                                  },
                                     }
                                 } 
                            ),
        d_fig = px.sunburst(df, path=['State', 'City'],
                            values='Sales', color='State',
                            hover_data=["Sales", 'City']
                            )
        d_fig.update_layout(margin=dict(t=40, l=0, r=0, b=0),
                            title='Citywise Sales Distribution',
                            height=700,
                            # width=410,
                            paper_bgcolor='#ffffff',
                            font={'size': 16}
                            )
        d_fig.data[0].update(
            hovertemplate="Sales: ₹%{customdata[0]},<br>City: %{customdata[1]}"
        )
        map_ = MapIndia(df)
        return html.Div([html.Div(bar1, className='cum-cases', id='cum-cases', 
                              style={'display': 'inline-block'}),
                          html.Div(bar2, className='cum-cases-1', id='cum-cases-1', 
                              style={'display': 'inline-block'}),
                          html.Div(children=[dcc.Graph(id='dist-chart', figure=d_fig)],
                            style={'display': 'inline-block', 'textAlign': 'center'}),
                          html.Br(),
                          html.Br(),
                          html.Br(),
                          html.Div(children=[dcc.Graph(figure=map_)], className='India-map',
                              style={'display': 'inline-block', 'textAlign': 'center'})]
                               , className='tab1-graph', id="tab1-graph", style={'textAlign': 'center'}),

    elif tab == 'tab-4':
        bar1= dcc.Graph(
                           id='graph-1',
                           figure={
                               'data': [
                                   {'x': df['Date'], 'y': df['Sales'], 'type': 'bar', 'name': 'Sales'},
                                       ],
                               'layout': {
                                   'title': 'Sales V/s Date',

                           'xaxis': {
                                  'title': 'Date',
                                  'showspikes': True,
                                  'spikedash': 'dot',
                                  'spikemode': 'across',
                                  'spikesnap': 'cursor',
                                  },
                          'yaxis': {
                                  'title': 'Sales',
                                  'showspikes': True,
                                  'spikedash': 'dot',
                                  'spikemode': 'across',
                                  'spikesnap': 'cursor'
                                  },
                                     }
                                 } 
                            ),
        bar2 = dcc.Graph(
                           id='graph-1',
                           figure={
                               'data': [
                                   {'x': df['City'], 'y': df['Profit'], 'type': 'bar', 'name': 'Profit'},
                                       ],
                               'layout': {
                                   'title': 'Profit V/s City',

                           'xaxis': {
                                  'title': 'Date',
                                  'showspikes': True,
                                  'spikedash': 'dot',
                                  'spikemode': 'across',
                                  'spikesnap': 'cursor',
                                  },
                          'yaxis': {
                                  'title': 'Sales',
                                  'showspikes': True,
                                  'spikedash': 'dot',
                                  'spikemode': 'across',
                                  'spikesnap': 'cursor'
                                  },
                                     }
                                 } 
                            ),
        d_fig = px.sunburst(df, path=['State', 'City'],
                            values='Sales', color='State',
                            hover_data=["Sales", 'City']
                            )
        d_fig.update_layout(margin=dict(t=40, l=0, r=0, b=0),
                            title='Citywise Sales Distribution',
                            height=700,
                            # width=410,
                            paper_bgcolor='#ffffff',
                            font={'size': 16}
                            )
        d_fig.data[0].update(
            hovertemplate="Sales: ₹%{customdata[0]},<br>City: %{customdata[1]}"
        )
        map_ = MapIndia(df)
        return html.Div([html.Div(bar1, className='cum-cases', id='cum-cases', 
                              style={'display': 'inline-block'}),
                          html.Div(bar2, className='cum-cases-1', id='cum-cases-1', 
                              style={'display': 'inline-block'}),
                          html.Div(children=[dcc.Graph(id='dist-chart', figure=d_fig)],
                            style={'display': 'inline-block', 'textAlign': 'center'}),
                          html.Br(),
                          html.Br(),
                          html.Br(),
                          html.Div(children=[dcc.Graph(figure=map_)], className='India-map',
                              style={'display': 'inline-block', 'textAlign': 'center'})]
                               , className='tab1-graph', id="tab1-graph", style={'textAlign': 'center'})

if __name__ == '__main__':
    app.run_server(debug=True)