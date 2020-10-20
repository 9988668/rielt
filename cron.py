#!/usr/bin/python3
# -*- coding: utf-8 -*-

# импортируем библиотеки
import pandas as pd 
from bs4 import BeautifulSoup
import requests
import datetime
import psycopg2
import numpy as np 
import sqlalchemy
import os 
import time


def main():
	# create random DataFrame

	data = np.random.choice(np.arange(1000), size=100, replace=False)

	first_df = pd.DataFrame(data, columns = ['Name_Id'])
	first_df['Product_Id'] = np.random.randint(0, 1000, 100)
	first_df['Sales'] = np.random.randint(0, 1000, 100)

	first_df.to_csv('file_cron.csv')
	time.sleep(5)

	os.remove('/home/ivan/python/rielt/rielt/file_cron.csv')


if __name__ == '__main__':
	main()
