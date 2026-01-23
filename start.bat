@echo off
chcp 65001 >nul
title EnergyBot
echo ========================================
echo   EnergyBot - Запуск
echo ========================================
echo.

cd /d "%~dp0"

if not exist .venv (
    echo ❌ Віртуальне оточення не знайдено!
    echo Спочатку запустіть setup.bat
    pause
    exit /b 1
)

if not exist .env (
    echo ❌ Файл .env не знайдено!
    echo Створіть .env з вашими налаштуваннями
    pause
    exit /b 1
)

echo 🚀 Запуск EnergyBot...
echo.
echo Для зупинки натисніть Ctrl+C
echo ========================================
echo.

"%~dp0.venv\Scripts\python.exe" "%~dp0main.py"

if %errorlevel% neq 0 (
    echo.
    echo ❌ Бот зупинився з помилкою
    pause
)
