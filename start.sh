#!/bin/bash
echo "========================================"
echo "   文献筛选工具 Literature Screener"
echo "========================================"
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到 Python3，请先安装"
    exit 1
fi

# Install dependencies
echo "[1/2] 安装依赖..."
pip3 install -r requirements.txt -q

# Start app
echo "[2/2] 启动应用..."
echo
echo "✅ 请在浏览器打开: http://127.0.0.1:5000"
echo "   按 Ctrl+C 停止服务"
echo
python3 app.py
