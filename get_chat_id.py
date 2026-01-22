"""
Скрипт для отримання Chat ID
Запустіть цей скрипт, потім напишіть боту /start в Telegram
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
import os

# Завантаження змінних середовища
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("❌ BOT_TOKEN не знайдено в .env файлі!")
    exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

print("✅ Бот запущено!")
print("📱 Напишіть боту /start в Telegram щоб отримати ваш Chat ID")
print("=" * 60)


@dp.message(Command("start"))
async def get_chat_id(message: types.Message):
    """Отримати Chat ID"""
    chat_id = message.chat.id
    user_name = message.from_user.full_name
    username = message.from_user.username
    
    info = f"""
✅ Chat ID отримано!

👤 Користувач: {user_name}
🆔 Username: @{username if username else 'немає'}
💬 Chat ID: {chat_id}

📝 Додайте цей Chat ID до файлу .env:
CHAT_IDS={chat_id}

Після цього натисніть Ctrl+C щоб зупинити цей скрипт.
"""
    
    logger.info("=" * 60)
    logger.info(info)
    logger.info("=" * 60)
    
    await message.answer(
        f"✅ Ваш Chat ID: <code>{chat_id}</code>\n\n"
        f"Додайте його до файлу .env",
        parse_mode="HTML"
    )


@dp.message()
async def any_message(message: types.Message):
    """Обробка будь-якого повідомлення"""
    await message.answer(
        "Використайте команду /start щоб отримати Chat ID"
    )


async def main():
    """Головна функція"""
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
