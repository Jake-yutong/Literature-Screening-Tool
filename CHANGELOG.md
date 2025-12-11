# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2025-12-11

### Added
- **Multi-Model AI Support**: Choose between different AI providers for screening
  - DeepSeek Chat (OpenAI SDK)
  - MiniMax-M2 (Anthropic SDK)
- **Model Selection Interface**: Dropdown menu to switch between AI models
- **MiniMax-M2 Integration**:
  - Advanced reasoning with thinking process
  - Anthropic SDK implementation
  - Automatic API endpoint configuration (China/International)
  - Full support for multi-turn conversations with complete message history
- **Enhanced API Management**: 
  - Unified API key input for all models
  - Automatic base URL configuration per model
  - Environment variable handling for MiniMax

### Changed
- Updated application version to 1.2.0
- Improved AI screening logic to support multiple model backends
- Enhanced error handling for different AI providers
- Updated UI labels to be model-agnostic (changed "DeepSeek API Key" to "API Key")

### Technical Improvements
- Added `anthropic` SDK dependency (v0.75.0)
- Implemented model-specific API call routing
- Added kwargs support in screening thread for model selection
- Updated verification logic for both OpenAI and Anthropic SDKs
- Maintained backward compatibility with existing DeepSeek implementation

### Documentation
- Updated README with AI configuration sections for both models
- Added MiniMax-M2 setup instructions
- Updated dependency table with anthropic package
- Enhanced usage instructions with model selection steps

## [1.1.0] - 2025-12-07

### Added
- **Bilingual Support**: Full English/Chinese interface with instant language switching
- **RIS Format Support**: 
  - Import RIS files from reference management software
  - Export screening results to RIS format for Zotero, Mendeley, EndNote
- **Multiple Export Formats**: Choose from CSV, Excel (.xlsx/.xls), TXT, or RIS
- **Professional UI Redesign**:
  - Academic-style interface with refined typography
  - Enhanced dark mode with near-black background (#0a0a0a)
  - Sticky navigation bar with language and theme controls
  - Improved button and card designs
  - Version tag display

### Changed
- Reduced emoji usage for more professional appearance
- Improved color scheme for better contrast and readability
- Updated typography with JetBrains Mono for code elements
- Enhanced hover effects and transitions
- Optimized shadow and border styles

### Technical Improvements
- Added `rispy` library for RIS file parsing and generation
- Added `xlwt` library for legacy Excel export (.xls)
- Refactored download endpoint to support multiple format conversions
- Improved DataFrame storage in session for flexible format conversion
- Enhanced file type validation and error handling

## [1.0.0] - 2024

### Initial Release
- CSV, Excel, and TXT file import
- Web of Science format auto-detection and conversion
- Keyword-based screening (title, abstract, journal)
- AI-powered screening with DeepSeek API
- Dual output (retained and excluded records)
- Progress tracking for long-running tasks
- Dark/light theme support
