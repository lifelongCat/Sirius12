import time

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.handlers.adminPanel import showAdminPanel

adminPasswords = {0: 'вероника', 1: 'vxworks'}
adminID = None


class Admin(StatesGroup):
    admin_ID = State()
    admin_password = State()


async def admin(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Тони Старк", callback_data="Тони Старк"),
        types.InlineKeyboardButton(text="Григорий Карнацевич", callback_data="Григорий Карнацевич")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.reply(f"👩‍🔧ВХОД В РЕЖИМ АДМИНИСТРАТОРА🧑‍🔧\n"
                        f"Созданно 2 аккаунта администратора. Выберите тот, в который хотите войти ➡️",
                        reply_markup=keyboard)


async def tonyStark(call: types.CallbackQuery):
    global adminID
    adminID = 0
    await Admin.admin_password.set()
    await call.message.answer(text="Добрый день, мистер Старк!👋\n"
                                   "🗝 Для входа в аккаунт, введите ответ на контрольный вопрос:\n"
                                   "Какое кодовое название носило модульное дополнение к костюму железного человека, предназначенное для борьбы с Халком?")


async def grigoryKarnacevich(call: types.CallbackQuery):
    global adminID
    adminID = 1
    await Admin.admin_password.set()
    await call.message.answer(text="Добрый день, мистер Карнацевич! 👋\n"
                                   "🗝 Для входа в аккаунт, введите ответ на контрольный вопрос:\n"
                                   "C помошью какой операционной систему управляется марсоход Curiosity?")


async def processPassword(message: types.Message, state: FSMContext):
    if message.text.lower() != adminPasswords[adminID]:
        await message.reply('❌НЕВЕРНЫЙ ОТВЕТ НА КОНТРОЛЬНЫЙ ВОПРОС❌\n'
                            'Проверьте ответ и введите его снова ➡️')
        await Admin.adminPassword.set()
        return
    await message.reply('Вход выполнен успешно!✅')
    await state.finish()
    time.sleep(5)
    await showAdminPanel(message)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin, commands="admin")
    dp.register_callback_query_handler(tonyStark, text="Тони Старк")
    dp.register_callback_query_handler(grigoryKarnacevich, text="Григорий Карнацевич")
    dp.register_message_handler(processPassword, state=Admin.admin_password)