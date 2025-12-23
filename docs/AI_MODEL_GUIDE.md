# AI Model Quick Reference - v1.2

## 模型选择指南 | Model Selection Guide

### DeepSeek Chat

**适用场景 | Best For:**
- 大批量文献筛选（成本优化）
- 快速初步筛选
- 标准排除标准
- Large-scale screening (cost-effective)
- Quick preliminary screening
- Standard exclusion criteria

**特点 | Features:**
- ⚡ 快速响应 | Fast response
- 💰 经济实惠 | Cost-effective
- 🎯 稳定可靠 | Reliable performance
- 📊 JSON格式输出 | JSON format output

**API配置 | API Setup:**
```bash
# 获取API密钥 | Get API key
https://platform.deepseek.com/

# 基础URL | Base URL
https://api.deepseek.com

# 模型名称 | Model name
deepseek-chat
```

---

### MiniMax-M2

**适用场景 | Best For:**
- 复杂筛选标准
- 需要详细推理过程
- 边界情况判断
- Complex exclusion criteria
- Need for reasoning transparency
- Edge case evaluation

**特点 | Features:**
- 🧠 高级推理 | Advanced reasoning
- 💭 思维过程可视化 | Thinking process visible
- 🔄 多轮对话支持 | Multi-turn conversation
- 🌍 国际/国内双端点 | China/International endpoints

**API配置 | API Setup:**
```bash
# 获取API密钥 | Get API key
国内 | China: https://platform.minimaxi.com/
国际 | International: https://platform.minimax.io/

# 基础URL | Base URL
国内 | China: https://api.minimaxi.com/anthropic
国际 | International: https://api.minimax.io/anthropic

# 模型名称 | Model name
MiniMax-M2
```

---

## 使用示例 | Usage Examples

### Example 1: 医学文献排除 | Medical Literature Exclusion

**DeepSeek适合 | DeepSeek Suitable:**
```
排除所有医学临床研究
Exclude all medical clinical studies
```
✅ 标准关键词匹配即可
✅ Standard keyword matching sufficient

**MiniMax-M2适合 | MiniMax-M2 Suitable:**
```
排除以医学应用为主，但保留医学教育相关的研究
Exclude medical applications but keep medical education studies
```
✅ 需要细致区分应用场景
✅ Requires nuanced context distinction

---

### Example 2: 教育科技筛选 | EdTech Screening

**DeepSeek适合 | DeepSeek Suitable:**
```
只保留K-12教育相关研究
Keep only K-12 education studies
```
✅ 明确的范围界定
✅ Clear scope definition

**MiniMax-M2适合 | MiniMax-M2 Suitable:**
```
保留AI驱动的游戏化学习，但排除纯技术实现和非教育应用
Keep AI-driven gamified learning, exclude pure technical implementations and non-educational applications
```
✅ 多条件综合判断
✅ Multi-criteria evaluation

---

## 性能对比 | Performance Comparison

| 指标 | DeepSeek Chat | MiniMax-M2 |
|------|---------------|------------|
| **速度 Speed** | ⚡⚡⚡⚡⚡ | ⚡⚡⚡⚡ |
| **成本 Cost** | 💰 低 Low | 💰💰 中等 Medium |
| **准确率 Accuracy** | 📊📊📊📊 | 📊📊📊📊📊 |
| **推理能力 Reasoning** | 🧠🧠🧠 | 🧠🧠🧠🧠🧠 |
| **透明度 Transparency** | 📄📄 | 📄📄📄📄📄 |
| **复杂场景 Complex Cases** | ✓ | ✓✓ |

---

## 切换模型 | Switching Models

### 在界面中 | In Web Interface

1. 打开工具 | Open tool
2. 找到"Select AI Model"下拉菜单
3. 选择模型：
   - DeepSeek Chat
   - MiniMax-M2
4. 输入对应API密钥
5. 开始筛选

### 程序化切换 | Programmatic Switch

```python
# v1.2新增参数 | v1.2 new parameter
ai_model = 'deepseek'  # 默认 | default
ai_model = 'minimax'   # MiniMax-M2

# 自动路由到正确的SDK | Auto-routes to correct SDK
# OpenAI SDK for DeepSeek
# Anthropic SDK for MiniMax
```

---

## 成本估算 | Cost Estimation

### DeepSeek Chat
- **输入 Input**: ~¥0.001 / 1K tokens
- **输出 Output**: ~¥0.002 / 1K tokens
- **1000篇文献 1000 papers**: ~¥20-50
- **适合 Best for**: 大规模筛选 | Large-scale screening

### MiniMax-M2
- **输入 Input**: ~¥0.03 / 1K tokens
- **输出 Output**: ~¥0.06 / 1K tokens
- **1000篇文献 1000 papers**: ~¥100-200
- **适合 Best for**: 精细筛选 | Detailed screening

*注：实际成本取决于文献长度和复杂度*
*Note: Actual costs depend on literature length and complexity*

---

## 常见问题 | FAQ

**Q: 可以混合使用两种模型吗？**
**Q: Can I mix both models?**

A: 可以！先用DeepSeek做初筛，再用MiniMax-M2对边界案例进行二次筛选。
A: Yes! Use DeepSeek for initial screening, then MiniMax-M2 for edge cases.

**Q: 哪个模型更准确？**
**Q: Which model is more accurate?**

A: MiniMax-M2在复杂场景下表现更好，但DeepSeek在标准场景下同样可靠。
A: MiniMax-M2 excels in complex scenarios, but DeepSeek is equally reliable for standard cases.

**Q: 如何选择？**
**Q: How to choose?**

A: 
- 预算充足+复杂标准 → MiniMax-M2
- 大规模+标准标准 → DeepSeek
- Budget sufficient + complex criteria → MiniMax-M2
- Large-scale + standard criteria → DeepSeek

---

## 技术支持 | Technical Support

- 📖 完整文档 | Full Docs: [README.md](./README.md)
- 🐛 问题反馈 | Report Issues: [GitHub Issues](https://github.com/Jake-yutong/Literature-Screening-Tool/issues)
- 📝 更新日志 | Changelog: [CHANGELOG.md](./CHANGELOG.md)
- 🚀 发布说明 | Release Notes: [RELEASE_v1.2.md](./RELEASE_v1.2.md)

---

**版本 Version**: 1.2.0  
**更新日期 Updated**: 2025-12-11
