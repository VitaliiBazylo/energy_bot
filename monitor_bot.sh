#!/bin/bash

# Скрипт моніторингу та автоперезапуску бота
# Використання: додайте в crontab для автоматичного моніторингу
# */5 * * * * /home3/tstcomua/dev.tst.com.ua/EnergyBot/monitor_bot.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$HOME/venv310"
LOG_FILE="$SCRIPT_DIR/monitor.log"

cd "$SCRIPT_DIR"

echo "$(date): 🔍 Перевірка статусу бота..." >> "$LOG_FILE"

# Перевіряємо чи працює бот
if pgrep -f "main.py" > /dev/null; then
    echo "$(date): ✅ Бот працює (PID: $(pgrep -f main.py))" >> "$LOG_FILE"
    exit 0
else
    echo "$(date): ❌ Бот не працює! Перезапуск..." >> "$LOG_FILE"
    
    # Запускаємо бота
    source "$VENV_PATH/bin/activate"
    nohup python main.py > bot.log 2>&1 &
    BOT_PID=$!
    
    echo "$(date): 🚀 Бот перезапущено (PID: $BOT_PID)" >> "$LOG_FILE"
    
    # Перевіряємо через 5 секунд
    sleep 5
    if pgrep -f "main.py" > /dev/null; then
        echo "$(date): ✅ Перезапуск успішний!" >> "$LOG_FILE"
    else
        echo "$(date): ❌ Помилка перезапуску!" >> "$LOG_FILE"
    fi
fi
