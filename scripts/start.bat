@echo off
chcp 65001 >nul 2>nul
title Literature Screening Tool
echo ========================================
echo    Literature Screening Tool
echo ========================================
echo.

:: Check Python (try multiple commands and verify they actually work)
echo Checking for Python installation...
echo.

:: Try 'py' first (Python Launcher for Windows - most reliable)
py --version >nul 2>&1
if %errorlevel%==0 (
    set PYTHON_CMD=py
    echo [OK] Found Python using 'py' launcher
    py --version
    echo.
    goto :found
)

:: Try 'python3'
python3 --version >nul 2>&1
if %errorlevel%==0 (
    set PYTHON_CMD=python3
    echo [OK] Found Python using 'python3' command
    python3 --version
    echo.
    goto :found
)

:: Try 'python' but verify it's not the Windows Store stub
python --version >nul 2>&1
if %errorlevel%==0 (
    :: Check if it's the Windows Store stub by trying to get the version
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_TEST=%%i
    echo !PYTHON_TEST! | findstr /C:"Python" >nul
    if %errorlevel%==0 (
        set PYTHON_CMD=python
        echo [OK] Found Python using 'python' command
        python --version
        echo.
        goto :found
    )
)

:: Python not found
echo ============================================================
echo [ERROR] Python is not installed on this computer
echo ============================================================
echo.
echo You need to install Python 3.8 or higher.
echo.
echo Step 1: Download Python from:
echo   https://www.python.org/downloads/
echo.
echo Step 2: During installation, CHECK these boxes:
echo   [X] Add Python to PATH
echo   [X] Install pip
echo.
echo Step 3: After installation, restart this program.
echo.
echo ============================================================
echo.
pause
exit /b 1

:found

:: Install dependencies
echo [1/2] Installing dependencies (this may take 1-2 minutes)...
echo.
%PYTHON_CMD% -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Failed to install some dependencies.
    echo Trying alternative installation method...
    %PYTHON_CMD% -m pip install --user -r requirements.txt
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Failed to install dependencies.
        echo.
        echo Please check your internet connection and try again.
        echo.
        pause
        exit /b 1
    )
)
echo.
echo [OK] Dependencies installed successfully
echo.

:: Start app using the launcher
echo [2/2] Starting application...
echo.
%PYTHON_CMD% launch.py

:: Keep window open if there was an error
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application failed to start.
    echo.
    pause
)
