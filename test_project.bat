@echo off
REM Pet Care Project Health Check Script for Windows
REM This script tests if the project is running correctly

echo.
echo ========================================
echo 🐾 Pet Care Project Health Check
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if requests library is available
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Installing required library: requests
    pip install requests
    if errorlevel 1 (
        echo ❌ Failed to install requests library
        pause
        exit /b 1
    )
)

REM Run the health check tests
echo 🔍 Running health check tests...
echo.

python project_health_tests.py

if errorlevel 1 (
    echo.
    echo ❌ Some tests failed. Please check the output above.
    echo.
    echo 💡 Common solutions:
    echo    1. Make sure Flask app is running: python app.py
    echo    2. Check if all dependencies are installed: pip install -r requirements.txt
    echo    3. Verify database is initialized
    echo.
) else (
    echo.
    echo ✅ All tests passed! Your project is running correctly.
    echo.
)

echo Press any key to exit...
pause >nul
