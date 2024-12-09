from dotenv import load_dotenv
import os
from telebot.async_telebot import AsyncTeleBot
from gpt import ChatGptService
from util import markups, CallBackHandler, load_prompt, load_message
import asyncio

# Загрузка переменных сетевого окружения

load_dotenv()

# Секреты

api_key = os.getenv("TELEGRAM_KEY")
secret_key = os.getenv("GPT_KEY")
bot = AsyncTeleBot(api_key)
chat_gpt = ChatGptService(secret_key)

# Хранение контекста:

bot_context = {'main': 'stop'}


# Обработчик базовых слэш комманд

@bot.message_handler(commands=['help', 'start', 'stop'])
async def send_welcome(message):
    bot_context['main'] = 'stop'
    text = f"""Привет, это бот о кулинарии на базе chatGPT!
Выбирай из меню ниже, чтобы продолжить:"""
    await bot.send_message(
        message.chat.id, text, reply_markup=markups['on_start_markup'])
    print(message.text)


# Возврат в главное меню с кнопок "Отмена" или "Закончить"
async def handle_start(call, **kwargs):
    # Проверяем команду
    if call.data == '/start' and bot_context['main'] != 'stop':
        bot_context['main'] = 'stop'
        await bot.edit_message_text('Возврат в главное меню',
                                    chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    reply_markup=None,
                                    timeout=2
                                    )
        await send_welcome(call.message)


# Функции упаковки вопросов/ответов к/от gpt:

# Обработчик текстов и отправка GPT
async def handle_text_message(message, markup=None):
    response = await chat_gpt.add_message(message.text)
    await bot.send_message(message.chat.id, response, reply_markup=markup)


# Обработчик картинок и отправка GPT
async def handle_photo_message(message, markup=None):
    if bot_context['main'] == 'guess':
        # Получаем id медиа файла
        file_id = message.photo[-1].file_id  # Get the highest resolution

        # Скачиваем файл в буфер
        file_info = await bot.get_file(file_id)
        print(f"file info - {file_info}")
        downloaded_file = await bot.download_file(file_info.file_path)
        print("file downloaded")

        # Сохраняем файл на сервере
        with open('guess_image.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)
        response = await chat_gpt.send_image_with_prompt(load_prompt('guess'), 'guess_image.jpg')
        await bot.send_message(message.chat.id, response, reply_markup=markup)
    else:
        await bot.send_message(
            message.chat.id, 'Для обработки изображенний выберите *Рецепт по фото* в меню ниже:',
            reply_markup=markups['on_start_markup'])


# Функции обработки кнопок главного меню

# Обработчик случайный факт
async def handle_random(call, re_quest, pic, **kwargs):
    bot_context['main'] = 'random'
    pic = 'resources/images/random.jpg'
    re_quest = 'random'

    # Удаляем inline-разметку из предыдущего сообщения

    await bot.edit_message_text("...Ищу интересный кулинарный факт...",
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


# Обработчик кнопки "Еще случайный факт"
async def handle_random_more(call, re_quest, **kwargs):
    if bot_context['main'] == 'random':
        re_quest = 'random'
        # Удаляем inline-разметку из предыдущего сообщения

        await bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None,
            timeout=2
        )

        response = await chat_gpt.add_message(load_prompt(re_quest))
        await bot.send_message(call.message.chat.id, response,
                               reply_markup=markups['random'])
    else:
        await send_welcome(call.message)


# Обработчик разговора со знаменитостью, отправляет кнопки выбора знаменитостей
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
    await bot.send_message(call.message.chat.id, 'Ниже выберите шефа для чата\n\n',
                           reply_markup=markups['menu_talk'])


# Обработчик кнопки смены знаменитости в контексте
async def handle_talk_more(call, re_quest, **kwargs):
    if bot_context['main'] == 'talk':
        re_quest = ''

        # Удаляем inline-разметку из предыдущего сообщения

        await bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None,
            timeout=2
        )

        await bot.send_message(call.message.chat.id, 'Ниже выберите шефа для чата\n\n',
                               reply_markup=markups['menu_talk'])
    else:
        await send_welcome(call.message)


# Обработчик чата с GPT напрямую, роль ассистент
async def handle_gpt(call, re_quest, pic, **kwargs):
    bot_context['main'] = 'gpt'
    pic = 'resources/images/gpt.jpg'
    re_quest = 'gpt'

    # Удаляем inline-разметку из предыдущего сообщения

    await bot.edit_message_text("Связываемся со свободным GPT ассистентом...\n\n",
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                reply_markup=None,
                                timeout=4
                                )
    with open(pic, 'rb') as photo:
        await bot.send_photo(call.message.chat.id, photo)
    response = await chat_gpt.send_question(load_prompt(re_quest), 'Представься и предложи помощь')
    await bot.send_message(call.message.chat.id, response, reply_markup=markups['gpt'])


