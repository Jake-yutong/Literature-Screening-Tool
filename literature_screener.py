#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Literature Screening Tool for Meta-Analysis / Bibliometrics
文献粗筛工具 - 用于元分析/文献计量学研究

Author: Auto-generated for research purposes
Usage: python literature_screener.py

This script automates the initial screening process for systematic reviews
by filtering literature based on title, abstract, and journal keywords.
"""

import pandas as pd
import os
import sys
from datetime import datetime
from pathlib import Path


# ============================================================================
# 🔧 CONFIGURATION SECTION - 配置区域
# Modify these lists according to your research needs
# 根据你的研究需求修改这些列表
# ============================================================================

# 📋 Keywords to EXCLUDE in Title or Abstract (case-insensitive)
# 在标题或摘要中需要排除的关键词（不区分大小写）
TITLE_ABSTRACT_BLACKLIST = [
    # Medical/Clinical terms - 医学/临床术语
    "surgical", "surgery", "patient", "patients", "clinical trial",
    "hospital", "physician", "nurse", "disease", "therapy", "therapeutic",
    "diagnosis", "treatment", "medication", "drug", "pharmaceutical",
    "pathology", "symptom", "syndrome", "cancer", "tumor", "tumour",
    
    # Sports/Physical terms - 体育/运动术语
    "athlete", "athletes", "sports", "swimming", "football", "basketball",
    "soccer", "marathon", "Olympic", "championship",
    
    # Game theory & unrelated fields - 博弈论及不相关领域
    "game theory", "game-theoretic", "poker", "chess", "video game",
    
    # Chemistry/Physics terms - 化学/物理术语
    "molecular", "molecule", "chemical", "chemistry", "physics",
    "quantum", "atomic", "electron", "polymer", "catalyst",
    
    # Biology/Life sciences - 生物/生命科学
    "genome", "genomic", "protein", "enzyme", "bacteria", "virus",
    "cell culture", "in vitro", "in vivo", "rodent", "mice", "rats",
    
    # Add your own keywords below - 在下方添加你自己的关键词
    # "your_keyword_here",
]

# 📰 Keywords to EXCLUDE in Source Title / Journal Name (case-insensitive)
# 在期刊名称中需要排除的关键词（不区分大小写）
JOURNAL_BLACKLIST = [
    # Medical journals - 医学期刊
    "medicine", "medical", "clinical", "surgery", "surgical",
    "hospital", "health", "nursing", "pharmacy", "pharmacology",
    "oncology", "cardiology", "neurology", "psychiatry", "pediatric",
    
    # Chemistry/Physics journals - 化学/物理期刊
    "chemistry", "chemical", "physics", "physical",
    
    # Biology journals - 生物期刊
    "biology", "biological", "biochemistry", "microbiology",
    "genetics", "genomics", "molecular", "cell",
    
    # Sports journals - 体育期刊
    "sports", "sport", "athletic", "exercise", "physical education",
    
    # Add your own journal keywords below - 在下方添加你自己的期刊关键词
    # "your_journal_keyword_here",
]

# 📊 Column name mappings (adjust based on your data source)
# 列名映射（根据你的数据来源调整）
# Supports: Web of Science, Scopus, and common export formats
COLUMN_MAPPINGS = {
    # Title columns
    "title": ["Title", "title", "TI", "Article Title", "Document Title"],
    # Abstract columns  
    "abstract": ["Abstract", "abstract", "AB", "Description"],
    # Source/Journal columns
    "source": ["Source Title", "source title", "SO", "Source", "Journal", 
               "Publication Name", "Publication", "Journal Title"],
}


# ============================================================================
# 🚀 MAIN SCREENING LOGIC - 主筛选逻辑
# ============================================================================

def find_column(df: pd.DataFrame, column_type: str) -> str | None:
    """Find the actual column name in the dataframe based on mappings."""
    possible_names = COLUMN_MAPPINGS.get(column_type, [])
    for name in possible_names:
        if name in df.columns:
            return name
    return None


def contains_blacklisted_keyword(text: str, blacklist: list) -> tuple[bool, str]:
    """
    Check if text contains any blacklisted keyword.
    Returns (is_blacklisted, matched_keyword).
    """
    if pd.isna(text) or not isinstance(text, str):
        return False, ""
    
    text_lower = text.lower()
    for keyword in blacklist:
        if keyword.lower() in text_lower:
            return True, keyword
    return False, ""


def screen_literature(input_file: str, output_dir: str = None) -> dict:
    """
    Main screening function.
    
    Args:
        input_file: Path to the input Excel/CSV file
        output_dir: Directory for output files (defaults to input file's directory)
    
    Returns:
        Dictionary with screening statistics
    """
    print("\n" + "=" * 60)
    print("📚 LITERATURE SCREENING TOOL / 文献筛选工具")
    print("=" * 60)
    
    # Determine file type and read data
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"❌ Error: File not found - {input_file}")
        sys.exit(1)
    
    print(f"\n📂 Reading file: {input_path.name}")
    
    if input_path.suffix.lower() in ['.xlsx', '.xls']:
        df = pd.read_excel(input_file, engine='openpyxl')
    elif input_path.suffix.lower() == '.csv':
        # Try different encodings
        for encoding in ['utf-8', 'utf-8-sig', 'gbk', 'latin-1']:
            try:
                df = pd.read_csv(input_file, encoding=encoding)
                break
            except UnicodeDecodeError:
                continue
        else:
            print("❌ Error: Could not decode CSV file with common encodings")
            sys.exit(1)
    else:
        print(f"❌ Error: Unsupported file format - {input_path.suffix}")
        print("   Supported formats: .xlsx, .xls, .csv")
        sys.exit(1)
    
    total_records = len(df)
    print(f"   Total records loaded: {total_records:,}")
    print(f"   Columns detected: {list(df.columns)[:5]}...")
    
    # Find relevant columns
    title_col = find_column(df, "title")
    abstract_col = find_column(df, "abstract")
    source_col = find_column(df, "source")
    
    print(f"\n🔍 Column Detection:")
    print(f"   Title column: {title_col or '❌ Not found'}")
    print(f"   Abstract column: {abstract_col or '❌ Not found'}")
    print(f"   Source/Journal column: {source_col or '❌ Not found'}")
    
    if not title_col:
        print("\n⚠️  Warning: No title column found. Screening accuracy may be reduced.")
    
    # Initialize tracking columns
    df['_EXCLUDED'] = False
    df['_EXCLUSION_REASON'] = ''
    
    # Screening process
    print(f"\n⏳ Screening in progress...")
    
    excluded_count = 0
    title_abstract_excluded = 0
    journal_excluded = 0
    
    for idx, row in df.iterrows():
        exclusion_reasons = []
        
        # Check Title
        if title_col:
            is_excluded, keyword = contains_blacklisted_keyword(
                row[title_col], TITLE_ABSTRACT_BLACKLIST
            )
            if is_excluded:
                exclusion_reasons.append(f"Title contains: '{keyword}'")
        
        # Check Abstract
        if abstract_col:
            is_excluded, keyword = contains_blacklisted_keyword(
                row[abstract_col], TITLE_ABSTRACT_BLACKLIST
            )
            if is_excluded:
                exclusion_reasons.append(f"Abstract contains: '{keyword}'")
        
        # Count title/abstract exclusions
        if exclusion_reasons:
            title_abstract_excluded += 1
        
        # Check Source/Journal
        if source_col:
            is_excluded, keyword = contains_blacklisted_keyword(
                row[source_col], JOURNAL_BLACKLIST
            )
            if is_excluded:
                exclusion_reasons.append(f"Journal contains: '{keyword}'")
                if len(exclusion_reasons) == 1:  # Only journal exclusion
                    journal_excluded += 1
        
        # Mark as excluded if any reason found
        if exclusion_reasons:
            df.at[idx, '_EXCLUDED'] = True
            df.at[idx, '_EXCLUSION_REASON'] = ' | '.join(exclusion_reasons)
            excluded_count += 1
    
    # Split into kept and removed dataframes
    df_kept = df[df['_EXCLUDED'] == False].drop(columns=['_EXCLUDED', '_EXCLUSION_REASON'])
    df_removed = df[df['_EXCLUDED'] == True].copy()
    df_removed = df_removed.rename(columns={'_EXCLUSION_REASON': 'Exclusion_Reason'})
    df_removed = df_removed.drop(columns=['_EXCLUDED'])
    
    # Output setup
    if output_dir is None:
        output_dir = input_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save cleaned data
    cleaned_file = output_dir / f"cleaned_data_{timestamp}.csv"
    df_kept.to_csv(cleaned_file, index=False, encoding='utf-8-sig')
    
    # Save removed data
    removed_file = output_dir / f"removed_data_{timestamp}.csv"
    df_removed.to_csv(removed_file, index=False, encoding='utf-8-sig')
    
    # Calculate statistics
    kept_count = len(df_kept)
    kept_percentage = (kept_count / total_records * 100) if total_records > 0 else 0
    
    # Print results
    print("\n" + "=" * 60)
    print("📊 SCREENING RESULTS / 筛选结果")
    print("=" * 60)
    print(f"""
    📥 Input records:           {total_records:,}
    ✅ Retained (clean):        {kept_count:,} ({kept_percentage:.1f}%)
    ❌ Excluded (removed):      {excluded_count:,} ({100-kept_percentage:.1f}%)
    
    Exclusion breakdown:
    ├─ Title/Abstract keywords: {title_abstract_excluded:,}
    └─ Journal name keywords:   {journal_excluded:,}
    
    📁 Output files:
    ├─ {cleaned_file.name}
    └─ {removed_file.name}
    
    📍 Output directory: {output_dir}
    """)
    
    print("=" * 60)
    print("✨ Screening complete! / 筛选完成！")
    print("=" * 60)
    
    # Tips
    print("""
💡 NEXT STEPS / 后续步骤:
   1. Check 'removed_data_*.csv' to verify no important papers were excluded
      检查 removed_data 文件，确认没有误删重要文献
   
   2. Import 'cleaned_data_*.csv' into VOSviewer for analysis
      将 cleaned_data 导入 VOSviewer 进行分析
   
   3. Use the exclusion data for PRISMA flow diagram
      使用排除数据绘制 PRISMA 流程图
    """)
    
    return {
        'total': total_records,
        'kept': kept_count,
        'excluded': excluded_count,
        'cleaned_file': str(cleaned_file),
        'removed_file': str(removed_file),
    }


# ============================================================================
# 🎯 ENTRY POINT - 程序入口
# ============================================================================

def main():
    """Main entry point with interactive mode."""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   📚 Literature Screening Tool for Meta-Analysis          ║
    ║   文献粗筛工具 - 元分析/文献计量学研究                      ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Check for command line argument
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        # Interactive mode
        print("Please enter the path to your literature file (Excel or CSV):")
        print("请输入文献文件的路径（支持 Excel 或 CSV）:\n")
        input_file = input(">>> ").strip().strip('"').strip("'")
    
    if not input_file:
        print("❌ No file provided. Exiting.")
        sys.exit(1)
    
    # Run screening
    results = screen_literature(input_file)
    
    print("\n🎉 All done! Press Enter to exit...")
    input()


if __name__ == "__main__":
    main()
