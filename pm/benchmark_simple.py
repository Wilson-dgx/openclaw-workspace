#!/usr/bin/env python3
"""
LMstudio 并发性能测试脚本 (简化版)
使用requests和concurrent.futures
"""

import requests
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics

# 配置
LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "qwen/qwen3.5-35b-a3b"
TEST_PROMPT = "请用中文详细介绍一下人工智能的发展历程，从1950年代开始讲起，包括重要的里程碑事件和代表性技术。"
MAX_TOKENS = 500
CONCURRENCY_LEVELS = [1, 2, 4, 8, 12, 16]
REQUESTS_PER_LEVEL = 5


def make_request(request_id):
    """发送单个请求并测量性能"""
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": TEST_PROMPT}],
        "max_tokens": MAX_TOKENS,
        "temperature": 0.7,
        "stream": False
    }
    
    start_time = time.time()
    try:
        response = requests.post(LMSTUDIO_URL, json=payload, timeout=120)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            completion_tokens = result.get("usage", {}).get("completion_tokens", 0)
            duration = end_time - start_time
            tokens_per_second = completion_tokens / duration if duration > 0 else 0
            
            return {
                "request_id": request_id,
                "success": True,
                "duration": duration,
                "completion_tokens": completion_tokens,
                "tokens_per_second": tokens_per_second
            }
        else:
            return {
                "request_id": request_id,
                "success": False,
                "error": f"HTTP {response.status_code}"
            }
    except Exception as e:
        return {
            "request_id": request_id,
            "success": False,
            "error": str(e)
        }


def test_concurrency_level(concurrency):
    """测试特定并发级别"""
    print(f"\n{'='*60}")
    print(f"测试并发数: {concurrency}")
    print(f"{'='*60}")
    
    start_time = time.time()
    results = []
    
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(make_request, i+1) for i in range(REQUESTS_PER_LEVEL)]
        results = [f.result() for f in as_completed(futures)]
    
    total_time = time.time() - start_time
    
    # 统计
    successful = [r for r in results if r.get("success")]
    failed = [r for r in results if not r.get("success")]
    
    if successful:
        tokens_per_second_list = [r["tokens_per_second"] for r in successful]
        total_tokens = sum([r["completion_tokens"] for r in successful])
        throughput = total_tokens / total_time if total_time > 0 else 0
        
        stats = {
            "concurrency": concurrency,
            "successful": len(successful),
            "failed": len(failed),
            "total_time": total_time,
            "total_tokens": total_tokens,
            "avg_speed": statistics.mean(tokens_per_second_list),
            "min_speed": min(tokens_per_second_list),
            "max_speed": max(tokens_per_second_list),
            "throughput": throughput,
            "avg_latency": statistics.mean([r["duration"] for r in successful])
        }
        
        print(f"✅ 成功: {stats['successful']}/{REQUESTS_PER_LEVEL}")
        print(f"⏱️  总耗时: {stats['total_time']:.2f}秒")
        print(f"📊 总token: {stats['total_tokens']}")
        print(f"⚡ 平均速度: {stats['avg_speed']:.2f} tokens/s")
        print(f"🚀 吞吐量: {stats['throughput']:.2f} tokens/s")
        print(f"📈 范围: {stats['min_speed']:.2f} - {stats['max_speed']:.2f} tokens/s")
        print(f"⌛ 平均延迟: {stats['avg_latency']:.2f}秒")
        
        return stats
    else:
        print(f"❌ 所有请求失败!")
        return {"concurrency": concurrency, "error": "All failed"}


def main():
    print("="*60)
    print("LMstudio 并发性能测试")
    print("="*60)
    print(f"模型: {MODEL_NAME}")
    print(f"每请求最大token: {MAX_TOKENS}")
    print(f"测试并发: {CONCURRENCY_LEVELS}")
    print(f"每级请求数: {REQUESTS_PER_LEVEL}")
    
    all_stats = []
    
    for concurrency in CONCURRENCY_LEVELS:
        stats = test_concurrency_level(concurrency)
        all_stats.append(stats)
        time.sleep(2)
    
    # 汇总
    print("\n" + "="*60)
    print("📊 性能汇总")
    print("="*60)
    print(f"{'并发':<8} {'成功率':<10} {'平均速度':<15} {'吞吐量':<15} {'延迟':<10}")
    print("-"*60)
    
    for s in all_stats:
        if "error" not in s:
            rate = s['successful'] / REQUESTS_PER_LEVEL * 100
            print(f"{s['concurrency']:<8} {rate:.0f}%{'':<6} {s['avg_speed']:.2f} t/s{'':<6} {s['throughput']:.2f} t/s{'':<6} {s['avg_latency']:.2f}s")
    
    # 最佳配置
    valid = [s for s in all_stats if "error" not in s]
    if valid:
        best = max(valid, key=lambda x: x.get("throughput", 0))
        print(f"\n🏆 最佳吞吐量: 并发{best['concurrency']} ({best['throughput']:.2f} tokens/s)")
    
    # 保存
    with open("benchmark_results.json", "w") as f:
        json.dump(all_stats, f, indent=2)
    print("\n💾 结果已保存: benchmark_results.json")


if __name__ == "__main__":
    main()
