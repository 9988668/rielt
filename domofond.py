#!/usr/bin/python
# -*- coding: utf-8 -*-

# импортируем библиотеки
import pandas as pd 
from bs4 import BeautifulSoup
import requests

SOURCE = []
URL = []
PRICE = []
PRICE_FOR_METRE = []
ADRESS = []

def get_html(url):
    r = requests.get(url)
    return r.text

def last_page(html):
    soup = BeautifulSoup(html, 'lxml')
    last_page_number = soup.find('ul', class_='pagination__mainPages___2v12k').find_all('li')[-1].find('a').text.strip()
    return int(last_page_number)

def change_price_for_metre(price):
    return ''.join(price.split(' ')[:-3])

def change_total_price(price):
    return ''.join(price.split(' ')[:-1])

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    notification_list = soup.find('div', class_='search-results__itemCardList___RdWje').find_all('a')

    for notification in notification_list:

        try:
            personal_url = 'https://www.domofond.ru' + notification.get('href')
        except:
            personal_url = 'empty'

        try:
            total_price = notification.find('div', class_='long-item-card__information___YXOtb').find('div', class_='long-item-card__informationHeader___v1HWy').find('span', class_='long-item-card__price___3A6JF').text.strip()
            total_price = int(change_total_price(total_price))
        except:
            total_price = 0

        try:
            price_for_metre = notification.find('div', class_='long-item-card__information___YXOtb').find('div', class_='long-item-card__informationHeader___v1HWy').find('div', class_='additional-price-info__additionalPriceInfo___lBqNv').text.strip()
            price_for_metre  = int(change_price_for_metre(price_for_metre))
        except:
            price_for_metre = 0

        try:
            adress = notification.find('span', class_='long-item-card__address___PVI5p').text.strip()
        except:
            adress = 'empty'

        SOURCE.append('Domofond.ru')
        URL.append(personal_url)
        PRICE.append(total_price)
        PRICE_FOR_METRE.append(price_for_metre)
        ADRESS.append(adress)

    
def main():
    url = 'https://www.domofond.ru/prodazha-dvuhkomnatnyh-kvartir-kotelniki-c3605'
    last_page_number = last_page(get_html(url))

    for page in range(last_page_number):
        gen_url = url + '?Page={}'.format(page + 1)

        get_page_data(get_html(gen_url))

    df = pd.DataFrame(list(zip(URL, PRICE, PRICE_FOR_METRE, ADRESS, SOURCE)), 
                          columns = ['URL', 'цена квартиры', 'цена за кв.метр', 'адрес квартриы', 'источник'])

    df.to_csv('kotelniki_2_room.csv')

    print('ok, file is save')    
    
if __name__ == '__main__':
    main()