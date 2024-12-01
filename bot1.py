from dotenv import load_dotenv
import os
from telebot.async_telebot import AsyncTeleBot
from gpt import ChatGptService
from util import on_start_markup, CallBackHandler

#загрузка переменных сетевого окружения
load_dotenv()

#Секреты

api_key = os.getenv("TELEGRAM_KEY")
secret_key = os.getenv("GPT_KEY")
bot = AsyncTeleBot(api_key)


# Обработчик базовых комманд
@bot.message_handler(commands=['help', 'start', 'stop'])
async def send_welcome(message):
    text = 'Hi, we start here!'
    await bot.send_message(message.chat.id, text, reply_markup=on_start_markup)
    print(message.text)


# Обработчик инлайн кнопок
#Создаём объект класса обработчика инлайн кнопок
callback_handler = CallBackHandler(bot)


#регистрируем функции обработчики команд с инлайн кнопок
callback_handler.callback_register('/random', lambda call: bot.send_message(call.message.chat.id, "random"))
callback_handler.callback_register('/start', lambda call: bot.send_message(call.message.chat.id, "start"))
callback_handler.callback_register('/stop', lambda call: bot.send_message(call.message.chat.id, "stop"))
callback_handler.callback_register('/gpt', lambda call: bot.send_message(call.message.chat.id, "gpt"))
callback_handler.callback_register('/quiz', lambda call: bot.send_message(call.message.chat.id, "quiz"))
callback_handler.callback_register('/recipe', lambda call: bot.send_message(call.message.chat.id, "recipe"))
callback_handler.callback_register('/guess', lambda call: bot.send_message(call.message.chat.id, "guess"))
callback_handler.callback_register('/ramzi', lambda call: bot.send_message(call.message.chat.id, "ramzi"))
callback_handler.callback_register('/oliver', lambda call: bot.send_message(call.message.chat.id, "oliver"))
callback_handler.callback_register('/ducas', lambda call: bot.send_message(call.message.chat.id, "ducas"))
callback_handler.callback_register('/bocus', lambda call: bot.send_message(call.message.chat.id, "bocus"))
callback_handler.callback_register('/blumental', lambda call: bot.send_message(call.message.chat.id, "blumental"))
@bot.callback_query_handler(func=lambda call: True)
async def inline(call):
    await callback_handler.handle_callback(call)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)


#chat_gpt = ChatGptService(secret_key)

#{
#       'start': 'Главное меню',
#
#  'gpt': 'Задать вопрос чату GPT 🤖',
#      'talk': 'Поговорить с известной личностью 👤',
#      'quiz': 'Поучаствовать в квизе ❓'
#      # Добавить команду в меню можно так:
# 'command': 'button text'

# })


import asyncio

asyncio.run(bot.polling())
