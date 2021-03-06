import logging
import asyncio

from aiogram import executor

from utils.sqliter import SQLighter
from hendlers.handlers import DP
from utils.parser import get_cars
from hendlers.handlers import send_message_handler


logging.basicConfig(level=logging.INFO)


async def scheduler():
    sql_obj = SQLighter()
    while True:
        cars = get_cars("https://auto.ru/moskva/cars/jeep/all/?sort=cr_date-desc&top_days=1")
        async for car in sql_obj.add_cars(cars):
            await send_message_handler(car)
        await asyncio.sleep(3000)


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    executor.start_polling(DP, skip_updates=True)
