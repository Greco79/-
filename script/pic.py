import openai
import base64
import os
import json
import re

from io import BytesIO
from emotion_classifier import emotion_analyze

# 填写openai的key
key = ""

# ✅ 设置代理（如 v2rayN 的 socks5）
os.environ["HTTPS_PROXY"] = "socks5://127.0.0.1:10808"

client = openai.OpenAI(api_key = key)


# ✅ 工具函数：图像转 base64
def pil_to_base64(pil_img):
    buffered = BytesIO()
    pil_img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def parse_reply(reply_text):
    def extract(key):
        pattern = rf"{key}[:：]\s*(.+)"
        match = re.search(pattern, reply_text)
        return match.group(1).strip() if match else ""

    return {
        "图文一致性": extract("图文一致性"),
        "优点": extract("优点"),
        "缺点": extract("缺点"),
        "综合评价": extract("综合评价"),
        "建议": extract("改进建议") or extract("建议") or extract("改进")
    }

# ✅ 主分析函数：商品图 + 评论图 + 评论文本
def analyze_with_images(product_img, review_img, comment_text):
    # 图像转 base64
    product_b64 = pil_to_base64(product_img)
    review_b64 = pil_to_base64(review_img)

    # 构造三重一致性分析 prompt
    prompt = f"""
你是一名电商平台的多模态分析专家，请根据以下信息判断图文是否一致，并进行结构化分析：

【任务】
请逐项分析以下三组图文是否一致，每项都要包含：
- 是否一致（是/否）
- 一致性评分（0~100）
- 不一致原因简述（若一致则写“无”）

【三项对比】
1. 商品图 vs 用户评论图
2. 用户评论图 vs 用户评论文字
3. 商品图 vs 用户评论文字

【用户评论】：
“{comment_text}”

【输出格式】
请使用标准 JSON 格式输出以下结构：

{{
  "商品图_vs_评论图": {{
    "一致性": "是/否",
    "评分": 92,
    "原因": "..."
  }},
  "评论图_vs_评论内容": {{
    "一致性": "是/否",
    "评分": 88,
    "原因": "..."
  }},
  "商品图_vs_评论内容": {{
    "一致性": "是/否",
    "评分": 90,
    "原因": "..."
  }},
  "综合评价": "...",
  "建议": "..."
}}
"""

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{product_b64}"}},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{review_b64}"}}
            ]
        }
    ]

    # 调用 GPT-4o
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=1024
    )

    reply = response.choices[0].message.content.strip()

    # 清洗 markdown 包裹
    reply_cleaned = reply.strip()
    if reply_cleaned.startswith("```json"):
        reply_cleaned = reply_cleaned.removeprefix("```json").strip()
    if reply_cleaned.endswith("```"):
        reply_cleaned = reply_cleaned.removesuffix("```").strip()

    # 本地模型情绪分析
    emotion = emotion_analyze(comment_text)

    # 尝试 JSON 解析
    try:
        result = json.loads(reply_cleaned)
        return (
            f"{result['商品图_vs_评论图']['一致性']}({result['商品图_vs_评论图']['评分']}分）：{result['商品图_vs_评论图']['原因']}",
            f"{result['评论图_vs_评论内容']['一致性']}({result['评论图_vs_评论内容']['评分']}分）：{result['评论图_vs_评论内容']['原因']}",
            f"{result['商品图_vs_评论内容']['一致性']}({result['商品图_vs_评论内容']['评分']}分）：{result['商品图_vs_评论内容']['原因']}",
            emotion,
            result['综合评价'],
            result['建议'],
            result['商品图_vs_评论图']['评分'],    
            result['评论图_vs_评论内容']['评分'],
            result['商品图_vs_评论内容']['评分']
        )
    except Exception as e:
        # fallback 原文输出
        return "", "", "", "", reply,"","","",""
