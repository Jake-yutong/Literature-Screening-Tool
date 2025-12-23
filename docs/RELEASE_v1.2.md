# Literature Screening Tool v1.2.0 Release Notes

**Release Date**: December 11, 2025

## 🎉 Major Update: Multi-Model AI Support

We're excited to announce version 1.2.0 with support for multiple AI models! Users can now choose between DeepSeek Chat and MiniMax-M2 for intelligent literature screening.

---

## ✨ New Features

### 🤖 Multi-Model AI Support
- **DeepSeek Chat**: Fast, cost-effective AI screening (existing feature, now selectable)
- **MiniMax-M2**: Advanced reasoning capabilities with thinking process visualization
- **Model Selector**: Easy-to-use dropdown menu in the interface
- **Unified API Key Input**: Single field for all AI providers

### 🔄 MiniMax-M2 Integration
- Powered by Anthropic SDK
- Advanced reasoning with explicit thinking blocks
- Support for multi-turn conversations
- Automatic endpoint configuration:
  - China users: `https://api.minimaxi.com/anthropic`
  - International users: `https://api.minimax.io/anthropic`

### 🌍 Intelligent API Routing
- Automatic base URL selection based on model choice
- Environment variable configuration for MiniMax
- Seamless switching between providers
- No code changes needed for different models

---

## 🔧 Technical Improvements

### Dependencies
- ✅ Added `anthropic` SDK (v0.75.0)
- ✅ Updated `requirements.txt`

### Backend Enhancements
- Model-specific API call routing
- Enhanced error handling for multiple providers
- kwargs support in screening threads
- Complete conversation history preservation
- Backward compatibility maintained

### Frontend Updates
- Model selection dropdown in UI
- Updated internationalization (EN/中文)
- Model-agnostic API key labels
- Version updated to v1.2

---

## 📚 Documentation Updates

### README.md
- Added AI Configuration section
- DeepSeek setup guide
- MiniMax-M2 setup guide
- Updated dependency table
- Enhanced usage instructions

### CHANGELOG.md
- Complete version history
- Detailed feature descriptions
- Technical improvement notes
- Breaking changes (none!)

---

## 🚀 Getting Started with v1.2

### Installation

```bash
# Clone or pull latest version
git clone https://github.com/Jake-yutong/Literature-Screening-Tool.git
cd Literature-Screening-Tool

# Update dependencies
pip install -r requirements.txt

# Launch
python app.py
```

### Using DeepSeek Chat

1. Get API key from [DeepSeek Platform](https://platform.deepseek.com/)
2. Select "DeepSeek Chat" in model dropdown
3. Enter API key
4. Add exclusion criteria
5. Start screening

### Using MiniMax-M2

1. Get API key from [MiniMax Platform](https://platform.minimaxi.com/)
2. Select "MiniMax-M2" in model dropdown
3. Enter API key
4. Add exclusion criteria
5. Start screening

---

## 🔍 What's Different?

### Before (v1.1)
```python
# Only DeepSeek was supported
# API key was hardcoded to DeepSeek endpoint
```

### After (v1.2)
```python
# Multiple models supported
ai_model = 'deepseek'  # or 'minimax'
# Automatic endpoint configuration
# Flexible model switching
```

---

## 🛠️ Migration Guide

**Good News**: No breaking changes! All existing functionality remains the same.

If you're upgrading from v1.1:
1. Pull latest code: `git pull origin main`
2. Update dependencies: `pip install -r requirements.txt`
3. Restart application: `python app.py`

Your existing DeepSeek API keys will work exactly as before. The new model selector defaults to DeepSeek for backward compatibility.

---

## 🐛 Known Issues

None reported yet! Please submit issues to [GitHub Issues](https://github.com/Jake-yutong/Literature-Screening-Tool/issues)

---

## 🙏 Acknowledgments

Special thanks to:
- **Anthropic** for the excellent SDK
- **MiniMax** for the powerful M2 model
- **DeepSeek** for reliable API service
- All users who requested multi-model support

---

## 📊 Statistics

- **Files Changed**: 5
- **Lines Added**: 208
- **Lines Removed**: 39
- **New Dependencies**: 1 (anthropic)
- **New Features**: 4 major
- **Breaking Changes**: 0

---

## 🔮 What's Next?

Planned for v1.3:
- Additional AI model support (Claude, GPT-4, etc.)
- Batch processing optimization
- Advanced filtering options
- Real-time collaboration features

---

## 📞 Support

- **Documentation**: [README.md](./README.md)
- **Issues**: [GitHub Issues](https://github.com/Jake-yutong/Literature-Screening-Tool/issues)
- **Changelog**: [CHANGELOG.md](./CHANGELOG.md)

---

**Happy Screening! 🎓📚**

*Literature Screening Tool Team*
