@echo off
chcp 65001 >nul
echo ========================================
echo   EnergyBot - Налаштування
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] Перевірка Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python не знайдено!
    echo.
    echo Завантажте Python з https://www.python.org/downloads/
    echo ВАЖЛИВО: Поставте галочку "Add Python to PATH"
    pause
    exit /b 1
)
python --version
echo ✅ Python встановлено
echo.

echo [2/4] Створення віртуального оточення...
if exist .venv (
    echo ⚠️ Віртуальне оточення вже існує
) else (
    python -m venv .venv
    echo ✅ Віртуальне оточення створено
)
echo.

echo [3/4] Встановлення залежностей...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Помилка встановлення залежностей
    pause
    exit /b 1
)
echo ✅ Залежності встановлено
echo.

echo [4/4] Перевірка конфігурації...
if exist .env (
    echo ✅ Файл .env знайдено
) else (
    echo ⚠️ Файл .env не знайдено!
    echo.
    echo Створіть файл .env з наступним вмістом:
    echo BOT_TOKEN=ваш_токен_від_BotFather
    echo CHAT_IDS=ваш_telegram_chat_id
    echo.
    if exist .env.example (
        copy .env.example .env
        echo Створено .env з .env.example
        echo Відредагуйте файл .env та додайте ваші дані
    )
)
echo.

echo ========================================
echo ✅ Налаштування завершено!
echo ========================================
echo.
echo Для запуску бота:
echo   1. Відредагуйте .env (додайте BOT_TOKEN та CHAT_IDS)
echo   2. Відредагуйте cameras.json (додайте IP камер)
echo   3. Запустіть start.bat
echo.
pause
