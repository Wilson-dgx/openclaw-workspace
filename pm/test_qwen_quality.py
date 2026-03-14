#!/usr/bin/env python3
"""Qwen3.5 能力质量对比测试: 27B vs 35B-A3B"""

import requests
import time
import json

API = "http://localhost:1234/v1/chat/completions"
MODEL1 = "qwen3.5-27b"
MODEL2 = "qwen/qwen3.5-35b-a3b"

# 能力测试用例（注重质量而非速度）
QUALITY_TESTS = [
    # 1. 复杂数学推理
    ("数学推理", """
一个水池有两个进水管和一个出水管。单独开A管6小时注满，单独开B管8小时注满，单独开C管12小时放完。
如果三管同时开，多久能注满水池？请给出详细的解题步骤和最终答案。
"""),
    
    # 2. 逻辑推理
    ("逻辑推理", """
在一个岛屿上有两种人：骑士只说真话，无赖只说假话。
你遇到三个人A、B、C：
- A说："B是骑士"
- B说："C是无赖"
- C说："A和我不同类"

请问A、B、C分别是什么人？请给出完整的推理过程。
"""),
    
    # 3. 代码质量
    ("代码实现", """
请用Python实现一个LRU缓存（Least Recently Used），要求：
1. 支持get(key)和put(key, value)操作
2. 容量满时淘汰最近最少使用的元素
3. 时间复杂度O(1)
4. 包含使用示例和测试用例
"""),
    
    # 4. 中文创意写作
    ("创意写作", """
请写一篇200-300字的科幻微小说，主题是"最后一条信息"。
要求：有意境、有反转、情感真挚。
"""),
    
    # 5. 知识准确性
    ("知识问答", """
请回答以下三个问题，每个问题给出准确答案和简要解释：
1. 光速在真空中是多少？（精确数值）
2. 人类基因组大约有多少个碱基对？
3. 世界上最深的海沟是什么？最深点在哪里？深度多少？
"""),
    
    # 6. 复杂指令理解
    ("多步任务", """
请完成以下任务：
1. 列出5个常见的排序算法名称
2. 用表格形式比较它们的时间复杂度（最好、平均、最坏）
3. 给出选择建议：什么场景用哪种算法
"""),
    
    # 7. 代码调试
    ("代码调试", """
以下代码有什么问题？请找出所有bug并修复：

```python
def fibonacci(n):
    if n = 0:
        return 0
    elif n = 1
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n+2)

for i in rang(10):
    print(fibonacci(i)
```
"""),
    
    # 8. 商业分析
    ("商业分析", """
假设你是一家AI初创公司的产品经理，公司刚完成A轮融资。
请分析：
1. 当前AI行业的3个主要机会
2. 3个主要风险
3. 给公司的3条战略建议
每条不超过50字。
"""),
]

def test_model(model, prompt, max_tokens=1500):
    """测试单个模型"""
    start = time.time() * 1000
    
    try:
        resp = requests.post(API, json={
            "model": model,
            "messages": [{"role": "user", "content": prompt.strip()}],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }, timeout=120)
        
        end = time.time() * 1000
        duration = end - start
        
        data = resp.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "ERROR")
        tokens = data.get("usage", {}).get("completion_tokens", 0)
        
        if tokens > 0:
            tps = tokens / (duration / 1000)
        else:
            tps = 0
            
        return {
            "duration": duration,
            "tokens": tokens,
            "tps": tps,
            "content": content
        }
    except Exception as e:
        return {
            "duration": 0,
            "tokens": 0,
            "tps": 0,
            "content": f"ERROR: {e}"
        }

def main():
    print("=" * 60)
    print("  Qwen3.5 能力质量对比测试")
    print(f"  {MODEL1} vs {MODEL2}")
    print("=" * 60)
    print()
    
    all_results = []
    
    for i, (test_name, prompt) in enumerate(QUALITY_TESTS, 1):
        print(f"\n{'━' * 60}")
        print(f"📋 测试 {i}/8: {test_name}")
        print(f"{'━' * 60}")
        
        # 测试模型1
        print(f"\n🟢 [{MODEL1}] 正在生成...")
        r1 = test_model(MODEL1, prompt)
        
        # 测试模型2
        print(f"🟢 [{MODEL2}] 正在生成...")
        r2 = test_model(MODEL2, prompt)
        
        all_results.append({
            "test": test_name,
            "model1": r1,
            "model2": r2
        })
        
        # 显示结果
        print(f"\n{'─' * 60}")
        print(f"📊 [{MODEL1}] 耗时: {r1['duration']/1000:.1f}s | Tokens: {r1['tokens']} | 速度: {r1['tps']:.1f} t/s")
        print(f"📊 [{MODEL2}] 耗时: {r2['duration']/1000:.1f}s | Tokens: {r2['tokens']} | 速度: {r2['tps']:.1f} t/s")
        
        # 速度对比
        if r1['duration'] < r2['duration']:
            diff = (r2['duration'] - r1['duration']) / 1000
            winner = MODEL1
        else:
            diff = (r1['duration'] - r2['duration']) / 1000
            winner = MODEL2
        print(f"🏆 速度胜出: {winner} (快 {diff:.1f}s)")
        
        # 显示完整回答（分开显示）
        print(f"\n{'─' * 60}")
        print(f"📝 [{MODEL1}] 完整回答:")
        print(f"{'─' * 60}")
        print(r1['content'])
        
        print(f"\n{'─' * 60}")
        print(f"📝 [{MODEL2}] 完整回答:")
        print(f"{'─' * 60}")
        print(r2['content'])
        
        print(f"\n{'━' * 60}")
        print("⏳ 2秒后继续下一个测试...")
        time.sleep(2)
    
    # 最终汇总
    print("\n" + "=" * 60)
    print("📈 最终汇总统计")
    print("=" * 60)
    
    for model_name, results_key in [(MODEL1, "model1"), (MODEL2, "model2")]:
        avg_duration = sum(r[results_key]['duration'] for r in all_results) / len(all_results)
        avg_tps = sum(r[results_key]['tps'] for r in all_results) / len(all_results)
        total_tokens = sum(r[results_key]['tokens'] for r in all_results)
        
        print(f"\n{model_name}:")
        print(f"  ⏱  平均耗时: {avg_duration/1000:.1f}s")
        print(f"  ⚡ 平均速度: {avg_tps:.1f} t/s")
        print(f"  📝 总Token: {total_tokens}")
    
    print("\n" + "=" * 60)
    print("✅ 能力质量测试完成！")
    print("💡 请根据上述回答内容评估两个模型的能力质量差异")
    print("=" * 60)

if __name__ == "__main__":
    main()
