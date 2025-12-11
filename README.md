# Literature Screening Tool v1.2

A Python-based tool for preliminary screening in systematic reviews, meta-analyses, and bibliometric studies. This tool facilitates the filtering of large literature datasets exported from Web of Science and Scopus.

## ✨ What's New in v1.2.0

- **🤖 Multi-Model AI Support**: Choose between DeepSeek Chat and MiniMax-M2 models
- **🔄 MiniMax-M2 Integration**: Advanced AI screening with MiniMax's latest model
- **⚙️ Flexible Model Selection**: Switch between different AI providers based on your needs
- **🔑 Unified API Interface**: Simplified API key management for multiple providers

### Previous Updates (v1.1.0)

- **🌐 Bilingual Interface**: Seamless EN/中文 language switching
- **📄 RIS File Support**: Import and export RIS (Research Information Systems) format
- **📊 Multiple Export Formats**: CSV, Excel (.xlsx/.xls), TXT, and RIS
- **🎨 Professional UI**: Refined academic-style interface with improved dark mode
- **⚡ Enhanced Performance**: Optimized file processing and format conversion

## Features

- **Batch processing**: Supports multiple file uploads (.xlsx, .xls, .csv, .ris, .txt)
- **Format standardization**: Automatically converts Web of Science export format to Scopus-compatible format for VOSviewer
- **Keyword-based exclusion**: Filter records by title, abstract, or journal name
- **Multi-Model AI Screening** (optional): 
  - **DeepSeek Chat**: Fast and cost-effective AI-powered screening
  - **MiniMax-M2**: Advanced reasoning with thinking process visualization
  - Natural language-based filtering criteria for both models
- **Flexible export options**: Download results in CSV, Excel, TXT, or RIS format
- **Structured output**:
  - Retained records for downstream analysis
  - Excluded records with documented exclusion reasons (for PRISMA reporting)

## Installation

### System Requirements
- **Python 3.8 or higher** (Must be properly installed, not Windows Store version)
- pip package manager
- Supported operating systems: Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)

### Option 1: One-Click Launch (Recommended)

**Windows:**

*If you don't have Python installed:*
1. Download Python from https://www.python.org/downloads/
2. **IMPORTANT**: During installation, check ☑️ "Add Python to PATH"
3. Complete the installation and restart your computer

*To run the tool:*
1. Download this repository: Click the green `Code` button → `Download ZIP`
2. Extract the ZIP file to any folder (e.g., Desktop or Documents)
3. Double-click `start.bat`
   - First run: Dependencies will be installed automatically (takes 1-2 minutes)
   - The terminal window will stay open showing server status
   - After ~3 seconds, your browser will open automatically to `http://127.0.0.1:5000`
4. To stop: Press `Ctrl+C` in the terminal window

**macOS:**

*方法一：右键快捷方式（推荐）*
1. 下载并解压此仓库到任意文件夹（如下载文件夹或桌面）
2. 在 Finder 中找到解压后的文件夹
3. 右键点击文件夹空白处 → 选择 **"新建位于文件夹位置的终端窗口"**
4. 在弹出的终端窗口中输入以下命令（首次运行需要授权）：
   ```bash
   chmod +x start.sh && ./start.sh
   ```
5. 等待3秒，浏览器将自动打开 `http://127.0.0.1:5000`
6. 停止服务：在终端按 `Ctrl+C`

*方法二：手动导航（如果右键菜单没有终端选项）*
1. 打开 **"终端"** 应用（在 应用程序 → 实用工具 中）
2. 输入 `cd ` (cd后面有个空格)
3. 将解压后的文件夹从 Finder 直接**拖拽**到终端窗口
4. 按回车键，然后运行：
   ```bash
   chmod +x start.sh && ./start.sh
   ```

