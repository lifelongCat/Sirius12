#!venv/bin/python
import logging
from aiogram import Bot, Dispatcher, executor, types
import random
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# Объект бота
bot = Bot(token="5763817832:AAHryUF70705YJcIOraaYVh1njprvtS752Y")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
adminPasswords = {0: 'Вероника', 1: 'VxWorks'}
adminID = 0
isLogin = False


class Form(StatesGroup):
    adminPassword = State()


# Хэндлер на команду /start
@dp.message_handler(commands="start")
async def start(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Статус", callback_data="Статус"),
        types.InlineKeyboardButton(text="Сброс груза", callback_data="Сброс груза")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.reply(f"{message.from_user.first_name}, добро пожаловать на борт Sirius 12! Выберите действие:",
                        reply_markup=keyboard)


# Колбэк на кнопку "Статус"
@dp.callback_query_handler(text="Статус")
async def _(call: types.CallbackQuery):
    # ОТФОРМАТИРОВАТЬ ПО PEP8
    await call.message.answer(f"""
Высота полета орбитальной станции: 25345 км;
Скорость станции: {random.randint(6000, 12000)} м/с;
Масса груза: 2308 кг;
Температура вокруг: +3 градуса по цельсию
    """)


# Колбэк на кнопку "Сброс груза"
@dp.callback_query_handler(text="Сброс груза")
async def _(call: types.CallbackQuery):
    await call.message.answer("Отправка груза заблокирована. Для выполнения этого действия необходимы права администратора.")


# Хэндлер на команду /admin
@dp.message_handler(commands="admin")
async def admin(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Тони Старк", callback_data="Тони Старк"),
        types.InlineKeyboardButton(text="Григорий Карнацевич", callback_data="Григорий Карнацевич")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.reply(f"Добрый день, администратор! Выберите свой аккаунт:",
                        reply_markup=keyboard)


# Колбэк на кнопку "Статус"
@dp.callback_query_handler(text="Тони Старк")
async def _(call: types.CallbackQuery):
    if Form.adminPassword is None:
        return
    global adminID
    adminID = 0
    await Form.adminPassword.set()
    await call.message.answer("Для входа в аккаунт введите ответ на контрольный вопрос: Какое кодовое название носило "
                              "модульное дополнение к костюму железного человека, предназначенное для борьбы с Халком?")


# Колбэк на кнопку "Сброс груза"
@dp.callback_query_handler(text="Григорий Карнацевич")
async def _(call: types.CallbackQuery):
    if Form.adminPassword is None:
        return
    global adminID
    adminID = 1
    await call.message.answer("Для входа в аккаунт введите ответ на контрольный вопрос: с помощью какой операционной "
                              "системы управляется марсоходом Curiosity?")


@dp.message_handler(state=Form.adminPassword)
async def processPassword(message: types.Message, state: FSMContext):
    await state.finish()
    if message.text != adminPasswords[adminID]:
        await message.reply('Ответ на контрольный вопрос неверен. Попробуйте снова.')
        await Form.adminPassword.set()
        return
    global isLogin
    isLogin = True
    await message.reply('Вход выполнен успешно!')


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)