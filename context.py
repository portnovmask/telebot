from dotenv import load_dotenv
import os
from telebot.async_telebot import AsyncTeleBot
from gpt import ChatGptService
from util import CallBackHandler
import logging

# Загрузка переменных сетевого окружения

load_dotenv()

# Секреты

api_key = os.getenv("TELEGRAM_KEY")
secret_key = os.getenv("GPT_KEY")
bot = AsyncTeleBot(api_key)
chat_gpt = ChatGptService(secret_key)

# Хранение контекста:

bot_context = {'main': 'stop'}

callback_handler = CallBackHandler(bot)

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")


def logger(user_name):
    logging.info(f'Пользоавтель {user_name} - ')


def get_score():
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter


score = get_score()
