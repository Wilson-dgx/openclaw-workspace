#!/usr/bin/env python3
"""
Qwen 3.5-35B-A3B 能力测试脚本
对比模型: minimax/minimax-m2.5
"""

import requests
import json
import time
from typing import Dict, List, Tuple

BASE_URL = "http://127.0.0.1:1234/v1"
QWEN_MODEL = "qwen/qwen3.5-35b-a3b"
MINIMAX_MODEL = "minimax-m2p5-mlx"

# 10道高难度逻辑题（与之前测试相同）
QUESTIONS = [
    {
        "id": 1,
        "title": "囚徒困境变体",
        "content": """三名囚徒A、B、C，每人有两个选择：认罪或不认罪。
如果三人都认罪，各判5年；
如果都不认罪，各判1年；
如果部分人认罪，认罪者判0年（转为污点证人），不认罪者判10年。
假设三人都是完全理性的，且不能沟通，他们会如何选择？最终均衡结果是什么？""",
        "expected": "三人都认罪，各判5年（纳什均衡）"
    },
    {
        "id": 2,
        "title": "海盗分金（5人版）",
        "content": """5名海盗要分配100枚金币，从船长开始依次提出分配方案，所有人（包括提议者）投票，如果≥50%同意则通过，否则提议者被扔下海。
海盗们优先级：1)活命 2)多得金币 3)看他人被扔下海。
船长应如何分配？""",
        "expected": "船长得98枚，给第3和第5名海盗各1枚"
    },
    {
        "id": 3,
        "title": "蒙提霍尔问题（三门问题）",
        "content": """你在三扇门中选一扇，背后有汽车，另两扇是山羊。
主持人（知道门后情况）打开一扇有山羊的门，然后问你是否要换门。
从概率角度，换门和不换门哪个获胜概率更高？各是多少？""",
        "expected": "换门概率2/3，不换门1/3"
    },
    {
        "id": 4,
        "title": "说谎者悖论变体",
        "content": """某人A说："我说的所有话都是假的。"
如果A说的是真话，那么他的话是假的；
如果他说的是假话，那么"他说的所有话都是假的"这句话是假的，意味着他说的有些话是真的。
这句话是否有意义？如何避免悖论？""",
        "expected": "悖论性语句，无法赋真值；避免方法：语言分层/禁止自指/多值逻辑"
    },
    {
        "id": 5,
        "title": "蓝眼睛岛民谜题",
        "content": """一个岛上有1000人，其中100人有蓝眼睛，其余是棕眼睛。
岛规：禁止讨论眼睛颜色，一旦有人知道自己眼睛颜色就必须当晚自杀。
某天旅行者当众说："我看到岛上有蓝眼睛的人。"
假设所有人都是完美逻辑学家，会发生什么？""",
        "expected": "第100天晚上，100个蓝眼睛的人同时自杀"
    },
    {
        "id": 6,
        "title": "爱因斯坦逻辑谜题（斑马谜题）",
        "content": """五间房子排成一列，颜色各异。
英国人住红房，瑞典人养狗，丹麦人喝茶，绿房在白房左边且相邻，绿房主人喝咖啡，抽Pall Mall的人养鸟，黄房主人抽Dunhill，中间房主人喝牛奶，挪威人住第一间，抽Blends的人住在养猫的人隔壁，养马的人住在抽Dunhill的人隔壁，抽Blue Master的人喝啤酒，德国人抽Prince，挪威人住在蓝房隔壁。
问：谁养鱼？谁喝水？""",
        "expected": "德国人养鱼，挪威人喝水"
    },
    {
        "id": 7,
        "title": "无限旅馆悖论",
        "content": """一个拥有无限多房间的旅馆住满了客人。
又来了一位新客人，老板如何安排？
如果来了无限多位新客人呢？
如果来了无限多辆巴士，每辆巴士上有无限多位乘客呢？
这说明无穷集合有什么性质？""",
        "expected": "后移法/奇偶法/质数幂法；说明ℵ₀+1=ℵ₀，ℵ₀+ℵ₀=ℵ₀，ℵ₀×ℵ₀=ℵ₀"
    },
    {
        "id": 8,
        "title": "意外绞刑悖论",
        "content": """法官宣布：囚犯将在下周一到周五的某天中午被绞刑，且行刑当天早上囚犯不会知道今天会被绞刑（即行刑是"意外"的）。
囚犯推理：不可能是周五，因为周四晚上如果还没被绞刑，就知道是周五，不是意外了；同理不可能是周四...最终推出不可能被绞刑。
但周四他被绞刑了，这算"意外"吗？问题出在哪里？""",
        "expected": "周四确实算意外；错误在于混淆事后确定性与事前不确定性"
    },
    {
        "id": 9,
        "title": "纽康姆悖论",
        "content": """两个盒子：盒子A透明且有1000元，盒子B不透明，可能为空或有100万元。
预言家已经预测了你的选择：如果你只拿B，他就放100万；如果你拿A和B，他就放0。
假设预言家预测准确率99%，你应该只拿B还是两个都拿？""",
        "expected": "只拿B期望99万，拿两个期望1.1万；推荐只拿B"
    },
    {
        "id": 10,
        "title": "理发师悖论",
        "content": """一个村庄里，理发师给所有不给自己刮脸的人刮脸。
那么理发师给自己刮脸吗？
这个问题在现代数学（集合论）中是如何解决的？""",
        "expected": "不存在这样的理发师；通过ZFC公理化集合论解决"
    }
]

