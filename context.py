from dotenv import load_dotenv
import os
from telebot.async_telebot import AsyncTeleBot
from gpt import ChatGptService
from util import markups, CallBackHandler, load_prompt, load_message

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

