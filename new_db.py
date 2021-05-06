import sqlite3
import pandas as pd

import logging
from aiogram import Bot, Dispatcher, executor, types
import sqlite3
import glob, os
import pandas as pd
from aiogram.types import message
from sklearn import datasets

TOKEN = '1772334389:AAE5wv8gssOFOgxQjQwKk7rUSKQHr6NTjus'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
path1 = 'C:\\Users\\const\\PycharmProjects\\t'

conn = sqlite3.connect('db_test.db')
cur = conn.cursor()
chunksize = 10

idfolder = "C:\\Users\\const\\PycharmProjects\\goskustoge\\data\\id"


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Портал Государственных услуг округа Кустоже\n\n Используете команду  /id + номер_паспорта \n для "
        "получения информации о владельце.\n\n Так же можно использовать команду /name + фио, для получения "
        "информации о гражданине, регистр и порядок не важен\n\n Для "
        "получения скана паспрорта используйте команду /get_scan_id + номер паспорта\n Для поиска по имени "
        "используйте команду /get_scan_name + имя фамилия гражданина, \n\n Для получения всех паспартов по "
        "национальности используйте /get_scan_nat барсогорец или отовичанин\n\n Для получения постпартов "
        "родственников иcпользуйте команду /get_scans_lastname + фамилия")


def print_all():
    cur.execute('SELECT * FROM persons')
    names = list(map(lambda x: x[0], cur.description))  # Returns the column names
    print(names)
    for row in cur:
        print(row)
    cur.close()


# print_all()


@dp.message_handler(commands=['add_gun_lic'])
async def echo(message: types.Message):
    arguments = message.get_args()
    s = arguments.split()
    print(s[0], s[1])
    cur.execute( " update citizens set gunlic=:gunlic where id=:id", {"gunlic":s[1], "id":s[0]})
    conn.commit()
    print("Record Updated successfully ")
    cur.execute("select * from citizens where id=:id", {"id": s[0]})
    res = cur.fetchone()

    await bot.send_message(message.from_user.id, res)
    cur.close()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
