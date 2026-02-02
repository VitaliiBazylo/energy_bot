@echo off
chcp 65001 > nul
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo ==========================================
    echo   Віртуальне оточення не знайдено!
    echo ==========================================
    echo.
    echo Бажаєте автоматично налаштувати проект?
    echo.
    choice /C YN /M "Запустити setup.bat"
    if errorlevel 2 exit /b 1
    if errorlevel 1 (
        call setup.bat
        if %errorlevel% neq 0 (
            echo.
            echo Помилка налаштування!
            pause
            exit /b 1
        )
    )
)

start "EnergyBot Launcher" "%~dp0.venv\Scripts\pythonw.exe" "%~dp0launcher.py"
