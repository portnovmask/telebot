from dotenv import load_dotenv
import os
from telebot.async_telebot import AsyncTeleBot
from gpt import ChatGptService
from util import on_start_markup, CallBackHandler, load_prompt
import asyncio
from telebot.types import InputFile

#загрузка переменных сетевого окружения
load_dotenv()

#Секреты

api_key = os.getenv("TELEGRAM_KEY")
secret_key = os.getenv("GPT_KEY")
bot = AsyncTeleBot(api_key)
chat_gpt = ChatGptService(secret_key)


# Обработчик базовых слэш комманд
@bot.message_handler(commands=['help', 'start', 'stop'])
async def send_welcome(message):
    text = 'Hi, we start here!'
    await bot.send_message(message.chat.id, text, reply_markup=on_start_markup)
    print(message.text)


#Функции упаковки ответов от gpt:

#Случайный запрос или просто сообщение без промпта
async def handle_random(call, re_quest, pic):
    with open(pic, 'rb') as photo:
        await bot.send_photo(call.message.chat.id, photo)
    response = await chat_gpt.add_message(load_prompt(re_quest))
    await bot.send_message(call.message.chat.id, response)


#Любой запрос без контекста, подразумевается, что промпт объекта установлен
async def handle_any(call, re_quest):
    response = await chat_gpt.add_message(re_quest)
    await bot.send_message(call.message.chat.id, response)


#Запросы с новым контекстом, промпт переустанавливается на новый
async def handle_questions(call, prompt, current_message):
    set_prompt = chat_gpt.set_prompt(load_prompt(prompt))
    response = await chat_gpt.send_question(set_prompt, current_message)
    await bot.send_message(call.message.chat.id, response)


#Задаём промпт для контекстных задач
async def set_prompt(call, prompt, message, pic, markup):
    with open(pic, 'rb') as photo:
        await bot.send_photo(call.message.chat.id, photo)
    chat_gpt.set_prompt(load_prompt(prompt))
    await bot.send_message(call.message.chat.id, message, reply_markup=markup)


# Обработчик инлайн кнопок
# Создаём объект класса обработчика инлайн кнопок
callback_handler = CallBackHandler(bot)

#регистрируем функции обработчики команд с инлайн кнопок

#Главное меню

callback_handler.callback_register(
    '/random', lambda call: asyncio.create_task(handle_random(call, 'random', 'resources/images/random.jpg')))

callback_handler.callback_register(
    '/gpt', lambda call: bot.send_message(
        call.message.chat.id, "Выберите шефа, с которым хотите початить:", reply_markup=on_start_markup))
callback_handler.callback_register(
    '/quiz', lambda call: asyncio.create_task(set_prompt(
        call, 'quiz', "Выберите тему квиза:", 'resources/images/quiz.jpg', on_start_markup)))
callback_handler.callback_register(
    '/recipe', lambda call: bot.send_message(call.message.chat.id, "Перечислите от 1 до 3 продуктов для рецепта",
                                             reply_markup=on_start_markup))
callback_handler.callback_register(
    '/guess', lambda call: bot.send_message(call.message.chat.id, "guess"))

#Знаменитости
callback_handler.callback_register(
    '/ramzi', lambda call: bot.send_message(call.message.chat.id, "ramzi"))
callback_handler.callback_register(
    '/oliver', lambda call: bot.send_message(call.message.chat.id, "oliver"))
callback_handler.callback_register(
    '/ducas', lambda call: bot.send_message(call.message.chat.id, "ducas"))
callback_handler.callback_register(
    '/bocus', lambda call: bot.send_message(call.message.chat.id, "bocus"))
callback_handler.callback_register(
    '/blumental', lambda call: bot.send_message(call.message.chat.id, "blumental"))

#Квизы
callback_handler.callback_register(
    '/start', lambda call: bot.send_message(call.message.chat.id, "start"))

#Хватит
callback_handler.callback_register(
    '/stop', lambda call: bot.send_message(call.message.chat.id, "stop"))


@bot.callback_query_handler(func=lambda call: True)
async def inline(call):
    await callback_handler.handle_callback(call)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo'])
async def echo_message(message):
    await bot.reply_to(message, message.text)


asyncio.run(bot.polling())
