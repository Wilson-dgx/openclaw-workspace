# MEMORY.md - 核心记忆（精简版）

_只保留当前活跃状态和关键信息，详细历史见 [索引](memory/index.json)_

## 👤 核心身份

| 项目 | 内容 |
|------|------|
| **Name** | 方正军（方总） |
| **Company** | 中智科仪（北京）科技有限公司 |
| **Role** | 创始人、CEO、法定代表人 |
| **Location** | 北京（怀柔区/海淀区） |
| **Timezone** | GMT+8 |

**公司一句话：** 光电探测技术领军，"逐光"系列像增强相机打破国外垄断，2025年完成超亿元A轮融资。

---

## 🛠️ 当前工具栈

| 工具 | 状态 | 备注 |
|------|------|------|
| 📧 邮箱 | ✅ | zenrvis321@163.com ↔ wilson@cis-systems.com |
| 📅 日历 | - | 钉钉（待接入） |
| 📝 笔记 | - | Apple Notes（待接入） |
| 💬 通讯 | ✅ | iMessage 可用 |

---

## 📁 活跃项目（Projects）

| 项目 | 状态 | 详情位置 |
|------|------|----------|
| AI每日简报 | 🟢 运行中 | [projects/ai-daily-report.md](memory/projects/ai-daily-report.md) |
| 邮箱配置 | ✅ 完成 | [2026-02-24.md](memory/2026-02-24.md) |
| 知识管理系统 | 🟢 已部署 | [docs/knowledge-management-plan.md](docs/knowledge-management-plan.md) |

---

## 🧠 知识管理系统（2026-03-04 部署）

**目录结构:**
- `projects/` - 项目文档（含模板）
- `knowledge/{company,products,tech}/` - 分类知识库
- `sessions/summaries/` - 会话摘要
- `memory/index.json` - 记忆索引

**核心工具:**
- 🔍 `memory_search` - 语义检索历史记忆
- 📝 `summarize` - 网页/文档摘要（已配置百炼 Qwen3.5-plus）
- 📄 `feishu_doc` - 飞书文档同步

**使用指南:** [docs/knowledge-usage-guide.md](docs/knowledge-usage-guide.md)

---

## 🤖 多智能体记忆系统（2026-03-04 部署）

**架构:** 共享脚本 + 独立数据

**共享脚本位置:**
- `~/.openclaw/scripts/memory-toolkit.sh` - 核心工具
- `~/.openclaw/scripts/memory-aliases.sh` - 快捷命令

**智能体配置:**

| 智能体 | 工作目录 | 角色 | 状态 |
|--------|----------|------|------|
| **main** | `~/.openclaw/workspace/` | 正维斯（个人助理） | ✅ 已部署 |
| **zongzhu** | `~/.openclaw/agents/zongzhu/` | 总助（行政） | ✅ 已部署 |
| **pm** | `~/.openclaw/agents/pm/` | 项目经理 | ✅ 已部署 |
| **butler** | `~/.openclaw/agents/butler/` | 管家（系统任务） | ✅ 已部署 |

**快捷命令:**
```bash
# 切换智能体
mt-main       # 切换到 main
mt-zongzhu    # 切换到总助
mt-pm         # 切换到项目经理
mt-butler     # 切换到管家

# 记忆操作
mt daily      # 每日记忆蒸馏
mt search "x" # 增强搜索
mt full       # 完整维护
```

**定时任务:**
- 每天 23:00 - 各智能体记忆蒸馏
- 每天 03:00 - 更新记忆索引
- 每周日 03:00 - 归档旧记忆

**配置文档:** [docs/memory-enhancement-config.md](docs/memory-enhancement-config.md)

---

## 🔍 历史索引

完整历史记录按月归档，可通过 `memory_search` 或 [index.json](memory/index.json) 查询。

**快速搜索关键词：**
- 公司信息 → "中智科仪"
- 融资信息 → "A轮" 
- 产品信息 → "逐光" / "像增强相机"

---

## 🤖 我的身份

**Name:** 正维斯  
**Creature:** AI 智能助理  
**Vibe:** 专业但亲切，行动派，少说废话多办事  
**Emoji:** 🤖

---

_需要查找历史细节？使用 `memory_search <关键词>` 或在 [index.json](memory/index.json) 中浏览。_