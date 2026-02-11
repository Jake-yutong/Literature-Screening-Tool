# RTF格式支持 - 功能说明

## 概述
已成功为Literature Screening Tool添加RTF（Rich Text Format）文件格式支持。

## 更新内容

### 1. 依赖项更新
- **requirements.txt**: 添加了 `striprtf` 库用于RTF文件解析

### 2. 后端更新 (app.py)
- 添加了 `parse_rtf_file()` 函数，支持解析EndNote样式的RTF导出文件
- 在文件上传处理流程中添加了`.rtf`文件类型支持
- 支持的EndNote字段码：
  - `%T` - 标题 (Title)
  - `%A` - 作者 (Authors)
  - `%J` - 期刊 (Journal/Source)
  - `%D` - 年份 (Year)
  - `%X` - 摘要 (Abstract)
  - `%K` - 关键词 (Keywords)
  - `%R` - DOI
  - `%U` - URL
  - `%0` - 文献类型 (Type)

### 3. 前端更新 (templates/index.html)
- 文件上传区域：更新支持格式显示为 `.xlsx .xls .csv .ris .bib .rtf .txt`
- 文件输入控件：添加 `.rtf` 到accept属性
- 中英文界面：更新了两种语言的格式提示文本
- JavaScript验证：添加 `.rtf` 到有效文件扩展名列表

### 4. 文档更新
- **README.md**: 在"Multi-format Support"特性中添加RTF格式

## RTF文件格式支持

### 支持的RTF格式
该功能主要支持EndNote样式的RTF导出格式，这是学术文献管理软件（如EndNote、Zotero、Mendeley等）常用的导出格式。

### RTF文件示例
```rtf
%T Machine Learning Applications in Business Analytics
%A Smith, John; Johnson, Mary; Brown, Robert
%J Journal of Business Research
%D 2023
%K machine learning, business analytics, data science
%X This paper explores the application of machine learning techniques...
%U https://doi.org/10.1234/jbr.2023.001
%R 10.1234/jbr.2023.001
%0 Journal Article

%T Deep Learning for Natural Language Processing
%A Wang, Li; Chen, Wei
%J Computational Linguistics
%D 2024
...
```

### 解析逻辑
1. **文件解码**: 尝试多种编码（UTF-8, Latin-1, CP1252等）
2. **RTF转文本**: 使用striprtf库将RTF格式转换为纯文本
3. **条目分割**: 通过空行分割不同的文献条目
4. **字段提取**: 识别EndNote字段码（%T, %A等）并提取内容
5. **DataFrame构建**: 将提取的数据组织成pandas DataFrame

### 使用方法
1. 从文献管理软件导出RTF格式文件
2. 在Literature Screening Tool中上传RTF文件
3. 系统自动解析文献信息（标题、作者、摘要、期刊等）
4. 继续进行正常的文献筛选流程

## 测试
- 创建了测试RTF文件：`data/test_data.rtf`
- 包含3条测试文献记录
- 所有字段（标题、作者、期刊、年份、摘要、DOI等）均能正确解析

## 技术细节
- **RTF解析库**: striprtf
- **字段映射**: 自动将EndNote字段码映射到标准列名
- **容错处理**: 支持多种编码格式，处理格式异常
- **回退机制**: 如果EndNote格式解析失败，会尝试通用段落解析

## 兼容性
- ✅ EndNote格式RTF导出
- ✅ 支持多作者（分号分隔）
- ✅ 支持长摘要（跨行内容）
- ✅ 自动字段映射
- ✅ 与现有格式（CSV, Excel, RIS, BibTeX）无缝集成

## 后续改进建议
1. 添加对其他RTF格式变体的支持
2. 改进通用段落解析逻辑（适用于非EndNote格式）
3. 添加更详细的解析错误提示
4. 支持RTF格式的导出功能
