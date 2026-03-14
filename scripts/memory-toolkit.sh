#!/bin/bash
# Memory Enhancement Toolkit for OpenClaw
# 功能：记忆搜索增强、自动整理、时间衰减权重

set -e

WORKSPACE="${HOME}/.openclaw/workspace"
MEMORY_DIR="${WORKSPACE}/memory"
MEMORY_FILE="${WORKSPACE}/MEMORY.md"
DAILY_PATTERN="${MEMORY_DIR}/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].md"
INDEX_FILE="${MEMORY_DIR}/index.json"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# ==================== 功能 1: 每日记忆蒸馏 ====================
daily_distill() {
    log "开始每日记忆蒸馏..."
    
    local today=$(date +%Y-%m-%d)
    local daily_file="${MEMORY_DIR}/${today}.md"
    
    if [ ! -f "$daily_file" ]; then
        warn "今日记忆文件不存在: $daily_file"
        return 0
    fi
    
    # 提取关键信息（事实、决策、待办）
    log "从今日记忆提取关键信息..."
    
    # 创建临时摘要文件
    local temp_summary="${MEMORY_DIR}/.temp_daily_${today}.md"
    
    cat > "$temp_summary" << EOF
## 📅 ${today} 关键信息

### 🎯 重要决策
$(grep -E "^[\-\*]\s*\*\*决策|决策:|决定:" "$daily_file" 2>/dev/null || echo "- 无")

### 📝 重要事实
$(grep -E "^[\-\*]\s*\*\*事实|事实是|了解到" "$daily_file" 2>/dev/null || echo "- 无")

### ✅ 待办事项
$(grep -E "^[\-\*]\s*\[ \]|待办|TODO" "$daily_file" 2>/dev/null || echo "- 无")

### 💡 关键洞察
$(grep -E "^[\-\*]\s*\*\*洞察|发现:|注意:" "$daily_file" 2>/dev/null || echo "- 无")

EOF
    
    # 合并到 MEMORY.md（去重）
    if [ -f "$MEMORY_FILE" ]; then
        # 检查是否已存在今日记录
        if ! grep -q "## 📅 ${today} 关键信息" "$MEMORY_FILE"; then
            log "合并到 MEMORY.md..."
            cat "$temp_summary" >> "$MEMORY_FILE"
            echo "" >> "$MEMORY_FILE"
        else
            log "今日记录已存在，跳过合并"
        fi
    fi
    
    rm -f "$temp_summary"
    log "✅ 每日记忆蒸馏完成"
}

# ==================== 功能 2: 记忆归档 ====================
archive_old_memories() {
    log "开始归档旧记忆..."
    
    local archive_dir="${MEMORY_DIR}/archive"
    mkdir -p "$archive_dir"
    
    # 归档 90 天前的记忆
    local cutoff_date=$(date -v-90d +%Y-%m-%d 2>/dev/null || date -d '90 days ago' +%Y-%m-%d)
    
    find "$MEMORY_DIR" -name "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].md" -type f | while read file; do
        local filename=$(basename "$file")
        local file_date="${filename%.md}"
        
        if [[ "$file_date" < "$cutoff_date" ]]; then
            log "归档: $filename"
            mv "$file" "$archive_dir/"
        fi
    done
    
    log "✅ 记忆归档完成"
}

# ==================== 功能 3: 更新记忆索引 ====================
update_index() {
    log "更新记忆索引..."
    
    local index_temp="${INDEX_FILE}.tmp"
    
    # 统计记忆文件
    local total_files=$(find "$MEMORY_DIR" -name "*.md" -type f | wc -l)
    local daily_files=$(find "$MEMORY_DIR" -name "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].md" -type f | wc -l)
    local project_files=$(find "$WORKSPACE/projects" -name "*.md" -type f 2>/dev/null | wc -l)
    
    cat > "$index_temp" << EOF
{
  "version": "1.1",
  "lastUpdated": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "stats": {
    "totalMemoryFiles": ${total_files},
    "dailyLogs": ${daily_files},
    "projectFiles": ${project_files}
  },
  "categories": {
    "daily": {
      "path": "memory/",
      "pattern": "YYYY-MM-DD.md",
      "description": "每日会话日志",
      "retentionDays": 90
    },
    "projects": {
      "path": "projects/",
      "pattern": "*.md",
      "description": "项目文档"
    },
    "knowledge": {
      "path": "knowledge/",
      "subdirs": ["company", "products", "tech"],
      "description": "知识库"
    },
    "sessions": {
      "path": "sessions/summaries/",
      "pattern": "*.md",
      "description": "会话摘要"
    }
  },
  "searchTips": [
    "使用 memory_search <关键词> 搜索历史记忆",
    "项目名称可在 projects/ 目录查找",
    "知识库按类别组织在 knowledge/ 下",
    "旧记忆自动归档到 memory/archive/"
  ],
  "maintenance": {
    "lastDistill": "$(date +%Y-%m-%d)",
    "lastArchive": "$(date +%Y-%m-%d)",
    "distillSchedule": "daily at 23:00",
    "archiveSchedule": "weekly on Monday 03:00"
  }
}
EOF
    
    mv "$index_temp" "$INDEX_FILE"
    log "✅ 记忆索引更新完成"
}

