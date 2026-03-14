#!/usr/bin/env python3
"""
本地大模型能力测试脚本
测试 LM Studio 上运行的 MiniMax M2.5 模型各项能力
"""

import requests
import json
import time
from datetime import datetime

# 配置
API_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL_ID = "minimax/minimax-m2.5"

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
    """调用本地模型API"""
    headers = {"Content-Type": "application/json"}
    data = {
        "model": MODEL_ID,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 500,
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"错误: {str(e)}"


def run_test(category, messages):
    """运行单个测试"""
    print(f"\n{'='*50}")
    print(f"📂 {category}")
    print('='*50)
    
    # 如果有多轮消息，逐轮测试
    full_conversation = []
    results = []
    
    for i, msg in enumerate(messages):
        full_conversation.append(msg)
        user_msg = msg["content"]
        
        print(f"\n❓ 用户: {user_msg[:100]}{'...' if len(user_msg)>100 else ''}")
        
        response = call_model(full_conversation)
        
        if "错误" in str(response):
            print(f"❌ 返回: {response}")
            results.append({"question": user_msg, "answer": response, "status": "failed"})
        else:
            print(f"🤖 回复: {response[:200]}{'...' if len(response)>200 else ''}")
            results.append({"question": user_msg, "answer": response, "status": "ok"})
        
        # 添加助手回复到对话历史
        if "错误" not in str(response):
            full_conversation.append({"role": "assistant", "content": response})
        
        time.sleep(1)  # 避免请求过快
    
    return results


def check_model_status():
    """检查模型是否在线"""
    try:
        response = requests.get("http://127.0.0.1:1234/v1/models", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print("✅ LM Studio API 在线")
            print(f"📋 可用模型: {models.get('data', [])}")
            return True
    except Exception as e:
        print(f"❌ LM Studio 未运行或API不可用: {e}")
        return False
    return False


def main():
    print("="*60)
    print("🧪 本地大模型能力测试")
    print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # 检查模型状态
    if not check_model_status():
        print("\n请确保 LM Studio 正在运行，然后重新执行脚本。")
        return
    
    # 运行所有测试
    all_results = {}
    
    for category, messages_list in TEST_CASES.items():
        results = run_test(category, messages_list)
        all_results[category] = results
    
    # 汇总结果
    print("\n" + "="*60)
    print("📊 测试结果汇总")
    print("="*60)
    
    passed = 0
    failed = 0
    
    for category, results in all_results.items():
        status = "✅" if all(r["status"] == "ok" for r in results) else "❌"
        if all(r["status"] == "ok" for r in results):
            passed += 1
        else:
            failed += 1
        print(f"{status} {category}")
    
    print(f"\n总计: ✅ 通过 {passed} / ❌ 失败 {failed}")
    
    # 保存详细报告
    import os
    report_dir = os.path.expanduser("~/.openclaw/agents/butler")
    os.makedirs(report_dir, exist_ok=True)
    report_file = f"{report_dir}/test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"\n📄 详细报告已保存: {report_file}")


if __name__ == "__main__":
    main()