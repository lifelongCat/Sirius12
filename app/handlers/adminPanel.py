import asyncio

from aiogram import Dispatcher, types
from aiogram.types import InputFile
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

acceptedCargos = 0
cargoNumbers = [72121022, 12102006, 78151290, 55005321]


class Answers(StatesGroup):
    flyControl = State()
    updateSoftware = State()
    cargoDumping = State()
    autoPilot = State()


async def showAdminPanel(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Управление полётом", callback_data="Управление полётом"),
        types.InlineKeyboardButton(text="Обновление ПО", callback_data="Обновление ПО"),
        types.InlineKeyboardButton(text="Сброс груза", callback_data="Сброс груза в режиме админа"),
        types.InlineKeyboardButton(text="Данные", callback_data="Данные"),
        types.InlineKeyboardButton(text="Режим автопилота", callback_data="Режим автопилота")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("В режиме администратора у вас есть доступ к панели управления станцией. "
                        "Каждое действие здесь имеет необратимые последствия",
                           reply_markup=keyboard)


# Колбэк на кнопку "Управление полётом"
async def callbackFlyControl(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text="Подсказка", callback_data="Подсказка1"))
    await call.message.answer("Введите ключ верификации, состоящий из 9 строчных латинских символов:",
                              reply_markup=keyboard)

# Колбэк на кнопку "Подсказка" в режиме "Управление полетами"
async def callbackHint_FlyControl(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("49.272598, -123.132872 város?")
    await Answers.flyControl.set()


# Проверка ответа на "Управление полётом"
async def processFlyControl(message: types.Message, state: FSMContext):
    await state.finish()
    if message.text.lower() != 'vancouver':
        await message.reply('Ключ верификации неверен. Попробуйте снова.')
        await Answers.flyControl.set()
        return
    await message.reply('Действие верифицировано. Введите желаемую высоту полета станции в километрах')
    # ВВОД ВЫСОТЫ В КИЛОМЕТРАХ
    await showAdminPanel(message)


# Колбэк на кнопку "Обновление ПО"
async def callbackUpdateSoftware(call: types.CallbackQuery):
    await call.message.answer('*Обнаружение ближайших спутников*')
    await asyncio.sleep(2)
    await call.message.answer('*Установка соединения*')
    await asyncio.sleep(2)
    await call.message.answer('*Обмен сообщениями*')
    await asyncio.sleep(2)
    await call.message.answer('*Сообщение отклонено*')
    await call.message.answer('Не удается подобрать пароль для подключения автоматически… Пароль содержит 9 символов'
                              ' алфавита: СТТАРКЕСЕ. Необходимо расставить их в определенном порядке и отправить сюда '
                              'для попытки подключения')
    await Answers.updateSoftware.set()
    await call.message.answer("Введите ключ верификации, состоящий из 9 строчных латинских символов:")


# Проверка ответа на "Обновление ПО"
async def processUpdateSoftware(message: types.Message, state: FSMContext):
    await state.finish()
    if message.text.lower() != 'тессеракт':
        await message.reply('Подключение не удалось. Попробуйте другую комбинацию')
        await Answers.updateSoftware.set()
        return
    await message.reply('Подключение произошло успешно! Начинаю загрузку обновлений')
    await asyncio.sleep(1.5)
    await message.answer('Загрузка обновления 5%')
    await asyncio.sleep(2)
    await message.answer('Загрузка обновления 15%')
    await asyncio.sleep(2)
    await message.answer('Загрузка обновления 25%')
    await asyncio.sleep(2)
    await message.answer('Загрузка обновления 50%')
    await asyncio.sleep(1)
    await message.answer('Загрузка обновления 53%')
    await asyncio.sleep(0.5)
    await message.answer('Загрузка обновления 59%')
    await asyncio.sleep(5)
    await message.answer('Загрузка обновления 99%')
    await asyncio.sleep(2)
    await message.answer('Загрузка обновления 112%')
    await asyncio.sleep(1.5)
    await message.answer('Установка обновления')
    await asyncio.sleep(5)
    await message.answer('Обновление программного обеспечение установлено')
    await showAdminPanel(message)


# Колбэк на кнопку "Сброс груза"
async def callbackCargoDumping(call: types.CallbackQuery):
    await Answers.cargoDumping.set()
    await call.message.answer(
        "Введите номер груза, который вы хотите вернуть отправителю. За раз можно отправить РОВНО 4 контейнера")


# Проверка ответа на "Сброс груза"
async def processCargoDumping(message: types.Message, state: FSMContext):
    await state.finish()
    global cargoNumbers
    if message.text.isdigit() is False or int(message.text) not in cargoNumbers:
        await message.reply('Некорректный номер груза. Проверьте правильность ввода и повторите отправку сообщения')
        await Answers.cargoDumping.set()
        return
    cargoNumbers.remove(int(message.text))
    if len(cargoNumbers) != 0:
        await message.reply('Груз готовится к отправке! Введите следующий номер')
        await Answers.cargoDumping.set()
        return
    await message.answer('Набор для доставки сформирован. Следующая доставка будет доступна через 42 часа')
    await showAdminPanel(message)


# Колбэк на кнопку "Данные"
async def callbackData(call: types.CallbackQuery):
    xls_path = "data.xlsx"
    await call.message.answer_document(InputFile(xls_path))
    await showAdminPanel(call.message)


# Колбэк на кнопку "Режим автопилота"
async def callbackAutopilot(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text="Подсказка", callback_data="Подсказка2"))
    await call.message.answer(f"Для выполнения этого действия необходима верификация!\n"
                              f"\n"
                              r"Нажмите на кнопку 'Подсказка', а после введите свой ключ авторизации, состоящий из 9 латинских символов:",
                              reply_markup=keyboard)

