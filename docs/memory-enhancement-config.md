# 🧠 OpenClaw 记忆增强配置方案

_实施时间: 2026-03-04 | 版本: v1.0_

---

## 📋 配置总览

### 阶段一：核心记忆能力（立即实施）

#### 1. 开启记忆搜索与自动刷新

在 `~/.openclaw/openclaw.json` 中添加以下配置：

```json
{
  "agents": {
    "defaults": {
      "memory": {
        "enabled": true,
        "search": {
          "enabled": true,
          "paths": [
            "memory/*.md",
            "MEMORY.md",
            "projects/*.md",
            "knowledge/**/*.md"
          ],
          "maxResults": 10,
          "maxSnippetChars": 2000,
          "semanticSearch": true
        },
        "flush": {
          "enabled": true,
          "softThresholdTokens": 120000,
          "reserveTokensFloor": 20000,
          "beforeCompaction": true
        }
      }
    }
  }
}
```

**参数说明：**
- `softThresholdTokens`: 120000 - 达到 12万 Token 时触发静默记忆写入
- `reserveTokensFloor`: 20000 - 保留 2万 Token 给记忆与系统提示
- `beforeCompaction`: true - 上下文压缩前自动写入记忆

#### 2. 会话配置增强

```json
{
  "session": {
    "dmScope": "per-channel-peer",
    "memory": {
      "autoSave": true,
      "extraction": {
        "enabled": true,
        "intervalRounds": 5,
        "extractFacts": true,
        "extractPreferences": true,
        "extractTodos": true
      },
      "timeDecay": {
        "enabled": true,
        "halfLifeDays": 30,
        "minScore": 0.1
      }
    }
  }
}
```

**参数说明：**
- `intervalRounds`: 5 - 每 5 轮对话自动提取一次
- `halfLifeDays`: 30 - 30 天半衰期，旧记忆得分衰减
- `extractFacts/Preferences/Todos`: 自动提取事实、偏好、待办

---

### 阶段二：向量检索优化（推荐实施）

#### 1. 向量模型配置

```json
{
  "agents": {
    "defaults": {
      "memory": {
        "embedding": {
          "model": "bge-m3",
          "provider": "local",
          "local": {
            "modelPath": "~/.openclaw/models/bge-m3",
            "dimensions": 1024
          }
        }
      }
    }
  }
}
```

**bge-m3 优势：**
- 免费开源
- 中文效果优秀
- 支持多语言
- 1024 维向量

#### 2. QMD 高级检索配置

```json
{
  "agents": {
    "defaults": {
      "memory": {
        "search": {
          "qmd": {
            "enabled": true,
            "maxResults": 10,
            "maxSnippetChars": 2000,
            "minRelevanceScore": 0.6,
            "hybridSearch": {
              "enabled": true,
              "keywordWeight": 0.3,
              "semanticWeight": 0.7
            },
            "fieldWeights": {
              "title": 2.0,
              "content": 1.0,
              "tags": 1.5
            }
          }
        }
      }
    }
  }
}
```

---

### 阶段三：分层记忆架构（高级）

```json
{
  "agents": {
    "defaults": {
      "memory": {
        "tiered": {
          "enabled": true,
          "tiers": {
            "hot": {
              "paths": ["MEMORY.md", "memory/2026-*.md"],
              "maxAgeDays": 7,
              "preload": true
            },
            "warm": {
              "paths": ["memory/*.md", "projects/*.md"],
              "maxAgeDays": 90,
              "vectorSearch": true
            },
            "cold": {
              "paths": ["memory/archive/*.md"],
              "maxAgeDays": 365,
              "compression": "gzip"
            }
          }
        }
      }
    }
  }
}
```

---

## ⏰ 定时记忆蒸馏

### 配置定时任务

添加 `~/.openclaw/workspace/cron/memory-distill.json`：

```json
{
  "jobs": [
    {
      "name": "daily-memory-distill",
      "schedule": "0 23 * * *",
      "task": "memory-distill",
      "params": {
        "source": "memory/daily/*.md",
        "target": "MEMORY.md",
        "mode": "extract-merge",
        "deduplicate": true
      }
    },
    {
      "name": "weekly-memory-archive",
      "schedule": "0 3 * * 1",
      "task": "memory-archive",
      "params": {
        "source": "memory/",
        "archivePath": "memory/archive/",
        "olderThanDays": 90,
        "compress": true
      }
    }
  ]
}
```

---

## 🔧 实施脚本

### 一键配置脚本

```bash
#!/bin/bash
# memory-enhancement-setup.sh

echo "🧠 OpenClaw 记忆增强配置"
echo "========================="

# 1. 备份原配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup.$(date +%Y%m%d)

# 2. 下载 bge-m3 模型（可选）
if [ ! -d "~/.openclaw/models/bge-m3" ]; then
    echo "📥 下载 bge-m3 模型..."
    mkdir -p ~/.openclaw/models
    # git clone 或下载脚本
fi

# 3. 创建目录结构
mkdir -p ~/.openclaw/workspace/{memory/archive,sessions/summaries,projects,knowledge/{company,products,tech}}

# 4. 验证配置
echo "✅ 配置完成"
echo "请手动编辑 ~/.openclaw/openclaw.json 添加 memory 配置"
```

---

## 📊 效果验证

### 测试命令

```bash
# 1. 测试记忆搜索
memory_search "测试关键词"

# 2. 验证长会话记忆
# 进行超过 5 轮对话，观察是否自动提取

# 3. 检查 Token 使用
openclaw session status
```

---

## 📝 维护清单

- [ ] 每日检查记忆写入是否正常
- [ ] 每周审查 MEMORY.md 更新
- [ ] 每月优化检索参数
- [ ] 每季度评估模型效果

---

_配置文档版本: v1.0 | 最后更新: 2026-03-04_
