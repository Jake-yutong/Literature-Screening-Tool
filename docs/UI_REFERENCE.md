# v1.1.0 UI Features 界面功能说明

## 🌐 Top Navigation Bar (顶部导航栏)

```
┌────────────────────────────────────────────────────────────┐
│  Literature Screening Tool         [🌐 EN] [☀]            │
└────────────────────────────────────────────────────────────┘
```

**Components**:
- **Left**: Application title (click area reserved for future home link)
- **Right**: 
  - Language toggle button (🌐 EN/ZH)
  - Theme toggle button (☀ Light / ☾ Dark)

**Functionality**:
- Sticky positioning (stays on top while scrolling)
- Instant language switching without page reload
- Theme preference saved in browser

---

## 📤 Upload Section (上传区域)

```
┌─────────────────────────────────────────────┐
│ ● Upload Literature Files                   │
├─────────────────────────────────────────────┤
│                                              │
│         ┌──────────┐                        │
│         │    ↑     │                        │
│         └──────────┘                        │
│                                              │
│   Click to upload or drag and drop          │
│   Support multiple files                    │
│                                              │
│   [.xlsx .xls .csv .ris .txt]               │
│                                              │
├─────────────────────────────────────────────┤
│  [      Start Screening      ]              │
└─────────────────────────────────────────────┘
```

**Key Changes**:
- Removed emoji icons (📁, ⬆️)
- Replaced with minimalist bordered icon
- Professional monospace format display
- Clear call-to-action

---

## ⚙️ Settings Section (设置区域)

