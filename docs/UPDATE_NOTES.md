# Literature Screening Tool v1.1.0 - Update Summary

## 🎯 Major Updates

### 1. Bilingual Interface (中英文切换)
**Location**: Top-right navigation bar
- Instant language switching between English and Chinese
- All UI elements translated
- Language preference saved in browser

**Implementation**:
- JavaScript-based i18n system
- 30+ translation keys
- Persistent storage using localStorage

---

### 2. RIS Format Support (RIS文件支持)

#### Import Capability
- Parse RIS files from reference management software
- Extract title, abstract, journal, authors, year, DOI, keywords
- Automatic conversion to internal DataFrame format

#### Export Capability
- Convert screening results back to RIS format
- Compatible with Zotero, Mendeley, EndNote, RefWorks
- Preserves metadata fields

**Technical Stack**:
- `rispy` library for parsing/serialization
- Bidirectional conversion support

---

### 3. Multiple Export Formats (多格式导出)

**Available Formats**:

| Format | Extension | Use Case |
|--------|-----------|----------|
| CSV | `.csv` | General purpose, Excel, R, Python |
| Excel Modern | `.xlsx` | Excel 2007+ (openpyxl) |
| Excel Legacy | `.xls` | Excel 97-2003 (xlwt) |
| Plain Text | `.txt` | Tab-separated, text editors |
| RIS | `.ris` | Reference managers |

**Features**:
- Single-file download (retained or excluded)
- Batch download (ZIP with both files)
- Format selector in results section
- Real-time filename preview

---

### 4. Professional UI Redesign (专业UI重构)

#### Color Scheme
**Light Mode**:
- Page: #fafafa (minimal gray)
- Cards: #ffffff (pure white)
- Primary: #4f46e5 (indigo)
- Borders: #e5e5e5 (subtle)

**Dark Mode**:
- Page: #0a0a0a (near-black, as requested)
- Cards: #171717 (dark gray)
- Primary: #6366f1 (lighter indigo)
- Enhanced contrast for readability

#### Design Changes
- **Removed excessive emojis**: Only essential icons remain
- **Top navigation bar**: Sticky header with logo and controls
- **Card headers**: Minimalist dot indicator instead of emoji
- **Typography**: JetBrains Mono for code elements
- **Shadows**: Subtle, professional depth
- **Borders**: Clean, thin lines
- **Buttons**: Modern, with hover effects

#### Layout Improvements
- Consistent spacing and padding
- Better visual hierarchy
- Improved form elements
- Enhanced upload zone design

---

## 📋 Technical Implementation Details

### New Dependencies
```python
rispy==0.10.0      # RIS file parsing
xlwt==1.3.0        # Excel legacy format
```

### Modified Files
1. **app.py**: 
   - Added RIS parsing function
   - Added RIS export function
   - Refactored download endpoint (3-parameter URL)
   - DataFrame-based format conversion

2. **templates/index.html**:
   - Complete UI redesign
   - i18n translation system
   - Language toggle logic
   - Updated all text elements

3. **requirements.txt**:
   - Added rispy
   - Added xlwt

### New Files
- `CHANGELOG.md`: Version history
- `USER_GUIDE.md`: Comprehensive usage guide
- `test_data.ris`: Sample RIS file for testing

---

## 🧪 Testing Checklist

- [x] RIS file import
- [x] CSV export
- [x] Excel (.xlsx) export
- [x] Excel (.xls) export
- [x] TXT export
- [x] RIS export
- [x] Language switching
- [x] Theme switching
- [x] Dark mode colors
- [x] Responsive layout
- [x] Multiple file upload
- [x] Format mixing (CSV + RIS + Excel)

---

## 🎨 UI Comparison

### Before (v1.0)
- Emoji-heavy interface (📚 🔍 📊 ✅ ❌)
- Dark mode: #0f172a (slate blue)
- Rounded corners: 16px
- Colorful, consumer-facing style
- Single language (mixed EN/ZH)

### After (v1.1)
- Minimal, professional icons
- Dark mode: #0a0a0a (near-black)
- Rounded corners: 8px (sharper)
- Academic, research-focused style
- Full bilingual support

---

## 🚀 Next Steps for Users

1. **Update Installation**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Restart Application**:
   - Close existing instance
   - Run `start.bat` (Windows) or `./start.sh` (Mac/Linux)

3. **Test New Features**:
   - Upload a RIS file
   - Switch to Chinese interface
   - Try different export formats
   - Check dark mode appearance

4. **Provide Feedback**:
   - Report any bugs
   - Suggest additional languages
   - Request new export formats

---

## 📝 Documentation Updates

Updated files:
- `README.md`: Added v1.1.0 features
- `CHANGELOG.md`: Detailed version history
- `USER_GUIDE.md`: Complete usage instructions

---

## 🔮 Future Considerations

Potential enhancements:
- [ ] More language support (Spanish, French, German)
- [ ] BibTeX format support
- [ ] XML format support
- [ ] Custom theme colors
- [ ] Export format presets
- [ ] Batch processing history
- [ ] Export templates

---

**Version**: 1.1.0  
**Release Date**: December 7, 2025  
**Status**: ✅ Production Ready
