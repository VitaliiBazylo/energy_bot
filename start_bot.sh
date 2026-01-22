#!/bin/bash

# Простий скрипт запуску бота у фоні
# Використання: ./start_bot.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🤖 Запуск EnergyBot..."

# Перевірка віртуального середовища
if [ ! -d ".venv" ]; then
    echo "❌ Віртуальне середовище не знайдено!"
    echo "Створюємо..."
    python3 -m venv .venv
fi

# Активація віртуального середовища
source .venv/bin/activate

# Перевірка файлів
if [ ! -f ".env" ]; then
    echo "❌ Файл .env не знайдено!"
    exit 1
fi

if [ ! -f "main.py" ]; then
    echo "❌ Файл main.py не знайдено!"
    exit 1
fi

# Перевірка чи не працює вже
if pgrep -f "main.py" > /dev/null; then
    echo "❌ Бот вже працює!"
    echo "🔍 PID: $(pgrep -f main.py)"
    exit 1
fi

# Запуск бота у фоні
nohup python main.py > bot.log 2>&1 &
BOT_PID=$!

echo "✅ Бот запущено у фоні!"
echo "🆔 PID: $BOT_PID"
echo "📋 Логи: tail -f bot.log"
echo "🛑 Зупинка: kill $BOT_PID"
