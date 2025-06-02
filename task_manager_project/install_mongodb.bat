@echo off
echo ========================================
echo Installing MongoDB for Windows
echo ========================================

echo.
echo Downloading MongoDB Community Server...
powershell -Command "Invoke-WebRequest -Uri 'https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.4.zip' -OutFile 'mongodb.zip'"

echo.
echo Extracting MongoDB...
powershell -Command "Expand-Archive -Path 'mongodb.zip' -DestinationPath '.'"

echo.
echo Setting up MongoDB...
if not exist "C:\mongodb" mkdir "C:\mongodb"
xcopy /E /I "mongodb-windows-x86_64-7.0.4\*" "C:\mongodb\"

echo.
echo Creating data directory...
if not exist "C:\data\db" mkdir "C:\data\db"

echo.
echo Cleaning up...
del mongodb.zip
rmdir /S /Q "mongodb-windows-x86_64-7.0.4"

echo.
echo MongoDB installed successfully!
echo Location: C:\mongodb
echo Data directory: C:\data\db

echo.
echo Starting MongoDB...
start "MongoDB Server" "C:\mongodb\bin\mongod.exe" --dbpath "C:\data\db"

echo.
echo MongoDB is starting in a new window...
echo Wait 10 seconds for MongoDB to start, then press any key to continue...
timeout /t 10

echo.
echo MongoDB setup complete!
pause
