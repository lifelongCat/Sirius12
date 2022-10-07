#!venv/bin/python
import logging
import random
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# ПЕРЕПИСАТЬ ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ НА STATE
# ДОБАВИТЬ ВЫЗОВ ГЛАВНОГО МЕНЮ В ОТДЕЛЬНОЙ ФУНКЦИИ
# ВОЗМОЖНО ПОМЕНЯТЬ ЗАДЕРЖКУ
# ЗАМЕНИТЬ ФРАЗЫ НА ФИНАЛЬНЫЕ
# ЗАМЕНИТЬ XLS ФАЙЛ С ДАННЫМИ
# РЕФАКТОР КОДА
# НАСТРОИТЬ ПРАВИЛЬНО ГДЕ-ТО REPLY, А ГДЕ-ТО ANSWER

# Объект бота
bot = Bot(token="5763817832:AAHryUF70705YJcIOraaYVh1njprvtS752Y")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
adminPasswords = {0: 'Вероника', 1: 'VxWorks'}
adminID = None
isLogin = False
acceptedCargos = 0
cargoNumbers = [72121022, 12102006, 78151290, 55005321]


class Form(StatesGroup):
    adminPassword = State()
    answerFlyControl = State()
    answerUpdateSoftware = State()
    answerCargoDumping = State()
    answerAutoPilot = State()


# Колбэк на кнопку "Подсказка"
@dp.callback_query_handler(text="Подсказка")
async def _(call: types.CallbackQuery):
    print("Подсказка callback")
    await call.message.answer("49.272598, -123.132872 város?")


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
    if adminID is None:
        await call.message.answer(
            "Отправка груза заблокирована. Для выполнения этого действия необходимы права администратора.")
        return
    await Form.answerCargoDumping.set()
    await call.message.answer(
        "Введите номер груза, который вы хотите вернуть отправителю. За раз можно отправить РОВНО 4 контейнера")


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


# Колбэк на кнопку "Тони Старк"
@dp.callback_query_handler(text="Тони Старк")
async def _(call: types.CallbackQuery):
    global adminID
    if adminID is not None:
        return
    adminID = 0
    await Form.adminPassword.set()
    await call.message.answer("Для входа в аккаунт введите ответ на контрольный вопрос: Какое кодовое название носило "
                              "модульное дополнение к костюму железного человека, предназначенное для борьбы с Халком?")


# Колбэк на кнопку "Григорий Карнацевич"
@dp.callback_query_handler(text="Григорий Карнацевич")
async def _(call: types.CallbackQuery):
    global adminID
    if adminID is not None:
        return
    adminID = 1
    await call.message.answer("Для входа в аккаунт введите ответ на контрольный вопрос: с помощью какой операционной "
                              "системы управляется марсоходом Curiosity?")


# Проверка пароля в /admin
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
    # Вывод сообщения с режимом админа
    buttons = [
        types.InlineKeyboardButton(text="Управление полётом", callback_data="Управление полётом"),
        types.InlineKeyboardButton(text="Обновление ПО", callback_data="Обновление ПО"),
        types.InlineKeyboardButton(text="Сброс груза", callback_data="Сброс груза"),
        types.InlineKeyboardButton(text="Данные", callback_data="Данные"),
        types.InlineKeyboardButton(text="Режим автопилота", callback_data="Режим автопилота")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("В режиме администратора у вас есть доступ к панели управления станцией. "
                        "Каждое действие здесь имеет необратимые последствия",
                        reply_markup=keyboard)


# Колбэк на кнопку "Управление полётом"
@dp.callback_query_handler(text="Управление полётом")
async def _(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text="Подсказка", callback_data="Подсказка"))
    await Form.answerFlyControl.set()
    await call.message.answer("Введите ключ верификации, состоящий из 9 строчных латинских символов:",
                              reply_markup=keyboard)


# Проверка ответа на "Управление полётом"
@dp.message_handler(state=Form.answerFlyControl)
async def processFlyControl(message: types.Message, state: FSMContext):
    await state.finish()
    if message.text != 'Vancouver':
        await message.reply('Ключ верификации неверен. Попробуйте снова.')
        await Form.answerFlyControl.set()
        return
    await message.reply('Действие верифицировано. Введите желаемую высоту полета станции в километрах')


# Колбэк на кнопку "Обновление ПО"
@dp.callback_query_handler(text="Обновление ПО")
async def _(call: types.CallbackQuery):
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
    await Form.answerUpdateSoftware.set()
    await call.message.answer("Введите ключ верификации, состоящий из 9 строчных латинских символов:")


# Проверка ответа на "Обновление ПО"
@dp.message_handler(state=Form.answerUpdateSoftware)
async def processUpdateSoftware(message: types.Message, state: FSMContext):
    await state.finish()
    if message.text != 'Тессеракт':
        await message.reply('Подключение не удалось. Попробуйте другую комбинацию')
        await Form.answerUpdateSoftware.set()
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


# Проверка ответа на "Сброс груза"
@dp.message_handler(state=Form.answerCargoDumping)
async def processCargoDumping(message: types.Message, state: FSMContext):
    await state.finish()
    global cargoNumbers
    if message.text.isdigit() is False or int(message.text) not in cargoNumbers:
        await message.reply('Некорректный номер груза. Проверьте правильность ввода и повторите отправку сообщения')
        await Form.answerCargoDumping.set()
        return
    cargoNumbers.remove(int(message.text))
    if len(cargoNumbers) != 0:
        await message.reply('Груз готовится к отправке! Введите следующий номер')
        await Form.answerCargoDumping.set()
        return
    await message.answer('Набор для доставки сформирован. Следующая доставка будет доступна через 42 часа')
    return


# Колбэк на кнопку "Данные"
@dp.callback_query_handler(text="Данные")
async def _(call: types.CallbackQuery):
    xls_path = "data.xlsx"
    await call.message.answer_document(InputFile(xls_path))


# Колбэк на кнопку "Режим автопилота"
@dp.callback_query_handler(text="Режим автопилота")
async def _(call: types.CallbackQuery):
    await Form.answerAutoPilot.set()
    await call.message.answer("Введите ключ верификации, состоящий из 9 строчных латинских символов:")


# Проверка ответа на "Режим автопилота"
@dp.message_handler(state=Form.answerAutoPilot)
async def processAutopilot(message: types.Message, state: FSMContext):
    await state.finish()
    if message.text != 'Vancouver':
        await message.reply('Ключ верификации неверен. Попробуйте снова.')
        await Form.answerAutoPilot.set()
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

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)