#!/bin/bash

# Скрипт автозапуску бота після перезавантаження сервера
# Використання: додайте в crontab
# @reboot /path/to/EnergyBot/autostart_bot.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/autostart.log"

cd "$SCRIPT_DIR"

echo "$(date): 🔄 Автозапуск бота після перезавантаження..." >> "$LOG_FILE"

# Чекаємо 30 секунд після старту системи
sleep 30

# Активація та запуск
source .venv/bin/activate
nohup python main.py > bot.log 2>&1 &
BOT_PID=$!

echo "$(date): ✅ Бот запущено (PID: $BOT_PID)" >> "$LOG_FILE"

# Перевірка через 10 секунд
sleep 10
if pgrep -f "main.py" > /dev/null; then
    echo "$(date): ✅ Автозапуск успішний!" >> "$LOG_FILE"
else
    echo "$(date): ❌ Помилка автозапуску!" >> "$LOG_FILE"
fi
