#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 14:18:48 2022

@author: yousufaziz
"""


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table as dt

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

### pandas dataframe to html table
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app = dash.Dash(__name__, external_stylesheets=stylesheet)
server = app.server

df = pd.read_csv('/Users/yousufaziz/Desktop/Classes/MA 705 - Data Science/Dashboard/scotch_review2020.csv')


checklist_options = [{'label' : pricerange, 'value' : pricerange} for pricerange in set(df.range)]


rating_options = sorted([{'label' : review, 'value' : review} for review in set(df.review)], key = lambda x: x['label'])

category_options = [{'label' : category, 'value' : category} for category in set(df.category)]




dff_counts2 = df.groupby(["range", "review"]).size().reset_index(name="Count")
fig = px.bar(dff_counts2,x="range",y="Count",color="review",
             title="Price wise bar chart of different Categories segregated by Ratings")

app.layout = html.Div([
    html.H1('Scotch Whisky Recommendation Dashboard',
            style={'textAlign' : 'center', 'background-color' :'lavender'}),
    html.H6('by Mohammed Yousuf Aziz', style={'textAlign' : 'right'}),
    
    html.H6("This dashboard summarizes information of over 2000 whiskys obtained from www.whiskyadvocate.com. It allows an user to find whiskys based on the following three search criteria :",style={'textAlign' : 'left'}),
    html.H6("Price Range : Multiple whiskys with prices varying from below $100 to over $10,000.",style={'textAlign' : 'left'}),
    html.H6("Rating : Range of ratings from 83 to 97. ",style={'textAlign' : 'left'}),
    html.H6("Category : Three types of different whiskys namely, Blended scotch, Single malt scotch and Blended malt scotch.",style={'textAlign' : 'left'}),
    html.H1("____________________________________________________",style={'textAlign' : 'center'}),
    
    
    dcc.Graph(id = 'my-hist',figure = fig, style={'width' : '50%', 'float' : 'right'}),
    html.H5('To use this dashboard, please select the following preferences:'),
    html.Div([html.H5("Pick Price Range:"),
              dcc.Dropdown(id = 'my-price',options=checklist_options,
                            value='0 to 100 Dollars', multi = False)
              ],
             style={'width' : '50%', 'float' : 'left'}
             ),
    html.Div([html.H5("Pick Prefered Rating:"),
              dcc.Dropdown(id = 'my-rating',options=rating_options,
                            value='92', multi = False)
              ],
             style={'width' : '50%', 'float' : 'left'}
             ),
    html.Div([html.H5("Please Prefered Category:"),
              dcc.Dropdown(id = 'my-category',options=category_options,
                            value='Single Malt Scotch', multi = False)
              ],
             style={'width' : '50%', 'float' : 'left'}
             ),
    html.H1('___________________________',
            style={'textAlign' : 'center', 'float' : 'center'}),
    html.H5('The recommendations according to your preferences are:'),
    dt.DataTable(df.to_dict('records'),id = 'my-table',
                 page_size = 8,
                 style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        'lineHeight': '15px',
        'backgroundColor': 'lavender',
        'color': 'black'
    }),
    html.H6("If blank please select different preferences as there are no whiskys in the chosen preferences."),
    html.H1("____________________________________________________",style={'textAlign' : 'center'}),
    html.H5('References and Dataset Source:'),
    html.Div([
    html.A("Whisky Advocate",
           href = 'https://www.whiskyadvocate.com'),
    html.Br(),
    html.A("Dataset : Scotch Whisky Review - 2020",
           href = 'https://www.kaggle.com/datasets/koki25ando/22000-scotch-whisky-reviews'),
    html.Br(),
    html.A("Plotly - Bar",
           href = 'https://plotly.com/python/Bar/'),
    html.Br(),
    html.A("Plotly - Data Table",
           href = "https://dash.plotly.com/datatable"),
    html.H6("May 2022, Mohammed Yousuf Aziz.",style={'textAlign' : 'left'})
    
   ])
    
    
    ])

@app.callback(
    Output('my-table', 'data'),
    Input('my-price', 'value'),
    Input('my-rating', 'value'),
    Input('my-category', 'value')

)


def display_table(select_price, select_rating, select_category):
    table = df[(df.range == select_price) & (df.review == int(select_rating)) & (df.category == select_category)]
    return table.to_dict('records')



@app.callback(
    Output('my-hist', 'figure'),
    Input('my-price','value'),
    Input('my-category', 'value')
)

 

def update_graph(selected_range, selected_category):
    
       dff = df[(df.category == selected_category)]
       dff_counts = dff.groupby(["range", "review"]).size().reset_index(name="Count")
       fig = px.bar(dff_counts,x="range",y="Count",color="review",
                    title="Price wise bar chart of different Categories segregated by Ratings")
       return fig

if __name__ == '__main__':
    app.run_server(debug=True)
    

  