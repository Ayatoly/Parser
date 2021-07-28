import sqlite3
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup
import config
import logging
from aiogram import Bot, Dispatcher, executor, types
from sqliter import SQLighter
import asyncio
import aioschedule as schedule




HEADERS = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
           'accept':'*/*'}
host = 'https://auto.ria.com'
# log lvl
logging.basicConfig(level=logging.INFO)

# Обработчик событий
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

db = SQLighter()
connection = sqlite3.connect('db.db')
cursor = connection.cursor()
# Команда активации подписки
@dp.message_handler(commands=['start'])
async def echo(message: types.Message):
    await bot.send_photo(chat_id=message.from_user.id,
                         photo='https://sun9-17.userapi.com/impf/c625430/v625430425/4ca25/jsCLXjqIy-M.jpg?size=604x229&quality=96&sign=0da7630d8a112982acec2a4801179f23&type=album')



@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if(not db.subcripter_exists(message.from_user.id)):
        db.add_subcripter(message.from_user.id)

    else:
        db.update_subcriptions(message.from_user.id,True)

    await message.answer('Вы успешно подписались на рассылку! \n Ждите скоро выйдут новые обзоры!')

@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if(not db.subcripter_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его в базу с неактивной подпиской
        db.add_subcripter(message.from_user.id,False)
        await message.answer('Вы и так не подписанны.')
    else:
        # Если он уже есть то просто обновляем ему статус подписки
        db.add_subcripter(message.from_user.id,False)
        await message.answer('Вы успешно отписанны от рассылки ')


async def parser4(URL = 'https://auto.ru/moskva/cars/jeep/all/?top_days=1&sort=cr_date-desc/'):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL, headers=HEADERS) as r:
            response = await r.text()
    soup = BeautifulSoup(response, 'lxml')
    cars = soup.findAll('div', class_='proposition')
    answer = []
    links = []
    l = cursor.execute('SELECT "url" FROM "link"').fetchall()
    for i in l:
        links.append(*i)

    for car in cars:
        url = car.find('a', class_='proposition_link').get('href')
        if url not in links:
            answer.append(
                {'name': car.find('span', class_='link').text.strip(),
                'price': car.find('div', class_='proposition_price').text.strip(),
                'city': car.find('span', class_='item region').text.strip(),
                'link': url})
            for name in answer:
                print(f'{name["name"]} | {name["price"][:9]} | {name["city"]} | https://auto.ria.com{name["link"]}')
            with connection:
                cursor.execute('INSERT INTO "link" (url,date) VALUES (?,?)',(url,
                                                                             datetime.now()))
            for i in db.get_all_id():
                try:
                    await dp.bot.send_message(
                        int(i[1]),
                        f"Появился новый автомобиль на auto.ria {host+url}")
                except:
                    pass


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
            l_auto_ru = cursor.execute('SELECT "links" FROM "Jeep_auto_ru"').fetchall()
            auto_ru_links = []

            for i in l_auto_ru:
                auto_ru_links.append(*i)
            print(len(auto_ru_links),auto_ru_links)
            for car in cars:
                try:
                    url_a = car.find('a', class_='Link ListingItemTitle__link').get('href')
                except:
                    print("не смог")
                try:
                    a = car.find('a', class_='Link ListingItemTitle__link').get('href')
                    b = car.find('div', class_='ListingItemPrice-module__content').text.strip()
                    l = car.find('span', class_='MetroListPlace__regionName MetroListPlace_nbsp').text.strip()
                    print(a,b,l)
                except:
                    print('Произошла ошибка')
                if url_a not in auto_ru_links:
                    with connection:
                        cursor.execute('INSERT INTO "Jeep_auto_ru"(links,price,city,date) VALUES (?,?,?,?)',
                                       (a, b, l, datetime.now()))
                    for i in db.get_all_id():
                        try:
                            await dp.bot.send_message(
                                int(i[1]),
                                f"Появился новый автомобиль на auto.ru {url_a}")
                        except:
                            pass

async def scheduler():
    schedule.every(5).seconds.do(parser4)
    schedule.every(5).seconds.do(parser_autoRU_Jeep)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(30)


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    executor.start_polling(dp, skip_updates=True)
