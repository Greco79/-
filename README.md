# 商品评论图文一致性与情绪分析系统
本项目是一个基于 Python + Gradio 的交互式图文评论分析工具，支持用户上传商品图、评论图与评论文本，输出图文一致性评分、可视化图表、综合评价、情绪分析结果，并一键导出 PDF 报告。

## 功能简介
1. 商品图上传：上传商品官方图                                                   
2. 评论图上传: 上传买家实拍图                                                   
3. 评论文本: 输入用户评价内容                                                  
4. 图文一致性分析: 分别评估三种组合的一致性：<br>商品图 vs 评论图<br>评论图 vs 评论文本<br>商品图 vs 评论文本 
5. 可视化展示: 条形图动态展示一致性评分，支持红黄绿渐变色条                                    
6. 情绪分析: 自动识别评论文本情绪倾向（积极/消极）                                       
7. PDF 报告导出: 包含评分图、评分文本、情绪分析的完整可视化报告                                

## 安装依赖
建议使用 Python 3.8+ 和虚拟环境：
pip install -r requirements.txt

主要依赖：
gradio
matplotlib
transformers
fpdf
Pillow
numpy

## 启动方式
在项目根目录下运行：
python scripts/main.py

或使用模块方式运行 UI：
python -m scripts.main

## 🤖 情绪分析模型说明

本项目中的情绪分析模块基于 Hugging Face 提供的中文预训练模型：

> [uer/roberta-base-finetuned-jd-binary-chinese](https://huggingface.co/uer/roberta-base-finetuned-jd-binary-chinese)

该模型由 UER 团队在京东商品评论数据上进行二分类情感微调，适用于判断中文评论的“积极/消极”倾向。

在此基础上，我们对其进行了二次微调，使用自定义的商品评论数据集进一步训练，使模型在本项目电商评论场景中的表现更为稳定和准确。

### 📂 本地模型加载路径

本地模型路径：`model/chinese_emotion_classify_model/`  
包含 tokenizer 和 PyTorch 格式的分类模型，可通过 transformers 加载使用。

### 📌 微调补充说明

- 基础模型：`uer/roberta-base-finetuned-jd-binary-chinese`
- 下游任务：二分类（积极 / 消极）
- 自定义数据集规模：约 XXX 条中文商品评论（可自行填写）
- 使用方式：transformers pipeline + 本地推理

## 大语言模型（LLM）调用说明
本项目部分自然语言处理任务（如综合评价生成、建议生成等）依赖于 OpenAI 的大语言模型 GPT-4o。

部署时需配置有效的 OpenAI API Key

推荐结合代理工具或本地部署控制请求频率与费用

### 示例 API 调用代码：
import openai

openai.api_key = "your-api-key"

response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "你是一个商品评论分析助手"},
        {"role": "user", "content": "请根据以下分析结果，生成综合评价与优化建议..."}
    ]
)


## 输出报告内容（PDF）

自动生成内容包括：
1. 图文一致性评分图
2. 每一项一致性分析结果
3. 综合一致性评价
4. 智能建议
5. 评论情绪分析结果

## 作者说明
该项目由Greco79独立开发完成，欢迎讨论和交流。
如需集成至电商平台、产品评论监控系统或教学演示，可通过 Issue 或邮箱联系我。
