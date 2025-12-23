# 📚 Literature Screening Tool

用于元分析和文献计量的自动化系统筛选工具 / Automated Literature Screening Tool for Meta-Analysis

[![Version](https://img.shields.io/badge/version-1.2.1-blue.svg)](https://github.com/Jake-yutong/Literature-Screening-Tool)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🚀 快速开始 / Quick Start

```bash
# 安装依赖 / Install dependencies
pip install -r requirements.txt

# 启动应用 / Start application
python app.py

# 或使用启动脚本 / Or use launch script
python scripts/launch.py
```

访问 http://127.0.0.1:5000

## ✨ 核心功能 / Features

- 📁 **多格式支持** - CSV, Excel, RIS, BibTeX, TXT
- 🔍 **关键词筛选** - 标题/摘要/期刊黑名单
- 🤖 **AI智能筛选** - 基于DeepSeek API的二次验证
- 🔄 **智能去重** - DOI和标题双重匹配
- 🌐 **双语界面** - 中文/English即时切换
- 🎨 **专业UI** - 深色/浅色主题

## 📁 项目结构 / Project Structure

```
Literature-Screening-Tool/
├── app.py                  # Flask主应用
├── requirements.txt        # Python依赖
├── Procfile               # 部署配置
├── literature_screener.py # 核心筛选逻辑
├── templates/             # HTML模板
│   └── index.html
├── static/                # 静态资源
├── docs/                  # 📖 文档
│   ├── README.md          # 详细文档
│   ├── USER_GUIDE.md      # 用户指南
│   ├── CHANGELOG.md       # 更新日志
│   ├── AI_MODEL_GUIDE.md  # AI模型说明
│   └── ...
├── scripts/               # 🛠️ 脚本
│   ├── launch.py          # 启动脚本
│   ├── start.sh           # Linux启动
│   └── start.bat          # Windows启动
├── tests/                 # 🧪 测试
│   └── verify_app.py
└── data/                  # 📊 测试数据
    ├── test_data.csv
    ├── test_data.ris
    └── test_data.bib
```

## 📖 详细文档 / Documentation

- [完整文档](docs/README.md) - 完整的使用说明
- [用户指南](docs/USER_GUIDE.md) - 详细操作步骤
- [更新日志](docs/CHANGELOG.md) - 版本历史
- [AI模型指南](docs/AI_MODEL_GUIDE.md) - AI筛选说明

## 🔧 开发 / Development

```bash
# 安装开发依赖
pip install -r requirements.txt

# 运行测试
python tests/verify_app.py

# 启动开发服务器
python app.py
```

## 📝 版本 / Version

当前版本: **v1.2.1** (2025-12-11)

查看 [更新日志](docs/CHANGELOG.md) 了解详细更新内容

## 🤝 贡献 / Contributing

欢迎提交 Issue 和 Pull Request！

## 📄 许可证 / License

MIT License - 详见 LICENSE 文件

## 👨‍💻 作者 / Author

LI Yutong (Jake) - [GitHub](https://github.com/Jake-yutong)

---

⭐ 如果这个项目对您有帮助，请给它一个星标！

