#!/usr/bin/env python3
"""
本地大模型能力测试脚本 V2
- 测试各项能力
- 记录每个问题的token输出速度
"""

import requests
import json
import time
import os
from datetime import datetime

# 配置
API_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL_ID = "minimax/m2p5"

# 测试用例
TEST_CASES = {
    "1. 基础对话": [
        {"role": "user", "content": "你好，请用一句话介绍自己"},
    ],
    
    "2. 数学推理": [
        {"role": "user", "content": "小明有15个苹果，给了小红1/3，又给了小张2个，还剩多少？"},
        {"role": "user", "content": "如果今天是星期三，那么100天后是星期几？"},
    ],
    
    "3. 逻辑推理": [
        {"role": "user", "content": "所有猫都是动物。所有动物都需要水。因此，所有猫都需要水。这个推理是否正确？"},
        {"role": "user", "content": "如果明天下雨，球赛就会取消。明天没有下雨，请问球赛有没有取消？"},
    ],
    
    "4. 知识问答": [
        {"role": "user", "content": "量子纠缠是什么？请用通俗语言解释"},
        {"role": "user", "content": "光速大约是多少？"},
    ],
    
    "5. 中文理解": [
        {"role": "user", "content": "请把以下句子改成反问句：我今天必须去开会。"},
        {"role": "user", "content": "\"我想吃饭\"和\"我想要吃饭\"有什么区别？"},
    ],
    
    "6. 创意写作": [
        {"role": "user", "content": "用一句话写一个科幻小故事"},
    ],
    
    "7. 代码能力": [
        {"role": "user", "content": "用Python写一个快速排序函数"},
    ],
    
    "8. 上下文记忆": [
        {"role": "user", "content": "记住这个数字：9527"},
        {"role": "user", "content": "我刚才说的数字是多少？"},
    ],
}


def call_model(messages, temperature=0.7):
    """调用本地模型API，返回回复、token数和耗时"""
    headers = {"Content-Type": "application/json"}
    data = {
        "model": MODEL_ID,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 500,
    }
    
    start_time = time.time()
    
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=60)
        elapsed_time = time.time() - start_time
        
        response.raise_for_status()
        result = response.json()
        
        content = result["choices"][0]["message"]["content"]
        
        # 估算token数（中文约1.5字符/token，英文约4字符/token）
        # 更准确的方式是使用tokenizer，但这里用简单估算
        token_count = estimate_tokens(content)
        
        # 计算速度 (tokens/秒)
        speed = token_count / elapsed_time if elapsed_time > 0 else 0
        
        return {
            "content": content,
            "token_count": token_count,
            "elapsed_time": elapsed_time,
            "speed": speed
        }
    except Exception as e:
        return {
            "content": f"错误: {str(e)}",
            "token_count": 0,
            "elapsed_time": time.time() - start_time,
            "speed": 0
        }


def estimate_tokens(text):
    """简单估算token数量"""
    # 中文字符大约每1.5个字符算1个token
    # 英文单词平均4个字符1个token
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    other_chars = len(text) - chinese_chars
    return int(chinese_chars / 1.5 + other_chars / 4)


def run_test(category, messages):
    """运行单个测试"""
    print(f"\n{'='*60}")
    print(f"📂 {category}")
    print('='*60)
    
    full_conversation = []
    results = []
    
    for i, msg in enumerate(messages):
        full_conversation.append(msg)
        user_msg = msg["content"]
        
        print(f"\n❓ 用户: {user_msg}")
        
        result = call_model(full_conversation)
        
        content = result["content"]
        token_count = result["token_count"]
        elapsed_time = result["elapsed_time"]
        speed = result["speed"]
        
        print(f"🤖 回复: {content[:150]}{'...' if len(content)>150 else ''}")
        print(f"   📊 Token数: {token_count}, 耗时: {elapsed_time:.2f}秒, 速度: {speed:.2f} tokens/s")
        
        results.append({
            "question": user_msg,
            "answer": content,
            "token_count": token_count,
            "elapsed_time": elapsed_time,
            "speed": speed
        })
        
        # 添加助手回复到对话历史
        if "错误" not in content:
            full_conversation.append({"role": "assistant", "content": content})
        
        time.sleep(1)
    
    return results


def check_model_status():
    """检查模型是否在线"""
    try:
        response = requests.get("http://127.0.0.1:1234/v1/models", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print("✅ LM Studio API 在线")
            model_list = [m['id'] for m in models.get('data', [])]
            print(f"📋 可用模型: {model_list}")
            return True
    except Exception as e:
        print(f"❌ LM Studio 未运行或API不可用: {e}")
        return False
    return False


def main():
    print("="*60)
    print("🧪 本地大模型能力测试 V2")
    print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    if not check_model_status():
        print("\n请确保 LM Studio 正在运行，然后重新执行脚本。")
        return
    
    all_results = {}
    total_tokens = 0
    total_time = 0
    
    for category, messages_list in TEST_CASES.items():
        results = run_test(category, messages_list)
        all_results[category] = results
        
        for r in results:
            total_tokens += r["token_count"]
            total_time += r["elapsed_time"]
    
    # 汇总结果
    print("\n" + "="*60)
    print("📊 测试结果汇总")
    print("="*60)
    
    passed = 0
    failed = 0
    
    for category, results in all_results.items():
        status = "✅" if all("错误" not in r["answer"] for r in results) else "❌"
        if all("错误" not in r["answer"] for r in results):
            passed += 1
        else:
            failed += 1
        
        cat_tokens = sum(r["token_count"] for r in results)
        cat_time = sum(r["elapsed_time"] for r in results)
        cat_speed = cat_tokens / cat_time if cat_time > 0 else 0
        
        print(f"{status} {category}")
        for r in results:
            print(f"   - {r['question'][:40]}...")
            print(f"     回答: {r['answer'][:60]}...")
            print(f"     📊 {r['token_count']} tokens / {r['elapsed_time']:.2f}s = {r['speed']:.1f} tokens/s")
    
    overall_speed = total_tokens / total_time if total_time > 0 else 0
    
    print(f"\n总计: ✅ 通过 {passed} / ❌ 失败 {failed}")
    print(f"📈 总Token数: {total_tokens}, 总耗时: {total_time:.2f}秒")
    print(f"⚡ 总体速度: {overall_speed:.2f} tokens/s")
    
    # 保存详细报告
    report = {
        "test_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "model": MODEL_ID,
        "results": all_results,
        "summary": {
            "passed": passed,
            "failed": failed,
            "total_tokens": total_tokens,
            "total_time": total_time,
            "overall_speed": overall_speed
        }
    }
    
    report_file = f"{os.path.expanduser('~/.openclaw/agents/butler')}/test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n📄 详细报告已保存: {report_file}")


if __name__ == "__main__":
    main()