@echo off
chcp 65001 >nul 2>nul
title Literature Screening Tool
echo ========================================
echo    Literature Screening Tool
echo ========================================
echo.

:: Check Python (try multiple commands)
echo Checking for Python installation...
where python >nul 2>&1
if %errorlevel%==0 (
    set PYTHON_CMD=python
    goto :found
)

where py >nul 2>&1
if %errorlevel%==0 (
    set PYTHON_CMD=py
    goto :found
)

where python3 >nul 2>&1
if %errorlevel%==0 (
    set PYTHON_CMD=python3
    goto :found
)

echo.
echo [ERROR] Python not found on this computer.
echo.
echo Please install Python 3.8 or higher from:
echo https://www.python.org/downloads/
echo.
echo IMPORTANT: During installation, check the box:
echo "Add Python to PATH"
echo.
echo After installing Python, run this script again.
echo.
pause
exit /b 1

:found
echo [OK] Found Python: %PYTHON_CMD%
%PYTHON_CMD% --version
if %errorlevel% neq 0 (
    echo [ERROR] Python command failed to execute
    pause
    exit /b 1
)
echo.

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