# ==================== 功能 4: 智能搜索增强 ====================
enhanced_search() {
    local query="$1"
    local max_results="${2:-10}"
    
    log "执行增强记忆搜索: '$query'"
    
    # 时间衰减权重计算
    local today_epoch=$(date +%s)
    local half_life=$((30 * 86400)) # 30天半衰期
    
    # 搜索所有记忆文件
    local results=$(grep -r -l -i "$query" "$WORKSPACE/memory" "$WORKSPACE/projects" "$WORKSPACE/knowledge" 2>/dev/null | head -$max_results)
    
    if [ -z "$results" ]; then
        warn "未找到相关记忆"
        return 1
    fi
    
    echo ""
    echo "🔍 搜索结果: '$query'"
    echo "========================"
    
    echo "$results" | while read file; do
        local filename=$(basename "$file")
        local file_epoch=$(stat -f %m "$file" 2>/dev/null || stat -c %Y "$file" 2>/dev/null || echo "$today_epoch")
        local age_days=$(( (today_epoch - file_epoch) / 86400 ))
        
        # 计算时间权重 (指数衰减)
        local weight=$(awk "BEGIN {printf \"%.2f\", exp(-$age_days * 0.693 / 30)}")
        
        # 显示结果
        echo ""
        echo "📄 $filename (权重: $weight, ${age_days}天前)"
        echo "   路径: $file"
        
        # 显示匹配片段
        grep -i -B 1 -A 2 "$query" "$file" 2>/dev/null | head -10 | sed 's/^/   /'
    done
    
    echo ""
    echo "💡 提示: 使用 'memory_get --path <文件> --from <行号>' 查看完整内容"
}

# ==================== 功能 5: 会话摘要生成 ====================
generate_session_summary() {
    local session_date="${1:-$(date +%Y-%m-%d)}"
    local daily_file="${MEMORY_DIR}/${session_date}.md"
    local summary_file="${WORKSPACE}/sessions/summaries/${session_date}.md"
    
    if [ ! -f "$daily_file" ]; then
        error "会话文件不存在: $daily_file"
        return 1
    fi
    
    log "生成会话摘要: $session_date"
    
    mkdir -p "${WORKSPACE}/sessions/summaries"
    
    cat > "$summary_file" << EOF
# 💬 会话摘要 - ${session_date}

_生成时间: $(date '+%Y-%m-%d %H:%M:%S')_

---

## 📌 会话主题

（请手动填写本次会话的主要主题）

---

## 🎯 关键决策

$(grep -E "^[\-\*]\s*\*\*决策|决策:|决定:" "$daily_file" 2>/dev/null || echo "- 待整理")

---

## 📝 重要信息

$(grep -E "^[\-\*]\s*\*\*事实|事实是|了解到|重要:" "$daily_file" 2>/dev/null || echo "- 待整理")

---

## ✅ 待办事项

$(grep -E "^[\-\*]\s*\[ \]|待办|TODO" "$daily_file" 2>/dev/null || echo "- 待整理")

---

## 💡 关键洞察

（请手动填写本次会话的重要洞察）

---

## 🔗 相关上下文

- 原始记忆: [memory/${session_date}.md](../../memory/${session_date}.md)
- 关联项目: 

---

_使用 memory_search "${session_date}" 可检索相关记忆_
EOF
    
    log "✅ 会话摘要已生成: $summary_file"
    echo "💡 提示: 请手动编辑补充摘要内容"
}

# ==================== 主函数 ====================
main() {
    local command="${1:-help}"
    
    case "$command" in
        "daily"|"distill")
            daily_distill
            update_index
            ;;
        "archive")
            archive_old_memories
            update_index
            ;;
        "index"|"update-index")
            update_index
            ;;
        "search")
            enhanced_search "$2" "$3"
            ;;
        "summary"|"session-summary")
            generate_session_summary "$2"
            ;;
        "full"|"all")
            log "执行完整记忆维护流程..."
            daily_distill
            archive_old_memories
            update_index
            log "✅ 完整维护流程完成"
            ;;
        "help"|*)
            echo "🧠 OpenClaw 记忆增强工具"
            echo ""
            echo "用法: $0 <命令> [参数]"
            echo ""
            echo "命令:"
            echo "  daily, distill          执行每日记忆蒸馏"
            echo "  archive                 归档旧记忆（90天前）"
            echo "  index, update-index     更新记忆索引"
            echo "  search <关键词> [数量]   增强搜索（带时间权重）"
            echo "  summary [日期]          生成会话摘要"
            echo "  full, all               执行完整维护流程"
            echo "  help                    显示帮助"
            echo ""
            echo "示例:"
            echo "  $0 daily"
            echo "  $0 search \"项目规划\" 5"
            echo "  $0 summary 2026-03-04"
            ;;
    esac
}

main "$@"
