#!/usr/bin/env python3
"""快速测试版本 - 较少token和请求"""

import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics

LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "qwen/qwen3.5-35b-a3b"
TEST_PROMPT = "请用100字左右介绍什么是人工智能。"
MAX_TOKENS = 150
CONCURRENCY_LEVELS = [1, 2, 4, 8]
REQUESTS_PER_LEVEL = 3


def make_request(request_id):
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": TEST_PROMPT}],
        "max_tokens": MAX_TOKENS,
        "temperature": 0.7,
        "stream": False
    }
    
    start = time.time()
    try:
        resp = requests.post(LMSTUDIO_URL, json=payload, timeout=60)
        duration = time.time() - start
        
        if resp.status_code == 200:
            result = resp.json()
            tokens = result.get("usage", {}).get("completion_tokens", 0)
            speed = tokens / duration if duration > 0 else 0
            print(f"  请求#{request_id}: {tokens} tokens, {duration:.2f}s, {speed:.1f} t/s")
            return {"success": True, "tokens": tokens, "duration": duration, "speed": speed}
        else:
            print(f"  请求#{request_id}: 失败 HTTP {resp.status_code}")
            return {"success": False, "error": resp.status_code}
    except Exception as e:
        print(f"  请求#{request_id}: 异常 {e}")
        return {"success": False, "error": str(e)}


def test_level(concurrency):
    print(f"\n{'='*50}")
    print(f"并发数: {concurrency}")
    print(f"{'='*50}")
    
    start = time.time()
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(make_request, i+1) for i in range(REQUESTS_PER_LEVEL)]
        results = [f.result() for f in as_completed(futures)]
    
    total_time = time.time() - start
    successful = [r for r in results if r.get("success")]
    
    if successful:
        total_tokens = sum(r["tokens"] for r in successful)
        avg_speed = statistics.mean([r["speed"] for r in successful])
        throughput = total_tokens / total_time
        avg_latency = statistics.mean([r["duration"] for r in successful])
        
        print(f"\n✅ 成功: {len(successful)}/{REQUESTS_PER_LEVEL}")
        print(f"总耗时: {total_time:.2f}s | 总token: {total_tokens}")
        print(f"平均速度: {avg_speed:.1f} t/s | 吞吐量: {throughput:.1f} t/s | 延迟: {avg_latency:.2f}s")
        
        return {
            "concurrency": concurrency,
            "success_rate": len(successful)/REQUESTS_PER_LEVEL,
            "avg_speed": avg_speed,
            "throughput": throughput,
            "latency": avg_latency
        }
    return None


print("LMstudio 并发性能测试 (快速版)")
print(f"模型: {MODEL_NAME}")
print(f"最大token: {MAX_TOKENS}")

results = []
for c in CONCURRENCY_LEVELS:
    r = test_level(c)
    if r:
        results.append(r)
    time.sleep(1)

print("\n" + "="*50)
print("汇总报告")
print("="*50)
print(f"{'并发':<8} {'平均速度':<12} {'吞吐量':<12} {'延迟':<10}")
print("-"*50)
for r in results:
    print(f"{r['concurrency']:<8} {r['avg_speed']:.1f} t/s{'':<4} {r['throughput']:.1f} t/s{'':<4} {r['latency']:.2f}s")

if results:
    best = max(results, key=lambda x: x["throughput"])
    print(f"\n🏆 最佳吞吐量: 并发{best['concurrency']} = {best['throughput']:.1f} tokens/s")
