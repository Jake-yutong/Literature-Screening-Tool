# 📚 Literature Screening Tool / 文献粗筛工具 v1.0

A Python-based automated screening tool for **Meta-Analysis** and **Bibliometrics** research.
Designed to streamline the process of filtering thousands of papers from **Web of Science** and **Scopus**.

用于元分析/文献计量学研究的 Python 自动化粗筛工具。

---

## ✨ Features / 功能特点

- ⚡ **Fast Processing**: Screen thousands of papers in seconds.
- 🔄 **Auto-Standardization**: Automatically unifies WoS and Scopus data formats for VOSviewer compatibility.
- 📂 **Multi-file Upload**: Batch upload multiple .xlsx, .xls, or .csv files.
- 🎯 **Smart Filtering**:
    - **Keyword Blacklist**: Exclude by Title, Abstract, or Journal Name.
    - **🤖 AI Screening**: Optional DeepSeek-V3 integration for natural language filtering.
- 🌗 **Dark/Light Mode**: Comfortable viewing in any environment.
- 📊 **Dual Output**:
    - `cleaned_data.csv`: For VOSviewer analysis.
    - `removed_data.csv`: For PRISMA flow diagrams (with exclusion reasons).

---

## 🚀 Quick Start / 快速开始

### 一键启动 (推荐)

**Windows 用户：**
1. 点击绿色 **Code** → **Download ZIP** 下载并解压
2. 双击 `start.bat`
3. 浏览器自动打开工具 ✅

**Mac / Linux 用户：**
1. 下载 ZIP 并解压
2. 终端运行：
   ```bash
   chmod +x start.sh && ./start.sh
   ```
3. 打开浏览器访问 http://127.0.0.1:5000

### 手动运行

1.  **Install Python**: Ensure Python 3.8+ is installed.
2.  **Download Code**: Clone this repository or download the ZIP.
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run Application**:
    ```bash
    python app.py
    ```
5.  **Access**: Open your browser at `http://127.0.0.1:5000`.

### Deploy to Cloud (Render/Heroku)

This project is ready for cloud deployment.

1.  **Push to GitHub**: Upload this code to a new GitHub repository.
2.  **Connect to Render/Heroku**:
    -   Select "Web Service".
    -   Connect your GitHub repo.
    -   **Build Command**: `pip install -r requirements.txt`
    -   **Start Command**: `gunicorn app:app`
3.  **Done!** Your tool is now online.

---

## 📖 Usage Guide / 使用指南

1.  **Upload / 上传**: Drag and drop your literature files (WoS or Scopus exports).
2.  **Configure / 配置**:
    *   **Keywords**: Enter exclusion keywords (one per line).
    *   **AI Screening**: (Optional) Enter DeepSeek API Key and criteria (e.g., "Exclude non-empirical studies").
3.  **Screen / 筛选**: Click "Start Screening".
4.  **Download / 下载**:
    *   ✅ `cleaned_data.csv`: Import this into **VOSviewer**.
    *   ❌ `removed_data.csv`: Check this for your **PRISMA** report.

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3 (Variables, Dark Mode), Vanilla JS
- **Backend**: Python (Flask), Pandas, OpenPyXL
- **AI**: OpenAI SDK (DeepSeek-V3)

---

## 📧 Contact

Created for Meta-Analysis & Bibliometrics Research.
If you encounter issues, please check your file encoding (UTF-8 recommended) and Python version.
