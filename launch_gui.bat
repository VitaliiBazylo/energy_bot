@echo off
chcp 65001 > nul
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Віртуальне оточення не знайдено! Запустіть setup.bat
    pause
    exit /b 1
)

start "EnergyBot Launcher" "%~dp0.venv\Scripts\pythonw.exe" "%~dp0launcher.py"
