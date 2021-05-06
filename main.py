import glob
import logging
import os
import sqlite3

from aiogram import Bot, Dispatcher, executor, types

TOKEN = '1772334389:AAE5wv8gssOFOgxQjQwKk7rUSKQHr6NTjus'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
path1 = 'C:\\Users\\const\\PycharmProjects\\t'

conn = sqlite3.connect('kustoge.db')
cur = conn.cursor()
chunksize = 10

idfolder = "C:\\Users\\const\\PycharmProjects\\goskustoge\\data\\id"


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Портал Государственных услуг округа Кустоже\n\n Используете команду  /id + номер_паспорта \n для "
        "получения информации о владельце.\n\n Так же можно использовать команду /fullname + имя + фамилия, "
        "для получения информации о гражданине, регистр и порядок не важен\n\n Для получения информации о гражданах по "
        "фамилии воспользуйтесь командой /lastname + Фамилия \n\n Для получения данных о гражданах по национальности "
        "используйте /get_scan_nat+ брасогорец\отовичанин \n\n Для добавления гражданина "
        "воспользуйтесь командой /add_person ИМЯ+ФАМИЛИЯ+НОМЕР_ПАСПОРТА+НАЦИОНАЛЬНОСТЬ+НОМЕР_ЛИЦЕНЗИИ_"
        "ОРУЖЕЙНОЙ+Преступление ( если нет лицензии и преступления пишем НЕТ \n\n Для удаления гражданина "
        "используйте /delete_person + номер паспорта \n\n Для добавления лицензии на оружение воспользуйтесь командой "
        "/add_gun_lic+id+номер_лицензии \n\n "
        "Для удалениея /delete_gun_lic + id \n\n Для добавления преступления гражданину используйте команду "
        "/add_crime  +id + преступление \n Для удаления преступления воспользуйтесь командой /delete_crime + id")


@dp.message_handler(commands=['id'])
async def echo(message: types.Message):
    print("попросили данные по ID")
    arguments = message.get_args()
    print(arguments)
    cur.execute("select * from barsa where id=:id", {"id": arguments})
    res = cur.fetchone()
    cur.execute("select count(*) from barsa where lastname=:lastname",
                {"lastname": res[2]})
    res2 = cur.fetchone()
    print(res2)
    result = 'Имя:' + '     ' + res[1] + '\n' + 'Фамилия:' + '     ' + res[2] + '\n' + 'Номер Паспорта:' + '     ' + \
             res[3] + '\n' + 'Национальность:' + '     ' + res[4] + "\n" + "Родвественников:" + '     ' + str(
        res2[0]) + '\n' + "Номер " \
                          "лицензии на " \
                          "оружие:" + "     " + \
             res[5] + '\n' + "Преступление:" + "     " + res[6]
    await bot.send_message(message.from_user.id, result)
    os.chdir(idfolder)
    for file in glob.glob(res[3] + ".jpg"):
        img = open(file, "rb")
        await bot.send_photo(message.from_user.id, img)


@dp.message_handler(commands=['fullname'])
async def echo(message: types.Message):
    print("попросили данные по имени")
    arguments = message.get_args()
    print(arguments)
    s = arguments.lower()
    s = s.split()
    cur.execute("select * from barsa where name=:name and lastname=:lastname or name=:lastname and lastname=:name",
                {"name": s[0], "lastname": s[1]})
    res = cur.fetchone()
    cur.execute("select count(*) from barsa where lastname=:lastname",
                {"lastname": s[1]})
    res2 = cur.fetchone()
    print(res2[0])
    result = 'Имя:' + '     ' + res[1] + '\n' + 'Фамилия:' + '     ' + res[2] + '\n' + 'Номер Паспорта:' + '     ' + \
             res[3] + '\n' + 'Национальность:' + '     ' + res[4] + "\n" + "Родвественников:" + '     ' + str(
        res2[0]) + '\n' + "Номер " \
                          "лицензии на " \
                          "оружие:" + "     " + \
             res[5] + '\n' + \
             "Преступление:" + "     " + res[6]
    await bot.send_message(message.from_user.id, result)
    os.chdir(idfolder)
    for file in glob.glob(res[3] + ".jpg"):
        img = open(file, "rb")
        await bot.send_photo(message.from_user.id, img)


