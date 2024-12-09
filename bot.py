from context import bot, bot_context, callback_handler
from util import load_message, markups
from handlers.callbacks import (handle_quiz_more,
                                handle_celeb, handle_gpt, handle_guess,
                                handle_quiz, handle_quiz_choices,
                                handle_random, handle_random_more,
                                handle_recipe, handle_talk,
                                handle_talk_more)
from handlers.message_handlers import handle_photo_message, handle_text_message
import asyncio


# Обработчик базовых слэш комманд

@bot.message_handler(commands=['help', 'start', 'stop'])
async def send_welcome(message):
    bot_context['main'] = 'stop'
    text = load_message('main')
    await bot.send_message(
        message.chat.id, text, reply_markup=markups['on_start_markup'])


# Возврат в главное меню с инлайн кнопок "Отмена", "Выход" или "Закончить"

async def handle_start(call, **kwargs):
    # Проверяем команду
    if call.data == '/start' and bot_context['main'] != 'stop':
        bot_context['main'] = 'stop'
        await bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None,
            timeout=2
        )
        await send_welcome(call.message)


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
    print(f"Сработала кнопка: {call.data}, "
          f"контекст: {context}")  # Отладочное - отслеживание контекста и callback
    await callback_handler.handle_callback(call)


# Ловим текстовые сообщения от пользователя
@bot.message_handler(func=lambda message: True)
async def message_handler(message):
    if (bot_context['main'] != 'guess'
            and bot_context['main'] != 'stop'
            and bot_context['main'] != 'random'
            and bot_context['main'] != 'quiz_more'):
        await callback_handler.handle_message(message, markup=markups[bot_context['main']])
    else:
        await bot.send_message(
            message.chat.id,
            load_message('sent_text_for_image'),
            reply_markup=markups['stop'])


# Ловим фотографии от пользователя
@bot.message_handler(func=lambda message: True, content_types=['photo'])
async def photo_handler(message):
    await callback_handler.handle_message(message, markup=markups[bot_context['main']])


asyncio.run(bot.polling())