# Колбэк на кнопку "Подсказка" в режиме "Управление полетами"
async def callbackHint_Autopilot(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("49.272598, -123.132872 város?")
    await Answers.autoPilot.set()


# Проверка ответа на "Режим автопилота"
async def processAutopilot(message: types.Message, state: FSMContext):
    await state.finish()
    if message.text.lower() != 'vancouver':
        await message.reply('Ключ верификации неверен. Попробуйте снова.')
        await Answers.autoPilot.set()
        return
    await message.reply('Станция переведена в режим автопилота. Ручное управление отключено. '
                        'Вы будете переведены в статус контролера')
    # Завершающая стадия квеста
    await asyncio.sleep(180)
    await message.answer('Ошибка корректировки траектории! '
                         'Для исправления ошибки будет сброшено несколько резервных грузовых отсеков')
    await asyncio.sleep(60)
    await message.answer("""
    Координаты сброшенных грузов:
    43.400330, 39.974873
    43.595834, 39.929211
    44.606875, 39.992500
    45.254240, 39.674883
    """)
    await message.answer('Один из грузов приземлился рядом с вашим местоположением.'
                         'Вам необходимо забрать его, во избежание загрязнения окружающей среды.'
                         'Содержимое груза вы можете оставить себе')


def register_handlers_adminPanel(dp: Dispatcher):
    dp.register_callback_query_handler(callbackFlyControl, text="Управление полётом")
    dp.register_callback_query_handler(callbackHint_FlyControl, text="Подсказка1")
    dp.register_message_handler(processFlyControl, state=Answers.flyControl)
    dp.register_callback_query_handler(callbackUpdateSoftware, text="Обновление ПО")
    dp.register_message_handler(processUpdateSoftware, state=Answers.updateSoftware)
    dp.register_callback_query_handler(callbackCargoDumping, text="Сброс груза в режиме админа")
    dp.register_message_handler(processCargoDumping, state=Answers.cargoDumping)
    dp.register_callback_query_handler(callbackData, text="Данные")
    dp.register_callback_query_handler(callbackAutopilot, text="Режим автопилота")
    dp.register_callback_query_handler(callbackHint_Autopilot, text="Подсказка2")
    dp.register_message_handler(processAutopilot, state=Answers.autoPilot)