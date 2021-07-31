import sys

from datetime import datetime
import sqlite3

sys.path.append("..")
from hendlers.handlers import send_message_handler


class SQLighter:

    def __init__(self):
        """Подключаемся к БД и вызываем курсор соединения"""
        self.connection = sqlite3.connect('db.db')
        self.cursor = self.connection.cursor()

    def get_all_ids(self) -> list:
        """Список всех пользователей"""
        return self.cursor.execute('select * from "id_users"').fetchall()

    def get_subscription(self, status: bool = True) -> list:
        """Получаем всех активных подписчеков бота"""
        return self.cursor.execute(
            'SELECT * FROM "id_users" WHERE "status" = ?',
            (status,),
        ).fetchall()

    def subcripter_exists(self, user_id: int) -> bool:
        """Проверяем есть ли юзер в базе"""
        result = self.cursor.execute(
            'SELECT * FROM "id_users" WHERE "user_id" = ?',
            (user_id,),
        ).fetchall()
        return bool(len(result))

    def add_subcripter(self, user_id: int, status: bool = True) -> None:
        """Добавление пользователя в базу"""
        user_ids = self.cursor.execute('select * from "id_users"').fetchall()
        if user_id not in user_ids:
            try:
                 self.cursor.execute(
                    'INSERT INTO "id_users" ("user_id","status") VALUES (?,?)',
                    (user_id, status)
                )
                 self.connection.commit()
            except:
                 print('Он уже есть в базе')

    def update_subcriptions(self, user_id: int, status: bool) -> tuple:
        """Обновляем статус подписки"""
        return self.cursor.execute('UPDATE "id_users" SET "status" = ? WHERE "user_id" = ?',(status,user_id))

    async def add_cars(self, cars: list) -> None:
        """Добавление машины в базу"""
        for car in cars:
            try:
                 self.cursor.execute('INSERT INTO "Jeep_auto_ru"(links,price,city,date) VALUES (?,?,?,?)',
                                     (car[0], car[1], car[2], datetime.now()))
                 self.connection.commit()
            except:
                print("Машина уже есть в базе")
            else:
                await send_message_handler(car[0])

    def close(self) -> None:
        """Закрываем соединение с БД"""
        self.connection.close()
