import os
import gradio as gr
import tempfile
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.patches as patches

from fpdf import FPDF
from pic import analyze_with_images
import matplotlib.font_manager as fm

# 设置字体路径
project_root = os.path.dirname(os.path.dirname(__file__))
simsun_path = os.path.join(project_root, "ttf", "simsun.ttf")

# 注册字体
if os.path.exists(simsun_path):
    my_font = fm.FontProperties(fname=simsun_path)
else:
    raise FileNotFoundError("找不到 simsun.ttf, 中文会乱码")

def draw_score_bar(score1, score2, score3):
    items = ["商品图 vs 评论图", "评论图 vs 评论内容", "商品图 vs 评论内容"]
    scores = [float(score1), float(score2), float(score3)]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.5, len(items) - 0.5)

    # 使用红-黄-绿颜色映射（0分红，50分黄，100分绿）
    cmap = cm.get_cmap('RdYlGn')
    gradient_full = np.linspace(0.0, 1.0, 500).reshape(1, -1)  # 全色条

    for i, (label, score) in enumerate(zip(items, scores)):
        # 渐变色：整条从红->绿的完整渐变
        ax.imshow(cmap(gradient_full),
                  extent=[0, 100, i - 0.2, i + 0.2],
                  aspect='auto',
                  interpolation='bicubic',
                  zorder=1)

        # 遮住超出得分区域（灰白遮罩）
        ax.barh(i, 100, height=0.4, left=score,
                color='white', edgecolor='none', zorder=2)

        # 分数文字
        ax.text(score + 1, i, f"{score:.1f} 分", va='center',
                fontsize=11, fontproperties=my_font)

    ax.set_yticks(range(len(items)))
    ax.set_yticklabels(items, fontproperties=my_font)
    ax.set_xlabel("一致性评分", fontproperties=my_font)
    ax.set_title("图文一致性分析评分可视化（按分数截断红-绿完整渐变）", fontproperties=my_font)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    return fig


def export_pdf(score_plot, product_vs_review, review_vs_text, product_vs_text, overall, suggestion, emotion_summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("SimSun", "", simsun_path, uni=True)
    pdf.set_font("SimSun", size=12)

    # 保存图像为临时文件
    plot_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
    score_plot.savefig(plot_path)

    # 插入图像
    pdf.cell(0, 10, "一致性评分可视化图：", ln=True)
    pdf.image(plot_path, x=10, y=None, w=180)
    pdf.ln(5)

    content = {
        
        "商品图 vs 评论图 一致性分析": product_vs_review,
        "评论图 vs 评论内容 一致性分析": review_vs_text,
        "商品图 vs 评论内容 一致性分析": product_vs_text,
        "综合评价": overall,
        "建议": suggestion,
        "评论情绪分析": emotion_summary
    }

    for k, v in content.items():
        pdf.multi_cell(0, 10, f"{k}：{v}")
        pdf.ln(5)

    tmp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    pdf.output(tmp_path)
    return tmp_path


def full_analysis(product_img, review_img, comment_text):
    r1, r2, r3, r4, r5, r6, s1, s2, s3 = analyze_with_images(product_img, review_img, comment_text)

    fig = draw_score_bar(s1, s2, s3)

    return r1, r2, r3, r4, r5, r6, fig, fig

def ui_entry():
    with gr.Blocks() as demo:
        gr.Markdown("<h1 style='text-align: left;'>🛍️ 商品评论智能分析系统</h1>")

        fig_state = gr.State() 

        with gr.Row():
            product_img = gr.Image(type="pil", label="商品图片（官方）", height=300, width=300)
            review_img = gr.Image(type="pil", label="评论图片（实拍）", height=300, width=300)

        comment_text = gr.Textbox(lines=4, label="用户评论文本", placeholder="例如：颜色干净，图案好看，穿着舒适")
        btn = gr.Button("分析")

        with gr.Row():
            with gr.Column(scale=4):  # 图放左边
                score_plot = gr.Plot(label="一致性评分可视化图")
            gr.Column(scale=1)  # 右侧空列，让图靠左
        out1 = gr.Textbox(label="商品图 vs 评论图 一致性分析")
        out2 = gr.Textbox(label="评论图 vs 评论内容 一致性分析")
        out3 = gr.Textbox(label="商品图 vs 评论内容 一致性分析")
        out4 = gr.Textbox(label="评论情绪分析")
        out5 = gr.Textbox(label="综合评价")
        out6 = gr.Textbox(label="建议 / 原始输出")

        btn_pdf = gr.Button("📄 下载 PDF 报告")
        file_pdf = gr.File(label="点击下载 PDF", visible=True)

        btn.click(
            full_analysis,
            inputs=[product_img, review_img, comment_text],
            outputs=[out1, out2, out3, out4, out5, out6, score_plot, fig_state]
        )
        btn_pdf.click(export_pdf, inputs=[fig_state, out1, out2, out3, out4, out5, out6], outputs=file_pdf)

    demo.launch()
