from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.handlers.adminPanel import showAdminPanel

adminPasswords = {0: 'Вероника', 1: 'VxWorks'}
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
    await message.reply(f"Добрый день, администратор! Выберите свой аккаунт:",
                        reply_markup=keyboard)


async def tonyStark(call: types.CallbackQuery):
    global adminID
    if adminID is not None:
        return
    adminID = 0
    await Admin.admin_password.set()
    await call.message.answer("Для входа в аккаунт введите ответ на контрольный вопрос: Какое кодовое название носило "
                              "модульное дополнение к костюму железного человека, предназначенное для борьбы с Халком?")


async def grigoryKarnacevich(call: types.CallbackQuery):
    global adminID
    if adminID is not None:
        return
    adminID = 1
    await call.message.answer("Для входа в аккаунт введите ответ на контрольный вопрос: с помощью какой операционной "
                              "системы управляется марсоходом Curiosity?")


async def processPassword(message: types.Message, state: FSMContext):
    await state.finish()
    if message.text != adminPasswords[adminID]:
        await message.reply('Ответ на контрольный вопрос неверен. Попробуйте снова.')
        await Admin.adminPassword.set()
        return
    await message.reply('Вход выполнен успешно!')
    await showAdminPanel(message)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin, commands="admin")
    dp.register_callback_query_handler(tonyStark, text="Тони Старк")
    dp.register_callback_query_handler(grigoryKarnacevich, text="Григорий Карнацевич")
    dp.register_message_handler(processPassword, state=Admin.admin_password)