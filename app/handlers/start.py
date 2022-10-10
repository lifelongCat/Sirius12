import datetime
import random
from aiogram import Dispatcher, types


async def start(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Статус", callback_data="Статус"),
        types.InlineKeyboardButton(text="Сброс груза", callback_data="Сброс груза")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.reply(f"Добро пожаловать в панель контроля за орбитальной станцией Sirius 12!🚀🛰\n\n"
                        f"Вы находитесь в режиме клиента 🧑‍🚀\n"
                        f"Здесь вы можете узнать текущий статус станции или заказать сброс своего груза📦📦📦",
                        reply_markup=keyboard)


async def status(call: types.CallbackQuery):
    # ОТФОРМАТИРОВАТЬ ПО PEP8
    time = datetime.datetime.now()
    await call.message.answer(text=f"Показатели станции на {time.year}/{time.month}/{time.day} {time.hour}:{time.minute} 🧭⏱🔋\n"
                                   f"🚀 Высота: {random.randint(20000, 30000)} километров н.у.м.\n"
                                   f"🎛 Скорость: {random.randint(6000, 12000)} м/с\n"
                                   f"📦 Масса груза: 4697 килогрмма\n"
                                   f"📡 Температура вокруг: +4°C")

async def cargoDumping(call: types.CallbackQuery):
    await call.message.answer(
        "❌Отправка груза заблокирована❌\n"
        "Для выполнения этого действия необходимы права администратора 🧑‍🔧")


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start, commands="start")
    dp.register_callback_query_handler(status, text="Статус")
    dp.register_callback_query_handler(cargoDumping, text="Сброс груза")