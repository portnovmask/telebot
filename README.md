# Телеграм-бот с интеграцией GPT и обработкой сообщений

## Описание проекта

Данный проект представляет собой Telegram-бот, который выполняет следующие функции:
- Обработка текстовых сообщений и фотографий.
- Интеграция с сервисом GPT для генерации текстов и ответов.
- Реализация многоуровневого меню с использованием callback кнопок.
- Обработка различных контекстов команд и сообщений.

## Файловая структура

- `bot.py` — основной файл, который запускает бота, регистрирует обработчики и определяет основную логику.
- `context.py` — файл, содержащий общие объекты, такие как бот, обработчик коллбэков и GPT-сервис.
- `handlers/` — модуль с обработчиками callback и текстовых сообщений.
- `util/` — вспомогательные функции для загрузки сообщений, разметок и других утилит.
- `gpt/` – OpenAI API /требуется подписка и api-key/
- `resourses/` - шаблоны промптов, сообщений, изображения

## Основные файлы

### `bot.py`
Главный файл проекта. В нем:
1. Регистрируются обработчики команд, callback кнопок и сообщений.
2. Определены функции для обработки стандартных команд `/start`, `/help`, `/stop`.
3. Вызовы функций из модуля `context.py` для доступа к глобальным объектам бота и контексту.

Пример кода регистрации обработчика:
```python
callback_handler.callback_register('/random', handle_random)
callback_handler.message_handler_register(handle_text_message, content_types=['text'])

context.py

Этот файл содержит:

Инициализацию бота с помощью API-ключа из .env.
Глобальные переменные контекста, такие как bot_context.
Экземпляр класса CallBackHandler для управления обработчиками.
Экземпляр класса библиотеки AsyncTeleBot

Пример кода:

from telebot.async_telebot import AsyncTeleBot
from util import CallBackHandler

bot = AsyncTeleBot(api_key)
callback_handler = CallBackHandler(bot)

Установка и запуск

1. Склонируйте репозиторий:

git clone https://github.com/portnovmask/telebot

2. Установите зависимости:

pip install -r requirements.txt

3. Создайте файл .env в корне проекта и добавьте API-ключи:

TELEGRAM_KEY=ваш_ключ_телеграм
GPT_KEY=ваш_ключ_gpt

4. Запустите бота:

python bot.py




Функциональность

Команды

/start — запуск бота, переход в главное меню.
/help — вывод справочной информации.
/stop — остановка текущего контекста.


Callback кнопки

Бот использует кнопки для взаимодействия с пользователем, такие как выбор квиза, работа с GPT, генерация случайных рецептов.

Пример регистрации кнопки:

callback_handler.callback_register('/quiz', handle_quiz)
Обработка сообщений
Текстовые сообщения: регистрируются обработчики для контекста пользователя.
Фотографии: бот принимает изображения и обрабатывает их.

Пример регистрации текстовых сообщений:

callback_handler.message_handler_register(handle_text_message, content_types=['text'])

Используемые технологии

Python 3.9+
aiogram / pyTelegramBotAPI — для работы с Telegram API.
OpenAI GPT API — для интеграции с GPT.
dotenv — для работы с переменными окружения.

Расширение и кастомизация

Для добавления новых команд или кнопок:

Определите новую функцию-обработчик в модуле handlers/.
Зарегистрируйте ее через callback_handler.callback_register.

Пример:

async def handle_new_feature(call, **kwargs):
    await bot.send_message(call.message.chat.id, "Эта функция еще в разработке!")

callback_handler.callback_register('/new_feature', handle_new_feature)


Лицензия

Этот проект распространяется свободно.



Этот `README.md` обеспечивает полное описание вашего проекта, включая настройку, структуру и использование.


# telebot
Java Rush Full Stack Python Course First Project 
