@echo off
chcp 65001 >nul
echo ========================================
echo    Literature Screening Tool
echo ========================================
echo.

:: Check Python (try multiple commands)
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

echo [ERROR] Python not found.
echo.
echo Please install Python 3.8+ from:
echo https://www.python.org/downloads/
echo.
echo IMPORTANT: During installation, check "Add Python to PATH"
echo.
pause
exit /b 1

:found
echo [OK] Found Python: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

:: Install dependencies
echo [1/2] Installing dependencies...
%PYTHON_CMD% -m pip install -r requirements.txt -q
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    echo Trying with --user flag...
    %PYTHON_CMD% -m pip install -r requirements.txt -q --user
)
echo.

:: Start app
echo [2/2] Starting application...
echo.
echo ================================================
echo   Open in browser: http://127.0.0.1:5000
echo   Press Ctrl+C to stop the server
echo ================================================
echo.

:: Start Python server in background, then open browser after delay
start /b %PYTHON_CMD% app.py

:: Wait for server to start
echo Waiting for server to start...
timeout /t 3 /nobreak >nul

:: Open browser
start http://127.0.0.1:5000

:: Keep window open and show server output
echo.
echo Server is running. Press Ctrl+C to stop.
echo.

:: Wait indefinitely (keep the window open)
cmd /k