@dp.message_handler(commands=['lastname'])
async def echo(message: types.Message):
    arguments = message.get_args()
    print("попросили данные по Фамилии:", arguments)
    s = arguments.lower()
    cur.execute("select * from barsa where lastname=:lastname ",
                {"lastname": s})
    res = cur.fetchall()
    os.chdir(idfolder)
    for f in res:
        print(f)
        cur.execute("select * from barsa where id=:id", {"id": f[3]})
        res = cur.fetchone()
        req = 'Имя:' + '     ' + res[1] + '\n' + 'Фамилия:' + '     ' + res[
            2] + '\n' + 'Номер Паспорта:' + '     ' + res[3] + '\n' + 'Национальность:' + '     ' + res[
                  4] + '\n' + "Номер " \
                              "лицензии на " \
                              "оружие:" + "     " + \
              res[5] + '\n' + \
              "Преступление:" + "     " + res[6]
        await bot.send_message(message.from_user.id, req)

        for file in glob.glob(res[3] + ".jpg"):
            img = open(file, "rb")
            await bot.send_photo(message.from_user.id, img)


@dp.message_handler(commands=['get_scan_nat'])
async def echo(message: types.Message):
    print("попросили ВСЕ СКАНЫ по по национальности")
    arguments = message.get_args()
    print(arguments)
    s = arguments
    s = s.capitalize()
    cur.execute("select id from barsa where nat_=:nat_", {"nat_": s})
    res = cur.fetchall()
    out = [item for t in res for item in t]
    out = [s.replace(" ", "") for s in out]
    os.chdir(idfolder)
    for f in out:
        print(f)
        if f == '472-641218' or f == '757-067985' or f == '642-741978' or f == '696-082959' or f == '442-446766' or f == '702-973965':
            cur.execute("select * from barsa where id=:id", {"id": f})
            res = cur.fetchone()
            req = 'Имя:' + '     ' + res[1] + '\n' + 'Фамилия:' + '     ' + res[
                2] + '\n' + 'Номер Паспорта:' + '     ' + res[3] + '\n' + 'Национальность:' + '     ' + res[
                      4] + '\n' + "Номер " \
                                  "лицензии на " \
                                  "оружие:" + "     " + \
                  res[5] + '\n' + \
                  "Преступление:" + "     " + res[6]
            await bot.send_message(message.from_user.id, req)
        else:
            img = open(f + '.jpg', "rb")
            print('ok')
            await bot.send_photo(message.from_user.id, img)


@dp.message_handler(commands=['add_person'])
async def echo(message: types.Message):
    arguments = message.get_args()
    s = arguments.split()
    print(s)
    sqlite_insert_query = """INSERT INTO barsa
                              (name, lastname, id, nat_,gunlic,crime)
                               VALUES
                              (?,?,?,?,?,?)"""
    data_tuple = (s[0], s[1], s[2], s[3], s[4], s[5])
    cur.execute(sqlite_insert_query, data_tuple)
    conn.commit()

    print("Запись о гражданине успешно добавлена ")
    cur.execute("select * from barsa where id=:id", {"id": s[2]})
    res = cur.fetchone()
    req = 'Имя:' + '     ' + res[1] + '\n' + 'Фамилия:' + '     ' + res[
        2] + '\n' + 'Номер Паспорта:' + '     ' + res[3] + '\n' + 'Национальность:' + '     ' + res[4] + '\n' + "Номер " \
                                                                                                                "лицензии на " \
                                                                                                                "оружие:" + "     " + \
          res[5] + '\n' + \
          "Преступление:" + "     " + res[6]
    await bot.send_message(message.from_user.id, req)


