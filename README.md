# Literature Screening Tool

A Python-based tool for preliminary screening in systematic reviews, meta-analyses, and bibliometric studies. This tool facilitates the filtering of large literature datasets exported from Web of Science and Scopus.

## Features

- **Batch processing**: Supports multiple file uploads (.xlsx, .xls, .csv)
- **Format standardization**: Automatically converts Web of Science export format to Scopus-compatible format for VOSviewer
- **Keyword-based exclusion**: Filter records by title, abstract, or journal name
- **LLM-assisted screening** (optional): Integration with DeepSeek API for natural language-based filtering criteria
- **Structured output**:
  - `cleaned_data.csv` — Retained records for downstream analysis
  - `removed_data.csv` — Excluded records with documented exclusion reasons (for PRISMA reporting)

## Installation

### System Requirements
- Python 3.8 or higher
- pip package manager
- Supported operating systems: Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)

### Option 1: One-Click Launch (Recommended)

**Windows:**
1. Download this repository: Click the green `Code` button → `Download ZIP`
2. Extract the ZIP file to any folder
3. Double-click `start.bat`
4. A browser window will open automatically at `http://127.0.0.1:5000`

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
4. Open `http://127.0.0.1:5000` in your browser

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
| `python` command not found | Try `python3` instead, or verify Python is added to PATH |
| Port 5000 already in use | Close other applications using this port, or modify `app.py` to use a different port |
| Excel file read errors | Ensure input files are in `.xlsx`, `.xls`, or `.csv` format with UTF-8 encoding |

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

