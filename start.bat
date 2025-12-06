@echo off
echo ========================================
echo    文献筛选工具 Literature Screener
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit
)

:: Install dependencies
echo [1/2] 安装依赖...
pip install -r requirements.txt -q

:: Start app
echo [2/2] 启动应用...
echo.
echo ✅ 请在浏览器打开: http://127.0.0.1:5000
echo    按 Ctrl+C 停止服务
echo.
python app.py
pause
