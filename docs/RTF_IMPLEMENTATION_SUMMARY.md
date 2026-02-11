# RTF格式支持 - 实施总结

## 更改摘要
为Literature Screening Tool添加了RTF（Rich Text Format）文件格式支持，使用户能够直接上传和解析EndNote等文献管理软件导出的RTF格式文件。

## 已修改的文件

### 1. requirements.txt
- **更改**: 添加了 `striprtf` 依赖库
- **作用**: 用于将RTF格式转换为纯文本

### 2. app.py
#### a) 导入更新
```python
from striprtf.striprtf import rtf_to_text
import re
```

#### b) 新增函数: parse_rtf_file()
- **位置**: 在 `df_to_bibtex()` 函数之后
- **功能**: 解析EndNote样式的RTF文件，提取文献信息
- **支持字段**: Title, Authors, Journal, Year, Abstract, Keywords, DOI, URL, Type
- **行数**: 约180行

#### c) 文件上传处理更新
- **位置**: 第829行附近（在 `.bib` 处理之后）
- **更改**: 添加了 `.rtf` 文件格式检测和处理逻辑
```python
elif filename.endswith('.rtf'):
    content = file.read()
    df = parse_rtf_file(content)
    print(f"   Parsed RTF file: {filename}, {len(df)} records", flush=True)
```

### 3. templates/index.html
#### a) 文件上传界面（第628行）
- **更改前**: `.xlsx .xls .csv .ris .bib .txt`
- **更改后**: `.xlsx .xls .csv .ris .bib .rtf .txt`

#### b) 文件输入控件（第629行）
- **更改**: accept属性添加 `.rtf`
- **更改后**: `accept=".xlsx,.xls,.csv,.ris,.bib,.rtf,.txt"`

#### c) 英文翻译（第797行）
- **更改**: 更新 'upload-formats' 文本

#### d) 中文翻译（第840行）
- **更改**: 更新 'upload-formats' 文本

#### e) JavaScript验证（第999行）
- **更改**: validExtensions数组添加 '.rtf'

### 4. README.md
- **更改**: 在"Core Features"部分更新"Multi-format Support"
- **更改前**: CSV, Excel (.xlsx/.xls), RIS, BibTeX, TXT
- **更改后**: CSV, Excel (.xlsx/.xls), RIS, BibTeX, RTF, TXT

## 新增文件

### 1. data/test_data.rtf
- **作用**: RTF格式测试数据
- **内容**: 包含3条测试文献记录（EndNote格式）

### 2. tests/test_rtf_parsing.py
- **作用**: RTF解析功能的单元测试
- **功能**: 测试RTF文件的读取、解析和DataFrame转换

### 3. tests/debug_rtf.py
- **作用**: RTF解析的调试脚本
- **功能**: 详细输出解析过程，用于排查问题

### 4. tests/test_rtf_final.py
- **作用**: 最终的RTF功能测试
- **功能**: 验证完整的解析流程

### 5. docs/RTF_SUPPORT.md
- **作用**: RTF格式支持的完整文档
- **内容**: 功能说明、使用方法、技术细节

## 功能特性

### EndNote字段码映射
| 字段码 | 含义 | 映射到 |
|--------|------|--------|
| %T | Title | Title |
| %A | Author | Authors |
| %J | Journal | Source title |
| %D | Date/Year | Year |
| %X | Abstract | Abstract |
| %K | Keywords | Keywords |
| %R | DOI/Reference | DOI |
| %U | URL | URL |
| %0 | Type | Type |

### 解析流程
1. 尝试多种编码解码RTF文件
2. 使用striprtf将RTF转换为纯文本
3. 按空行分割独立的文献条目
4. 逐行解析EndNote字段码
5. 构建DataFrame返回

### 容错机制
- 支持多种编码格式（UTF-8, Latin-1, CP1252, Windows-1252等）
- 处理跨行内容（如长摘要）
- 多作者自动合并
- 回退到通用段落解析（如EndNote格式不适用）

## 测试结果
✅ 所有测试通过
- 成功解析3条测试记录
- 所有字段正确提取（Title, Year, Authors, Journal, Abstract, DOI, Keywords, URL, Type）
- 无Python语法错误
- 无HTML错误

## 用户影响
- ✅ 增加文件格式支持，提升工具实用性
- ✅ 无需转换即可上传EndNote等软件的RTF导出
- ✅ 保持与现有功能的完全兼容
- ✅ 用户界面自动更新，支持中英文

## 部署说明
1. 安装新依赖: `pip install striprtf`
2. 重启Flask应用
3. 无需额外配置

## 版本建议
建议将版本号从 1.2.3 更新到 1.3.0（添加新功能）

## 后续优化建议
1. 添加RTF格式的导出功能
2. 支持更多RTF格式变体
3. 改进错误提示的用户友好性
4. 添加RTF文件预览功能
