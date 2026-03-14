#!/usr/bin/env python3
"""
编程能力测试 - 对比 Qwen vs Minimax
测试内容：算法、调试、重构、系统设计
"""

import requests
import json
import time
import sys

BASE_URL = "http://127.0.0.1:1234/v1"

# 10道编程能力测试题
PROGRAMMING_QUESTIONS = [
    {
        "id": 1,
        "title": "实现LRU缓存",
        "type": "算法实现",
        "content": """请用Python实现一个LRU（最近最少使用）缓存，要求：
1. 支持get和put操作，时间复杂度O(1)
2. 使用双向链表+哈希表实现
3. 需要处理容量限制，超出时淘汰最久未使用的
4. 提供完整的类定义和使用示例"""
    },
    {
        "id": 2,
        "title": "快速排序优化",
        "type": "算法优化",
        "content": """下面是一个快速排序的实现，请找出问题并优化：

```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr if x < pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + [pivot] + quicksort(right)
```

要求：
1. 指出原代码的问题（时间/空间复杂度、重复元素处理等）
2. 提供原地排序版本，空间复杂度O(log n)
3. 处理重复元素的情况
4. 优化pivot选择策略"""
    },
    {
        "id": 3,
        "title": "并发下载器",
        "type": "异步编程",
        "content": """用Python asyncio实现一个并发文件下载器，要求：
1. 支持同时下载多个URL
2. 限制最大并发数（如5个）
3. 实现超时重试机制（最多3次）
4. 显示下载进度和速度
5. 处理下载失败的情况，返回成功/失败列表

假设使用aiohttp库，提供完整可运行代码"""
    },
    {
        "id": 4,
        "title": "SQL查询优化",
        "type": "数据库优化",
        "content": """有用户表users和订单表orders，请优化以下查询：

```sql
SELECT u.name, u.email, COUNT(o.id) as order_count
FROM users u, orders o
WHERE u.id = o.user_id
AND o.created_at > '2024-01-01'
GROUP BY u.id
HAVING order_count > 5
ORDER BY order_count DESC;
```

表结构：
- users: id(主键), name, email, created_at
- orders: id(主键), user_id, amount, created_at, status

要求：
1. 指出原SQL的问题（性能/语法）
2. 优化后的SQL语句
3. 需要的索引设计
4. 估算大数据量下的查询性能"""
    },
    {
        "id": 5,
        "title": "找出死锁",
        "type": "代码调试",
        "content": """以下多线程代码存在死锁风险，请找出并修复：

```python
import threading

class Account:
    def __init__(self, balance):
        self.balance = balance
        self.lock = threading.Lock()

def transfer(a1, a2, amount):
    with a1.lock:
        with a2.lock:
            a1.balance -= amount
            a2.balance += amount

# 两个线程同时执行
# 线程1: transfer(accountA, accountB, 100)
# 线程2: transfer(accountB, accountA, 100)
```

要求：
1. 解释死锁发生的原因
2. 提供修复后的代码
3. 说明使用的同步策略"""
    },
    {
        "id": 6,
        "title": "装饰器实现",
        "type": "Python特性",
        "content": """实现一个带参数的装饰器@retry(max_attempts=3, delay=1)，要求：
1. 在函数抛出异常时自动重试
2. 支持指定最大重试次数
3. 支持指定每次重试间隔（秒）
4. 保留原函数的元信息（docstring等）
5. 提供使用示例，包括带参数和不带参数的函数"""
    },
    {
        "id": 7,
        "title": "内存泄漏排查",
        "type": "调试分析",
        "content": """以下代码存在内存泄漏，请分析原因并提供解决方案：

```python
class EventManager:
    def __init__(self):
        self.listeners = []
    
    def subscribe(self, callback):
        self.listeners.append(callback)
    
    def emit(self, event):
        for listener in self.listeners:
            listener(event)

# 使用场景
class DataProcessor:
    def __init__(self, event_manager):
        self.data = [0] * 1000000  # 大对象
        event_manager.subscribe(self.on_event)
    
    def on_event(self, event):
        self.data.append(event)

# 频繁创建和"销毁"DataProcessor
manager = EventManager()
for i in range(100):
    processor = DataProcessor(manager)  # 这些对象不会被回收
    # processor 理论上应该被回收，但实际没有
```

要求：
1. 解释内存泄漏的根本原因
2. 提供修复方案（至少两种方法）
3. 说明如何避免此类问题"""
    },
    {
        "id": 8,
        "title": "API限流器",
        "type": "系统设计",
        "content": """设计并实现一个API限流器，要求：
1. 支持令牌桶(Token Bucket)和漏桶(Leaky Bucket)两种算法
2. 支持按用户/IP限流
3. 支持Redis作为分布式存储
4. 提供装饰器模式使用：@rate_limit(requests=100, window=60)
5. 超过限流时返回429状态码

假设使用Flask框架，提供核心限流逻辑代码"""
    },
    {
        "id": 9,
        "title": "正则表达式优化",
        "type": "正则优化",
        "content": """以下正则表达式存在性能问题（灾难性回溯），请优化：

```python
import re

# 验证邮箱地址 - 慢！
pattern = r'^(.*)@(.*)\\.(.*)$'

# 测试文本
emails = ["a" * 20 + "@test.com" for _ in range(1000)]

for email in emails:
    re.match(pattern, email)
```

要求：
1. 解释什么是灾难性回溯(Catastrophic Backtracking)
2. 优化后的正则表达式
3. 解释优化原理
4. 提供其他常见正则陷阱及避免方法"""
    },
    {
        "id": 10,
        "title": "二叉树序列化",
        "type": "数据结构",
        "content": """实现二叉树的序列化和反序列化，要求：
1. 支持前序遍历序列化
2. 序列化格式为字符串（如"1,2,null,null,3,4,null,null,5,null,null"）
3. 反序列化能完整还原原树结构
4. 处理空树的情况
5. 提供测试用例验证正确性

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```"""
    }
]

