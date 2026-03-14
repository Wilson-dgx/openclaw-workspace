#!/usr/bin/env python3
"""
管家任务执行器
使用本地 LM Studio 模型处理任务
"""
import subprocess
import json
import os
import sys

WORKSPACE = "/Users/ciss-ai/.openclaw/workspace"
LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL_ID = "minimax/minimax-m2.5"

def lmstudio_chat(messages, temperature=0.7, max_tokens=2000):
    """调用 LM Studio API"""
    payload = {
        "model": MODEL_ID,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    result = subprocess.run(
        ['curl', '-s', '-X', 'POST', LM_STUDIO_URL,
         '-H', 'Content-Type: application/json',
         '-d', json.dumps(payload)],
        capture_output=True,
        text=True,
        timeout=120
    )
    
    if result.returncode != 0:
        return None, result.stderr
    
    try:
        response = json.loads(result.stdout)
        content = response['choices'][0]['message']['content']
        return content, None
    except:
        return None, result.stdout[:500]


def generate_ai_daily_report():
    """生成AI每日简报"""
    # 调用工作区的脚本
    result = subprocess.run(
        ['python3', f'{WORKSPACE}/tools/ai_daily_report.py'],
        capture_output=True,
        text=True,
        timeout=300,
        cwd=WORKSPACE
    )
    return result.stdout if result.returncode == 0 else result.stderr


def archive_memory():
    """归档memory文件"""
    result = subprocess.run(
        ['python3', f'{WORKSPACE}/tools/memory_manager.py', 'archive', '7'],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=WORKSPACE
    )
    return result.stdout if result.returncode == 0 else result.stderr


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: butler_task.py <task> [args...]")
        print("")
        print("Tasks:")
        print("  ai-report              生成AI每日简报")
        print("  memory-archive         归档旧memory文件")
        print("  chat '<message>'       使用本地模型对话")
        print("")
        sys.exit(1)
    
    task = sys.argv[1]
    
    if task == "ai-report":
        print("🏠 管家：开始执行AI每日简报任务...")
        result = generate_ai_daily_report()
        print(result)
        
    elif task == "memory-archive":
        print("🏠 管家：开始执行Memory归档任务...")
        result = archive_memory()
        print(result)
        
    elif task == "chat":
        message = sys.argv[2] if len(sys.argv) > 2 else "你好"
        system = "你是方正军（方总）的管家智能体，使用本地MiniMax M2.5模型运行。你稳重可靠、细致周到，负责处理日常事务。"
        
        print(f"🏠 管家：处理请求...")
        response, error = lmstudio_chat([
            {"role": "system", "content": system},
            {"role": "user", "content": message}
        ])
        
        if response:
            print(response)
        else:
            print(f"❌ 错误: {error}")
    else:
        print(f"❌ 未知任务: {task}")


if __name__ == "__main__":
    main()