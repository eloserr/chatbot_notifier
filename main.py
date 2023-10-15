import telebot
from telebot.types import Message
import json
from TOKEN import token
import requests
from datetime import datetime



bot = telebot.TeleBot(token=token)
ADMIN_CHAT_ID = 1256457948

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

# чтобы после логгирования можно было выявить еще ошибки
while True:
    try:
        bot.polling()
    except Exception as err:
        # при возникновении ошибки сообщит админу(мне)
        print('Ошибка', err)
        requests.post(f'https://api.telegram.org/bot6580423597:AAHp_hi9VriNd6uvUwkmuj6_'
                    f'wxy5A48qjMQ/sendMessage?chat_id=1256457948&text={datetime.now()}:::{err.__class__}:::{err}')