#!/bin/bash
echo "========================================"
echo "   文献筛选工具 Literature Screener"
echo "========================================"
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到 Python3,请先安装"
    exit 1
fi

# Install dependencies
echo "[1/2] 安装依赖..."
pip3 install -r requirements.txt -q

# Start app with browser auto-open
echo "[2/2] 启动应用..."
echo

# Start server in background and capture its output
python3 -c "
import subprocess
import time
import webbrowser
import re
import sys

# Start Flask app
process = subprocess.Popen(
    ['python3', 'app.py'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    universal_newlines=True,
    bufsize=1
)

port_found = False
url = None

# Read output line by line
for line in process.stdout:
    print(line, end='', flush=True)
    
    # Look for the port number in the output
    if not port_found and 'http://127.0.0.1:' in line:
        match = re.search(r'http://127\.0\.0\.1:(\d+)', line)
        if match:
            port = match.group(1)
            url = f'http://127.0.0.1:{port}'
            port_found = True
            # Wait a moment for server to be fully ready
            time.sleep(2)
            print(f'\n🚀 正在打开浏览器: {url}\n', flush=True)
            try:
                webbrowser.open(url)
            except Exception as e:
                print(f'⚠️  无法自动打开浏览器，请手动访问: {url}')

# Wait for process to complete
process.wait()
sys.exit(process.returncode)
"
