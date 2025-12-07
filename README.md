# Literature Screening Tool

A Python-based tool for preliminary screening in systematic reviews, meta-analyses, and bibliometric studies. This tool facilitates the filtering of large literature datasets exported from Web of Science and Scopus.

## ✨ What's New in v1.1.0

- **🌐 Bilingual Interface**: Seamless EN/中文 language switching
- **📄 RIS File Support**: Import and export RIS (Research Information Systems) format
- **📊 Multiple Export Formats**: CSV, Excel (.xlsx/.xls), TXT, and RIS
- **🎨 Professional UI**: Refined academic-style interface with improved dark mode
- **⚡ Enhanced Performance**: Optimized file processing and format conversion

## Features

- **Batch processing**: Supports multiple file uploads (.xlsx, .xls, .csv, .ris, .txt)
- **Format standardization**: Automatically converts Web of Science export format to Scopus-compatible format for VOSviewer
- **Keyword-based exclusion**: Filter records by title, abstract, or journal name
- **LLM-assisted screening** (optional): Integration with DeepSeek API for natural language-based filtering criteria
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

**macOS / Linux:**
1. Download and extract this repository
2. Open Terminal and navigate to the extracted folder:
   ```bash
   cd /path/to/Results-Sifting-Tool
   ```
3. Run the launcher script:
   ```bash
   chmod +x start.sh
   ./start.sh
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
| Port 5000 already in use | Another application is using this port. Close it or modify `PORT` in `app.py` |
| Excel file read errors | Ensure files are in `.xlsx`, `.xls`, or `.csv` format with UTF-8 encoding |

## Usage

1. **Upload** literature export files (Web of Science or Scopus format)
2. **Configure** exclusion keywords for title/abstract and journal name fields
3. **Run** the screening process
4. **Download** results:
   - `cleaned_data.csv` for bibliometric analysis (e.g., VOSviewer)
   - `removed_data.csv` for PRISMA flow diagram documentation

## Dependencies

| Package | Purpose |
|---------|---------|
| Flask | Web framework |
| Pandas | Data manipulation |
| OpenPyXL | Excel file handling |
| xlrd | Legacy Excel format support |
| openai | LLM API integration (optional) |
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

