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
    echo [WARNING] Failed to install some dependencies.
    echo Trying with --user flag...
    %PYTHON_CMD% -m pip install -r requirements.txt -q --user
)
echo.

:: Start app using the launcher
echo [2/2] Starting application...
echo.
%PYTHON_CMD% launch.py
