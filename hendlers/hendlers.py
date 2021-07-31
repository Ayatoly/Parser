import sys

from aiogram import Bot, Dispatcher, types
from sqliter import SQLighter

sys.path.append("../data/")
import config


db = SQLighter()

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message) -> None:
    """Приветствие"""
    await bot.send_photo(chat_id=message.from_user.id,
                         photo='https://sun9-17.userapi.com/impf/c625430/v625430425/4ca25/jsCLXjqIy-M.jpg?size=604x229&quality=96&sign=0da7630d8a112982acec2a4801179f23&type=album')
    

@dp.message_handler(commands=['subscribe'])
async def subscribe_handler(message: types.Message) -> None:
    """Подписка"""
    if not db.subcripter_exists(message.from_user.id):
        db.add_subcripter(message.from_user.id)
    else:
        db.update_subcriptions(message.from_user.id,True)

    await message.answer('Вы успешно подписались на рассылку! \n Ждите скоро выйдут новые обзоры!')

    
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe_handler(message: types.Message) -> None:
    """Отписка"""
    if not db.subcripter_exists(message.from_user.id):
        # если юзера нет в базе, добавляем его в базу с неактивной подпиской
        db.add_subcripter(message.from_user.id,False)
        await message.answer('Вы и так не подписанны.')
    else:
        # Если он уже есть то просто обновляем ему статус подписки
        db.add_subcripter(message.from_user.id,False)
        await message.answer('Вы успешно отписанны от рассылки ')

        
async def send_messange_handler(url_a: str) -> None:
    """Уведомление пользователей о новых машинах"""
    for i in db.get_all_ids():
        try:
            await dp.bot.send_message(
                int(i[1]),
                f"Появился новый автомобиль на auto.ru {url_a}"
            )
        except:
            pass
