import os

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

project_root = os.path.dirname(os.path.dirname(__file__))  
model_path = os.path.join(project_root, "model", "chinese_emotion_classify_model")

# 加载模型和 tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# 加载 pipeline
classifier = pipeline(
    "sentiment-analysis",
    model=model,
    tokenizer=tokenizer,
    top_k=None,  
)

# 情绪标签映射
label_map = {
    "negative (stars 1, 2 and 3)": "消极",
    "positive (stars 4 and 5)": "积极"
}


# 主函数
def emotion_analyze(text):
    print("📝 评论内容：", text)

    # 情绪分析
    result = classifier(text)[0]
    print("\n📊 情感评分：")
    for r in result:
        label_zh = label_map.get(r['label'], r['label'])
        print(f"- {label_zh}: {r['score']:.4f}")

    top_result = max(result, key=lambda x: x['score'])
    top_label = label_map.get(top_result['label'], top_result['label']) 
    top_score = label_map.get(top_result['score'], top_result['score'])
    print(f"🎯 最终判断：{top_label}, {round(top_score,4)}")
    return f"{top_label}, 置信度：{round(top_score,4)}"

# 示例调用
if __name__ == "__main__":
    emotion_analyze("T恤大小合适，颜色干净，版型好看，透气性好，穿着很舒服，就是花纹有点丑")