@dp.message_handler(commands=['delete_person'])
async def echo(message: types.Message):
    arguments = message.get_args()
    print("попросили удалить гражаднина с ID:", arguments)
    s = arguments
    cur.execute("delete from barsa where id=:id", {"id": s})
    conn.commit()
    print("Гражданин с ID :", arguments, 'удален')
    res = "Гражданин с ID :", arguments, 'удален'
    await bot.send_message(message.from_user.id, res)


@dp.message_handler(commands=['add_gun_lic'])
async def echo(message: types.Message):
    arguments = message.get_args()
    s = arguments.split()
    print(s[0], s[1])
    cur.execute(" update barsa set gunlic=:gunlic where id=:id", {"gunlic": s[1], "id": s[0]})
    conn.commit()
    print("Record Updated successfully ")
    cur.execute("select * from barsa where id=:id", {"id": s[0]})
    res = cur.fetchone()
    print(res)
    req = 'Имя:' + '     ' + res[1] + '\n' + 'Фамилия:' + '     ' + res[
        2] + '\n' + 'Номер Паспорта:' + '     ' + res[3] + '\n' + 'Национальность:' + '     ' + res[4] + '\n' + "Номер " \
                                                                                                                "лицензии на " \
                                                                                                                "оружие:" + "     " + \
          res[5]
    await bot.send_message(message.from_user.id, req)


@dp.message_handler(commands=['gun_lic'])
async def echo(message: types.Message):
    arguments = message.get_args()
    s = arguments
    print(s)
    cur.execute("select * from barsa where gunlic=:gunlic", {"gunlic": s})
    res = cur.fetchone()
    print(res)
    req = 'Имя:' + '     ' + res[1] + '\n' + 'Фамилия:' + '     ' + res[
        2] + '\n' + 'Номер Паспорта:' + '     ' + res[3] + '\n' + 'Национальность:' + '     ' + res[4] + '\n' + "Номер " \
                                                                                                                "лицензии на " \
                                                                                                                "оружие:" + "     " + \
          res[5] + '\n' + \
          "Преступление:" + "     " + res[6]
    await bot.send_message(message.from_user.id, req)


@dp.message_handler(commands=['delete_gun_lic'])
async def echo(message: types.Message):
    arguments = message.get_args()
    s = arguments
    print(s)
    no = 'нет'
    cur.execute("update barsa set gunlic=:gunlic1 where id=:id", {"gunlic1": no, "id": s})
    res1 = cur.fetchone()
    conn.commit()
    ans =  "Оружейная лицения гражданина:",s, "  удалена"
    await bot.send_message(message.from_user.id, ans)


@dp.message_handler(commands=['add_crime'])
async def echo(message: types.Message):
    arguments = message.get_args()
    s = arguments.split()
    print(s[0], s[1])
    cur.execute(" update barsa set crime=:crime where id=:id", {"crime": s[1], "id": s[0]})
    conn.commit()
    print("Record Updated successfully ")
    cur.execute("select * from barsa where id=:id", {"id": s[0]})
    res = cur.fetchone()
    print(res)
    req = 'Имя:' + '     ' + res[1] + '\n' + 'Фамилия:' + '     ' + res[
        2] + '\n' + 'Номер Паспорта:' + '     ' + res[3] + '\n' + 'Национальность:' + '     ' + res[4] + '\n' + "Номер " \
                                                                                                                "лицензии на " \
                                                                                                                "оружие:" + "     " + \
          res[5] + '\n' + \
          "Преступление:" + "     " + res[6]
    await bot.send_message(message.from_user.id, req)

@dp.message_handler(commands=['delete_crime'])
async def echo(message: types.Message):
    arguments = message.get_args()
    s = arguments
    print(s)
    no = 'нет'
    cur.execute("update barsa set crime=:crime where id=:id", {"crime": no, "id": s})
    res1 = cur.fetchone()
    conn.commit()
    ans =  "Преступление гражданина:",s, "  удалено"
    await bot.send_message(message.from_user.id, ans)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
