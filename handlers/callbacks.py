from context import callback_handler, chat_gpt, bot, bot_context, questions
from util import markups, load_prompt, load_message


# Функции обработки callback кнопок главного меню

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
        await bot.send_message(
            call.message.chat.id, load_message('wrong'),
            reply_markup=markups['on_start_markup'])


# Обработчик разговора со знаменитостью, отправляет кнопки выбора знаменитостей
async def handle_talk(call, re_quest, pic, **kwargs):
    bot_context['main'] = 'talk'
    pic = 'resources/images/talk.jpg'
    re_quest = ''

    # Редактирование предыдущего сообщения

    await bot.edit_message_text(load_message('celeb_intro'),
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                reply_markup=None,
                                timeout=2
                                )
    with open(pic, 'rb') as photo:
        await bot.send_photo(call.message.chat.id, photo)
    await bot.send_message(call.message.chat.id, load_message('talk'),
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

        await bot.send_message(call.message.chat.id, 'Ниже выберите шефа для чата',
                               reply_markup=markups['menu_talk'])
    else:
        await bot.send_message(
            call.message.chat.id, load_message('wrong2'),
            reply_markup=markups['on_start_markup'])


# кнопки выбора знаменитости
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
        name = ''
        match call.data:
            case '/ramzi':
                case_string = 'ramzi'
                pic = f'resources/images/{case_string}.png'
                re_quest = case_string
                name = 'Гордон Рамзи'
            case '/oliver':
                case_string = 'oliver'
                pic = f'resources/images/{case_string}.png'
                re_quest = case_string
                name = 'Джейми Оливер'
            case '/ducas':
                case_string = 'ducas'
                pic = f'resources/images/{case_string}.png'
                re_quest = case_string
                name = 'Ален Дюкасс'
            case '/bocus':
                case_string = 'bocus'
                pic = f'resources/images/{case_string}.png'
                re_quest = case_string
                name = 'Поль Бокюз'
            case '/blumental':
                case_string = 'blumental'
                pic = f'resources/images/{case_string}.png'
                re_quest = case_string
                name = 'Хестон Блюменталь'
            case '/biden':
                case_string = 'biden'
                pic = f'resources/images/{case_string}.png'
                re_quest = case_string
                name = 'Джо Байден'
            case _:
                case_string = '/stop'
                pic = f'resources/images/bye.jpg'
                re_quest = case_string
        prompt = load_prompt(re_quest)
        # Удаляем inline-разметку из предыдущего сообщения
        text = f"С вами будет говорить {name}, пытаюсь с ним связаться..."
        await bot.edit_message_text(text,
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
    else:
        await bot.send_message(
            call.message.chat.id, load_message('wrong4'),
            reply_markup=markups['on_start_markup'])


# Обработчик чата с GPT напрямую, роль ассистент
async def handle_gpt(call, re_quest, pic, **kwargs):
    bot_context['main'] = 'gpt'
    pic = 'resources/images/gpt.jpg'
    re_quest = 'gpt'

    # Удаляем inline-разметку из предыдущего сообщения

    await bot.edit_message_text("Связываемся со свободным GPT ассистентом...",
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
    pic = 'resources/images/recipe.png'
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
    questions()   # добавляем порядковый номер вопроса

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
    await bot.send_message(call.message.chat.id, 'Выберите тему квиза:',
                           reply_markup=markups['quiz_pick'])


# При нажатии кнопки смены темы квиза в контексте
async def handle_quiz_more(call, re_quest, **kwargs):
    if bot_context['main'] == 'quiz':
        re_quest = ''

        # Удаляем inline-разметку из предыдущего сообщения

        await bot.edit_message_text("***Меняем тему квиза***",
                                    chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    reply_markup=None,
                                    timeout=2
                                    )
        await bot.send_message(call.message.chat.id, 'Выберите квиз:\n\n',
                               reply_markup=markups['quiz_pick'])
    else:
        await bot.send_message(
            call.message.chat.id, load_message('wrong3'),
            reply_markup=markups['on_start_markup'])


# Кнопки выбора темы квиза
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
    else:
        await bot.send_message(
            call.message.chat.id, load_message('wrong5'),
            reply_markup=markups['on_start_markup'])


# Угадываем картинку, меняем контекст на подходящий для приема изображений
async def handle_guess(call, re_quest, pic, **kwargs):
    bot_context['main'] = 'guess'
    pic = 'resources/images/guess.png'
    re_quest = 'guess'

    # Удаляем inline-разметку из предыдущего сообщения

    await bot.edit_message_text("Опытный повар угадает блюдо по картинке.",
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                reply_markup=None,
                                timeout=4
                                )
    with open(pic, 'rb') as photo:
        await bot.send_photo(call.message.chat.id, photo)
    await bot.send_message(call.message.chat.id, load_message('guess_intro'),
                           reply_markup=markups['guess'])


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

