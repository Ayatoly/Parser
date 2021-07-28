import aiohttp
from bs4 import BeautifulSoup
import asyncio
import sqlite3
from datetime import datetime

connection = sqlite3.connect('db.db')
cursor = connection.cursor()

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    # noqa
    'accept': '*/*',
}


async def parser_autoRU_Jeep(URL='https://auto.ru/cars/jeep/all/'):
    async with aiohttp.ClientSession() as session:
        ''''Создание сессии'''
        async with session.get(URL, headers=HEADERS) as response:
            response = await response.read()
            html_page = response.decode('utf-8')

        soup = BeautifulSoup(html_page, 'lxml')
        cars = soup.findAll(
            'div',
            class_='ListingItem-module__description',
        )
        for car in cars:
            try:
                a = car.find('a', class_='Link ListingItemTitle__link').get('href')
                b = car.find('div', class_='ListingItemPrice-module__content').text.strip()
                l = car.find('span', class_='MetroListPlace__regionName MetroListPlace_nbsp').text.strip()
                print(a,b,l,len(cars))
                with connection:
                    cursor.execute('INSERT INTO "Jeep_auto_ru"(links,price,city,date) VALUES (?,?,?,?)',(a,b,l,datetime.now()))

            except:
                pass




loop = asyncio.get_event_loop()

loop.run_until_complete(parser_autoRU_Jeep())
