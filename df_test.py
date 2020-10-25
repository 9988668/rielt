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


def main():
    # получаем данные и трансформируем их

    # connect to postgresql
    table_name = 'kotelniki'  # имя таблицы из которой будут браться данные
    engine = sqlalchemy.create_engine('postgresql://postgres:paedf5l5@localhost/postgres')
    con = engine.connect()
    all_flat = pd.read_sql_table(table_name, engine)
    # close connection
    con.close()

    print(all_flat['url'].value_counts())




if __name__ == '__main__':
    main()