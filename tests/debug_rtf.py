#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug RTF parsing
"""

from striprtf.striprtf import rtf_to_text
import pandas as pd
import re

rtf_file_path = '/Users/liyutong/Nutstore Files/我的坚果云/2026-2027春季学期课程文件/元分析/review searching/Literature-Screening-Tool/data/test_data.rtf'

with open(rtf_file_path, 'rb') as f:
    file_content = f.read()

rtf_content = file_content.decode('utf-8')
text_content = rtf_to_text(rtf_content)

records = []
entries = re.split(r'\n\s*\n+', text_content)

for entry_idx, entry_text in enumerate(entries):
    entry_text = entry_text.strip()
    if not entry_text or not entry_text.startswith('%'):
        continue
        
    print(f"\n=== Processing Entry {entry_idx} ===")
    
    record = {
        'Title': '',
        'Abstract': '',
        'Source title': '',
        'Authors': '',
        'Year': '',
        'DOI': '',
        'Keywords': '',
        'Type': '',
        'URL': '',
    }
    
    lines = entry_text.split('\n')
    current_field = None
    current_value = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith('%'):
            # Save previous field
            if current_field and current_value:
                value = ' '.join(current_value).strip()
                print(f"  Saving {current_field} = {value[:50]}")
                if current_field == 'title':
                    record['Title'] = value
                elif current_field == 'abstract':
                    record['Abstract'] = value
                elif current_field == 'journal':
                    record['Source title'] = value
                elif current_field == 'author':
                    record['Authors'] = value
                elif current_field == 'year':
                    record['Year'] = value
                    print(f"    *** YEAR SET TO: {record['Year']}")
                elif current_field == 'doi':
                    record['DOI'] = value
                elif current_field == 'keywords':
                    record['Keywords'] = value
                elif current_field == 'url':
                    record['URL'] = value
                elif current_field == 'type':
                    record['Type'] = value
            
            # Start new field
            current_value = []
            field_code = line[1:2].upper()
            field_content = line[2:].strip()
            
            field_map = {
                'T': 'title',
                'A': 'author',
                'J': 'journal',
                'D': 'year',
                'K': 'keywords',
                'X': 'abstract',
                'N': 'abstract',
                'U': 'url',
                'R': 'doi',
                '0': 'type',
            }
            
            current_field = field_map.get(field_code)
            print(f"  New field: {line[:20]} -> field_code={field_code} -> {current_field}")
            if field_content:
                current_value.append(field_content)
        else:
            if current_field:
                current_value.append(line)
    
    # Save last field
    if current_field and current_value:
        value = ' '.join(current_value).strip()
        print(f"  Saving LAST {current_field} = {value[:50]}")
        if current_field == 'title':
            record['Title'] = value
        elif current_field == 'abstract':
            record['Abstract'] = value
        elif current_field == 'journal':
            record['Source title'] = value
        elif current_field == 'author':
            record['Authors'] = value
        elif current_field == 'year':
            record['Year'] = value
            print(f"    *** YEAR SET TO: {record['Year']}")
        elif current_field == 'doi':
            record['DOI'] = value
        elif current_field == 'keywords':
            record['Keywords'] = value
        elif current_field == 'url':
            record['URL'] = value
        elif current_field == 'type':
            record['Type'] = value
    
    if record['Title']:
        print(f"\n  Final record: Title={record['Title'][:40]}, Year={record['Year']}")
        records.append(record)

df = pd.DataFrame(records)
print(f"\n\n=== FINAL DATAFRAME ===")
print(df[['Title', 'Year', 'Authors']])
