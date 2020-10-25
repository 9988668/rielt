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

import math

# получаем данные и трансформируем их

# connect to postgresql
table_name = 'kotelniki'  # имя таблицы из которой будут браться данные
engine = sqlalchemy.create_engine('postgresql://postgres:paedf5l5@localhost/postgres')
con = engine.connect()
all_flat = pd.read_sql_table(table_name, engine)
# close connection
con.close()

style_text = {
            'textAlign':'left',
            'color':'grey',
            'font-size':'150%'
            }

style_table_header = {
            'textAlign':'center',
            'color':'grey',
            'font-size':'100%',
            'font-weight':'bold',
            'fill_color':'paleturquoise'
}

all_flat_share_rooms = (all_flat.groupby('rooms_cnt')
                                . agg({'url':'nunique'})
                                . reset_index())

all_flat_group = (all_flat.groupby('rooms_cnt')
                          .agg({'floor':'mean'})
                          .reset_index()
                          .sort_values(by = 'floor', ascending = False))

all_flat_left_table = (all_flat.groupby('rooms_cnt')
                               .agg({'url':'nunique', 'price_one_metre':['min', 'mean', 'max']})
                               .reset_index())

all_flat_left_table['price_one_metre'] = all_flat_left_table['price_one_metre'].astype('int')

# задаём лейаут
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[

    # формируем заголовок тегом HTML
    html.H1(children = 'Квартиры в г. Котельники',
            style = {
            'textAlign':'center',
            'color':'grey'
            }
            ),
    html.Br(),  # устанавливаем один пробел

    html.Label(
               'статистика предложений квартир в г. Котельники',
               style = {
                        'textAlign':'center',
                        'color':'grey',
                        'font-size':'220%'
                        }
              ),
    html.Br(),
    
    # блок селекторов для управления изменяемыми параметрами
    # выбор количества комнат
    # выбор площад квартиры
    # выбор временног интервала
    html.Div([
        html.Div([
            html.Br(),
            html.Label('количество комнат',
                        style = style_text
                       ),
            dcc.Checklist(
                        options=[
                                 {'label':'студия', 'value':0},
                                 {'label':'1-комн.', 'value':1},
                                 {'label':'2-комн.', 'value':2},
                                 {'label':'3-комн.', 'value':3}
                                 ],
                        value = [1, 2],
                        labelStyle = {'display':'inline-block'},
                        id = 'rooms_cnt_selector'
                        )
                ], className = 'four columns'),

        html.Div([
            html.Br(),
            html.Label('площадь квартиры (кв.м.)',
                        style = style_text
                       ),
            dcc.RangeSlider(
                        id = 'space_selector',
                        min = all_flat['space'].min(),
                        max = all_flat['space'].max(),
                        step = 0.1,
                        value = [35, 80],
                        allowCross = False,
                        tooltip = {'always_visible':True, 'placement':'bottomLeft'},
                        updatemode = 'mouseup',
                           )
                ], className = 'four columns'),

        html.Div([
            html.Br(),
            html.Label('веременной интервал',
                        style = style_text
                       ),
            dcc.DatePickerRange(
                        id = 'dt_range_selector',
                        start_date = all_flat['date'].min(),
                        end_date = all_flat['date'].max()
                               )
            ], className = 'four columns'),

            ]),

    html.Div([
        html.Div([
            html.Br(),
            html.Label('выберите дату',
                style = style_text
                        ),
            dcc.DatePickerSingle(
                        id = 'dt_single_selector',
                        min_date_allowed = all_flat['date'].min(),
                        max_date_allowed = all_flat['date'].max(),
                        date = datetime.date.today()
                                ),

            dcc.Graph(
                    # figure = {
                    #         'data' : [go.Pie(labels = all_flat_share_rooms['rooms_cnt'], 
                    #                          values = all_flat_share_rooms['url'],
                    #                          name = 'pie'
                    #                          )],
                    #         'layout':go.Layout()

                    #         },
                    id = 'pie_chart'
                    ),

            dcc.Graph(
                    # figure = {
                    #         'data' : [go.Table(
                    #                             header = dict(values=['квартира', 'количество', 'мин. цена кв.м.', 'средняя цена кв.м.', 'макс. цена кв.м.'],
                    #                                           fill_color = 'paleturquoise'
                    #                                         ),
                    #                             cells = dict(values=[all_flat_left_table.rooms_cnt, 
                    #                                                  all_flat_left_table.url, 
                    #                                                  all_flat_left_table.price_one_metre['min'],
                    #                                                  all_flat_left_table.price_one_metre['mean'],
                    #                                                  all_flat_left_table.price_one_metre['max']],
                    #                                         fill_color='lavender'
                    #                                         )
                    #                            ) 
                    #                  ]
                    #         },
                    id = 'table'
                    )

                ], className = 'four columns'),

        html.Div([
            html.Br(),
            html.Label('предложения квартир в г. Котельники',
                        style = style_text
                      )
                ], className = 'eight columns')
            ])

])

#описываем логику дашборда
@app.callback(
    [Output('pie_chart', 'figure'),
     Output('table', 'figure'),
    ],
    [Input('dt_range_selector', 'start_date'),
     Input('dt_range_selector', 'end_date'),
     Input('space_selector', 'value'),
     Input('dt_single_selector', 'date'),
     Input('rooms_cnt_selector', 'value'),
    ])

def update_figure(start_date, end_date, value, single_date, rooms):

    min_space = value[0]
    max_space = value[1]

    update_all_flats = all_flat.query('date == @single_date')
    update_all_flats = update_all_flats.query('@min_space <= space and space <= @max_space')
    update_all_flats = update_all_flats.query('rooms_cnt in @rooms')

    left_table_data = (update_all_flats.groupby('rooms_cnt')
                                      .agg({'url':'nunique', 'price_one_metre':['min', 'mean', 'max']})
                                      .reset_index())
    left_table_data['price_one_metre'] = left_table_data['price_one_metre'].astype('int')

    pie_chart_data = (update_all_flats.groupby('rooms_cnt')
                                      . agg({'url':'nunique'})
                                      . reset_index())

    pie_chart = [go.Pie(labels = pie_chart_data['rooms_cnt'], 
                         values = pie_chart_data['url'],
                         name = 'pie')]

    left_table = [go.Table(
                    header = dict(values=['квартира (количество комнат)', 'количество квартир в продаже', 'мин. цена кв.м.', 'средняя цена кв.м.', 'макс. цена кв.м.'],
                                  fill_color = 'paleturquoise'
                                ),
                    cells = dict(values=[left_table_data.rooms_cnt, 
                                         left_table_data.url, 
                                         left_table_data.price_one_metre['min'],
                                         left_table_data.price_one_metre['mean'],
                                         left_table_data.price_one_metre['max']],
                                fill_color='lavender'
                                )
                            ) 
                 ]

    return (
            {
                'data':pie_chart,
                'layout':go.Layout()
            },
            {
                'data':left_table,
                'layout':go.Layout()
            }
        )


if __name__ == '__main__':
    print(all_flat_left_table)
    app.run_server(debug=True)

