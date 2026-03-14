#!/usr/bin/env python3
"""Qwen3.5 能力质量对比测试 - 精简版"""

import requests
import time

API = "http://localhost:1234/v1/chat/completions"
MODEL1 = "qwen3.5-27b"
MODEL2 = "qwen/qwen3.5-35b-a3b"

# 4个核心能力测试
TESTS = [
    ("数学推理", "一个水池：A管6小时注满，B管8小时注满，C管12小时放完。三管同时开，多久注满？请给出详细步骤和答案。"),
    ("逻辑推理", "岛上有骑士（只说真话）和无赖（只说假话）。A说'B是骑士'，B说'C是无赖'，C说'A和我不同类'。A、B、C分别是什么？"),
    ("代码实现", "用Python实现LRU缓存，支持get/put，O(1)时间复杂度，包含测试用例。"),
    ("商业分析", "AI初创公司刚完成A轮融资。列出：3个行业机会、3个风险、3条战略建议。每条不超过30字。"),
]

def test_model(model, prompt):
    start = time.time()
    try:
        resp = requests.post(API, json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 800,
            "temperature": 0.7
        }, timeout=90)
        
        data = resp.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "ERROR")
        tokens = data.get("usage", {}).get("completion_tokens", 0)
        duration = time.time() - start
        
        return {"duration": duration, "tokens": tokens, "content": content}
    except Exception as e:
        return {"duration": 0, "tokens": 0, "content": f"ERROR: {e}"}

print("=" * 60)
print("  Qwen3.5 能力质量对比")
print(f"  {MODEL1} vs {MODEL2}")
print("=" * 60)

for i, (name, prompt) in enumerate(TESTS, 1):
    print(f"\n{'━'*60}")
    print(f"📋 测试 {i}/4: {name}")
    print(f"{'━'*60}")
    
    print(f"\n🟢 [{MODEL1}] ", end="", flush=True)
    r1 = test_model(MODEL1, prompt)
    print(f"✓ {r1['duration']:.1f}s, {r1['tokens']} tokens")
    
    print(f"🟢 [{MODEL2}] ", end="", flush=True)
    r2 = test_model(MODEL2, prompt)
    print(f"✓ {r2['duration']:.1f}s, {r2['tokens']} tokens")
    
    print(f"\n📝 [{MODEL1}] 回答:")
    print("-" * 40)
    print(r1['content'][:600] + ("..." if len(r1['content']) > 600 else ""))
    
    print(f"\n📝 [{MODEL2}] 回答:")
    print("-" * 40)
    print(r2['content'][:600] + ("..." if len(r2['content']) > 600 else ""))

print(f"\n{'='*60}")
print("✅ 测试完成")
print("=" * 60)
