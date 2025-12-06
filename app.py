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


def screen_literature_task(task_id, df, title_abstract_keywords, journal_keywords, api_key=None, ai_criteria=None):
    """Background task for screening literature."""
    try:
        tasks[task_id]['status'] = 'processing'
        tasks[task_id]['progress'] = 0
        tasks[task_id]['message'] = 'Initializing...'
        
        # Find relevant columns
        title_col = find_column(df, "title")
        abstract_col = find_column(df, "abstract")
        source_col = find_column(df, "source")
        
        # Parse keywords
        ta_blacklist = [k.strip() for k in title_abstract_keywords.split('\n') if k.strip()]
        j_blacklist = [k.strip() for k in journal_keywords.split('\n') if k.strip()]
        
        # Initialize tracking columns
        df['_EXCLUDED'] = False
        df['_EXCLUSION_REASON'] = ''
        
        stats = {
            'total': len(df),
            'title_col': title_col,
            'abstract_col': abstract_col,
            'source_col': source_col,
            'title_abstract_excluded': 0,
            'journal_excluded': 0,
            'ai_excluded': 0
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
        
        # Create CSV outputs in memory
        cleaned_buffer = io.StringIO()
        removed_buffer = io.StringIO()
        
        df_kept.to_csv(cleaned_buffer, index=False, encoding='utf-8')
        df_removed.to_csv(removed_buffer, index=False, encoding='utf-8')
        
        tasks[task_id]['result'] = {
            'stats': stats,
            'cleaned': cleaned_buffer.getvalue(),
            'removed': removed_buffer.getvalue(),
            'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S")
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
    return render_template('index.html',
                         default_ta='\n'.join(DEFAULT_TITLE_ABSTRACT_BLACKLIST),
                         default_journal='\n'.join(DEFAULT_JOURNAL_BLACKLIST))


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
                                args=(task_id, df, ta_keywords, journal_keywords, api_key, ai_criteria))
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


@app.route('/download/<task_id>/<filetype>')
def download(task_id, filetype):
    """Download the processed files."""
    print(f"📥 Download request: task_id={task_id}, filetype={filetype}", flush=True)
    
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
        
        if filetype == 'cleaned':
            data = result['cleaned']
            print(f"   Preparing cleaned data: {len(data)} chars", flush=True)
            buffer = io.BytesIO()
            buffer.write(data.encode('utf-8-sig'))
            buffer.seek(0)
            return send_file(buffer, as_attachment=True, 
                            download_name=f'cleaned_data_{timestamp}.csv',
                            mimetype='text/csv')
        
        elif filetype == 'removed':
            data = result['removed']
            print(f"   Preparing removed data: {len(data)} chars", flush=True)
            buffer = io.BytesIO()
            buffer.write(data.encode('utf-8-sig'))
            buffer.seek(0)
            return send_file(buffer, as_attachment=True,
                            download_name=f'removed_data_{timestamp}.csv',
                            mimetype='text/csv')
        
        elif filetype == 'both':
            print(f"   Preparing ZIP file", flush=True)
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.writestr(f'cleaned_data_{timestamp}.csv', 
                           result['cleaned'].encode('utf-8-sig'))
                zf.writestr(f'removed_data_{timestamp}.csv', 
                           result['removed'].encode('utf-8-sig'))
            zip_buffer.seek(0)
            return send_file(zip_buffer, as_attachment=True,
                            download_name=f'screening_results_{timestamp}.zip',
                            mimetype='application/zip')
        
        print(f"❌ Invalid filetype: {filetype}", flush=True)
        return "Invalid file type", 400
        
    except Exception as e:
        print(f"❌ Download Error: {e}", flush=True)
        return f"Server Error: {str(e)}", 500


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("📚 Literature Screening Web App")
    print("=" * 50)
    print("\n🌐 Open your browser and go to: http://127.0.0.1:5000")
    print("   Press Ctrl+C to stop the server\n")
    app.run(debug=True, host='127.0.0.1', port=5000)
