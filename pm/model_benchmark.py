#!/usr/bin/env python3
"""
模型对比评测脚本
对比: super-120b-a12b vs qwen/qwen3.5-35b-a3b
"""

import requests
import time
import json
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed

LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"

# 测试用例
TEST_CASES = {
    "reasoning": {
        "prompt": "一个房间里有3个开关，分别控制隔壁房间的3盏灯。你只能进入隔壁房间一次。如何确定哪个开关控制哪盏灯？",
        "max_tokens": 500
    },
    "coding": {
        "prompt": "用Python实现一个LRU缓存，支持get和put操作，时间复杂度O(1)。",
        "max_tokens": 600
    },
    "chinese": {
        "prompt": "请解释量子纠缠现象，并用通俗的比喻说明其原理。",
        "max_tokens": 400
    },
    "math": {
        "prompt": "求解：一个圆锥的底面半径为3cm，高为4cm，求其体积和侧面积。",
        "max_tokens": 300
    },
    "creative": {
        "prompt": "写一个科幻短篇开头（200字以内）：2157年，人类首次接收到来自半人马座的信号...",
        "max_tokens": 300
    }
}

def call_model(model_id, prompt, max_tokens=500, temperature=0.7):
    """调用模型并返回结果"""
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    start_time = time.time()
    try:
        response = requests.post(LMSTUDIO_URL, json=payload, timeout=120)
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

def benchmark_speed(model_id, concurrent=1, num_requests=5):
    """并发速度测试"""
    prompt = "请用100字左右介绍人工智能的发展历史。"
    results = []
    
    with ThreadPoolExecutor(max_workers=concurrent) as executor:
        futures = [executor.submit(call_model, model_id, prompt, 200) 
                   for _ in range(num_requests)]
        
        for future in as_completed(futures):
            result = future.result()
            if result["success"]:
                results.append(result)
    
    if not results:
        return None
    
    speeds = [r["speed"] for r in results]
    times = [r["elapsed"] for r in results]
    
    return {
        "avg_speed": statistics.mean(speeds),
        "total_throughput": sum(r["tokens"] for r in results) / max(sum(times), 0.001),
        "avg_latency": statistics.mean(times),
        "success_rate": len(results) / num_requests
    }

def main():
    models = ["super-120b-a12b", "qwen/qwen3.5-35b-a3b"]
    
    print("=" * 60)
    print("模型对比评测")
    print("=" * 60)
    
    # 1. 能力测试
    print("\n【能力测试】")
    print("-" * 60)
    
    results = {}
    for model_id in models:
        print(f"\n测试模型: {model_id}")
        results[model_id] = {}
        
        for test_name, test_case in TEST_CASES.items():
            print(f"  {test_name}...", end=" ", flush=True)
            result = call_model(model_id, test_case["prompt"], test_case["max_tokens"])
            
            if result["success"]:
                results[model_id][test_name] = result
                print(f"✓ {result['tokens']} tokens, {result['speed']:.1f} t/s")
            else:
                results[model_id][test_name] = result
                print(f"✗ {result.get('error', 'Unknown error')}")
    
    # 2. 性能测试
    print("\n【性能测试】")
    print("-" * 60)
    
    for model_id in models:
        print(f"\n模型: {model_id}")
        
        for concurrent in [1, 2, 4]:
            print(f"  并发{concurrent}...", end=" ", flush=True)
            result = benchmark_speed(model_id, concurrent)
            if result:
                print(f"速度: {result['avg_speed']:.1f} t/s, "
                      f"吞吐: {result['total_throughput']:.1f} t/s, "
                      f"延迟: {result['avg_latency']:.2f}s")
                results[model_id][f"concurrent_{concurrent}"] = result
            else:
                print("✗ 测试失败")
    
    # 3. 保存结果
    with open("benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print("测试完成！结果已保存到 benchmark_results.json")
    print("=" * 60)
    
    # 4. 输出对比摘要
    print("\n【对比摘要】")
    print("-" * 60)
    
    print("\n单请求速度对比:")
    for test_name in TEST_CASES.keys():
        print(f"\n{test_name}:")
        for model_id in models:
            if test_name in results[model_id] and results[model_id][test_name]["success"]:
                r = results[model_id][test_name]
                print(f"  {model_id}: {r['speed']:.1f} t/s, {r['tokens']} tokens")

if __name__ == "__main__":
    main()
