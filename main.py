
import logging
from aiogram import executor

import asyncio
import aioschedule as schedule



logging.basicConfig(level=logging.INFO)

async def scheduler():
    schedule.every(5).seconds.do()
    while True:
        await schedule.run_pending()
        await asyncio.sleep(30)


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    executor.start_polling(dp, skip_updates=True)
