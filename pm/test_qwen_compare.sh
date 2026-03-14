#!/bin/bash
# Qwen3.5 模型对比测试
# 对比: qwen3.5-27b vs qwen/qwen3.5-35b-a3b

API="http://localhost:1234/v1/chat/completions"
MODEL1="qwen3.5-27b"
MODEL2="qwen/qwen3.5-35b-a3b"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "  Qwen3.5 模型对比测试"
echo "  $MODEL1 vs $MODEL2"
echo "=========================================="
echo ""

# 测试用例
declare -A TESTS=(
    ["速度-短"]="写一首关于春天的五言绝句"
    ["速度-中"]="解释一下量子纠缠的原理，用通俗易懂的语言，200字左右"
    ["逻辑推理"]="如果所有的A都是B，所有的B都是C，那么所有的A都是C吗？请详细解释你的推理过程。"
    ["数学计算"]="计算: 1234 × 5678 = ? 请展示计算过程。"
    ["代码生成"]="用Python写一个快速排序算法，并添加注释"
    ["中文写作"]="写一段100字左右的科技新闻报道，主题是AI大模型的发展"
    ["复杂指令"]="请用三个要点总结以下内容，然后用英文翻译每个要点：人工智能正在改变我们的生活方式，从智能手机到自动驾驶，AI技术已经深入到日常生活的方方面面。"
)

# 测试函数
test_model() {
    local model=$1
    local test_name=$2
    local prompt=$3
    
    local start_time=$(python3 -c "import time; print(time.time()*1000)")
    
    result=$(curl -s "$API" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"$model\",
            \"messages\": [{\"role\": \"user\", \"content\": \"$prompt\"}],
            \"max_tokens\": 500,
            \"temperature\": 0.7
        }" 2>/dev/null)
    
    local end_time=$(python3 -c "import time; print(time.time()*1000)")
    local duration=$((end_time - start_time))
    
    # 解析结果
    content=$(echo "$result" | jq -r '.choices[0].message.content // "ERROR"' 2>/dev/null)
    tokens=$(echo "$result" | jq '.usage.completion_tokens // 0' 2>/dev/null)
    
    if [ "$tokens" -gt 0 ]; then
        local tps=$(python3 -c "print(f'{$tokens / ($duration / 1000):.1f}')")
    else
        local tps="0"
    fi
    
    echo "$duration|$tokens|$tps|$content"
}

# 运行测试
echo -e "${BLUE}开始测试...${NC}"
echo ""

for test_name in "${!TESTS[@]}"; do
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}测试: $test_name${NC}"
    echo -e "${YELLOW}提示: ${TESTS[$test_name]}${NC}"
    echo ""
    
    # 测试模型1
    echo -e "${GREEN}[$MODEL1]${NC}"
    result1=$(test_model "$MODEL1" "$test_name" "${TESTS[$test_name]}")
    time1=$(echo "$result1" | cut -d'|' -f1)
    tokens1=$(echo "$result1" | cut -d'|' -f2)
    tps1=$(echo "$result1" | cut -d'|' -f3)
    content1=$(echo "$result1" | cut -d'|' -f4-)
    
    echo "  耗时: ${time1}ms | Tokens: ${tokens1} | 速度: ${tps1} t/s"
    echo "  回答: $(echo "$content1" | head -c 150)..."
    echo ""
    
    sleep 1
    
    # 测试模型2
    echo -e "${GREEN}[$MODEL2]${NC}"
    result2=$(test_model "$MODEL2" "$test_name" "${TESTS[$test_name]}")
    time2=$(echo "$result2" | cut -d'|' -f1)
    tokens2=$(echo "$result2" | cut -d'|' -f2)
    tps2=$(echo "$result2" | cut -d'|' -f3)
    content2=$(echo "$result2" | cut -d'|' -f4-)
    
    echo "  耗时: ${time2}ms | Tokens: ${tokens2} | 速度: ${tps2} t/s"
    echo "  回答: $(echo "$content2" | head -c 150)..."
    echo ""
    
    # 对比
    if [ "$time1" -lt "$time2" ]; then
        diff=$((time2 - time1))
        echo -e "  ${BLUE}速度胜出: $MODEL1 (快 ${diff}ms)${NC}"
    else
        diff=$((time1 - time2))
        echo -e "  ${BLUE}速度胜出: $MODEL2 (快 ${diff}ms)${NC}"
    fi
    
    echo ""
done

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}测试完成！${NC}"
