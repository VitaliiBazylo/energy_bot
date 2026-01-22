"""
EnergyBot - Телеграм бот для моніторингу електроенергії через пінгування камер
"""
import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from config import Config
from monitor import CameraMonitor

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Ініціалізація бота
config = Config()
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
monitor = CameraMonitor(config.CAMERAS, bot, config.CHAT_IDS)


@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Команда /start"""
    await message.answer(
        "👋 Вітаю! Я EnergyBot - моніторю стан електроенергії через камери відеоспостереження.\n\n"
        "Доступні команди:\n"
        "/status - Перевірити поточний стан камер\n"
        "/cameras - Список камер\n"
        "/help - Допомога"
    )


@dp.message(Command("status"))
async def cmd_status(message: Message):
    """Команда /status - показати стан камер"""
    status_text = monitor.get_status_report()
    await message.answer(status_text)


@dp.message(Command("cameras"))
async def cmd_cameras(message: Message):
    """Команда /cameras - список камер"""
    cameras_list = "\n".join([
        f"📹 {camera['name']}: {camera['ip']}"
        for camera in config.CAMERAS
    ])
    await message.answer(f"Камери під моніторингом:\n\n{cameras_list}")


@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Команда /help"""
    await message.answer(
        "ℹ️ Допомога\n\n"
        "Бот автоматично моніторить камери та повідомляє про:\n"
        "⚡ Появу електроенергії (камера відповідає)\n"
        "🔌 Відключення електроенергії (камера не відповідає)\n\n"
        "Команди:\n"
        "/status - Поточний стан камер\n"
        "/cameras - Список камер\n"
        "/help - Ця довідка"
    )


async def main():
    """Головна функція"""
    logger.info("Запуск EnergyBot...")
    
    # Запуск моніторингу в фоновому режимі
    monitor_task = asyncio.create_task(monitor.start_monitoring())
    
    # Запуск бота
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except KeyboardInterrupt:
        logger.info("Отримано сигнал зупинки")
    except Exception as e:
        logger.error(f"Помилка: {e}")
    finally:
        monitor_task.cancel()
        try:
            await monitor_task
        except asyncio.CancelledError:
            pass
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
