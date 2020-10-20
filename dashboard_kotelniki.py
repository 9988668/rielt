# -*- coding: utf-8 -*-

# импортируем библиотеки
import pandas as pd 
from bs4 import BeautifulSoup
import requests
import datetime
import psycopg2
import numpy as np 
import sqlalchemy


def get_data_in_data_base(table_name):
    # conect to postgresql
    engine = sqlalchemy.create_engine('postgresql://postgres:paedf5l5@localhost/postgres')
    con = engine.connect()
    df = pd.read_sql_table(table_name, engine)

    # close connection
    con.close()

    return df 


def main():

    today = datetime.date.today()
    table_name = 'kotelniki'

    df = get_data_in_data_base(table_name)

    print(df.head())

if __name__ == '__main__':
    main()