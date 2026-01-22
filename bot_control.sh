#!/bin/bash

# Скрипт управління ботом
# Використання: ./bot_control.sh {start|stop|restart|status|logs}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$HOME/venv310"
cd "$SCRIPT_DIR"

PID_FILE="$SCRIPT_DIR/bot.pid"
LOG_FILE="$SCRIPT_DIR/bot.log"

start_bot() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "🟢 Бот вже запущений (PID: $PID)"
            return 1
        else
            rm -f "$PID_FILE"
        fi
    fi

    echo "🤖 Запуск бота у фоні..."
    
    # Активація віртуального середовища та запуск
    source "$VENV_PATH/bin/activate"
    nohup python main.py > "$LOG_FILE" 2>&1 &
    
    PID=$!
    echo $PID > "$PID_FILE"
    
    echo "✅ Бот запущений у фоні (PID: $PID)"
    echo "📝 Логи: $LOG_FILE"
    echo "🛑 Зупинка: ./bot_control.sh stop"
}

stop_bot() {
    if [ ! -f "$PID_FILE" ]; then
        echo "❌ PID файл не знайдено. Бот не запущений?"
        return 1
    fi

    PID=$(cat "$PID_FILE")
    
    if kill -0 "$PID" 2>/dev/null; then
        echo "🛑 Зупинка бота (PID: $PID)..."
        kill "$PID"
        
        # Чекаємо завершення
        for i in {1..10}; do
            if ! kill -0 "$PID" 2>/dev/null; then
                break
            fi
            sleep 1
        done
        
        if kill -0 "$PID" 2>/dev/null; then
            echo "⚠️ Примусова зупинка..."
            kill -9 "$PID"
        fi
        
        rm -f "$PID_FILE"
        echo "✅ Бот зупинено"
    else
        echo "❌ Процес не знайдено"
        rm -f "$PID_FILE"
    fi
}

status_bot() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "🟢 Бот працює (PID: $PID)"
            echo "📊 Використання пам'яті:"
            ps -p "$PID" -o pid,vsz,rss,cmd
        else
            echo "❌ Бот не працює (застарілий PID файл)"
            rm -f "$PID_FILE"
        fi
    else
        echo "❌ Бот не запущений"
    fi
}

show_logs() {
    if [ -f "$LOG_FILE" ]; then
        tail -f "$LOG_FILE"
    else
        echo "❌ Лог файл не знайдено"
    fi
}

case "$1" in
    start)
        start_bot
        ;;
    stop)
        stop_bot
        ;;
    restart)
        stop_bot
        sleep 2
        start_bot
        ;;
    status)
        status_bot
        ;;
    logs)
        show_logs
        ;;
    *)
        echo "Використання: $0 {start|stop|restart|status|logs}"
        exit 1
        ;;
esac
