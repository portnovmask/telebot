from context import chat_gpt, bot, bot_context, score, questions
from util import load_prompt, load_message, markups

count = 'Правильных ответов: 0'


async def handle_text_message(message, markup=None):
    global count
    response = await chat_gpt.add_message(message.text)

    #  Даём очко если ответ правильный, считаем вопросы, обращаемся к функции
    #  get_score в модуле context

    if response == "Правильно!":
        count = f"Правильных ответов: {score()}"
    await bot.send_message(message.chat.id, response, reply_markup=markup)
    if bot_context['main'] == 'quiz':
        user_score = f"{count} / {questions() - 1}."  # Кол-во правильных ответов из заданных вопросов
        await bot.send_message(message.chat.id, user_score, reply_markup=markups['quiz_next'])


# Обработчик картинок и отправка GPT

async def handle_photo_message(message, markup=None):
    if bot_context['main'] == 'guess':
        # Получаем id медиа файла
        file_id = message.photo[-1].file_id  # Get the highest resolution

        # Скачиваем файл в буфер
        file_info = await bot.get_file(file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        print("file downloaded")  # Отладочное подтверждение, что файл получен

        # Сохраняем файл на сервере
        with open('guess_image.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)
        response = await chat_gpt.send_image_with_prompt(
            load_prompt('guess'), 'guess_image.jpg')
        await bot.send_message(message.chat.id, response, reply_markup=markup)
    else:
        await bot.send_message(
            message.chat.id, load_message('sent_image_for_text'),
            reply_markup=markups['on_start_markup'])
