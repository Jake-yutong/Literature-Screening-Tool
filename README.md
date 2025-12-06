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

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

**Windows:**
1. Download and extract this repository
2. Double-click `start.bat`

**macOS / Linux:**
```bash
chmod +x start.sh && ./start.sh
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/Jake-yutong/Results-Sifting-Tool.git
cd Results-Sifting-Tool

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The web interface will be available at `http://127.0.0.1:5000`.

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

