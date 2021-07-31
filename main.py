import logging
import asyncio

from aiogram import executor

from utils.sqliter import SQLighter
from hendlers.handlers import DP
from utils.parser import get_cars


logging.basicConfig(level=logging.INFO)


async def scheduler():
    sql_obj = SQLighter()
    while True:
        cars = get_cars("https://auto.ru/moskva/cars/jeep/all/?sort=cr_date-desc&top_days=1")
        sql_obj.add_cars(cars)
        await asyncio.sleep(30)


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    executor.start_polling(DP, skip_updates=True)
