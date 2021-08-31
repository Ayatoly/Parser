import sys

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from States import Tuning

sys.path.append("..")
from utils.sqliter import SQLighter
from config import BOT_TOKEN


DB = SQLighter()
BOT = Bot(token=BOT_TOKEN)
DP = Dispatcher(BOT,storage=MemoryStorage())



@DP.message_handler(commands=['tuning'])
async def enter_tuning(message:types.Message):
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=3)
    """default row_width is 3, so here we can omit it actually"""
    """"" kept for clearness """

    btns_text = ('Пользовался!', 'Еще нет','Показать тюнинг сервисы')
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))
    await message.reply("Пользовались тюнинг сервисами?", reply_markup=keyboard_markup)

@DP.message_handler()
async def all_msg_handler(message: types.Message):
    button_text = message.text
    if button_text == "Пользовался!":
        await message.reply("Как назывался сервис в каком городе он находится?", reply_markup=types.ReplyKeyboardRemove())
        await Tuning.Q1.set()

    elif button_text == 'Еще нет':
        await message.reply("ну лан", reply_markup=types.ReplyKeyboardRemove())

    elif button_text == 'Показать тюнинг сервисы':
        await message.reply("я пока их не знаю", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.reply("Что это было? Ты должен был нажать на кнопку! MAZAFAKA", reply_markup=types.ReplyKeyboardRemove())

@DP.message_handler(state=Tuning.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data["answer1"] = answer
    await message.answer("Расскажите о послднем визите")
    await Tuning.next()

@DP.message_handler(state=Tuning.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = message.text
    await message.answer("Спасибо за ваши ответы!")
    print(answer1,answer2)
    await state.finish()


@DP.message_handler(commands=['start'])
async def start_handler(message: types.Message) -> None:
    """Приветствие"""
    if not DB.subcripter_exists(message.from_user.id):
        DB.add_subcripter(message.from_user.id)
    await message.answer('Наш бот, это автоматизированный сбор открытой информации! \n'
                         'который «вытаскивают» нужную информацию и представляют ее в структурированном виде.\n'
                         'В ближайшее время тут появится информация и ссылки на тюнинг центры \n'
                         'А так же аукцион JEEP где можно будет продать свой автомбиль в обход перекупщиков и салонов')


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
        DB.update_subcriptions(message.from_user.id, False)
        await message.answer('Вы успешно отписанны от рассылки ')


async def send_message_handler(url_a: str) -> None:
    """Уведомление пользователей о новых машинах"""
    for i in DB.get_all_ids():
        try:
            if int(i[2]) == 1:
                await DP.bot.send_message(
                    int(i[1]),
                    f"Появился новый автомобиль на auto.ru {url_a}"
                )
        except Exception as e0:
            print("Произошла ошибка в момент отправки сообщения - {}".format(e0))
