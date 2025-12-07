#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Literature Screening Web App - Flask Backend
文献筛选网页应用 - Flask 后端
"""

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import io
import zipfile
import threading
import uuid
import time
from datetime import datetime
import rispy
import xlwt
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Default blacklists
DEFAULT_TITLE_ABSTRACT_BLACKLIST = [
    "surgical", "surgery", "patient", "patients", "clinical trial",
    "hospital", "physician", "nurse", "disease", "therapy",
    "diagnosis", "treatment", "medication", "drug", "pharmaceutical",
    "cancer", "tumor", "tumour", "athlete", "athletes", "sports",
    "game theory", "game-theoretic", "molecular", "molecule",
    "chemical", "chemistry", "physics", "quantum", "genome", "protein",
]

DEFAULT_JOURNAL_BLACKLIST = [
    "medicine", "medical", "clinical", "surgery", "surgical",
    "hospital", "health", "nursing", "pharmacy", "pharmacology",
    "chemistry", "chemical", "physics", "physical", "biology",
    "biological", "biochemistry", "sports", "sport", "athletic",
]

# Column mappings for different data sources
COLUMN_MAPPINGS = {
    "title": ["Title", "title", "TI", "Article Title", "Document Title"],
    "abstract": ["Abstract", "abstract", "AB", "Description"],
    "source": ["Source Title", "source title", "SO", "Source", "Journal", 
               "Publication Name", "Publication", "Journal Title"],
}

# Global storage for tasks
tasks = {}

def find_column(df, column_type):
    """Find the actual column name in the dataframe based on mappings."""
    possible_names = COLUMN_MAPPINGS.get(column_type, [])
    for name in possible_names:
        if name in df.columns:
            return name
    return None


def contains_blacklisted_keyword(text, blacklist):
    """Check if text contains any blacklisted keyword."""
    if pd.isna(text) or not isinstance(text, str):
        return False, ""
    text_lower = text.lower()
    for keyword in blacklist:
        if keyword.lower().strip() in text_lower:
            return True, keyword
    return False, ""


def remove_duplicates(df, title_col='Title', method='doi_title'):
    """
    Remove duplicate records from DataFrame.
    
    Args:
        df: DataFrame to deduplicate
        title_col: Name of the title column
        method: Deduplication method
            - 'doi': Remove duplicates based on DOI (if available)
            - 'title': Remove duplicates based on title similarity
            - 'doi_title': Try DOI first, then title (default)
    
    Returns:
        Tuple of (deduplicated_df, duplicate_info_dict)
    """
    original_count = len(df)
    df_clean = df.copy()
    
    # Track duplicates
    duplicates_removed = 0
    duplicate_details = []
    
    # Step 1: Remove DOI-based duplicates
    if 'DOI' in df_clean.columns and method in ['doi', 'doi_title']:
        # Only consider rows with non-empty DOI
        doi_mask = df_clean['DOI'].notna() & (df_clean['DOI'].astype(str).str.strip() != '')
        
        if doi_mask.any():
            # Mark duplicates based on DOI (keep first occurrence)
            df_clean['_temp_doi_dup'] = df_clean['DOI'].where(doi_mask)
            duplicated_doi = df_clean.duplicated(subset=['_temp_doi_dup'], keep='first')
            
            if duplicated_doi.any():
                dup_count = duplicated_doi.sum()
                duplicates_removed += dup_count
                duplicate_details.append(f"DOI-based: {dup_count} duplicates")
                df_clean = df_clean[~duplicated_doi]
            
            df_clean = df_clean.drop(columns=['_temp_doi_dup'])
    
    # Step 2: Remove title-based duplicates
    if title_col in df_clean.columns and method in ['title', 'doi_title']:
        # Normalize titles for comparison
        df_clean['_temp_title_norm'] = df_clean[title_col].astype(str).str.lower().str.strip()
        df_clean['_temp_title_norm'] = df_clean['_temp_title_norm'].str.replace(r'[^\w\s]', '', regex=True)
        df_clean['_temp_title_norm'] = df_clean['_temp_title_norm'].str.replace(r'\s+', ' ', regex=True)
        
        # Remove exact title duplicates (keep first)
        duplicated_title = df_clean.duplicated(subset=['_temp_title_norm'], keep='first')
        
        if duplicated_title.any():
            dup_count = duplicated_title.sum()
            duplicates_removed += dup_count
            duplicate_details.append(f"Title-based: {dup_count} duplicates")
            df_clean = df_clean[~duplicated_title]
        
        df_clean = df_clean.drop(columns=['_temp_title_norm'])
    
    # Reset index
    df_clean = df_clean.reset_index(drop=True)
    
    dedup_info = {
        'original_count': int(original_count),
        'duplicates_removed': int(duplicates_removed),
        'final_count': int(len(df_clean)),
        'details': duplicate_details,
        'method': method
    }
    
    return df_clean, dedup_info


def parse_ris_file(file_content):
    """Parse RIS file content and convert to DataFrame."""
    try:
        # RIS files are text-based
        text_content = file_content.decode('utf-8')
        entries = rispy.loads(text_content)
        
        # Convert to DataFrame
        records = []
        for entry in entries:
            record = {
                'Title': entry.get('title') or entry.get('primary_title', ''),
                'Abstract': entry.get('abstract', ''),
                'Source title': entry.get('journal_name') or entry.get('secondary_title', ''),
                'Authors': '; '.join(entry.get('authors', [])),
                'Year': entry.get('year', ''),
                'DOI': entry.get('doi', ''),
                'Keywords': '; '.join(entry.get('keywords', [])),
                'Type': entry.get('type_of_reference', ''),
                'URL': entry.get('url', ''),
            }
            records.append(record)
        
        return pd.DataFrame(records)
    except Exception as e:
        raise ValueError(f"Error parsing RIS file: {str(e)}")


def df_to_ris(df, title_col='Title', abstract_col='Abstract', source_col='Source title'):
    """Convert DataFrame to RIS format string."""
    ris_entries = []
    
    for idx, row in df.iterrows():
        entry = {
            'type_of_reference': 'JOUR',  # Journal Article
            'title': str(row.get(title_col, '')) if pd.notna(row.get(title_col)) else '',
            'abstract': str(row.get(abstract_col, '')) if pd.notna(row.get(abstract_col)) else '',
            'journal_name': str(row.get(source_col, '')) if pd.notna(row.get(source_col)) else '',
        }
        
        # Add optional fields if they exist
        if 'Authors' in row and pd.notna(row['Authors']):
            authors_str = str(row['Authors'])
            entry['authors'] = [a.strip() for a in authors_str.split(';') if a.strip()]
        
        if 'Year' in row and pd.notna(row['Year']):
            entry['year'] = str(row['Year'])
        
        if 'DOI' in row and pd.notna(row['DOI']):
            entry['doi'] = str(row['DOI'])
        
        if 'Keywords' in row and pd.notna(row['Keywords']):
            keywords_str = str(row['Keywords'])
            entry['keywords'] = [k.strip() for k in keywords_str.split(';') if k.strip()]
        
        if 'URL' in row and pd.notna(row['URL']):
            entry['url'] = str(row['URL'])
        
        ris_entries.append(entry)
    
    # Use rispy to dump to string
    ris_string = rispy.dumps(ris_entries)
    return ris_string


def parse_bibtex_file(file_content):
    """Parse BibTeX file content and convert to DataFrame."""
    try:
        text_content = file_content.decode('utf-8')
        bib_database = bibtexparser.loads(text_content)
        
        records = []
        for entry in bib_database.entries:
            record = {
                'Title': entry.get('title', '').replace('{', '').replace('}', ''),
                'Abstract': entry.get('abstract', ''),
                'Source title': entry.get('journal', '') or entry.get('booktitle', ''),
                'Authors': entry.get('author', '').replace(' and ', '; '),
                'Year': entry.get('year', ''),
                'DOI': entry.get('doi', ''),
                'Keywords': entry.get('keywords', ''),
                'Type': entry.get('ENTRYTYPE', ''),
                'URL': entry.get('url', ''),
                'Publisher': entry.get('publisher', ''),
                'Volume': entry.get('volume', ''),
                'Pages': entry.get('pages', ''),
            }
            records.append(record)
        
        return pd.DataFrame(records)
    except Exception as e:
        raise ValueError(f"Error parsing BibTeX file: {str(e)}")


def df_to_bibtex(df, title_col='Title', abstract_col='Abstract', source_col='Source title'):
    """Convert DataFrame to BibTeX format string."""
    bib_db = BibDatabase()
    entries = []
    
    for idx, row in df.iterrows():
        # Generate citation key from author and year or use index
        year = str(row.get('Year', '')) if pd.notna(row.get('Year')) else ''
        authors = str(row.get('Authors', '')) if pd.notna(row.get('Authors')) else ''
        
        if authors and year:
            first_author = authors.split(';')[0].split(',')[0].strip().replace(' ', '')
            cite_key = f"{first_author}{year}"
        else:
            cite_key = f"ref{idx+1}"
        
        entry = {
            'ID': cite_key,
            'ENTRYTYPE': 'article',
            'title': str(row.get(title_col, '')) if pd.notna(row.get(title_col)) else '',
            'abstract': str(row.get(abstract_col, '')) if pd.notna(row.get(abstract_col)) else '',
            'journal': str(row.get(source_col, '')) if pd.notna(row.get(source_col)) else '',
        }
        
        # Add optional fields
        if 'Authors' in row and pd.notna(row['Authors']):
            entry['author'] = str(row['Authors']).replace(';', ' and')
        
        if 'Year' in row and pd.notna(row['Year']):
            entry['year'] = str(row['Year'])
        
        if 'DOI' in row and pd.notna(row['DOI']):
            entry['doi'] = str(row['DOI'])
        
        if 'Keywords' in row and pd.notna(row['Keywords']):
            entry['keywords'] = str(row['Keywords'])
        
        if 'URL' in row and pd.notna(row['URL']):
            entry['url'] = str(row['URL'])
        
        if 'Publisher' in row and pd.notna(row['Publisher']):
            entry['publisher'] = str(row['Publisher'])
        
        if 'Volume' in row and pd.notna(row['Volume']):
            entry['volume'] = str(row['Volume'])
        
        if 'Pages' in row and pd.notna(row['Pages']):
            entry['pages'] = str(row['Pages'])
        
        entries.append(entry)
    
    bib_db.entries = entries
    writer = BibTexWriter()
    writer.indent = '  '
    return writer.write(bib_db)


def screen_literature_task(task_id, df, title_abstract_keywords, journal_keywords, api_key=None, ai_criteria=None, remove_duplicates_flag=False):
    """Background task for screening literature."""
    try:
        tasks[task_id]['status'] = 'processing'
        tasks[task_id]['progress'] = 0
        tasks[task_id]['message'] = 'Initializing...'
        
        original_total = len(df)
        
        # Find relevant columns
        title_col = find_column(df, "title")
        abstract_col = find_column(df, "abstract")
        source_col = find_column(df, "source")
        
        # --- Step 0: Remove duplicates if requested ---
        dedup_info = None
        if remove_duplicates_flag:
            tasks[task_id]['message'] = 'Removing duplicates...'
            df, dedup_info = remove_duplicates(df, title_col=title_col or 'Title', method='doi_title')
            print(f"🔄 Deduplication: {dedup_info['duplicates_removed']} duplicates removed ({dedup_info['original_count']} → {dedup_info['final_count']})", flush=True)
        
        # Parse keywords
        ta_blacklist = [k.strip() for k in title_abstract_keywords.split('\n') if k.strip()]
        j_blacklist = [k.strip() for k in journal_keywords.split('\n') if k.strip()]
        
        # Initialize tracking columns
        df['_EXCLUDED'] = False
        df['_EXCLUSION_REASON'] = ''
        
        stats = {
            'original_total': int(original_total),
            'total': int(len(df)),
            'title_col': title_col,
            'abstract_col': abstract_col,
            'source_col': source_col,
            'title_abstract_excluded': 0,
            'journal_excluded': 0,
            'ai_excluded': 0,
            'deduplication': dedup_info
        }
        
        tasks[task_id]['message'] = 'Keyword Screening...'
        
        # --- Step 1: Keyword Screening ---
        for idx, row in df.iterrows():
            exclusion_reasons = []
            
            # Check Title
            if title_col:
                is_excluded, keyword = contains_blacklisted_keyword(row[title_col], ta_blacklist)
                if is_excluded:
                    exclusion_reasons.append(f"Title: '{keyword}'")
            
            # Check Abstract
            if abstract_col:
                is_excluded, keyword = contains_blacklisted_keyword(row[abstract_col], ta_blacklist)
                if is_excluded:
                    exclusion_reasons.append(f"Abstract: '{keyword}'")
            
            if exclusion_reasons:
                stats['title_abstract_excluded'] += 1
            
            # Check Source/Journal
            if source_col:
                is_excluded, keyword = contains_blacklisted_keyword(row[source_col], j_blacklist)
                if is_excluded:
                    exclusion_reasons.append(f"Journal: '{keyword}'")
                    if len(exclusion_reasons) == 1:
                        stats['journal_excluded'] += 1
            
            if exclusion_reasons:
                df.at[idx, '_EXCLUDED'] = True
                df.at[idx, '_EXCLUSION_REASON'] = ' | '.join(exclusion_reasons)

        # --- Step 2: AI Screening (Optional) ---
        if api_key and ai_criteria:
            try:
                from openai import OpenAI
                import json
                
                tasks[task_id]['message'] = 'Connecting to AI...'
                client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
                
                # Only screen papers that passed the keyword filter
                candidates = df[df['_EXCLUDED'] == False]
                total_candidates = len(candidates)
                
                print(f"🤖 Starting AI Screening for {total_candidates} papers...", flush=True)
                
                for i, (idx, row) in enumerate(candidates.iterrows()):
                    # Update progress
                    progress_pct = int((i / total_candidates) * 100)
                    tasks[task_id]['progress'] = progress_pct
                    tasks[task_id]['message'] = f"AI Screening: {i+1}/{total_candidates}"
                    
                    title = row[title_col] if title_col else "N/A"
                    abstract = row[abstract_col] if abstract_col else "N/A"
                    
                    prompt = f"""
                    You are a research assistant. Screen this paper based on the following exclusion criteria:
                    "{ai_criteria}"
                    
                    Paper Title: {title}
                    Paper Abstract: {abstract}
                    
                    Reply strictly in JSON format: {{"exclude": boolean, "reason": "short reason"}}
                    """
                    
                    try:
                        response = client.chat.completions.create(
                            model="deepseek-chat",
                            messages=[
                                {"role": "system", "content": "You are a helpful assistant that outputs JSON."},
                                {"role": "user", "content": prompt}
                            ],
                            response_format={"type": "json_object"},
                            temperature=0.0
                        )
                        
                        result = json.loads(response.choices[0].message.content)
                        
                        if result.get('exclude', False):
                            df.at[idx, '_EXCLUDED'] = True
                            df.at[idx, '_EXCLUSION_REASON'] = f"AI: {result.get('reason', 'Criteria matched')}"
                            stats['ai_excluded'] += 1
                            print(f"   ❌ Excluded: {result.get('reason', 'Criteria matched')}", flush=True)
                        else:
                            print(f"   ✅ Kept", flush=True)
                            
                    except Exception as e:
                        print(f"   ⚠️ AI Error for row {idx}: {e}", flush=True)
                        continue
                
                print("🤖 AI Screening Completed.", flush=True)
                        
            except Exception as e:
                print(f"❌ AI Setup Error: {e}", flush=True)
                # Continue without AI if it fails, or maybe we should fail? 
                # For now, let's just log it and finish.

        # Split dataframes
        df_kept = df[df['_EXCLUDED'] == False].drop(columns=['_EXCLUDED', '_EXCLUSION_REASON'])
        df_removed = df[df['_EXCLUDED'] == True].copy()
        df_removed = df_removed.rename(columns={'_EXCLUSION_REASON': 'Exclusion_Reason'})
        df_removed = df_removed.drop(columns=['_EXCLUDED'])
        
        stats['kept'] = len(df_kept)
        stats['excluded'] = len(df_removed)
        
        # Store dataframes directly for later format conversion
        tasks[task_id]['result'] = {
            'stats': stats,
            'df_kept': df_kept,
            'df_removed': df_removed,
            'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S"),
            'title_col': title_col,
            'abstract_col': abstract_col,
            'source_col': source_col
        }
        tasks[task_id]['status'] = 'completed'
        tasks[task_id]['progress'] = 100
        tasks[task_id]['message'] = 'Completed!'
        
    except Exception as e:
        print(f"❌ Task Error: {e}", flush=True)
        tasks[task_id]['status'] = 'error'
        tasks[task_id]['error'] = str(e)


@app.route('/')
def index():
    """Serve the main page."""
    response = app.make_response(render_template('index.html',
                         default_ta='\n'.join(DEFAULT_TITLE_ABSTRACT_BLACKLIST),
                         default_journal='\n'.join(DEFAULT_JOURNAL_BLACKLIST)))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/screen', methods=['POST'])
def screen():
    """Start the screening process."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        files = request.files.getlist('file')
        if not files or files[0].filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Get keywords from form
        ta_keywords = request.form.get('ta_keywords', '')
        journal_keywords = request.form.get('journal_keywords', '')
        api_key = request.form.get('api_key', '').strip()
        ai_criteria = request.form.get('ai_criteria', '').strip()
        
        # Read and merge files
        dfs = []
        
        # WoS to Scopus Mapping
        WOS_MAPPING = {
            'TI': 'Title',
            'AB': 'Abstract',
            'AU': 'Authors',
            'SO': 'Source title',
            'PY': 'Year',
            'DE': 'Author Keywords',
            'ID': 'Keywords Plus',
            'DI': 'DOI',
            'DT': 'Document Type',
            'CR': 'References',
            'C1': 'Affiliations',
            'TC': 'Cited by',
            'SN': 'ISSN',
            'EI': 'EISSN'
        }

        for file in files:
            filename = file.filename.lower()
            try:
                if filename.endswith('.xlsx'):
                    df = pd.read_excel(file, engine='openpyxl')
                elif filename.endswith('.xls'):
                    df = pd.read_excel(file, engine='xlrd')
                elif filename.endswith('.ris'):
                    # RIS file support
                    content = file.read()
                    df = parse_ris_file(content)
                    print(f"   Parsed RIS file: {filename}, {len(df)} records", flush=True)
                elif filename.endswith('.bib'):
                    # BibTeX file support
                    content = file.read()
                    df = parse_bibtex_file(content)
                    print(f"   Parsed BibTeX file: {filename}, {len(df)} records", flush=True)
                elif filename.endswith('.csv') or filename.endswith('.txt'):
                    # WoS exports often come as tab-delimited .txt or .csv
                    content = file.read()
                    # Try tab separator first for .txt or potential WoS files
                    try:
                        df = pd.read_csv(io.BytesIO(content), sep='\t', encoding='utf-8', on_bad_lines='skip')
                        if 'TI' not in df.columns and 'Title' not in df.columns:
                            # Fallback to comma
                            raise ValueError("Not tab delimited")
                    except:
                        for encoding in ['utf-8', 'utf-8-sig', 'gbk', 'latin-1']:
                            try:
                                df = pd.read_csv(io.BytesIO(content), encoding=encoding)
                                break
                            except UnicodeDecodeError:
                                continue
                        else:
                            return jsonify({'error': f'Could not decode file: {file.filename}'}), 400
                else:
                    return jsonify({'error': f'Unsupported file format: {file.filename}'}), 400
                
                # Standardize Columns
                # Check if it looks like WoS (has TI and SO)
                if 'TI' in df.columns and 'SO' in df.columns:
                    print(f"   Detected WoS format for {filename}, standardizing...", flush=True)
                    df = df.rename(columns=WOS_MAPPING)
                
                # Ensure essential columns exist
                required_cols = ['Title', 'Abstract', 'Source title']
                for col in required_cols:
                    if col not in df.columns:
                        # Try case-insensitive match
                        found = False
                        for existing_col in df.columns:
                            if existing_col.lower() == col.lower():
                                df = df.rename(columns={existing_col: col})
                                found = True
                                break
                        if not found:
                            df[col] = '' # Create empty if missing
                
                dfs.append(df)
            except Exception as e:
                return jsonify({'error': f'Error reading file {file.filename}: {str(e)}'}), 400
        
        if not dfs:
            return jsonify({'error': 'No valid files processed'}), 400
            
        # Merge all dataframes
        df = pd.concat(dfs, ignore_index=True)
        print(f"Merged {len(dfs)} files. Total rows: {len(df)}", flush=True)
        
        # Get deduplication preference
        remove_duplicates_flag = request.form.get('remove_duplicates', 'false').lower() == 'true'
        
        # Create task
        task_id = str(uuid.uuid4())
        tasks[task_id] = {
            'status': 'queued',
            'progress': 0,
            'message': 'Queued...',
            'result': None
        }
        
        # Start background thread
        thread = threading.Thread(target=screen_literature_task, 
                                args=(task_id, df, ta_keywords, journal_keywords, api_key, ai_criteria, remove_duplicates_flag))
        thread.daemon = True
        thread.start()
        
        return jsonify({'task_id': task_id})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/status/<task_id>')
