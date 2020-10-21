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
    # connect to postgresql
    engine = sqlalchemy.create_engine('postgresql://postgres:paedf5l5@localhost/postgres')
    con = engine.connect()
    df = pd.read_sql_table(table_name, engine)
    # close connection
    con.close()
    return df 

def averange_price(df):
    return pd.pivot_table(df, index='rooms_cnt', columns='date', values='price_one_metre', aggfunc='mean')

def new_addition_cnt(df, today, yesterday):
    addition_today = df.query('date == @today')
    addition_yesterday = df.query('date == @yesterday')

    return len(addition_today) - len(addition_yesterday)


def main():

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    table_name = 'kotelniki'

    df = get_data_in_data_base(table_name)

    print(df.info())
    
    df_1 = new_addition_cnt(df, today, yesterday)

    print('new addition is {}'.format(df_1))

    rezult = averange_price(df)

    print(rezult)

if __name__ == '__main__':
    main()