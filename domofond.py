#!/usr/bin/python
# -*- coding: utf-8 -*-

# импортируем библиотеки
import pandas as pd 
from bs4 import BeautifulSoup
import requests
import datetime

DATE = []
ROOMS_CNT = []
SOURCE = []
URL = []
PRICE = []
PRICE_FOR_METRE = []
SPACE = []
FLOOR = []
NUMBER_OF_FLOORS = []
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

def change_rooms_cnt(rooms_cnt):
    if rooms_cnt.isdigit():
        return int(rooms_cnt)
    else:
        return 'студия'

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    notification_list = soup.find('div', class_='search-results__itemCardList___RdWje').find_all('a')

    for notification in notification_list:

        try:
            date = datetime.date.today()
        except:
            date = ''

        try:
            rooms_cnt = notification.find('div', class_='long-item-card__information___YXOtb').find('span', class_='long-item-card__title___16K7W').text.strip().split('-')[0]
            rooms_cnt = change_rooms_cnt(rooms_cnt)
        except:
            rooms_cnt = ''

        try:
            personal_url = 'https://www.domofond.ru' + notification.get('href')
        except:
            personal_url = ''

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
            space = float(notification.find('div', class_='long-item-card__information___YXOtb').find('span', class_='long-item-card__title___16K7W').text.strip().split(',')[1].strip().split(' ')[0])
        except:
            space = ''

        try:
            floor = int(notification.find('div', class_='long-item-card__information___YXOtb').find('span', class_='long-item-card__title___16K7W').text.strip().split(',')[-1].split('/')[0])
        except:
            floor = ''

        try:
            numbers_of_floors = int(notification.find('div', class_='long-item-card__information___YXOtb').find('span', class_='long-item-card__title___16K7W').text.strip().split(',')[-1].strip().split(' ')[0].split('/')[-1])
        except:
            numbers_of_floors = ''

        try:
            adress = notification.find('span', class_='long-item-card__address___PVI5p').text.strip()
        except:
            adress = ''

        DATE.append(date)
        ROOMS_CNT.append(rooms_cnt)
        SOURCE.append('Domofond.ru')
        URL.append(personal_url)
        PRICE.append(total_price)
        PRICE_FOR_METRE.append(price_for_metre)
        SPACE.append(space)
        FLOOR.append(floor)
        NUMBER_OF_FLOORS.append(numbers_of_floors)
        ADRESS.append(adress)

    
def main():
    # url = 'https://www.domofond.ru/prodazha-dvuhkomnatnyh-kvartir-kotelniki-c3605'
    url = 'https://www.domofond.ru/prodazha-kvartiry-kotelniki-c3605?Rooms=Two%2CThree%2COne'
    last_page_number = last_page(get_html(url))

    for page in range(last_page_number):
        gen_url = url + '?Page={}'.format(page + 1)

        get_page_data(get_html(gen_url))

    df = pd.DataFrame(list(zip(DATE, ROOMS_CNT, URL, PRICE, PRICE_FOR_METRE, SPACE, FLOOR, NUMBER_OF_FLOORS, ADRESS, SOURCE)), 
                          columns = ['дата', 'количество комнат', 'URL', 'цена квартиры', 'цена за кв.метр', 'площадь квартиры', 'этаж', 'этажность дома', 'адрес квартиры', 'источник'])

    df.to_csv('kotelniki_all_flat.csv')

    print('ok, file is save')    
    
if __name__ == '__main__':
    main()