import telebot
from telebot import types
import sqlite3
import os

db = os.path.dirname(os.path.abspath(__file__)) + "/robofest.db"
bot = telebot.TeleBot('5063766859:AAHMEx6EcmQEcOiCmVLKeR2TC6JieszJV4Q')
user_id=''
name = ''
surname = ''
age = 0
team =''
namination = ''
phone = ''


def insert_varible_into_table(sqlphone, sqlname, sqlsurname, sqlage, sqlteam, sqlnamination):
    try:
        sqlite_connection = sqlite3.connect(db)
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_insert_with_param = """INSERT INTO users
                              (phone, name, surname, age, team, namination)
                              VALUES (?, ?, ?, ?, ?,?);"""

        data_tuple = (sqlphone, sqlname, sqlsurname, sqlage, sqlteam, sqlnamination)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()
        print("Переменные Python успешно вставлены в таблицу Users")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Спасибо, Как тебя зовут?")
        bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Это бот для регистрации на региональный этап всероссийской олипиады Робофест. Если хочешь зарегистрироваться - напиши /reg')

def get_name(message): #получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Введи номер своего телефона')
    bot.register_next_step_handler(message, get_phone)

def get_phone(message): #получаем телефон
    global phone
    phone = message.text
    bot.send_message(message.from_user.id, 'Как называется твоя команда')
    bot.register_next_step_handler(message, get_team)
    user_id = str(message.chat.id)
    print(phone)



def get_team(message): #Название команды
    global team
    team = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя номинация?')
    bot.register_next_step_handler(message, get_namination)

def get_namination(message): #в какой номинации участвует участник
    global namination
    namination = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    global age
    age=message.text
    while age == 0: #проверяем что возраст изменился
        try:
             age = int(message.text) #проверяем, что возраст введен корректно
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
    # bot.send_message(message.from_user.id, 'Тебе '+str(age)+' лет, тебя зовут '+name+' '+surname+'?'+'твоя команда '+team+'в наминации '+namination)
    keyboard = types.InlineKeyboardMarkup() #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes') #кнопка «Да»
    keyboard.add(key_yes) #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Тебе '+str(age)+' лет, тебя зовут '+name+' '+surname+' ты участвуешь в наминации '+namination+' в команде '+team
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки #код сохранения данных, или их обработки
        bot.send_message(call.message.chat.id, 'Спасибо, увидимся на Робофесте : )')
        insert_varible_into_table(phone, name, surname, age, team, namination)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Если хочешь попробовать ещё раз напиши  /reg ')


# print(db)
# sqlite_connection = sqlite3.connect(db)
# cursor = sqlite_connection.cursor()
# print("Подключен к SQLite")

# cursor.execute("SELECT name FROM sqlite_master;")
# print(cursor.fetchall())


bot.polling(none_stop=True, interval=0)
