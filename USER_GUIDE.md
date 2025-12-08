# Literature Screening Tool v1.1.0 - 使用指南

## 🚀 快速开始

### 1. 启动应用

#### Windows
1. 双击 `start.bat` 文件
2. 等待终端窗口显示 "Running on http://127.0.0.1:5000"
3. 浏览器会自动打开应用

#### macOS
1. **找到文件夹**: 在 Finder 中打开解压后的工具文件夹
2. **打开终端**: 右键点击文件夹空白处 → "新建位于文件夹位置的终端窗口"
   - 如果没有此选项：打开终端应用，输入 `cd ` (有空格)，然后把文件夹拖进终端窗口，按回车
3. **运行工具**: 在终端中输入 `chmod +x start.sh && ./start.sh` 按回车
4. 等待浏览器自动打开 `http://127.0.0.1:5000`

#### Linux
1. 打开终端并切换到工具目录
2. 运行 `chmod +x start.sh && ./start.sh`
3. 浏览器自动打开 `http://127.0.0.1:5000`

### 2. 界面功能

#### 顶部导航栏
- **🌐 语言切换**: 点击切换中英文界面
- **☀/☾ 主题切换**: 在浅色/深色主题间切换

### 3. 文件上传

**支持格式**:
- ✅ `.xlsx` - Excel 2007+
- ✅ `.xls` - Excel 旧版
- ✅ `.csv` - 逗号分隔
- ✅ `.txt` - 制表符分隔 (Web of Science 导出)
- ✅ `.ris` - 参考文献管理格式

**数据源支持**:
- Web of Science (自动识别并转换格式)
- Scopus
- EndNote/Zotero/Mendeley (RIS 格式)

**操作方式**:
- 拖拽文件到上传区域
- 或点击上传区域选择文件
- 支持同时上传多个文件（自动合并）

### 4. 筛选设置

#### 关键词黑名单
设置两类排除关键词：

**标题/摘要关键词**:
- 每行一个关键词
- 不区分大小写
- 示例：
  ```
  surgical
  patient
  clinical trial
  ```

**期刊名称关键词**:
- 每行一个期刊相关关键词
- 用于排除特定领域期刊
- 示例：
  ```
  medicine
  clinical
  surgery
  ```

#### AI 智能筛选 (可选)
- **API Key**: 输入 DeepSeek API 密钥
- **筛选标准**: 用自然语言描述排除标准
- 示例：
  ```
  排除所有医学临床研究、动物实验研究和纯理论研究
  ```

### 5. 开始筛选
1. 点击 **"开始筛选"** 按钮
2. 等待处理完成（显示进度）
3. 查看筛选结果统计

### 6. 导出结果

#### 选择导出格式
- **CSV**: 通用格式，适合 Excel、R、Python
- **Excel (.xlsx)**: 现代 Excel 格式
- **Excel (.xls)**: 兼容旧版 Excel
- **TXT**: 制表符分隔，适合文本编辑器
- **RIS**: 文献管理软件格式 (Zotero/Mendeley/EndNote)

#### 下载选项
- **下载保留数据**: 通过筛选的文献
- **下载排除数据**: 被排除的文献（含排除原因）
- **下载全部 (ZIP)**: 打包下载两个文件

### 7. 后续分析

#### VOSviewer 可视化
1. 选择 CSV 或 Excel 格式导出
2. 打开 [VOSviewer](https://www.vosviewer.com/)
3. 导入 `cleaned_data` 文件
4. 进行共现分析和可视化

#### 文献管理软件
1. 选择 RIS 格式导出
2. 导入到 Zotero/Mendeley/EndNote
3. 继续文献管理和引用

## 📊 数据列映射

工具自动识别以下列名：

| 数据项 | 可识别的列名 |
|--------|-------------|
| 标题 | Title, TI, Article Title, Document Title |
| 摘要 | Abstract, AB, Description |
| 期刊 | Source Title, SO, Journal, Publication Name |

## ⚠️ 注意事项

1. **文件大小**: 建议单次处理不超过 50MB
2. **AI 筛选**: 
   - 需要有效的 DeepSeek API 密钥
   - 会增加处理时间
   - 仅对通过关键词筛选的文献进行二次筛选
3. **浏览器**: 推荐使用 Chrome、Firefox 或 Edge
4. **数据隐私**: 所有处理在本地完成，文件不上传到服务器

## 🔧 常见问题

**Q: 为什么没有检测到标题/摘要列？**
A: 检查文件列名是否标准。可手动重命名为 "Title", "Abstract", "Source title"

**Q: 可以同时上传不同格式的文件吗？**
A: 可以！工具会自动识别格式并合并数据

**Q: RIS 文件导入失败？**
A: 确保 RIS 文件编码为 UTF-8，且格式符合标准

**Q: 导出的 Excel 文件打不开？**
A: 尝试使用 .xlsx 格式，或改用 CSV 格式

## 📝 PRISMA 流程图使用

使用 `removed_data` 文件中的统计信息：
- Total records: 初始文献数
- Retained: 纳入研究数
- Excluded: 排除研究数
- Exclusion_Reason: 排除原因（用于报告）

## 🆘 技术支持

如遇问题，请检查：
1. Python 版本 >= 3.8
2. 所有依赖已安装 (`pip install -r requirements.txt`)
3. 浏览器控制台是否有错误信息
4. 终端窗口是否有错误日志
