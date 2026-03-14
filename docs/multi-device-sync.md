# 🔄 多设备同步使用指南

> 长期有效的 OpenClaw 跨 Mac 同步方案

---

## 📦 仓库结构

```
~/.openclaw/workspace/
├── config/
│   └── openclaw.json.template    # 通用配置模板
├── scripts/
│   ├── setup-openclaw.sh         # 新机器初始化脚本 ⭐
│   ├── post-merge                # Git 同步后钩子
│   └── memory-toolkit.sh         # 记忆管理工具
├── zongzhu/                      # 总助智能体
├── pm/                           # PM 智能体
├── butler/                       # 管家智能体
└── ...                           # 其他配置
```

---

## 🚀 新 Mac 初始化流程（只需一次）

```bash
# 1. 克隆仓库
git clone https://github.com/Wilson-dgx/openclaw-workspace.git ~/.openclaw/workspace

# 2. 进入工作区
cd ~/.openclaw/workspace

# 3. 运行初始化脚本（自动配置所有路径）
./scripts/setup-openclaw.sh

# 4. 验证配置
cat ~/.openclaw/openclaw.json | grep workspace
```

**初始化脚本会做什么：**
- ✅ 从模板生成正确的 `openclaw.json`（使用当前用户的 `$HOME`）
- ✅ 创建 `HEARTBEAT.md` 和 `TOOLS.md` 本地专属文件
- ✅ 设置 Git 用户信息（如未设置）
- ✅ 添加常用快捷命令到 `.zshrc`

---

## 🔄 日常使用（保持同步）

### 同步更新（拉取最新）
```bash
# 方式 1：使用快捷命令（推荐）
pullw

# 方式 2：完整命令
cd ~/.openclaw/workspace && git pull
```

**Git 钩子会自动执行：**
- 修复配置中的路径（如有旧路径）
- 创建缺失的本地专属文件
- 更新记忆索引

### 提交更改（推送）
```bash
# 方式 1：使用快捷命令
gitw add -A
gitw commit -m "更新记忆"
pushw

# 方式 2：完整命令
cd ~/.openclaw/workspace
git add -A
git commit -m "更新记忆"
git push
```

---

## 🧠 记忆系统跨设备

同步后，所有智能体的记忆自动生效：

| 智能体 | 记忆位置 | 同步状态 |
|--------|----------|----------|
| main | `workspace/memory/` | ✅ 同步 |
| zongzhu | `workspace/zongzhu/memory/` | ✅ 同步 |
| pm | `workspace/pm/memory/` | ✅ 同步 |
| butler | `workspace/butler/memory/` | ✅ 同步 |

**注意：**
- 本地专属文件（`HEARTBEAT.md`, `TOOLS.md`）每台机器独立
- 定时任务配置（`cron/`）可根据需要各自设置
- 会话历史（`sessions/`）自动记录，但每台机器独立运行

---

## ⚡ 快捷命令

初始化后可用：

```bash
# 目录跳转
cdw                    # cd ~/.openclaw/workspace

# Git 操作
gitw status            # git status
pullw                  # git pull
pushw                  # git push

# 记忆操作
mt daily               # 每日记忆蒸馏
mt search "关键词"      # 搜索记忆
```

---

## 🛠️ 故障排除

### 问题 1：智能体找不到记忆
```bash
# 检查配置路径是否正确
grep "workspace" ~/.openclaw/openclaw.json

# 应该显示你的 home 路径，如 /Users/yourname/.openclaw/workspace/...
# 如果显示 /Users/ciss-ai，运行：
./scripts/setup-openclaw.sh
```

### 问题 2：Git 冲突
```bash
cd ~/.openclaw/workspace
git pull --rebase  # 尝试变基合并
# 或
git stash && git pull && git stash pop
```

### 问题 3：权限错误
```bash
chmod +x ~/.openclaw/workspace/scripts/*.sh
```

---

## 🔐 安全提醒

1. **不要提交敏感信息**：API 密钥、密码等保存在 `~/.openclaw/openclaw.json`（不在 Git 中）
2. **私有仓库**：确保 GitHub 仓库是私有的
3. **Token 安全**：GitHub Personal Access Token 不要共享

---

## 📋 检查清单

新机器部署后确认：

- [ ] `git clone` 成功
- [ ] `./scripts/setup-openclaw.sh` 运行成功
- [ ] `cat ~/.openclaw/openclaw.json | grep workspace` 显示正确路径
- [ ] `ls memory/` 能看到历史记忆文件
- [ ] 智能体能正常读取记忆
- [ ] `git pull` 和 `git push` 正常工作

---

_最后更新: 2026-03-14 | 版本: v1.0_
