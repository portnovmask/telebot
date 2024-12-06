#import aiohttp
#import asyncio
#from telebot.async_telebot import AsyncTeleBot
from telebot.util import quick_markup


class CallBackHandler:  #Класс для обработки инлайн кнопок и регистрации функций
    def __init__(self, bot):
        self.bot = bot
        self.callbacks = {}
        self.last_state = None
        self.last_args = {}
        self.message_handlers = []

    #Регистрация обработчиков кнопок
    def callback_register(self, command, func):
        self.callbacks[command] = func

    def message_handler_register(self, func, content_types=None):
        self.message_handlers.append({"func": func, "content_types": content_types or ['text']})

    #Вызов обработчика для конкретной кнопки
    async def handle_callback(self, call, markup=None, **kwargs):
        command = call.data
        if command in self.callbacks:

            func = self.callbacks[command]
            self.last_state = func
            self.last_args = {
                "call": call,
                "prompt": kwargs.get("prompt", None),
                "re_quest": kwargs.get("current_message", None),
                "pic": kwargs.get("pic", None),
                "markup": markup,
            }
            try:
                await func(**self.last_args)
            except Exception as e:
                await self.bot.send_message(call.message.chat.id,
                                            f"Ошибка обработки команды {command}: {e}"
                                            )
        else:
            await self.bot.send_message(
                call.message.chat.id,
                "Незарегистрированная команда")

    async def handle_message(self, message, markup, **kwargs):
        for handler in self.message_handlers:
            content_types = self.message_handlers['content_types']
            if message.content_type in content_types:
                try:
                    await handler["func"](message, markup=markup, **kwargs)
                except Exception as e:
                    await self.bot.send_message(
                        message.chat.id,
                        f"Ошибка обработки сообщения: {e}"
                    )
                break


async def handle_next(self, call, **kwargs):
    if not self.last_state:
        return await self.handle_callback(call, **kwargs)

    self.last_args.update(kwargs)
    try:
        await self.last_state(**self.last_args)
    except Exception as e:
        call = self.last_args.get("call")
        if call:
            await self.bot.send_message(
                call.message.chat.id,
                f"Ошибка при повторном вызове: {e}"
            )


#Наборы кнопок
#Стартовое меню
markups = {}
markups['on_start_markup'] = quick_markup({
    'Интересный факт': {'callback_data': '/random'},
    'Спросить у эксперта': {'callback_data': '/talk'},
    'Кулинарный квиз': {'callback_data': '/quiz'},
    'Рецепт по фото': {'callback_data': '/guess'},
    'Спросить chatGPT': {'callback_data': '/gpt'},
    'Приготовить': {'callback_data': '/recipe'}
}, row_width=2)

#Случайный факт
markups['random'] = quick_markup({
    'Хочу еще факт': {'callback_data': '/random'},
    'Закончить': {'callback_data': '/start'},
}, row_width=2)

#Завершение квиза
markups['quiz'] = quick_markup({
    'Новый квиз': {'callback_data': '/quiz'},
    'Закончить': {'callback_data': '/start'},
}, row_width=2)

#Выбор квиза
markups['menu_quiz_pick_markup'] = quick_markup({
    'История кулинарии': {'callback_data': '/history'},
    'Угадай ингридиент': {'callback_data': '/ingredient'},
    'Бабушкины хитрости': {'callback_data': '/how'},
    'Диеты': {'callback_data': '/diets'},
}, row_width=2)

#Следующий вопрос квиза
markups['quiz_next'] = quick_markup({
    'Следующий вопрос': {'callback_data': '/next'},
    'Пропустить вопрос': {'callback_data': '/pass'},
}, row_width=2)

#Завершение gpt диалога
markups['gpt'] = quick_markup({
    'Начать новый чат': {'callback_data': '/gpt'},
    'Закончить': {'callback_data': '/start'},
}, row_width=2)

#Завершение общения со знаменитостью
markups['talk'] = quick_markup({
    'Другая знаменитость': {'callback_data': '/talk'},
    'Закончить': {'callback_data': '/start'},
}, row_width=2)

#Выбор знаменитости
markups['menu_talk_person_markup'] = quick_markup({
    'Хестон Блюменталь': {'callback_data': '/blumental'},
    'Алан Дюкас': {'callback_data': '/ducas'},
    'Поль Бокюз': {'callback_data': '/bocus'},
    'Гордон Рамзи': {'callback_data': '/ramzi'},
    'Джейми Оливер': {'callback_data': '/oliver'},
    'Джо Байден': {'callback_data': '/biden'},
}, row_width=2)

#Завершение составления рецептов
markups['recipe'] = quick_markup({
    'Новый рецепт': {'callback_data': '/recipe'},
    'Закончить': {'callback_data': '/start'},
}, row_width=2)

#Завершения угадывания картинки
markups['guess'] = quick_markup({
    'Еще картинка': {'callback_data': '/guess'},
    'Не угадал!': {'callback_data': '/edit_guess'},
    'Закончить': {'callback_data': '/start'},
}, row_width=2)

markups['stop'] = quick_markup({
    'Закончить': {'callback_data': '/start'},
}, row_width=1)


#Набор вспомогательных функций:

# загружает сообщение из папки  /resources/messages/
def load_message(name):
    with open("resources/messages/" + name + ".txt", "r",
              encoding="utf8") as file:
        return file.read()


# загружает промпт из папки  /resources/messages/
def load_prompt(name):
    with open("resources/prompts/" + name + ".txt", "r",
              encoding="utf8") as file:
        return file.read()


class Dialog:
    pass
