#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test RTF parsing functionality
"""

from striprtf.striprtf import rtf_to_text
import pandas as pd
import re

def parse_rtf_file_test(file_content):
    """
    Test version of parse_rtf_file function
    """
    try:
        # Decode RTF content
        text_content = None
        for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'windows-1252']:
            try:
                rtf_content = file_content.decode(encoding)
                # Convert RTF to plain text
                text_content = rtf_to_text(rtf_content)
                break
            except:
                continue
        
        if text_content is None:
            raise ValueError("Could not decode RTF file with any supported encoding")
        
        records = []
        
        # Try EndNote-style format
        endnote_pattern = r'(?:^|\n)(?=%[A-Z])'
        entries = re.split(endnote_pattern, text_content)
        
        if len(entries) > 1:
            for entry_text in entries:
                if not entry_text.strip():
                    continue
                    
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
                            if current_field == 'title':
                                record['Title'] = value
                            elif current_field == 'abstract':
                                record['Abstract'] = value
                            elif current_field == 'journal':
                                record['Source title'] = value
                            elif current_field == 'author':
                                if record['Authors']:
                                    record['Authors'] += '; ' + value
                                else:
                                    record['Authors'] = value
                            elif current_field == 'year':
                                record['Year'] = value
                            elif current_field == 'doi':
                                record['DOI'] = value
                            elif current_field == 'keywords':
                                record['Keywords'] = value
                            elif current_field == 'url':
                                record['URL'] = value
                            elif current_field == 'type':
                                record['Type'] = value
                        
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
                        if field_content:
                            current_value.append(field_content)
                    else:
                        if current_field:
                            current_value.append(line)
                
                # Save last field
                if current_field and current_value:
                    value = ' '.join(current_value).strip()
                    if current_field == 'title':
                        record['Title'] = value
                    elif current_field == 'abstract':
                        record['Abstract'] = value
                    elif current_field == 'journal':
                        record['Source title'] = value
                    elif current_field == 'author':
                        if record['Authors']:
                            record['Authors'] += '; ' + value
                        else:
                            record['Authors'] = value
                    elif current_field == 'year':
                        record['Year'] = value
                
                if record['Title']:
                    records.append(record)
        
        if not records:
            raise ValueError("Could not extract any bibliographic records from RTF file")
        
        df = pd.DataFrame(records)
        return df
        
    except Exception as e:
        raise ValueError(f"Error parsing RTF file: {str(e)}")

def test_rtf_parsing():
    """Test the RTF file parsing"""
    
    rtf_file_path = '/Users/liyutong/Nutstore Files/我的坚果云/2026-2027春季学期课程文件/元分析/review searching/Literature-Screening-Tool/data/test_data.rtf'
    
    print("Testing RTF file parsing...")
    print("=" * 60)
    
    try:
        # Read RTF file
        with open(rtf_file_path, 'rb') as f:
            file_content = f.read()
        
        # Decode and convert RTF to text
        rtf_content = file_content.decode('utf-8')
        text_content = rtf_to_text(rtf_content)
        
        print("✓ Successfully decoded RTF file")
        print(f"\nExtracted text (first 500 chars):\n{text_content[:500]}")
        print("\n" + "=" * 60)
        
        # Now test with the parse function
        df = parse_rtf_file_test(file_content)
        
        print(f"\n✓ Successfully parsed RTF file!")
        print(f"  Found {len(df)} records\n")
        
        print("DataFrame columns:", list(df.columns))
        print("\nFirst record:")
        for col in df.columns:
            value = df.iloc[0][col]
            if value:
                print(f"  {col}: {value[:100] if len(str(value)) > 100 else value}")
        
        print("\n" + "=" * 60)
        print("All records (Title and Year only):")
        for idx, row in df.iterrows():
            print(f"  {idx + 1}. {row['Title']} ({row['Year']})")
        
        print("\n✅ RTF parsing test PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ RTF parsing test FAILED!")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_rtf_parsing()
