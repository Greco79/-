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

## 项目结构
project/
├── scripts/
│   ├── main.py              # 项目入口
│   ├── ui.py                # Gradio UI 主函数
│   └── emotion_classifier.py# 情绪分析模块
├── ttf/
│   └── simsun.ttf           # 中文字体支持
├── model/
│   └── chinese_emotion_classify_model/  # 本地transformers模型
├── utils/
│   └── draw_score_bar.py    # 可视化评分绘图函数
└── README.md                # 项目说明文档

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