def test_model(model_id: str, question: Dict) -> Tuple[str, float, Dict]:
    """测试单个问题，返回答案、耗时和统计信息"""
    
    prompt = f"""请用中文详细回答以下逻辑题，给出完整推理过程和最终答案：

【题目{question['id']}：{question['title']}】
{question['content']}

要求：
1. 给出详细的推理过程
2. 给出明确的最终答案
3. 使用中文回答"""
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            json={
                "model": model_id,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 2000
            },
            timeout=180
        )
        
        elapsed = time.time() - start_time
        result = response.json()
        
        if "choices" in result and len(result["choices"]) > 0:
            answer = result["choices"][0]["message"]["content"]
            usage = result.get("usage", {})
            return answer, elapsed, {
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0)
            }
        else:
            return f"Error: {result}", elapsed, {}
            
    except Exception as e:
        return f"Exception: {str(e)}", time.time() - start_time, {}

def run_tests(model_id: str, model_name: str) -> List[Dict]:
    """运行所有测试"""
    results = []
    
    print(f"\n{'='*60}")
    print(f"开始测试: {model_name}")
    print(f"{'='*60}\n")
    
    for q in QUESTIONS:
        print(f"测试 Q{q['id']}: {q['title']}...", end=" ", flush=True)
        
        answer, elapsed, usage = test_model(model_id, q)
        
        result = {
            "id": q["id"],
            "title": q["title"],
            "expected": q["expected"],
            "answer": answer,
            "time": elapsed,
            "usage": usage
        }
        results.append(result)
        
        print(f"✓ ({elapsed:.1f}s, {usage.get('total_tokens', 0)} tokens)")
    
    return results

def save_results(qwen_results: List[Dict], minimax_results: List[Dict]):
    """保存测试结果为JSON和Markdown报告"""
    
    # JSON格式
    data = {
        "qwen_qwen3.5-35b-a3b": qwen_results,
        "minimax_m2p5": minimax_results,
        "metadata": {
            "test_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "test_questions": 10,
            "test_type": "高难度逻辑题"
        }
    }
    
    with open("memory/model_comparison_raw.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n原始结果已保存: memory/model_comparison_raw.json")

if __name__ == "__main__":
    # 测试 Qwen
    qwen_results = run_tests(QWEN_MODEL, "Qwen 3.5-35B-A3B")
    
    # 测试 Minimax
    minimax_results = run_tests(MINIMAX_MODEL, "Minimax M2.5")
    
    # 保存结果
    save_results(qwen_results, minimax_results)
    
    print("\n" + "="*60)
    print("测试完成！正在生成详细报告...")
    print("="*60)
