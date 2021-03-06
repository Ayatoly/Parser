from datetime import datetime
import sqlite3


class SQLighter:

    def __init__(self):
        """Подключаемся к БД и вызываем курсор соединения"""
        self.connection = sqlite3.connect('new_db.db')
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

    def add_subcripter(self, user_id: str, status: bool = True) -> None:
        """Добавление пользователя в базу"""
        with self.connection:
            if user_id not in self.cursor.execute('select * from "id_users"').fetchall():
                try:
                    self.cursor.execute('INSERT INTO "id_users" ("user_id", "status") VALUES (?,?)', (user_id, status))
                    self.connection.commit()
                except:
                    print('Он уже есть в базе')

    def update_subcriptions(self, user_id: int, status: bool):
        """Обновляем статус подписки"""
        with self.connection:
            self.cursor.execute('UPDATE "id_users" SET "status" = ? WHERE "user_id" = ?', (status, user_id))
            self.connection.commit()

    async def add_cars(self, cars: list):
        """Добавление машины в базу"""
        with self.connection:
            for car in cars:
                try:
                    self.cursor.execute('INSERT INTO "Jeep_auto_ru"(links,price,city,date) VALUES (?,?,?,?)',
                                      (car[0], car[1], car[2], datetime.now()))
                    self.connection.commit()
                except:
                    print("Машина уже есть в базе")
                else:
                    print("Машина успешно добавлена")
                    yield car[0]

    def close(self) -> None:
        """Закрываем соединение с БД"""
        self.connection.close()
