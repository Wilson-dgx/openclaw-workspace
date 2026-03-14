#!/usr/bin/env python3
"""
复杂推理能力测试
对比: super-120b-a12b vs qwen/qwen3.5-35b-a3b
"""

import requests
import time
import json

LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"

REASONING_TESTS = [
    {
        "name": "多步逻辑推理",
        "prompt": """已知以下条件：
1. 所有参加会议的人都要么是工程师，要么是设计师
2. 所有设计师都会画画
3. 小王不会画画
4. 小王参加了会议
5. 小李是工程师
6. 所有工程师都会编程
7. 小张会编程但不会画画

请回答：谁一定是工程师？谁一定是设计师？谁的身份无法确定？请逐步推理并说明每一步的依据。""",
        "max_tokens": 800
    },
    {
        "name": "数学证明",
        "prompt": """证明：对于任意正整数 n，1³ + 2³ + 3³ + ... + n³ = (1 + 2 + 3 + ... + n)²

要求：
1. 用数学归纳法证明
2. 每一步都要写清楚
3. 验证基础情况
4. 完整写出归纳步骤""",
        "max_tokens": 1000
    },
    {
        "name": "囚徒困境变体",
        "prompt": """有三个囚犯A、B、C，法官告诉他们：
- 你们中至少有两人会被释放
- 每个人不知道自己是否被释放，但可以看到其他人的状态

囚犯A问看守："B会被释放吗？"看守回答："是的。"

现在囚犯A能确定自己被释放吗？请详细分析推理过程，并说明为什么。如果看守回答"不是"，结果会怎样？""",
        "max_tokens": 700
    },
    {
        "name": "因果推理",
        "prompt": """某城市发现：
- 引入X政策后，犯罪率下降30%
- 同时期经济好转，失业率下降
- 邻近城市（无X政策）犯罪率下降10%
- X政策实施后第3个月才开始看到效果

问题：
1. X政策是犯罪率下降的原因吗？
2. 还有哪些可能的解释？
3. 如何设计实验来验证因果关系？
请运用因果推理的方法进行分析。""",
        "max_tokens": 900
    },
    {
        "name": "悖论分析",
        "prompt": """分析以下悖论：

"这个句子是假的。"

问题：
1. 如果这个句子是真的，那么它是假的
2. 如果这个句子是假的，那么它是真的

请分析：
1. 这个悖论的本质是什么？
2. 它与罗素悖论有什么关系？
3. 现代逻辑学如何解决这类悖论？
4. 给出一个可能的解决方案""",
        "max_tokens": 800
    },
    {
        "name": "算法复杂度分析",
        "prompt": """分析以下递归算法的时间复杂度：

def mystery(n):
    if n <= 1:
        return 1
    result = 0
    for i in range(n):
        result += mystery(i)
    return result

要求：
1. 写出递推关系式
2. 用代入法或递归树方法求解
3. 给出紧确界（Θ表示法）
4. 验证你的答案""",
        "max_tokens": 800
    },
    {
        "name": "概率推理",
        "prompt": """三门问题变体：

有4扇门，其中1扇后面有奖。你选择了门1。
主持人（知道哪扇门有奖）打开了门2和门3，都空着。
现在给你机会换到门4。

问题：
1. 换门的中奖概率是多少？
2. 请用贝叶斯公式严格证明
3. 如果主持人不知道哪扇门有奖，只是碰巧开了两扇空门，概率会变吗？
4. 解释为什么会有这种差异""",
        "max_tokens": 900
    },
    {
        "name": "系统设计推理",
        "prompt": """设计一个分布式缓存系统，要求：
- 支持100万QPS
- 数据一致性要求：最终一致即可
- 可用性要求：99.99%
- 单个key-value大小：1KB

请分析：
1. 需要多少台服务器？（假设单机10万QPS）
2. 如何处理热点key？
3. 如何保证高可用？
4. 缓存失效策略如何设计？
给出具体的数值计算和设计理由。""",
        "max_tokens": 1000
    }
]

def call_model(model_id, prompt, max_tokens=800):
    """调用模型"""
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }
    
    start_time = time.time()
    try:
        response = requests.post(LMSTUDIO_URL, json=payload, timeout=180)
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            tokens = data.get("usage", {}).get("completion_tokens", 0)
            speed = tokens / elapsed if elapsed > 0 else 0
            
            return {
                "success": True,
                "content": content,
                "tokens": tokens,
                "elapsed": elapsed,
                "speed": speed
            }
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    models = ["super-120b-a12b", "qwen/qwen3.5-35b-a3b"]
    
    print("=" * 80)
    print("复杂推理能力对比测试")
    print("=" * 80)
    
    results = {}
    
    for test in REASONING_TESTS:
        print(f"\n{'='*80}")
        print(f"【{test['name']}】")
        print("=" * 80)
        
        results[test['name']] = {}
        
        for model_id in models:
            short_name = model_id.split("/")[-1]
            print(f"\n>>> {short_name}:")
            print("-" * 80)
            
            result = call_model(model_id, test['prompt'], test['max_tokens'])
            results[test['name']][model_id] = result
            
            if result["success"]:
                # 显示完整输出（推理任务需要看完整内容）
                print(result["content"])
                print(f"\n[统计: {result['tokens']} tokens, {result['speed']:.1f} t/s, {result['elapsed']:.1f}s]")
            else:
                print(f"❌ 错误: {result.get('error', 'Unknown')}")
    
    # 保存结果
    with open("reasoning_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 性能对比摘要
    print("\n" + "=" * 80)
    print("性能对比摘要")
    print("=" * 80)
    print(f"\n{'测试项目':<20} {'super-120b':<20} {'Qwen3.5-35B':<20} {'胜出':<10}")
    print("-" * 70)
    
    for test in REASONING_TESTS:
        name = test['name']
        s_result = results[name].get("super-120b-a12b", {})
        q_result = results[name].get("qwen/qwen3.5-35b-a3b", {})
        
        s_speed = s_result.get("speed", 0) if s_result.get("success") else 0
        q_speed = q_result.get("speed", 0) if q_result.get("success") else 0
        
        winner = "super-120b" if s_speed > q_speed * 1.1 else ("Qwen" if q_speed > s_speed * 1.1 else "相当")
        
        print(f"{name:<20} {s_speed:>8.1f} t/s        {q_speed:>8.1f} t/s        {winner}")
    
    print("\n完整结果已保存到 reasoning_results.json")

if __name__ == "__main__":
    main()
