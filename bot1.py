import asyncio
from dotenv import load_dotenv
import os
from telebot.async_telebot import AsyncTeleBot
from gpt import ChatGptService
from util import on_start_markup

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
@bot.callback_query_handler(func=lambda call: True)
async def inline(call):
    while call.message:

        if call.data == '/random':
            await bot.send_message(call.message.chat.id, "random")
            print("random")

        if call.data == '/talk':
            await bot.send_message(call.message.chat.id, "talk")

        if call.data == '/quiz':
            await bot.send_message(call.message.chat.id, "quiz")

        if call.data == '/gpt':
            await bot.send_message(call.message.chat.id, "gpt")
        break


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

asyncio.run(bot.polling())
