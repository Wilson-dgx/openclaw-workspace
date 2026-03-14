#!/usr/bin/env python3
"""
质量评估脚本 - 对比两个模型的输出质量
"""

import requests
import json

LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"

EVAL_QUESTIONS = [
    {
        "category": "推理能力",
        "question": "如果所有的A都是B，所有的B都是C，那么所有的A都是C吗？请解释你的推理过程。",
        "criteria": ["逻辑清晰", "步骤明确", "结论正确"]
    },
    {
        "category": "代码质量",
        "question": "实现一个函数，判断一个字符串是否是回文，考虑空格和大小写。",
        "criteria": ["代码正确", "考虑边界", "可读性好"]
    },
    {
        "category": "中文表达",
        "question": "用文言文风格写一段关于'春日'的短文（约100字）。",
        "criteria": ["文言准确", "意境优美", "符合格式"]
    },
    {
        "category": "数学计算",
        "question": "计算：∫(0 to π) sin²(x)dx，并解释积分过程。",
        "criteria": ["结果正确", "步骤清晰", "解释详细"]
    },
    {
        "category": "专业知识",
        "question": "解释Transformer架构中的自注意力机制（Self-Attention），包括Q、K、V的含义。",
        "criteria": ["概念准确", "解释清晰", "举例说明"]
    }
]

def call_model(model_id, prompt, max_tokens=800):
    """调用模型"""
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(LMSTUDIO_URL, json=payload, timeout=120)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: HTTP {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    models = ["super-120b-a12b", "qwen/qwen3.5-35b-a3b"]
    
    print("=" * 80)
    print("模型输出质量对比评估")
    print("=" * 80)
    
    results = {}
    
    for question in EVAL_QUESTIONS:
        print(f"\n【{question['category']}】")
        print(f"问题: {question['question']}")
        print("-" * 80)
        
        results[question['category']] = {}
        
        for model_id in models:
            short_name = model_id.split("/")[-1]
            print(f"\n>>> {short_name}:")
            
            answer = call_model(model_id, question['question'])
            results[question['category']][model_id] = answer
            
            # 显示前300字符
            preview = answer[:300] + "..." if len(answer) > 300 else answer
            print(preview)
            print()
    
    # 保存完整结果
    with open("quality_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 80)
    print("评估完成！完整结果已保存到 quality_results.json")
    print("=" * 80)

if __name__ == "__main__":
    main()