*常见问题：*
- 如果提示 "无法打开，因为来自身份不明的开发者"：右键点击 `start.sh` → 选择 "打开" → 再次点击 "打开" 确认
- 如果 Python 命令不存在：先安装 [Homebrew](https://brew.sh/)，然后运行 `brew install python3`

**Linux:**
1. Download and extract this repository
2. Open Terminal and navigate to the extracted folder:
   ```bash
   cd ~/Downloads/Literature-Screening-Tool  # 根据实际路径调整
   ```
3. Run the launcher script:
   ```bash
   chmod +x start.sh && ./start.sh
   ```
4. Your browser will open automatically to `http://127.0.0.1:5000`

### Option 2: Manual Installation

```bash
# Step 1: Clone the repository
git clone https://github.com/Jake-yutong/Results-Sifting-Tool.git

# Step 2: Navigate to the project directory
cd Results-Sifting-Tool

# Step 3: (Optional) Create a virtual environment
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Step 4: Install required packages
pip install -r requirements.txt

# Step 5: Launch the application
python app.py
```

The web interface will be available at `http://127.0.0.1:5000`.

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Terminal closes immediately without output | Python is not installed correctly. Download from python.org and check "Add to PATH" during installation |
| "Python was not found" error | This is the Windows Store placeholder. Install real Python from python.org OR disable the placeholder in Settings → Apps → App execution aliases |
| Browser shows "Connection Refused" | Wait 5 seconds for the server to fully start, then refresh the page |
| Dependencies fail to install | Check your internet connection. If behind a proxy, configure pip with: `pip config set global.proxy http://your-proxy:port` |
| "Port 5000 already in use" (macOS) | **Automatic**: The tool will auto-switch to port 5001+<br>**Manual fix**: Disable AirPlay Receiver in System Settings → General → AirPlay Receiver (uncheck "Allow Handoff between this Mac and your iCloud devices") |
| "Address already in use" error | The tool automatically finds an available port. Check the terminal output for the actual port number |
| Excel file read errors | Ensure files are in `.xlsx`, `.xls`, or `.csv` format with UTF-8 encoding |

## AI Configuration (Optional)

### DeepSeek API Setup

1. Get your API key from [DeepSeek Platform](https://platform.deepseek.com/)
2. In the web interface, select **DeepSeek Chat** from the model dropdown
3. Enter your API key in the "API Key" field
4. Add natural language exclusion criteria

### MiniMax-M2 API Setup

1. Get your API key from [MiniMax Platform](https://platform.minimaxi.com/)
2. In the web interface, select **MiniMax-M2** from the model dropdown
3. Enter your API key in the "API Key" field
4. Add natural language exclusion criteria

**Note**: The tool automatically configures the appropriate API endpoint based on your model selection:
- DeepSeek: `https://api.deepseek.com`
- MiniMax (China): `https://api.minimaxi.com/anthropic`
- MiniMax (International): `https://api.minimax.io/anthropic`

## Usage

1. **Upload** literature export files (Web of Science or Scopus format)
2. **Configure** exclusion keywords for title/abstract and journal name fields
3. **(Optional)** Select AI model and provide API key for intelligent screening
4. **Run** the screening process
5. **Download** results:
   - `cleaned_data.csv` for bibliometric analysis (e.g., VOSviewer)
   - `removed_data.csv` for PRISMA flow diagram documentation

## Dependencies

| Package | Purpose |
|---------|---------|
| Flask | Web framework |
| Pandas | Data manipulation |
| OpenPyXL | Excel file handling |
| xlrd | Legacy Excel format support |
| openai | DeepSeek API integration (optional) |
| anthropic | MiniMax-M2 API integration (optional) |
| gunicorn | Production server |

## File Structure

```
├── app.py                  # Flask application
├── literature_screener.py  # Command-line interface
├── templates/
│   └── index.html          # Web interface
├── requirements.txt
├── start.bat               # Windows launcher
└── start.sh                # Unix launcher
```

## Citation

If you use this tool in your research, please cite:

```
Literature Screening Tool. Available at: https://github.com/Jake-yutong/Results-Sifting-Tool
```

## License

This project is provided for academic and research purposes.

