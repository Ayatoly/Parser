import sys

from aiogram import Bot, Dispatcher, types

sys.path.append("..")
from utils.sqliter import SQLighter
from config import BOT_TOKEN


DB = SQLighter()
BOT = Bot(token=BOT_TOKEN)
DP = Dispatcher(BOT)


@DP.message_handler(commands=['start'])
async def start_handler(message: types.Message) -> None:
    """Приветствие"""
    await BOT.send_photo(chat_id=message.from_user.id,
                         photo='https://sun9-17.userapi.com/impf/c625430/v625430425/4ca25/jsCLXjqIy-M.jpg?size=604x229&quality=96&sign=0da7630d8a112982acec2a4801179f23&type=album')


@DP.message_handler(commands=['subscribe'])
async def subscribe_handler(message: types.Message) -> None:
    """Подписка"""
    if not DB.subcripter_exists(message.from_user.id):
        DB.add_subcripter(message.from_user.id)
    else:
        DB.update_subcriptions(message.from_user.id, True)

    await message.answer('Вы успешно подписались на рассылку! \n Ждите скоро выйдут новые обзоры!')


@DP.message_handler(commands=['unsubscribe'])
async def unsubscribe_handler(message: types.Message) -> None:
    """Отписка"""
    if not DB.subcripter_exists(message.from_user.id):
        # если юзера нет в базе, добавляем его в базу с неактивной подпиской
        DB.add_subcripter(message.from_user.id, False)
        await message.answer('Вы и так не подписанны.')
    else:
        # Если он уже есть то просто обновляем ему статус подписки
        DB.add_subcripter(message.from_user.id, False)
        await message.answer('Вы успешно отписанны от рассылки ')


async def send_message_handler(url_a: str) -> None:
    """Уведомление пользователей о новых машинах"""
    for i in DB.get_all_ids():
        try:
            await DP.bot.send_message(
                int(i[1]),
                f"Появился новый автомобиль на auto.ru {url_a}"
            )
        except Exception as e0:
            print("Произошла ошибка в момент отправки сообщения - {}".format(e0))
