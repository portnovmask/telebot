from dotenv import load_dotenv
import os
from telebot.async_telebot import AsyncTeleBot
from gpt import ChatGptService
from util import markups, CallBackHandler, load_prompt
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
    text = f"""Привет, это бот о кулинарии на базе chatGPT!
Выбирай из меню ниже, чтобы продолжить:"""
    await bot.send_message(
        message.chat.id, text, reply_markup=markups['on_start_markup'])
    print(message.text)

async def handle_start(call):
    # Проверяем команду
    if call.data == '/start':
        await send_welcome(call.message)

#Функции упаковки ответов от gpt:


#Хранение контекста:

bot_context = {'main': 'random'}


#Случайный запрос или просто сообщение без промпта
async def handle_random(call, re_quest, pic, **kwargs):
    pic = 'resources/images/random.jpg'
    re_quest = 'random'

    # Удаляем inline-разметку из предыдущего сообщения
    await bot.edit_message_text("Ищу интересный факт о кулинарии и еде...",
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                reply_markup=None,
                                timeout=2
                                )
    with open(pic, 'rb') as photo:
        await bot.send_photo(call.message.chat.id, photo)
    response = await chat_gpt.add_message(load_prompt(re_quest))
    await bot.send_message(call.message.chat.id, response,
                           reply_markup=markups['random'])


#Любой запрос без контекста, подразумевается, что промпт объекта установлен
async def handle_answers(re_quest, context, markup):
    bot_context['main'] = context
    mode = 0
    response = await chat_gpt.add_message(re_quest)
    return response, mode


#Запросы с новым контекстом, промпт переустанавливается на новый
async def handle_questions(call, prompt, current_message, pic, markup):
    new_prompt = load_prompt(prompt)
    bot_context['main'] = prompt
    with open(pic, 'rb') as photo:
        await bot.send_photo(call.message.chat.id, photo)
    response = await chat_gpt.send_question(new_prompt, current_message)
    await bot.send_message(call.message.chat.id, response, reply_markup=markup)


#Задаём промпт для контекстных задач
async def set_prompt(call, prompt, message, pic, markup):
    bot_context['main'] = prompt
    with open(pic, 'rb') as photo:
        await bot.send_photo(call.message.chat.id, photo)
    chat_gpt.set_prompt(load_prompt(prompt))
    await bot.send_message(call.message.chat.id, message, reply_markup=markup)


# Обработчик инлайн кнопок
# Создаём объект класса обработчика инлайн кнопок
callback_handler = CallBackHandler(bot)

#регистрируем функции обработчики команд с инлайн кнопок

#Главное меню

callback_handler.callback_register('/random', handle_random)

callback_handler.callback_register(
    '/talk', lambda call: asyncio.create_task(bot.send_message(
        call.message.chat.id, "Выберите шефа, с которым хотите початить:",
        reply_markup=markups['menu_talk_person_markup'])))
callback_handler.callback_register(
    '/quiz', lambda call: asyncio.create_task(set_prompt(
        call, 'quiz', "Выберите тему квиза:",
        'resources/images/quiz.jpg',
        markups['menu_quiz_pick_markup'])))
callback_handler.callback_register(
    '/recipe', lambda call: asyncio.create_task(handle_questions(
        call, 'set_recipe',
        "Представься креатором рецептов и жди набора продуктов в следующем сообщении",
        'resources/images/message.jpg',
        None)))
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
callback_handler.callback_register(
    '/biden', lambda call: bot.send_message(call.message.chat.id, "biden"))

#Квизы
callback_handler.callback_register(
    '/start', lambda call: bot.send_message(call.message.chat.id, "start"))
callback_handler.callback_register(
    '/start', lambda call: bot.send_message(call.message.chat.id, "start"))
callback_handler.callback_register(
    '/start', lambda call: bot.send_message(call.message.chat.id, "start"))
callback_handler.callback_register(
    '/start', lambda call: bot.send_message(call.message.chat.id, "start"))
callback_handler.callback_register(
    '/start', lambda call: bot.send_message(call.message.chat.id, "start"))

#Хватит
callback_handler.callback_register(
    '/start', handle_start)


@bot.callback_query_handler(func=lambda call: True)
async def inline(call):
    await callback_handler.handle_callback(call)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(content_types=['text'])
async def handle_a(message):
    re_quest = message.text
    context = bot_context['main']
    markup = None
    response, mode = await callback_handler.handle_next(call=message, re_quest=re_quest)
    await bot.send_message(message.chat.id, response)

asyncio.run(bot.polling())
