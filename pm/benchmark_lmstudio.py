#!/usr/bin/env python3
"""
LMstudio 并发性能测试脚本
测试不同并发数下的token生成速度
"""

import asyncio
import aiohttp
import time
import json
from typing import List, Dict
import statistics

# 配置
LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "qwen/qwen3.5-35b-a3b"  # 可根据实际情况修改
TEST_PROMPT = "请用中文详细介绍一下人工智能的发展历程，从1950年代开始讲起，包括重要的里程碑事件和代表性技术。"
MAX_TOKENS = 500  # 每个请求生成的最大token数
CONCURRENCY_LEVELS = [1, 2, 4, 8, 12, 16]  # 要测试的并发数
REQUESTS_PER_LEVEL = 5  # 每个并发级别的测试次数


async def make_request(session: aiohttp.ClientSession, request_id: int) -> Dict:
    """发送单个请求并测量性能"""
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": TEST_PROMPT}
        ],
        "max_tokens": MAX_TOKENS,
        "temperature": 0.7,
        "stream": False
    }
    
    start_time = time.time()
    try:
        async with session.post(LMSTUDIO_URL, json=payload) as response:
            if response.status == 200:
                result = await response.json()
                end_time = time.time()
                
                # 计算token数
                completion_tokens = result.get("usage", {}).get("completion_tokens", 0)
                total_tokens = result.get("usage", {}).get("total_tokens", 0)
                
                # 计算速度
                duration = end_time - start_time
                tokens_per_second = completion_tokens / duration if duration > 0 else 0
                
                return {
                    "request_id": request_id,
                    "success": True,
                    "duration": duration,
                    "completion_tokens": completion_tokens,
                    "total_tokens": total_tokens,
                    "tokens_per_second": tokens_per_second
                }
            else:
                error_text = await response.text()
                return {
                    "request_id": request_id,
                    "success": False,
                    "error": f"HTTP {response.status}: {error_text}"
                }
    except Exception as e:
        return {
            "request_id": request_id,
            "success": False,
            "error": str(e)
        }


async def test_concurrency_level(concurrency: int) -> Dict:
    """测试特定并发级别"""
    print(f"\n{'='*60}")
    print(f"测试并发数: {concurrency}")
    print(f"{'='*60}")
    
    results = []
    
    async with aiohttp.ClientSession() as session:
        # 创建并发请求
        tasks = []
        for i in range(REQUESTS_PER_LEVEL):
            task = make_request(session, i + 1)
            tasks.append(task)
        
        # 并发执行
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_time
        
        # 统计结果
        successful_results = [r for r in results if r.get("success")]
        failed_results = [r for r in results if not r.get("success")]
        
        if successful_results:
            tokens_per_second_list = [r["tokens_per_second"] for r in successful_results]
            total_tokens = sum([r["completion_tokens"] for r in successful_results])
            
            # 计算总体吞吐量（总token数 / 总时间）
            throughput = total_tokens / total_time if total_time > 0 else 0
            
            stats = {
                "concurrency": concurrency,
                "total_requests": REQUESTS_PER_LEVEL,
                "successful_requests": len(successful_results),
                "failed_requests": len(failed_results),
                "total_time": total_time,
                "total_tokens": total_tokens,
                "avg_tokens_per_second": statistics.mean(tokens_per_second_list),
                "min_tokens_per_second": min(tokens_per_second_list),
                "max_tokens_per_second": max(tokens_per_second_list),
                "throughput": throughput,  # 系统整体吞吐量
                "avg_request_duration": statistics.mean([r["duration"] for r in successful_results])
            }
            
            # 打印结果
            print(f"✅ 成功请求: {stats['successful_requests']}/{stats['total_requests']}")
            print(f"⏱️  总耗时: {stats['total_time']:.2f}秒")
            print(f"📊 总token数: {stats['total_tokens']}")
            print(f"⚡ 平均单请求速度: {stats['avg_tokens_per_second']:.2f} tokens/s")
            print(f"🚀 系统吞吐量: {stats['throughput']:.2f} tokens/s")
            print(f"📈 速度范围: {stats['min_tokens_per_second']:.2f} - {stats['max_tokens_per_second']:.2f} tokens/s")
            print(f"⌛ 平均请求延迟: {stats['avg_request_duration']:.2f}秒")
            
            if failed_results:
                print(f"\n❌ 失败请求: {len(failed_results)}")
                for r in failed_results[:3]:  # 只显示前3个错误
                    print(f"   - 请求#{r['request_id']}: {r.get('error', 'Unknown error')}")
            
            return stats
        else:
            print(f"❌ 所有请求失败!")
            for r in failed_results[:3]:
                print(f"   - 请求#{r['request_id']}: {r.get('error', 'Unknown error')}")
            return {
                "concurrency": concurrency,
                "error": "All requests failed"
            }


async def main():
    """主测试流程"""
    print("="*60)
    print("LMstudio 并发性能测试")
    print("="*60)
    print(f"模型: {MODEL_NAME}")
    print(f"测试URL: {LMSTUDIO_URL}")
    print(f"每个请求最大token: {MAX_TOKENS}")
    print(f"测试并发级别: {CONCURRENCY_LEVELS}")
    print(f"每级别请求数: {REQUESTS_PER_LEVEL}")
    
    all_stats = []
    
    for concurrency in CONCURRENCY_LEVELS:
        stats = await test_concurrency_level(concurrency)
        all_stats.append(stats)
        await asyncio.sleep(2)  # 测试间隔，让系统恢复
    
    # 打印汇总报告
    print("\n" + "="*60)
    print("📊 性能测试汇总报告")
    print("="*60)
    print(f"{'并发数':<10} {'成功率':<10} {'平均速度':<15} {'吞吐量':<15} {'平均延迟':<10}")
    print("-"*60)
    
    for stats in all_stats:
        if "error" not in stats:
            success_rate = stats['successful_requests'] / stats['total_requests'] * 100
            print(f"{stats['concurrency']:<10} "
                  f"{success_rate:.0f}%{'':<6} "
                  f"{stats['avg_tokens_per_second']:.2f} t/s{'':<6} "
                  f"{stats['throughput']:.2f} t/s{'':<6} "
                  f"{stats['avg_request_duration']:.2f}s")
    
    # 找出最佳并发数
    valid_stats = [s for s in all_stats if "error" not in s]
    if valid_stats:
        best_throughput = max(valid_stats, key=lambda x: x.get("throughput", 0))
        print(f"\n🏆 最佳吞吐量并发数: {best_throughput['concurrency']} "
              f"(吞吐量: {best_throughput['throughput']:.2f} tokens/s)")
    
    # 保存结果到JSON
    with open("benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(all_stats, f, ensure_ascii=False, indent=2)
    print("\n💾 详细结果已保存到: benchmark_results.json")


if __name__ == "__main__":
    asyncio.run(main())
