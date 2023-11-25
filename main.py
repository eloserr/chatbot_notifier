import telebot
from telebot.types import Message
import json
import requests
from datetime import datetime
from envparse import Env
from clients.telegram_client import TelegramClient

env = Env()
TOKEN = env.str("TOKEN")
ADMINCHATID = env.int("ADMINCHATID")
bot = telebot.TeleBot(token=TOKEN)

class MyBot(telebot.Telebot):
    def __init__(self, telegram_client: TelegramClient, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.telegram_client = telegram_client
        
telegram_client = TelegramClient(token=TOKEN, base_url="https://api.telegram.org")
bot = MyBot(token=TOKEN, telegram_client=telegram_client)
    

@bot.message_handler(commands=["start"])
def start(message: Message):
    # регистрация при помощи json файла
    with open("users.json", "r") as f_o:
        data_from_json = json.load(f_o)

    user_id = message.from_user.id
    username = message.from_user.username

    if str(user_id) not in data_from_json:
        data_from_json[user_id] = {"username": username}
    with open("users.json", "w") as f_o:
        json.dump(data_from_json, f_o, indent=3, ensure_ascii=False)

    bot.send_message(message.chat.id, text="Это чат-бот напоминалка!")


def handle_say_standup_speech(message: Message):
    bot.reply_to(message, "Удачного тебе дня!")


@bot.message_handler(commands=["say_standup_speech"])
def say_standup_speech(message: Message):
    bot.send_message(message.chat.id, text="Привет-привет! Как дела?")

    bot.register_next_step_handler(message, handle_say_standup_speech)


# чтобы после логгирования можно было выявить еще ошибки
while True:
    try:
        bot.polling()
    except Exception as err:
        # при возникновении ошибки сообщит админу(мне)
        bot.telegram_client.post()
        requests.post(
            f"https://api.telegram.org/bot6580423597:AAHp_hi9VriNd6uvUwkmuj6_"
            f"wxy5A48qjMQ/sendMessage?chat_id=1256457948&text={datetime.now()}:::{err.__class__}:::{err}"
        )
