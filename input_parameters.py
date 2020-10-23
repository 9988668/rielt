#!/usr/bin/python
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

from datetime import datetime

import pandas as pd

import datetime
import psycopg2
import numpy as np 
import sqlalchemy

# получаем данные и трансформируем их

# connect to postgresql
table_name = 'kotelniki'
engine = sqlalchemy.create_engine('postgresql://postgres:paedf5l5@localhost/postgres')
con = engine.connect()
all_flat = pd.read_sql_table(table_name, engine)
# close connection
con.close()

all_flat_group = (all_flat.groupby('rooms_cnt')
                          .agg({'floor':'mean'})
                          .reset_index()
                          .sort_values(by = 'floor', ascending = False))

# задаём лейаут
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[

    # формируем заголовок тегом HTML
    html.H1(children = 'Квартиры в г. Котельники'),
    html.Br(),

    html.Label('статистика предложений квартир в г. Котельники'),
    html.Br(),

    html.Div([
        html.Div([
            html.Br(),
            html.Label('количество комнат'),
            dcc.Checklist(
                        options=[
                                 {'label':'студия', 'value':0},
                                 {'label':'1-комн.', 'value':1},
                                 {'label':'2-комн.', 'value':2},
                                 {'label':'3-комн.', 'value':3}
                                 ],
                        value = [1, 2],
                        labelStyle = {'display':'inline-block'}
                        )
                ], className = 'four columns'),

        html.Div([
            html.Br(),
            html.Label('площадь квартиры (кв.м.)'),
            dcc.RangeSlider(
                        id = 'space',
                        min = all_flat['space'].min(),
                        max = all_flat['space'].max(),
                        step = 0.1,
                        value = [35, 80],
                        allowCross = False,
                        tooltip = {'always_visible':True, 'placement':'bottomLeft'},
                        updatemode = 'mouseup'
                           )
                ], className = 'four columns'),

        html.Div([
            html.Br(),
            html.Label('веременной интервал'),
            dcc.DatePickerRange(
                        id = 'dt_selector',
                        start_date = all_flat['date'].min(),
                        end_date = all_flat['date'].max()
                               )
            ], className = 'four columns'),

            ])


    # # выбор временного периода
    # html.Label('Временной период:'),
    # dcc.DatePickerRange(
    #   start_date = all_flat['date'].min(),
    #   end_date = all_flat['date'].max(),
    #   id = 'dt_selector',
    #   ),

    # # график изменения цены
    # dcc.Graph(
    #   figure = {
    #            'data': [go.Bar(x = all_flat_group['rooms_cnt'],
    #                            y = all_flat_group['floor'],
    #                            name = 'price_one_metre')],
    #            'layout' : go.Layout(xaxis = {'title': 'количество комнат'},
    #                                 yaxis = {'title': 'средняя цена кв.метра'})
    #   },
    #   id = 'price_one_metre_by_rooms_cnt'
    #   ),

])

if __name__ == '__main__':
    app.run_server(debug=True)