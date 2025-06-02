@echo off
echo ========================================
echo Django + MongoDB Task Manager Setup
echo ========================================

echo.
echo Step 1: Installing MongoDB...
echo Downloading MongoDB Community Server...

powershell -Command "& {
    $url = 'https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.4.zip'
    $output = 'mongodb.zip'
    Write-Host 'Downloading MongoDB...'
    try {
        Invoke-WebRequest -Uri $url -OutFile $output -TimeoutSec 300
        Write-Host 'Download completed!'
    } catch {
        Write-Host 'Download failed, trying alternative method...'
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($url, $output)
    }
}"

if not exist mongodb.zip (
    echo Download failed. Please download MongoDB manually.
    echo URL: https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.4.zip
    pause
    exit /b 1
)

echo.
echo Step 2: Extracting MongoDB...
powershell -Command "Expand-Archive -Path 'mongodb.zip' -DestinationPath '.' -Force"

if exist mongodb-windows-x86_64-7.0.4 (
    if exist mongodb rmdir /s /q mongodb
    ren mongodb-windows-x86_64-7.0.4 mongodb
)

echo.
echo Step 3: Setting up directories...
if not exist data\db mkdir data\db
if not exist data\log mkdir data\log

echo.
echo Step 4: Starting MongoDB...
start "MongoDB Server" /min mongodb\bin\mongod.exe --dbpath data\db --logpath data\log\mongodb.log --port 27017

echo.
echo Waiting for MongoDB to start...
timeout /t 10

echo.
echo Step 5: Setting up Django...
python manage.py migrate --run-syncdb

echo.
echo Step 6: Creating superuser...
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager_project.settings')
django.setup()
from django.contrib.auth.models import User
try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('Superuser created: admin/admin123')
    else:
        print('Superuser already exists')
except Exception as e:
    print(f'Error creating superuser: {e}')
"

echo.
echo Step 7: Creating sample data...
python manage.py create_sample_data

echo.
echo Step 8: Starting Django server...
echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo MongoDB: Running on localhost:27017
echo Django: Starting on http://127.0.0.1:8000
echo Login: admin / admin123
echo ========================================
echo.

python manage.py runserver 8000
