import telebot
from telebot.types import Message
import json
from TOKEN import token

bot = telebot.TeleBot(token=token)

@bot.message_handler(commands=['start'])
def start(message: Message):
    # регистрация при помощи json файла
    with open('users.json', 'r') as f_o:
        data_from_json = json.load(f_o)

    user_id = message.from_user.id
    username = message.from_user.username
    if str(user_id) not in data_from_json:
        data_from_json[user_id] = {"username": username}

    with open('users.json', 'w') as f_o:
        json.dump(data_from_json, f_o, indent=3, ensure_ascii=False)

    bot.send_message(message.chat.id, text='Это чат-бот напоминалка!')


def handle_say_standup_speech(message: Message):
    bot.reply_to(message, "Удачного тебе дня!")


@bot.message_handler(commands=['say_standup_speech'])
def say_standup_speech(message: Message):
    bot.send_message(message.chat.id, text='Привет-привет! Как дела?')

    bot.register_next_step_handler(message, handle_say_standup_speech)



bot.polling()