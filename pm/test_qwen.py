#!/usr/bin/env python3
"""Qwen3.5 模型对比测试: 27B vs 35B-A3B"""

import requests
import time
import json

API = "http://localhost:1234/v1/chat/completions"
MODEL1 = "qwen3.5-27b"
MODEL2 = "qwen/qwen3.5-35b-a3b"

# 测试用例
TESTS = [
    ("速度-短", "写一首关于春天的五言绝句"),
    ("速度-中", "解释一下量子纠缠的原理，用通俗易懂的语言，200字左右"),
    ("逻辑推理", "如果所有的A都是B，所有的B都是C，那么所有的A都是C吗？请详细解释你的推理过程。"),
    ("数学计算", "计算: 1234 × 5678 = ? 请展示计算过程。"),
    ("代码生成", "用Python写一个快速排序算法，并添加注释"),
    ("中文写作", "写一段100字左右的科技新闻报道，主题是AI大模型的发展"),
    ("复杂指令", "请用三个要点总结以下内容，然后用英文翻译每个要点：人工智能正在改变我们的生活方式，从智能手机到自动驾驶，AI技术已经深入到日常生活的方方面面。"),
]

def test_model(model, prompt):
    """测试单个模型"""
    start = time.time() * 1000
    
    try:
        resp = requests.post(API, json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500,
            "temperature": 0.7
        }, timeout=60)
        
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
    print("=" * 50)
    print("  Qwen3.5 模型对比测试")
    print(f"  {MODEL1} vs {MODEL2}")
    print("=" * 50)
    print()
    
    results = {MODEL1: [], MODEL2: []}
    
    for test_name, prompt in TESTS:
        print(f"\n{'━' * 50}")
        print(f"📊 测试: {test_name}")
        print(f"💬 提示: {prompt[:50]}...")
        print()
        
        # 测试模型1
        print(f"🟢 [{MODEL1}]")
        r1 = test_model(MODEL1, prompt)
        print(f"   ⏱  耗时: {r1['duration']:.0f}ms")
        print(f"   📝 Tokens: {r1['tokens']}")
        print(f"   ⚡ 速度: {r1['tps']:.1f} t/s")
        print(f"   💬 回答: {r1['content'][:100]}...")
        results[MODEL1].append((test_name, r1))
        
        time.sleep(0.5)
        
        # 测试模型2
        print(f"\n🟢 [{MODEL2}]")
        r2 = test_model(MODEL2, prompt)
        print(f"   ⏱  耗时: {r2['duration']:.0f}ms")
        print(f"   📝 Tokens: {r2['tokens']}")
        print(f"   ⚡ 速度: {r2['tps']:.1f} t/s")
        print(f"   💬 回答: {r2['content'][:100]}...")
        results[MODEL2].append((test_name, r2))
        
        # 对比
        if r1['duration'] < r2['duration']:
            diff = r2['duration'] - r1['duration']
            print(f"\n   🏆 速度胜出: {MODEL1} (快 {diff:.0f}ms)")
        else:
            diff = r1['duration'] - r2['duration']
            print(f"\n   🏆 速度胜出: {MODEL2} (快 {diff:.0f}ms)")
    
    # 汇总统计
    print("\n" + "=" * 50)
    print("📈 汇总统计")
    print("=" * 50)
    
    for model in [MODEL1, MODEL2]:
        avg_duration = sum(r[1]['duration'] for r in results[model]) / len(results[model])
        avg_tps = sum(r[1]['tps'] for r in results[model]) / len(results[model])
        total_tokens = sum(r[1]['tokens'] for r in results[model])
        
        print(f"\n{model}:")
        print(f"  平均耗时: {avg_duration:.0f}ms")
        print(f"  平均速度: {avg_tps:.1f} t/s")
        print(f"  总Token: {total_tokens}")
    
    print("\n" + "=" * 50)
    print("✅ 测试完成！")
    print("=" * 50)

if __name__ == "__main__":
    main()