```
┌─────────────────────────────────────────────┐
│ ● Screening Settings                        │
├─────────────────────────────────────────────┤
│                                              │
│ Title/Abstract Exclusion Keywords            │
│ One keyword per line                        │
│ ┌─────────────────────────────────────────┐ │
│ │ surgical                                 │ │
│ │ patient                                  │ │
│ │ clinical trial                           │ │
│ └─────────────────────────────────────────┘ │
│                                              │
│ Journal Exclusion Keywords                   │
│ One keyword per line                        │
│ ┌─────────────────────────────────────────┐ │
│ │ medicine                                 │ │
│ │ clinical                                 │ │
│ └─────────────────────────────────────────┘ │
│                                              │
│ ─────────────────────────────────────────   │
│                                              │
│ AI-Powered Screening (Optional)              │
│ DeepSeek API Key                            │
│ ┌─────────────────────────────────────────┐ │
│ │ sk-...                                   │ │
│ └─────────────────────────────────────────┘ │
│                                              │
│ Natural language exclusion criteria          │
│ ┌─────────────────────────────────────────┐ │
│ │                                          │ │
│ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

**Key Changes**:
- Removed 🏷️ and 🤖 emojis
- Clean section headers with dot indicator
- Italic hint text
- Consistent spacing

---

## 📊 Results Section (结果区域)

```
┌─────────────────────────────────────────────┐
│ ● Screening Results                         │
├─────────────────────────────────────────────┤
│                                              │
│ Title Column:        ✓ Title                │
│ Abstract Column:     ✓ Abstract             │
│ Journal Column:      ✓ Source title         │
│                                              │
├─────────────────────────────────────────────┤
│                                              │
│    ┌──────────┐  ┌──────────┐  ┌──────────┐│
│    │   1000   │  │   847    │  │   153    ││
│    │  Total   │  │ Retained │  │ Excluded ││
│    └──────────┘  └──────────┘  └──────────┘│
│                                              │
├─────────────────────────────────────────────┤
│                                              │
│ Export Format                                │
│ ┌─────────────────────────────────────────┐ │
│ │ CSV (Comma-Separated Values)         ▼ │ │
│ └─────────────────────────────────────────┘ │
│                                              │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────┐│
│ │  Download   │ │  Download   │ │Download ││
│ │  Retained   │ │  Excluded   │ │All (ZIP)││
│ │cleaned.csv  │ │removed.csv  │ │results  ││
│ └─────────────┘ └─────────────┘ └─────────┘│
└─────────────────────────────────────────────┘
```

**Key Changes**:
- Removed 📊, ✅, ❌ emojis from headers
- Clean text-only buttons
- Format selector with 5 options
- Professional color coding (green for success, red for exclusion)

---

## 🎨 Color Palette

### Light Mode
```
Primary:      #4f46e5  ████  (Indigo)
Success:      #16a34a  ████  (Green)
Danger:       #dc2626  ████  (Red)
Background:   #fafafa  ████  (Light Gray)
Card:         #ffffff  ████  (White)
Text:         #171717  ████  (Near Black)
Border:       #e5e5e5  ████  (Light Border)
```

### Dark Mode
```
Primary:      #6366f1  ████  (Light Indigo)
Success:      #22c55e  ████  (Light Green)
Danger:       #ef4444  ████  (Light Red)
Background:   #0a0a0a  ████  (Near Black) ← Key change!
Card:         #171717  ████  (Dark Gray)
Text:         #fafafa  ████  (Off White)
Border:       #262626  ████  (Dark Border)
```

---

## 🔤 Typography

**Font Families**:
- **Body Text**: Inter, system fonts
- **Code/Technical**: JetBrains Mono (for version tag, formats)

**Font Sizes**:
- Headers: 1.125rem (18px)
- Body: 0.9375rem (15px)
- Hints: 0.8125rem (13px)
- Code: 0.75rem (12px)

**Font Weights**:
- Regular: 400
- Medium: 500
- Semibold: 600
- Bold: 700

---

## 📐 Spacing & Layout

**Border Radius**:
- Cards: 8px (reduced from 16px)
- Buttons: 6px (reduced from 8px)
- Inputs: 6px
- Badges: 4px

**Shadows**:
- Small: `0 1px 2px rgba(0,0,0,0.05)`
- Medium: `0 4px 6px rgba(0,0,0,0.08)`
- Large: `0 10px 15px rgba(0,0,0,0.08)`

**Padding**:
- Cards: 1.75rem (28px)
- Buttons: 0.75rem × 1.25rem
- Inputs: 0.75rem

---

## 🌍 Language Support

### English (EN)
- Professional, academic tone
- Full technical terminology
- Clear, concise instructions

### 中文 (ZH)
- 正式的学术语气
- 完整的技术术语翻译
- 清晰简洁的说明

**Implementation**:
- 30+ translation keys
- Data attributes: `data-i18n="key"`
- JavaScript i18n object
- localStorage persistence

---

## 💾 Export Formats

| Icon | Format | MIME Type |
|------|--------|-----------|
| 📄 | CSV | text/csv |
| 📊 | XLSX | application/vnd.openxmlformats... |
| 📊 | XLS | application/vnd.ms-excel |
| 📝 | TXT | text/plain |
| 📚 | RIS | application/x-research-info-systems |

---

## 🎯 Interaction States

**Buttons**:
- Default: Border, subtle background
- Hover: Darker background, shadow
- Active/Focus: Primary color, ring
- Disabled: Gray, no cursor

**Inputs**:
- Default: Light border, light background
- Focus: Primary border, shadow ring
- Error: Red border, red background tint

**Cards**:
- Default: Subtle shadow
- Hover: Enhanced shadow (lift effect)

---

## 📱 Responsive Breakpoints

```
Desktop:  > 768px  → 2-column grid
Tablet:   ≤ 768px  → 1-column stack
Mobile:   < 640px  → Reduced padding
```

**Adaptations**:
- Navigation: Always full width
- Grid: Collapses to single column
- Buttons: Maintain full width
- Text: Scales proportionally

---

## ✨ Animation & Transitions

**Timing**:
- Default: 0.2s ease
- Theme switch: 0.3s ease
- Shadows: 0.3s ease

**Effects**:
- Button hover: Scale, shadow
- Card hover: Shadow lift
- Theme toggle: Smooth color transition
- Language switch: Instant text replacement

---

## 🔒 Accessibility

**Improvements**:
- Semantic HTML elements
- ARIA labels on buttons
- Keyboard navigation support
- High contrast in both themes
- Focus indicators
- Alt text for icons (when applicable)

---

**Note**: This is a text representation of the UI. For actual screenshots, run the application and capture screens in both light/dark modes and both languages.