def task_status(task_id):
    """Check the status of a task."""
    task = tasks.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    response = {
        'status': task['status'],
        'progress': task.get('progress', 0),
        'message': task.get('message', ''),
    }
    
    if task['status'] == 'completed':
        response['stats'] = task['result']['stats']
    elif task['status'] == 'error':
        response['error'] = task.get('error', 'Unknown error')
        
    return jsonify(response)


@app.route('/download/<task_id>/<dataset>/<format>')
def download(task_id, dataset, format):
    """Download the processed files in various formats.
    
    Args:
        task_id: The task identifier
        dataset: 'cleaned', 'removed', or 'both'
        format: 'csv', 'xlsx', 'xls', 'txt', or 'ris'
    """
    print(f"📥 Download request: task_id={task_id}, dataset={dataset}, format={format}", flush=True)
    
    task = tasks.get(task_id)
    if not task:
        print(f"❌ Task not found: {task_id}", flush=True)
        return "Task not found", 404
        
    if task['status'] != 'completed':
        print(f"❌ Task not completed: {task['status']}", flush=True)
        return "Result not ready", 404
    
    try:
        result = task['result']
        timestamp = result['timestamp']
        df_kept = result['df_kept']
        df_removed = result['df_removed']
        title_col = result.get('title_col', 'Title')
        abstract_col = result.get('abstract_col', 'Abstract')
        source_col = result.get('source_col', 'Source title')
        
        # Helper function to convert df to requested format
        def df_to_buffer(df, fmt, filename_base):
            buffer = io.BytesIO()
            
            if fmt == 'csv':
                csv_str = df.to_csv(index=False, encoding='utf-8')
                buffer.write(csv_str.encode('utf-8-sig'))
                mimetype = 'text/csv'
                filename = f'{filename_base}.csv'
                
            elif fmt == 'xlsx':
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Sheet1')
                mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                filename = f'{filename_base}.xlsx'
                
            elif fmt == 'xls':
                # Use xlwt for old Excel format
                with pd.ExcelWriter(buffer, engine='xlwt') as writer:
                    df.to_excel(writer, index=False, sheet_name='Sheet1')
                mimetype = 'application/vnd.ms-excel'
                filename = f'{filename_base}.xls'
                
            elif fmt == 'txt':
                # Tab-separated text file
                txt_str = df.to_csv(index=False, sep='\t', encoding='utf-8')
                buffer.write(txt_str.encode('utf-8-sig'))
                mimetype = 'text/plain'
                filename = f'{filename_base}.txt'
                
            elif fmt == 'ris':
                ris_str = df_to_ris(df, title_col, abstract_col, source_col)
                buffer.write(ris_str.encode('utf-8'))
                mimetype = 'application/x-research-info-systems'
                filename = f'{filename_base}.ris'
                
            elif fmt == 'bib':
                bib_str = df_to_bibtex(df, title_col, abstract_col, source_col)
                buffer.write(bib_str.encode('utf-8'))
                mimetype = 'application/x-bibtex'
                filename = f'{filename_base}.bib'
                
            else:
                raise ValueError(f"Unsupported format: {fmt}")
            
            buffer.seek(0)
            return buffer, filename, mimetype
        
        # Single file download
        if dataset == 'cleaned':
            buffer, filename, mimetype = df_to_buffer(df_kept, format, f'cleaned_data_{timestamp}')
            print(f"   Preparing cleaned data: {filename}", flush=True)
            return send_file(buffer, as_attachment=True, download_name=filename, mimetype=mimetype)
        
        elif dataset == 'removed':
            buffer, filename, mimetype = df_to_buffer(df_removed, format, f'removed_data_{timestamp}')
            print(f"   Preparing removed data: {filename}", flush=True)
            return send_file(buffer, as_attachment=True, download_name=filename, mimetype=mimetype)
        
        # Download both as ZIP
        elif dataset == 'both':
            print(f"   Preparing ZIP file with format: {format}", flush=True)
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                # Add cleaned file
                buffer_clean, filename_clean, _ = df_to_buffer(df_kept, format, f'cleaned_data_{timestamp}')
                zf.writestr(filename_clean, buffer_clean.read())
                
                # Add removed file
                buffer_removed, filename_removed, _ = df_to_buffer(df_removed, format, f'removed_data_{timestamp}')
                zf.writestr(filename_removed, buffer_removed.read())
            
            zip_buffer.seek(0)
            return send_file(zip_buffer, as_attachment=True,
                            download_name=f'screening_results_{timestamp}.zip',
                            mimetype='application/zip')
        
        print(f"❌ Invalid dataset: {dataset}", flush=True)
        return "Invalid dataset type", 400
        
    except Exception as e:
        print(f"❌ Download Error: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return f"Server Error: {str(e)}", 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print("\n" + "=" * 50)
    print("📚 Literature Screening Web App")
    print("=" * 50)
    print(f"\n🌐 Open your browser and go to: http://127.0.0.1:{port}")
    print("   Press Ctrl+C to stop the server\n")
    app.run(debug=False, host='0.0.0.0', port=port)
