# Literature Screening Tool v1.2.0 - 发布总结

## 🎉 发布完成！

**版本号**: v1.2.0  
**发布日期**: 2025年12月11日  
**提交SHA**: 759b16e

---

## ✅ 完成的工作

### 1. 核心功能开发

#### 🤖 多模型AI支持
- ✅ DeepSeek Chat集成（OpenAI SDK）
- ✅ MiniMax-M2集成（Anthropic SDK）
- ✅ 模型选择界面（下拉菜单）
- ✅ 自动API端点配置
- ✅ 完整对话历史支持

#### 🔧 后端实现
```python
# 添加的主要功能
- 模型选择参数传递
- API路由逻辑（根据模型选择不同SDK）
- MiniMax思维块解析
- DeepSeek和MiniMax的双重验证逻辑
- 环境变量配置支持
```

#### 🎨 前端界面
- ✅ 模型选择下拉菜单
- ✅ 统一API密钥输入
- ✅ 双语支持（中英文）
- ✅ 版本号更新到v1.2

### 2. 依赖管理

**新增依赖:**
```
anthropic==0.75.0
```

**requirements.txt更新:**
```
flask
pandas
openpyxl
xlrd
xlwt
rispy
bibtexparser
openai
anthropic  ← 新增
gunicorn
```

### 3. 文档完善

#### 📚 创建的文档
1. **RELEASE_v1.2.md** - 详细发布说明
   - 新功能介绍
   - 技术改进
   - 迁移指南
   - 已知问题

2. **AI_MODEL_GUIDE.md** - 模型选择指南
   - 双语对照
   - 使用场景建议
   - 成本估算
   - 性能对比
   - 常见问题

3. **CHANGELOG.md更新**
   - v1.2.0变更记录
   - 完整功能列表
   - 技术改进说明

4. **README.md更新**
   - AI配置章节
   - DeepSeek设置指南
   - MiniMax设置指南
   - 更新依赖表格

### 4. 代码质量

#### 语法检查
```bash
✅ Python语法检查通过
✅ 无编译错误
✅ 应用成功启动
```

#### Git管理
```
✅ 所有更改已提交
✅ 版本标签正确
✅ .gitignore已更新
✅ 测试文件已排除
```

---

## 📊 变更统计

### 提交记录
```
fea4dc6 - Update .gitignore to exclude test files and user data
25bdd23 - Add v1.2 release documentation
759b16e - Release v1.2.0: Multi-Model AI Support
```

### 文件变更
| 文件 | 变更类型 | 行数 |
|------|---------|------|
| app.py | 修改 | +134 / -24 |
| requirements.txt | 修改 | +1 |
| templates/index.html | 修改 | +20 / -5 |
| README.md | 修改 | +38 / -8 |
| CHANGELOG.md | 修改 | +42 |
| RELEASE_v1.2.md | 新增 | +173 |
| AI_MODEL_GUIDE.md | 新增 | +303 |
| .gitignore | 修改 | +13 |

**总计:**
- 5个文件修改
- 2个新文件
- 约520行新增代码/文档
- 约37行删除

---

## 🧪 测试验证

### ✅ 功能测试
- [x] 应用启动成功
- [x] 端口自动检测正常
- [x] 界面显示正确
- [x] 模型选择器显示
- [x] 双语切换正常

### ⏳ 待用户测试
- [ ] DeepSeek API调用
- [ ] MiniMax-M2 API调用
- [ ] 模型切换功能
- [ ] 完整筛选流程
- [ ] 导出功能

---

## 🚀 部署状态

### GitHub仓库
- **仓库**: Jake-yutong/Literature-Screening-Tool
- **分支**: main
- **最新提交**: fea4dc6
- **状态**: ✅ 已同步

### 可用版本
```bash
# 克隆最新版本
git clone https://github.com/Jake-yutong/Literature-Screening-Tool.git

# 或拉取更新
git pull origin main
```

---

## 📝 使用示例

### 选择DeepSeek模型
```python
1. 打开工具界面
2. 选择 "DeepSeek Chat"
3. 输入DeepSeek API密钥
4. 添加筛选标准
5. 开始筛选
```

### 选择MiniMax-M2模型
```python
1. 打开工具界面
2. 选择 "MiniMax-M2"
3. 输入MiniMax API密钥
4. 添加筛选标准
5. 开始筛选
```

---

## 🎯 下一步计划

### v1.3候选功能
1. **更多AI模型支持**
   - Claude 3.5
   - GPT-4
   - Gemini Pro

2. **性能优化**
   - 批量处理优化
   - 缓存机制
   - 并行处理

3. **高级功能**
   - 自定义提示词模板
   - 筛选历史记录
   - 协作功能

---

## 🙏 致谢

感谢以下技术和平台：
- **Anthropic**: 提供优秀的SDK
- **MiniMax**: 提供强大的M2模型
- **DeepSeek**: 可靠的API服务
- **Flask**: 轻量级Web框架
- **GitHub**: 代码托管平台

---

## 📞 支持与反馈

- **文档**: [README.md](./README.md)
- **问题报告**: [GitHub Issues](https://github.com/Jake-yutong/Literature-Screening-Tool/issues)
- **更新日志**: [CHANGELOG.md](./CHANGELOG.md)
- **发布说明**: [RELEASE_v1.2.md](./RELEASE_v1.2.md)
- **模型指南**: [AI_MODEL_GUIDE.md](./AI_MODEL_GUIDE.md)

---

## 🎊 发布成功！

Literature Screening Tool v1.2.0 现已正式发布！

**主要亮点:**
- 🤖 双AI模型支持
- 🔄 灵活切换
- 📚 完整文档
- 🌐 双语界面

**立即开始使用:**
```bash
git clone https://github.com/Jake-yutong/Literature-Screening-Tool.git
cd Literature-Screening-Tool
pip install -r requirements.txt
python app.py
```

**访问地址:**
http://127.0.0.1:5000

---

*Literature Screening Tool Team*  
*2025年12月11日*
