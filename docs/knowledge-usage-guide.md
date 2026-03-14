# 📖 知识管理使用指南

## 🔍 检索记忆

### 搜索历史记忆
```
memory_search "关键词"
```

### 查看记忆片段
```
memory_get --path memory/2026-03-04.md --from 1 --lines 50
```

## 📝 管理项目

### 创建新项目
1. 复制模板：`cp projects/_template.md projects/新项目.md`
2. 填写项目信息
3. 使用 `memory_search "新项目"` 可检索

### 更新项目状态
- 直接在 `projects/xxx.md` 中编辑
- 重要决策同步到 `MEMORY.md`

## 📚 知识库管理

### 目录结构
- `knowledge/company/` - 公司相关（战略、组织架构）
- `knowledge/products/` - 产品资料（功能、技术规格）
- `knowledge/tech/` - 技术文档（架构、代码规范）

### 添加文档
1. 放入对应目录
2. 使用 summarize 生成摘要
3. 在 MEMORY.md 中记录关键信息

## 🗣️ 会话历史

### 长会话管理流程
1. 会话中 → 自动记录到 `memory/YYYY-MM-DD.md`
2. 会话结束 → 创建 `sessions/summaries/摘要.md`
3. 每周整理 → 归档旧记忆

### 生成会话摘要
```bash
# 会话结束后手动创建摘要
cp sessions/_summary_template.md sessions/summaries/2026-03-04-主题.md
```

## 🛠️ 工具组合

| 任务 | 命令/工具 |
|------|-----------|
| 摘要网页 | `summarize "URL"` |
| 摘要文档 | `summarize "/path/to/file.pdf"` |
| 搜索记忆 | `memory_search "关键词"` |
| 编辑项目 | `read projects/xxx.md` |
| 飞书同步 | `feishu_doc` |

## ⚡ 快捷命令

```bash
# 快速搜索
ms() { memory_search "$1"; }

# 查看今日记忆
today() { read memory/$(date +%Y-%m-%d).md; }

# 列出项目
projects() { ls -la projects/; }
```

---

_有问题随时问正维斯 🤖_
