import sqlite3
from parser import parce
from datetime import datetime
from hendlers import sned_messange

class SQLighter:

    def __init__(self):
        '''Подключаемся к БД и вызываем курсор соединения'''
        self.connection = sqlite3.connect('db.db')
        self.cursor = self.connection.cursor()

    def get_all_ids(self):
        return self.cursor.execute('select * from "id_users"').fetchall()

    def get_subscription(self, status=True):
        '''Получаем всех активных подписчеков бота'''
        result = self.cursor.execute(
            'SELECT * FROM "id_users" WHERE "status" = ?',
            (status,),
        ).fetchall()
        self.connection.commit()
        return result

    def subcripter_exists(self, user_id):
        '''Проверяем есть ли юзер в базе'''
        result = self.cursor.execute(
            'SELECT * FROM "id_users" WHERE "user_id" = ?',
            (user_id,),
        ).fetchall()
        return bool(len(result))

    def add_subcripter(self, user_id, status=True):
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


    def update_subcriptions(self,user_id,status):
        '''Обновляем статус подписки'''
        return self.cursor.execute('UPDATE "id_users" SET "status" = ? WHERE "user_id" = ?',(status,user_id))

    def add_car(self):
        for i in parce():
            try:
                 self.cursor.execute('INSERT INTO "Jeep_auto_ru"(links,price,city,date) VALUES (?,?,?,?)',
                                     (i[0],i[1],i[2],datetime.now()))
                 self.connection.commit()
                 sned_messange(i[0])

            except:
                pass


    def close(self):
        '''Закрываем соединение с БД'''
        self.connection.close()