def test_single(model_id: str, q: dict) -> dict:
    """测试单个编程题"""
    prompt = f"""你是一位资深软件工程师。请用中文回答以下编程问题，要求：
1. 代码完整、可运行
2. 解释清晰、有注释
3. 考虑边界情况和异常处理

【题目：{q['title']}】
类型：{q['type']}

{q['content']}"""
    
    start = time.time()
    try:
        resp = requests.post(
            f"{BASE_URL}/chat/completions",
            json={
                "model": model_id,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 2500
            },
            timeout=180  # 编程题给更长时间
        )
        elapsed = time.time() - start
        data = resp.json()
        
        if "choices" in data:
            return {
                "id": q["id"],
                "title": q["title"],
                "type": q["type"],
                "answer": data["choices"][0]["message"]["content"],
                "time": elapsed,
                "tokens": data.get("usage", {}).get("total_tokens", 0)
            }
    except Exception as e:
        return {
            "id": q["id"],
            "title": q["title"],
            "error": str(e),
            "time": time.time() - start
        }
    
    return {"id": q["id"], "title": q["title"], "error": "Unknown"}

def main():
    if len(sys.argv) < 2:
        print("用法: python test_coding.py <model_id> [output.json]")
        print("示例: python test_coding.py qwen/qwen3.5-35b-a3b memory/qwen_coding.json")
        sys.exit(1)
    
    model_id = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else f"memory/{model_id.replace('/', '_')}_coding.json"
    
    print(f"🚀 编程能力测试")
    print(f"模型: {model_id}")
    print(f"题目数: {len(PROGRAMMING_QUESTIONS)}")
    print("-" * 50)
    
    results = []
    for q in PROGRAMMING_QUESTIONS:
        print(f"Q{q['id']:2d}: [{q['type']:8s}] {q['title'][:30]}...", end=" ", flush=True)
        result = test_single(model_id, q)
        results.append(result)
        
        if "error" in result:
            print(f"❌ Error: {result['error'][:30]}")
        else:
            print(f"✅ ({result['time']:.1f}s, {result.get('tokens', 0)} tokens)")
    
    with open(output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 统计
    avg_time = sum(r['time'] for r in results if 'error' not in r) / len([r for r in results if 'error' not in r])
    avg_tokens = sum(r.get('tokens', 0) for r in results if 'error' not in r) / len([r for r in results if 'error' not in r])
    
    print("-" * 50)
    print(f"✅ 完成: {len([r for r in results if 'error' not in r])}/{len(results)}")
    print(f"⏱️  平均时间: {avg_time:.1f}s")
    print(f"📝 平均Token: {avg_tokens:.0f}")
    print(f"💾 结果保存: {output}")

if __name__ == "__main__":
    main()
