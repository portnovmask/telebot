from dotenv import load_dotenv
import os
from telebot.async_telebot import AsyncTeleBot
from gpt import ChatGptService
from util import markups, CallBackHandler, load_prompt
import asyncio

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


async def handle_start(call, **kwargs):
    # Проверяем команду
    if call.data == '/start':
        await bot.edit_message_reply_markup(
                                    chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    reply_markup=None,
                                    timeout=2
                                    )
        await send_welcome(call.message)


#Функции упаковки ответов от gpt:


#Хранение контекста:

bot_context = {'main': 'stop'}


#Обработчик текстов посылаемых GPT
async def handle_text_message(message, markup=None):
    response = await chat_gpt.add_message(message.text)
    await bot.send_message(message.chat.id, response, reply_markup=markup)


#Обработчик картинок посылаемых GPT
async def handle_photo_message(message, markup=None):
    # Get the file ID of the uploaded image
    file_id = message.photo[-1].file_id  # Get the highest resolution


    # Download the image
    file_info = await bot.get_file(file_id)
    print(f"file info - {file_info}")
    downloaded_file = await bot.download_file(file_info.file_path)
    print("file downloaded")
    # Save the photo locally (optional)
    with open('guess_image.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)
    response = await chat_gpt.send_image_with_prompt(load_prompt('guess'), 'guess_image.jpg')
    await bot.send_message(message.chat.id, response, reply_markup=markup)

#Случайный запрос или просто сообщение без промпта
async def handle_random(call, re_quest, pic, **kwargs):
    bot_context['main'] = 'random'
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


async def handle_talk(call, re_quest, pic, **kwargs):
    bot_context['main'] = 'talk'
    pic = 'resources/images/talk.jpg'
    re_quest = ''

    # Редактирование предыдущего сообщения
    await bot.edit_message_text('Проконсультируйтесь со знаменитым шефом или экспертом!',
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                reply_markup=None,
                                timeout=2
                                )
    with open(pic, 'rb') as photo:
        await bot.send_photo(call.message.chat.id, photo)
    await bot.send_message(call.message.chat.id, 'Ниже выберите шефа для чата\n',
                           reply_markup=markups['menu_talk'])


async def handle_gpt(call, re_quest, pic, **kwargs):
    bot_context['main'] = 'gpt'
    pic = 'resources/images/gpt.jpg'
    re_quest = 'gpt'

    # Удаляем inline-разметку из предыдущего сообщения
    await bot.edit_message_text("GPT на связи, чем могу помочь?",
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                reply_markup=None,
                                timeout=2
                                )
    with open(pic, 'rb') as photo:
        await bot.send_photo(call.message.chat.id, photo)
    response = await chat_gpt.add_message(load_prompt(re_quest))
    await bot.send_message(call.message.chat.id, response, reply_markup=markups['gpt'])


async def handle_recipe(call, re_quest, pic, **kwargs):
    bot_context['main'] = 'recipe'
    pic = 'resources/images/random.jpg'
    re_quest = 'set_recipe'

    # Удаляем inline-разметку из предыдущего сообщения
    await bot.edit_message_text("...",
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                reply_markup=None,
                                timeout=2
                                )
    with open(pic, 'rb') as photo:
        await bot.send_photo(call.message.chat.id, photo)
    chat_gpt.set_prompt(load_prompt(re_quest))
    await bot.send_message(call.message.chat.id, 'Введите от 1 до 5 продуктов через запятую.',
                           reply_markup=markups['recipe'])


async def handle_quiz(call, re_quest, pic, **kwargs):
    bot_context['main'] = 'quiz'
    pic = 'resources/images/quiz.jpg'
    re_quest = 'quiz'

    # Удаляем inline-разметку из предыдущего сообщения
    await bot.edit_message_text("Выберите тему квиза.",
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                reply_markup=None,
                                timeout=2
                                )
    with open(pic, 'rb') as photo:
        await bot.send_photo(call.message.chat.id, photo)
    chat_gpt.set_prompt(load_prompt(re_quest))
    await bot.send_message(call.message.chat.id, '',
                           reply_markup=markups['quiz'])


async def handle_guess(call, re_quest, pic, **kwargs):
    bot_context['main'] = 'guess'
    pic = 'resources/images/random.jpg'
    re_quest = 'guess'

    # Удаляем inline-разметку из предыдущего сообщения
    await bot.edit_message_text("Подготовьте фото для отправки, оно должно быть разрешением не более... и размером не более...",
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                reply_markup=None,
                                timeout=2
                                )
    await bot.send_message(call.message.chat.id, 'Прикрепите ваше фото, я постараюсь угадать блюдо:',
                           reply_markup=markups['stop'])


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

callback_handler.callback_register('/talk', handle_talk)
callback_handler.callback_register('/gpt', handle_gpt)
callback_handler.callback_register('/recipe', handle_recipe)
callback_handler.callback_register('/guess', handle_guess)
callback_handler.callback_register('/quiz', handle_quiz)

#Знаменитости
#callback_handler.callback_register('/ramzi', handle_ramzi)
#callback_handler.callback_register('/oilver', handle_oliver)

#callback_handler.callback_register('/ducas', handle_ducas)
#callback_handler.callback_register('/bocus', handle_bocus)
#callback_handler.callback_register('/blumental', handle_blumental)
#callback_handler.callback_register('/biden', handle_biden)

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

#Регистрируем обработчики текстовых и медиа сообщений

callback_handler.message_handler_register(handle_text_message, content_types=['text'])
callback_handler.message_handler_register(handle_photo_message, content_types=['photo'])



@bot.callback_query_handler(func=lambda call: True)
async def inline(call):
    await callback_handler.handle_callback(call)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def message_handler(message):
    print("Я в декораторе")
    await callback_handler.handle_message(message, markup=markups[bot_context['main']])

@bot.message_handler(func=lambda message: True, content_types=['photo'])
async def photo_handler(message):
    print("Я в фото декораторе")
    await callback_handler.handle_message(message, markup=markups[bot_context['main']])


asyncio.run(bot.polling())
