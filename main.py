import sqlite3
import csv
import telebot

bot = telebot.TeleBot("7062787659:AAGvQNRhY97i8I4OkNMjD39ZR27tgz8tSTM")
# Создание базы данных SQLite и таблицы
def create_database():
    conn = sqlite3.connect('tg1base.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tgClient(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        first_name TEXT,
        username TEXT,
        f TEXT,
        i TEXT,
        o TEXT,
        datarosh TEXT
        )
        ''')
    conn.commit()
    conn.close()

# Вызываем функцию создания базы данных при старте
create_database()

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Начнем считывать данные?")

@bot.message_handler(func=lambda message: message.text.lower() == 'да')
def handle_yes(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username

    bot.send_message(message.chat.id, "Введите фамилию:")
    bot.register_next_step_handler(message, handle_surname, user_id, first_name, username)

def handle_surname(message, user_id, first_name, username):
    surname = message.text

    bot.send_message(message.chat.id, "Введите имя:")
    bot.register_next_step_handler(message, handle_name, user_id, first_name, username, surname)

def handle_name(message, user_id, first_name, username, surname):
    name = message.text

    bot.send_message(message.chat.id, "Введите отчество:")
    bot.register_next_step_handler(message, handle_patronymic, user_id, first_name, username, surname, name)

def handle_patronymic(message, user_id, first_name, username, surname, name):
    patronymic = message.text

    bot.send_message(message.chat.id, "Введите дату рождения в формате ДД.ММ.ГГГГ:")
    bot.register_next_step_handler(message, handle_birthday, user_id, first_name, username, surname, name, patronymic)

def handle_birthday(message, user_id, first_name, username, surname, name, patronymic):
    birthday = message.text

    # Считывание данных из файла CSV и вставка их в базу данных SQLite
    con = sqlite3.connect('tgbase.db')
    cur = con.cursor()
    cur.execute("INSERT INTO tgClient(user_id, first_name, username, f, i, o, datarosh) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (user_id, first_name, username, surname, name, patronymic, birthday))
    con.commit()
    con.close()

    # Запись данных в файл CSV
    with open('tgClient.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(['user_id', 'first_name', 'username', 'surname', 'name', 'patronymic', 'birthday'])
        writer.writerow([user_id, first_name, username, surname, name, patronymic, birthday])

    bot.send_message(message.chat.id, "Данные успешно записаны.")

bot.polling()
