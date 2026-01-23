@echo off
chcp 65001 > nul
echo ========================================
echo   EnergyBot - Компіляція в EXE
echo ========================================
echo.

REM Перевірка віртуального оточення
if not exist ".venv\Scripts\python.exe" (
    echo [ПОМИЛКА] Віртуальне оточення не знайдено!
    echo Спочатку запустіть setup.bat
    pause
    exit /b 1
)

echo [1/3] Встановлення PyInstaller...
call .venv\Scripts\pip.exe install pyinstaller

echo.
echo [2/3] Компіляція launcher_standalone.py в EXE...
call .venv\Scripts\pyinstaller.exe --onefile --windowed --name="EnergyBot" --icon=NONE ^
    --add-data "config.py;." ^
    --add-data "monitor.py;." ^
    --add-data "main.py;." ^
    --hidden-import=aiogram ^
    --hidden-import=aiogram.types ^
    --hidden-import=aiogram.filters ^
    --hidden-import=asyncio ^
    --hidden-import=dotenv ^
    --collect-all=aiogram ^
    launcher_standalone.py

echo.
echo [3/3] Створення портативної версії...
if not exist "dist\EnergyBot_Portable" mkdir "dist\EnergyBot_Portable"
copy "dist\EnergyBot.exe" "dist\EnergyBot_Portable\"
copy ".env.example" "dist\EnergyBot_Portable\.env" 2>nul
copy "cameras.json" "dist\EnergyBot_Portable\" 2>nul
copy "README.md" "dist\EnergyBot_Portable\" 2>nul

echo.
echo Створення інструкції...
(
echo EnergyBot - Портативна версія
echo ================================
echo.
echo 1. Відредагуйте .env файл:
echo    - Вкажіть BOT_TOKEN вашого Telegram бота
echo    - Вкажіть CHAT_IDS через кому
echo.
echo 2. Відредагуйте cameras.json:
echo    - Додайте ваші камери з IP адресами
echo.
echo 3. Запустіть EnergyBot.exe
echo.
echo Для отримання Chat ID:
echo    - Відправте /start вашому боту
echo    - Chat ID буде показано в інтерфейсі
) > "dist\EnergyBot_Portable\START_HERE.txt"

echo.
echo ========================================
echo ✅ Компіляція завершена!
echo.
echo Файл EXE: dist\EnergyBot.exe
echo Портативна версія: dist\EnergyBot_Portable\
echo.
echo ⚠️ УВАГА:
echo Портативна папка містить ВСЕ необхідне!
echo Просто скопіюйте папку EnergyBot_Portable
echo на інший комп'ютер і запустіть EnergyBot.exe
echo.
echo Не потрібно встановлювати Python!
echo Не потрібно setup.bat!
echo ========================================
pause
