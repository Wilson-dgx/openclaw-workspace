#!/usr/bin/env python3
"""
管家 - LM Studio 本地模型调用工具
绕开 OpenClaw 模型路由，直接使用本地 API
"""
import subprocess
import json
import sys

LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL_ID = "minimax/minimax-m2.5"

def chat_with_lmstudio(messages, temperature=0.7, max_tokens=2000):
    """
    直接调用 LM Studio API
    messages: list of {"role": "user"|"assistant"|"system", "content": "..."}
    """
    payload = {
        "model": MODEL_ID,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        result = subprocess.run(
            ['curl', '-s', '-X', 'POST', LM_STUDIO_URL,
             '-H', 'Content-Type: application/json',
             '-d', json.dumps(payload)],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        
        response = json.loads(result.stdout)
        
        if 'choices' in response and len(response['choices']) > 0:
            return response['choices'][0]['message']['content']
        else:
            return f"Error: Unexpected response format: {result.stdout[:200]}"
            
    except subprocess.TimeoutExpired:
        return "Error: Request timed out (120s)"
    except json.JSONDecodeError:
        return f"Error: Invalid JSON response: {result.stdout[:200]}"
    except Exception as e:
        return f"Error: {str(e)}"


def simple_chat(user_message, system_prompt=None):
    """
    简单对话模式
    """
    messages = []
    
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    messages.append({"role": "user", "content": user_message})
    
    return chat_with_lmstudio(messages)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("Usage: python3 lmstudio_chat.py '你的消息'")
        print("   or: python3 lmstudio_chat.py --system '系统提示' '你的消息'")
        sys.exit(1)
    
    if sys.argv[1] == '--system' and len(sys.argv) >= 4:
        system_prompt = sys.argv[2]
        user_message = sys.argv[3]
        response = simple_chat(user_message, system_prompt)
    else:
        user_message = sys.argv[1]
        response = simple_chat(user_message)
    
    print(response)


if __name__ == "__main__":
    main()