# Обработчик составления рецепта из набора продуктов, задаёт роль и ожидает ввод продуктов
async def handle_recipe(call, re_quest, pic, **kwargs):
    bot_context['main'] = 'recipe'
    pic = 'resources/images/random.jpg'
    re_quest = 'set_recipe'

    # Удаляем inline-разметку из предыдущего сообщения

    await bot.edit_message_text("GPT составит рецепт из предложенных ингредиентов.",
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


# Обработчик квиза, задаёт роль и правила, отправляет кнопки выбора темы квиза
async def handle_quiz(call, re_quest, pic, **kwargs):
    bot_context['main'] = 'quiz'
    pic = 'resources/images/quiz.jpg'
    re_quest = 'quiz'

    # Удаляем inline-разметку из предыдущего сообщения

    await bot.edit_message_text("Готовы  проверить ваши знания о кулинарии?",
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                reply_markup=None,
                                timeout=2
                                )
    with open(pic, 'rb') as photo:
        await bot.send_photo(call.message.chat.id, photo)
    chat_gpt.set_prompt(load_prompt(re_quest))
    await bot.send_message(call.message.chat.id, 'Выберите тему ниже:\n\n',
                           reply_markup=markups['quiz_pick'])


# При нажатии кнопки смены темы квиза в контексте
async def handle_quiz_more(call, re_quest, **kwargs):
    if bot_context['main'] == 'quiz':
        re_quest = ''

        # Удаляем inline-разметку из предыдущего сообщения

        await bot.edit_message_text("Меняем тему квиза...",
                                    chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    reply_markup=None,
                                    timeout=2
                                    )
        await bot.send_message(call.message.chat.id, 'Выберите тему ниже:\n\n',
                               reply_markup=markups['quiz_pick'])
    else:
        await send_welcome(call.message)


# Угадываем картинку
async def handle_guess(call, re_quest, pic, **kwargs):
    bot_context['main'] = 'guess'
    pic = 'resources/images/random.jpg'
    re_quest = 'guess'

    # Удаляем inline-разметку из предыдущего сообщения

    await bot.edit_message_text("Опытный повар угадает блюдо по картинке.",
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                reply_markup=None,
                                timeout=4
                                )
    await bot.send_message(call.message.chat.id, load_message('guess_intro'),
                           reply_markup=markups['guess'])


# Выбор знаменитости

async def handle_celeb(call, re_quest, pic, **kwargs):
    if bot_context['main'] == 'talk':
        # '/ramzi'
        # '/olver'
        # '/ducas'
        # '/bocus'
        # '/blumental'
        # '/biden'
        pic = 'resources/images/talk.jpg'
        re_quest = 'menu_talk'
        match call.data:
            case '/ramzi':
                case_string = 'ramzi'
                pic = f'resources/images/{case_string}.png'
                re_quest = case_string
            case '/oliver':
                case_string = 'oliver'
                pic = f'resources/images/{case_string}.png'
                re_quest = case_string
            case '/ducas':
                case_string = 'ducas'
                pic = f'resources/images/{case_string}.png'
                re_quest = case_string
            case '/bocus':
                case_string = 'bocus'
                pic = f'resources/images/{case_string}.png'
                re_quest = case_string
            case '/blumental':
                case_string = 'blumental'
                pic = f'resources/images/{case_string}.png'
                re_quest = case_string
            case '/biden':
                case_string = 'biden'
                pic = f'resources/images/{case_string}.png'
                re_quest = case_string
            case _:
                case_string = '/stop'
                pic = f'resources/images/bye.jpg'
                re_quest = case_string
        prompt = load_prompt(re_quest)
        # Удаляем inline-разметку из предыдущего сообщения

        await bot.edit_message_text("Вы выбрали знаменитость, пытаюсь с ним связаться...",
                                    chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    reply_markup=None,
                                    timeout=4
                                    )
        with open(pic, 'rb') as photo:
            await bot.send_photo(call.message.chat.id, photo)
        response = await chat_gpt.send_question(prompt, "Представься, пожалуйста.")
        await bot.send_message(call.message.chat.id, response,
                               reply_markup=markups['talk'])


# Выбор темы квиза
async def handle_quiz_choices(call, re_quest, pic, **kwargs):
    if bot_context['main'] == 'quiz':
        # 'История кулинарии': {'callback_data': 'quiz_history'},
        # 'Угадай ингридиент': {'callback_data': 'quiz_ingredient'},
        # 'Бабушкины хитрости': {'callback_data': 'quiz_how'},
        # 'Диеты': {'callback_data': 'quiz_diets'},
        # 'Еще вопрос': {'callback_data': 'quiz_more'},
        pic = 'resources/images/quiz.jpg'
        re_quest = 'quiz_pick'
        match call.data:
            case 'quiz_history':
                case_string = 'Тема: История кулинарии'
                re_quest = 'quiz_history'
            case 'quiz_ingredient':
                case_string = 'Тема: Угадай ингридиент'
                re_quest = 'quiz_ingredient'
            case 'quiz_how':
                case_string = 'Тема: Бабушкины кулинарные хитрости'
                re_quest = 'quiz_how'
            case 'quiz_diets':
                case_string = 'Тема: Диеты'
                re_quest = 'quiz_diets'
            case 'quiz_more':
                case_string = 'Еще вопрос'
                re_quest = 'quiz_more'
            case _:
                case_string = 'Закончить с квизами'
                pic = f'resources/images/bye.jpg'
                re_quest = '/stop'

        # Удаляем inline-разметку из предыдущего сообщения

        await bot.edit_message_text(case_string,
                                    chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    reply_markup=None,
                                    timeout=4
                                    )
        if re_quest != '/stop':
            response = await chat_gpt.add_message(re_quest)
            await bot.send_message(call.message.chat.id, response,
                                   reply_markup=markups['quiz_more'])


# Обработчики инлайн кнопок и сообщений

# Создаём объект класса обработчиков инлайн кнопок и сообщений
callback_handler = CallBackHandler(bot)

# Регистрируем функции обработчики команд с кнопок и из сообщений

# Главное меню кнопки

callback_handler.callback_register('/random', handle_random)
callback_handler.callback_register('/random_more', handle_random_more)
callback_handler.callback_register('/talk', handle_talk)
callback_handler.callback_register('/talk_more', handle_talk_more)
callback_handler.callback_register('/gpt', handle_gpt)
callback_handler.callback_register('/recipe', handle_recipe)
callback_handler.callback_register('/guess', handle_guess)
callback_handler.callback_register('/quiz', handle_quiz)
callback_handler.callback_register('/quiz_pick', handle_quiz_more)

# Знаменитости кнопки

callback_handler.callback_register('/ramzi', handle_celeb)
callback_handler.callback_register('/oliver', handle_celeb)
callback_handler.callback_register('/ducas', handle_celeb)
callback_handler.callback_register('/bocus', handle_celeb)
callback_handler.callback_register('/blumental', handle_celeb)
callback_handler.callback_register('/biden', handle_celeb)

# Квизы кнопки
callback_handler.callback_register('quiz_history', handle_quiz_choices)
callback_handler.callback_register('quiz_ingredient', handle_quiz_choices)
callback_handler.callback_register('quiz_how', handle_quiz_choices)
callback_handler.callback_register('quiz_diets', handle_quiz_choices)
callback_handler.callback_register('quiz_more', handle_quiz_choices)

# Одна кнопка Хватит, Законить или отмена
callback_handler.callback_register(
    '/start', handle_start)

# Регистрируем обработчики текстовых и медиа сообщений

callback_handler.message_handler_register(handle_text_message, content_types=['text'])
callback_handler.message_handler_register(handle_photo_message, content_types=['photo'])


# Ловим сигналы с кнопок от пользователя
@bot.callback_query_handler(func=lambda call: True)
async def inline(call):
    context = bot_context['main']
    print(f"Сработала кнопка: {call.data}, контекст: {context}")
    await callback_handler.handle_callback(call)


# Ловим текстовые сообщения от пользователя
@bot.message_handler(func=lambda message: True)
async def message_handler(message):
    print("Я в декораторе")
    if bot_context['main'] != 'guess' and bot_context['main'] != 'stop' and bot_context['main'] != 'random':
        await callback_handler.handle_message(message, markup=markups[bot_context['main']])
    else:
        await bot.send_message(
            message.chat.id,
            'В данном режиме GPT не принимает текстовые сообщения, выберите подходящий режим в меню выше',
            reply_markup=markups['stop'])


# Ловим фотографии от пользователя
@bot.message_handler(func=lambda message: True, content_types=['photo'])
async def photo_handler(message):
    print("Я в фото декораторе")
    await callback_handler.handle_message(message, markup=markups[bot_context['main']])


asyncio.run(bot.polling())
