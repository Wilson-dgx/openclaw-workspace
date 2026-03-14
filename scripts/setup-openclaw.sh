#!/bin/bash
# OpenClaw 多设备同步初始化脚本
# 用法: ./scripts/setup-openclaw.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"
HOME_DIR="$HOME"
OPENCLAW_DIR="$HOME/.openclaw"

echo "🔧 OpenClaw 多设备同步初始化"
echo "=============================="
echo ""

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 1. 检查工作区位置
if [ ! -d "$WORKSPACE_DIR/.git" ]; then
    error "工作区不是 Git 仓库，请确保从 GitHub 克隆"
    exit 1
fi

log "工作区位置: $WORKSPACE_DIR"

# 2. 创建 OpenClaw 目录结构
log "创建 OpenClaw 目录结构..."
mkdir -p "$OPENCLAW_DIR"
mkdir -p "$OPENCLAW_DIR/logs"
mkdir -p "$OPENCLAW_DIR/.cron"

# 3. 生成配置文件（从模板）
CONFIG_TEMPLATE="$WORKSPACE_DIR/config/openclaw.json.template"
CONFIG_TARGET="$OPENCLAW_DIR/openclaw.json"

if [ ! -f "$CONFIG_TEMPLATE" ]; then
    error "配置模板不存在: $CONFIG_TEMPLATE"
    exit 1
fi

if [ -f "$CONFIG_TARGET" ]; then
    warn "配置文件已存在，备份到: $CONFIG_TARGET.backup.$(date +%Y%m%d%H%M%S)"
    cp "$CONFIG_TARGET" "$CONFIG_TARGET.backup.$(date +%Y%m%d%H%M%S)"
fi

log "生成配置文件..."
sed "s|{{HOME}}|$HOME_DIR|g" "$CONFIG_TEMPLATE" > "$CONFIG_TARGET"

# 4. 创建本地专属文件
log "创建本地专属文件..."
touch "$WORKSPACE_DIR/HEARTBEAT.md"
touch "$WORKSPACE_DIR/TOOLS.md"

# 为每个智能体创建本地专属文件
for agent in butler pm zongzhu; do
    if [ -d "$WORKSPACE_DIR/$agent" ]; then
        touch "$WORKSPACE_DIR/$agent/HEARTBEAT.md" 2>/dev/null || true
        touch "$WORKSPACE_DIR/$agent/TOOLS.md" 2>/dev/null || true
    fi
done

# 5. 创建符号链接（可选，兼容旧路径）
if [ "$HOME_DIR" != "/Users/ciss-ai" ] && [ ! -L "/Users/ciss-ai" ]; then
    warn "注意：原配置使用 /Users/ciss-ai 路径"
    warn "当前用户: $(whoami)， home: $HOME_DIR"
    log "配置已自动适配当前用户"
fi

# 6. 验证配置
log "验证配置..."
if grep -q "$HOME_DIR/.openclaw/workspace" "$CONFIG_TARGET"; then
    log "✅ 配置验证通过"
else
    error "配置生成可能有问题，请检查: $CONFIG_TARGET"
    exit 1
fi

# 7. 设置 Git 用户（如果未设置）
if ! git config --global user.name >/dev/null 2>&1; then
    log "设置 Git 用户名..."
    git config --global user.name "$(whoami)"
fi

if ! git config --global user.email >/dev/null 2>&1; then
    log "设置 Git 邮箱..."
    git config --global user.email "$(whoami)@localhost"
fi

# 8. 创建快捷命令（可选）
SHELL_RC=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [ -n "$SHELL_RC" ] && ! grep -q "openclaw-workspace" "$SHELL_RC" 2>/dev/null; then
    log "添加快捷命令到 $SHELL_RC..."
    cat >> "$SHELL_RC" << 'EOF'

# OpenClaw Workspace
export OPENCLAW_WORKSPACE="$HOME/.openclaw/workspace"
alias cdw='cd $OPENCLAW_WORKSPACE'
alias gitw='git -C $OPENCLAW_WORKSPACE'
alias pullw='git -C $OPENCLAW_WORKSPACE pull'
alias pushw='git -C $OPENCLAW_WORKSPACE push'
EOF
    log "快捷命令已添加，运行 'source $SHELL_RC' 生效"
fi

echo ""
echo "✅ 初始化完成！"
echo ""
echo "📋 后续操作："
echo "   1. 检查配置: cat ~/.openclaw/openclaw.json | grep workspace"
echo "   2. 测试同步: cd $WORKSPACE_DIR && git pull"
echo "   3. 快捷命令: cdw, gitw, pullw, pushw"
echo ""
echo "🔄 日常使用："
echo "   - 同步更新: pullw"
echo "   - 提交更改: gitw add -A && gitw commit -m '更新' && pushw"
echo ""
