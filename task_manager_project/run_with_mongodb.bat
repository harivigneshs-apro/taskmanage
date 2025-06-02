@echo off
echo ========================================
echo Django + MongoDB Task Manager Setup
echo ========================================

echo.
echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python first.
    pause
    exit /b 1
)

echo.
echo Setting up MongoDB and Django...
python setup_mongodb.py

echo.
echo Starting Django development server...
python manage.py runserver 8000

pause
