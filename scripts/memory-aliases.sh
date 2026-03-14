# OpenClaw 记忆增强 - 快捷命令
# 添加到 ~/.zshrc 或 ~/.bashrc

# 记忆工具快速访问
alias mt='~/.openclaw/workspace/scripts/memory-toolkit.sh'
alias mt-daily='mt daily'
alias mt-archive='mt archive'
alias mt-search='mt search'
alias mt-summary='mt summary'

# 增强的记忆搜索（带时间权重显示）
ms() {
    if [ -z "$1" ]; then
        echo "用法: ms <关键词> [结果数量]"
        echo "示例: ms '项目规划' 5"
        return 1
    fi
    ~/.openclaw/workspace/scripts/memory-toolkit.sh search "$1" "${2:-10}"
}

# 快速查看今日记忆
today-memory() {
    local today=$(date +%Y-%m-%d)
    local file="~/.openclaw/workspace/memory/${today}.md"
    if [ -f "$file" ]; then
        echo "📅 今日记忆 ($today):"
        echo "========================"
        cat "$file"
    else
        echo "今日暂无记忆记录"
    fi
}

# 快速查看项目列表
projects() {
    echo "📁 项目列表:"
    ls -la ~/.openclaw/workspace/projects/*.md 2>/dev/null | awk '{print "  " $9}' | xargs -I {} basename {}
}

# 快速查看记忆索引
memory-index() {
    cat ~/.openclaw/workspace/memory/index.json | python3 -m json.tool 2>/dev/null || cat ~/.openclaw/workspace/memory/index.json
}

# 生成今日会话摘要
today-summary() {
    local today=$(date +%Y-%m-%d)
    ~/.openclaw/workspace/scripts/memory-toolkit.sh summary "$today"
}

# 完整记忆维护
memory-maintain() {
    echo "🧠 执行完整记忆维护..."
    ~/.openclaw/workspace/scripts/memory-toolkit.sh full
}

# 记忆统计
memory-stats() {
    echo "📊 记忆系统统计"
    echo "========================"
    echo "记忆文件数: $(find ~/.openclaw/workspace/memory -name '*.md' -type f | wc -l)"
    echo "每日日志: $(find ~/.openclaw/workspace/memory -name '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].md' -type f | wc -l)"
    echo "项目文档: $(find ~/.openclaw/workspace/projects -name '*.md' -type f 2>/dev/null | wc -l)"
    echo "知识库: $(find ~/.openclaw/workspace/knowledge -name '*.md' -type f 2>/dev/null | wc -l)"
    echo "会话摘要: $(find ~/.openclaw/workspace/sessions/summaries -name '*.md' -type f 2>/dev/null | wc -l)"
    echo ""
    echo "最后更新: $(cat ~/.openclaw/workspace/memory/index.json | grep lastUpdated | cut -d'"' -f4)"
}
