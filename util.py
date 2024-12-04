#import aiohttp
#import asyncio
#from telebot.async_telebot import AsyncTeleBot
from telebot.util import quick_markup


class CallBackHandler:  #Класс для обработки инлайн кнопок и регистрации функций
    def __init__(self, bot):
        self.bot = bot
        self.callbacks = {}

    #Регистрация обработчиков кнопок
    def callback_register(self, command, func):
        self.callbacks[command] = func

    #Вызов обработчика для конкретной кнопки
    async def handle_callback(self, call):
        if call.data in self.callbacks:
            try:
                await self.callbacks[call.data](call)
            except Exception as e:
                await self.bot.send_message(
                    call.message.chat.id,
                    f"Ошибка обработки команды {call.data}: {e}")
        else:
            await self.bot.send_message(
                call.message.chat.id,
                "Незарегистрированная команда")


#Наборы кнопок
#Стартовое меню
on_start_markup = quick_markup({
    'Интересный факт': {'callback_data': '/random'},
    'Спросить у эксперта': {'callback_data': '/talk'},
    'Кулинарный квиз': {'callback_data': '/quiz'},
    'Рецепт по фото': {'callback_data': '/guess'},
    'Спросить chatGPT': {'callback_data': '/gpt'},
    'Приготовить': {'callback_data': '/recipe'}
}, row_width=2)

#Случайный факт
menu_random_end_markup = quick_markup({
    'Хочу еще факт': {'callback_data': '/random'},
    'Закончить': {'callback_data': '/start'},
}, row_width=2)

#Завершение квиза
menu_quiz_end_markup = quick_markup({
    'Новый квиз': {'callback_data': '/quiz'},
    'Закончить': {'callback_data': '/start'},
}, row_width=2)

#Выбор квиза
menu_quiz_pick_markup = quick_markup({
    'История кулинарии': {'callback_data': '/history'},
    'Угадай ингридиент': {'callback_data': '/ingredient'},
    'Бабушкины хитрости': {'callback_data': '/how'},
    'Диеты': {'callback_data': '/diets'},
}, row_width=2)

#Следующий вопрос квиза
menu_quiz_next_markup = quick_markup({
    'Следующий вопрос': {'callback_data': '/next'},
    'Пропустить вопрос': {'callback_data': '/pass'},
}, row_width=2)

#Завершение gpt диалога
menu_gpt_end_markup = quick_markup({
    'Начать новый чат': {'callback_data': '/gpt'},
    'Закончить': {'callback_data': '/start'},
}, row_width=2)

#Завершение общения со знаменитостью
menu_talk_end_markup = quick_markup({
    'Другая знаменитость': {'callback_data': '/talk'},
    'Закончить': {'callback_data': '/start'},
}, row_width=2)


menu_talk_person_markup = quick_markup({
    'Блюменталь': {'callback_data': '/blumental'},
    'Байден': {'callback_data': '/biden'},
}, row_width=2)


menu_recipe_end_markup = quick_markup({
    'Новый рецепт': {'callback_data': '/recipe'},
    'Закончить': {'callback_data': '/start'},
}, row_width=2)


menu_guess_end_markup = quick_markup({
    'Еще картинка': {'callback_data': '/guess'},
    'Не угадал!': {'callback_data': '/edit_guess'},
    'Закончить': {'callback_data': '/start'},
}, row_width=2)

#Набор вспомогательных функций:

#
# конвертирует объект user в строку
def dialog_user_info_to_str(user_data) -> str:
    mapper = {'language_from': 'Язык оригинала', 'language_to': 'Язык перевода',
              'text_to_translate': 'Текст для перевода'}
    return '\n'.join(map(lambda k, v: (mapper[k], v), user_data.items()))


# посылает в чат текстовое сообщение
#async def send_text(update: Update, context: ContextTypes.DEFAULT_TYPE,
#                 text: str) -> Message:
# if text.count('_') % 2 != 0:
#     message = f"Строка '{text}' является невалидной с точки зрения markdown. Воспользуйтесь методом send_html()"
#     print(message)
#     return await update.message.reply_text(message)
#
# text = text.encode('utf16', errors='surrogatepass').decode('utf16')
# return await context.bot.send_message(chat_id=update.effective_chat.id,
#                                       text=text,
#                                       parse_mode=ParseMode.MARKDOWN)


# посылает в чат html сообщение
# async def send_html(update: Update, context: ContextTypes.DEFAULT_TYPE,
#                     text: str) -> Message:
#     text = text.encode('utf16', errors='surrogatepass').decode('utf16')
#     return await context.bot.send_message(chat_id=update.effective_chat.id,
#                                           text=text, parse_mode=ParseMode.HTML)
#

# посылает в чат текстовое сообщение, и добавляет к нему кнопки
# async def send_text_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE,
#                             text: str, buttons: dict) -> Message:
#     text = text.encode('utf16', errors='surrogatepass').decode('utf16')
#     keyboard = []
#     for key, value in buttons.items():
#         button = InlineKeyboardButton(str(value), callback_data=str(key))
#         keyboard.append([button])
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     return await context.bot.send_message(
#         update.effective_message.chat_id,
#         text=text, reply_markup=reply_markup,
#         message_thread_id=update.effective_message.message_thread_id)
#

# посылает в чат фото
# async def send_image(update: Update, context: ContextTypes.DEFAULT_TYPE,
#                      name: str) -> Message:
#     with open(f'resources/images/{name}.jpg', 'rb') as image:
#         return await context.bot.send_photo(chat_id=update.effective_chat.id,
#                                             photo=image)
#

# отображает команду и главное меню
# async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE,
#                          commands: dict):
#     command_list = [BotCommand(key, value) for key, value in commands.items()]
#     await context.bot.set_my_commands(command_list, scope=BotCommandScopeChat(
#         chat_id=update.effective_chat.id))
#     await context.bot.set_chat_menu_button(menu_button=MenuButtonCommands(),
#                                            chat_id=update.effective_chat.id)
#

# Удаляем команды для конкретного чата
# async def hide_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.delete_my_commands(
#         scope=BotCommandScopeChat(chat_id=update.effective_chat.id))
#     await context.bot.set_chat_menu_button(menu_button=MenuButtonDefault(),
#                                            chat_id=update.effective_chat.id)
#

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


# async def default_callback_handler(update: Update,
#                                    context: ContextTypes.DEFAULT_TYPE):
#     await update.callback_query.answer()
#     query = update.callback_query.data
#     await send_html(update, context, f'You have pressed button with {query} callback')


class Dialog:
    pass
