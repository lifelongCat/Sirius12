import random
from aiogram import Dispatcher, types


async def start(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Статус", callback_data="Статус"),
        types.InlineKeyboardButton(text="Сброс груза", callback_data="Сброс груза")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.reply(f"{message.from_user.first_name}, добро пожаловать на борт Sirius 12! Выберите действие:",
                        reply_markup=keyboard)


async def status(call: types.CallbackQuery):
    # ОТФОРМАТИРОВАТЬ ПО PEP8
    await call.message.answer(f"""
Высота полета орбитальной станции: 25345 км;
Скорость станции: {random.randint(6000, 12000)} м/с;
Масса груза: 2308 кг;
Температура вокруг: +3 градуса по цельсию
    """)


async def cargoDumping(call: types.CallbackQuery):
    await call.message.answer(
        "Отправка груза заблокирована. Для выполнения этого действия необходимы права администратора")


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start, commands="start")
    dp.register_callback_query_handler(status, text="Статус")
    dp.register_callback_query_handler(cargoDumping, text="Сброс груза")