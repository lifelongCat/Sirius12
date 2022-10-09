#!venv/bin/python
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config_reader import load_config
from app.handlers.start import register_handlers_start
from app.handlers.admin import register_handlers_admin, Admin
from app.handlers.adminPanel import register_handlers_adminPanel

adminClass = Admin()
logger = logging.getLogger(__name__)


# ПЕРЕПИСАТЬ ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ НА STATE
# ДОБАВИТЬ ВЫЗОВ ГЛАВНОГО МЕНЮ В ОТДЕЛЬНОЙ ФУНКЦИИ
# ВОЗМОЖНО ПОМЕНЯТЬ ЗАДЕРЖКУ
# ЗАМЕНИТЬ ФРАЗЫ НА ФИНАЛЬНЫЕ
# НАСТРОИТЬ ПРАВИЛЬНО ГДЕ-ТО REPLY, А ГДЕ-ТО ANSWER


# Регистрация команд, отображаемых в интерфейсе Telegram
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать"),
        BotCommand(command="/admin", description="Вход в панель администратора")
    ]
    await bot.set_my_commands(commands)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s \n---------------------------------------------------"
    )

    # Парсинг файла конфигурации
    config = load_config("config/bot.ini")
    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    register_handlers_start(dp)
    register_handlers_admin(dp)
    register_handlers_adminPanel(dp)
    # Установка команд бота
    await set_commands(bot)
    # Запуск поллинга
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())