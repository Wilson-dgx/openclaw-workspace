#!/usr/bin/env python3
"""
Qwen 3.5-35B-A3B 能力测试 - 单模型测试
"""

import requests
import json
import time
import sys

BASE_URL = "http://127.0.0.1:1234/v1"

QUESTIONS = [
    {
        "id": 1,
        "title": "囚徒困境变体",
        "content": """三名囚徒A、B、C，每人有两个选择：认罪或不认罪。
如果三人都认罪，各判5年；如果都不认罪，各判1年；如果部分人认罪，认罪者判0年，不认罪者判10年。
假设三人都是完全理性的，且不能沟通，他们会如何选择？"""
    },
    {
        "id": 2,
        "title": "海盗分金",
        "content": """5名海盗分100枚金币，从船长开始提方案，≥50%同意则通过，否则提议者被扔下海。
海盗优先级：1)活命 2)多得金币 3)看他人被扔下海。船长应如何分配？"""
    },
    {
        "id": 3,
        "title": "蒙提霍尔问题",
        "content": """三扇门中选一扇，背后有汽车，另两扇是山羊。主持人知道门后情况，打开一扇有山羊的门，问你是否换门。
换门和不换门哪个获胜概率更高？"""
    },
    {
        "id": 4,
        "title": "说谎者悖论",
        "content": """某人A说："我说的所有话都是假的。"这句话是否有意义？如何避免悖论？"""
    },
    {
        "id": 5,
        "title": "蓝眼睛岛民",
        "content": """岛上有1000人，100人有蓝眼睛。岛规：知道眼睛颜色必须当晚自杀。
旅行者当众说："我看到岛上有蓝眼睛的人。"会发生什么？"""
    },
    {
        "id": 6,
        "title": "爱因斯坦逻辑谜题",
        "content": """五间房子排成一列。英国人住红房，瑞典人养狗，丹麦人喝茶，绿房在白房左边相邻，绿房喝咖啡，抽Pall Mall养鸟，黄房抽Dunhill，中间喝牛奶，挪威人住第一间，抽Blends住养猫隔壁，养马住抽Dunhill隔壁，抽Blue Master喝啤酒，德国人抽Prince，挪威人住蓝房隔壁。谁养鱼？谁喝水？"""
    },
    {
        "id": 7,
        "title": "无限旅馆",
        "content": """无限房间旅馆住满客人。又来一位新客人，如何安排？来无限多位呢？来无限多辆巴士每辆无限乘客呢？"""
    },
    {
        "id": 8,
        "title": "意外绞刑",
        "content": """法官宣布下周一到周五某天绞刑，当天早上囚犯不会知道。囚犯推理排除所有可能，但周四被绞刑了，这算"意外"吗？问题在哪？"""
    },
    {
        "id": 9,
        "title": "纽康姆悖论",
        "content": """盒子A有1000元，盒子B可能有100万。预言家预测：只拿B则放100万，拿A和B则放0。预测准确率99%，应只拿B还是两个都拿？"""
    },
    {
        "id": 10,
        "title": "理发师悖论",
        "content": """理发师给所有不给自己刮脸的人刮脸。理发师给自己刮脸吗？现代数学如何解决？"""
    }
]

def test_single(model_id: str, q: dict) -> dict:
    """测试单个问题"""
    prompt = f"""用中文详细回答，给出完整推理过程和最终答案：

【题目：{q['title']}】
{q['content']}"""
    
    start = time.time()
    try:
        resp = requests.post(
            f"{BASE_URL}/chat/completions",
            json={
                "model": model_id,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 2000
            },
            timeout=120
        )
        elapsed = time.time() - start
        data = resp.json()
        
        if "choices" in data:
            return {
                "id": q["id"],
                "title": q["title"],
                "answer": data["choices"][0]["message"]["content"],
                "time": elapsed,
                "tokens": data.get("usage", {}).get("total_tokens", 0)
            }
    except Exception as e:
        return {"id": q["id"], "title": q["title"], "error": str(e), "time": time.time()-start}
    
    return {"id": q["id"], "title": q["title"], "error": "Unknown"}

def main():
    model_id = sys.argv[1] if len(sys.argv) > 1 else "qwen/qwen3.5-35b-a3b"
    output = sys.argv[2] if len(sys.argv) > 2 else "memory/qwen_results.json"
    
    print(f"测试模型: {model_id}")
    results = []
    
    for q in QUESTIONS:
        print(f"Q{q['id']}: {q['title'][:20]}...", end=" ", flush=True)
        result = test_single(model_id, q)
        results.append(result)
        if "error" in result:
            print(f"✗ Error")
        else:
            print(f"✓ ({result['time']:.1f}s)")
    
    with open(output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n结果保存: {output}")

if __name__ == "__main__":
    main()
