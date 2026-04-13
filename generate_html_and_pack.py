#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成IP成果展示HTML页面 + 全量文件打包
"""

import os
import zipfile
from datetime import datetime

def generate_html():
    """生成HTML展示页面"""
    output_dir = "C:/Users/User/.openclaw/workspace/skills/siri-ip-series-wanxiang/output"
    
    # 收集所有文件
    files = os.listdir(output_dir)
    images = [f for f in files if f.endswith(('.jpg', '.png', '.jpeg'))]
    videos = [f for f in files if f.endswith('.mp4')]
    
    # 按类别分组
    categories = {
        "基础三视图": [f for f in images if "3view" in f],
        "风格转换系列": [f for f in images if any(t in f for t in ["guochao", "qstyle", "watercolor"])],
        "动作延展系列": [f for f in images if "action" in f],
        "文创设计系列": [f for f in images if "cultural" in f],
        "表情包系列": [f for f in images if "emoji" in f],
    }
    
    # HTML模板
    html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>长颈鹿IP系列化成果展示</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }}
        .header h1 {{
            font-size: 48px;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .header p {{
            font-size: 18px;
            opacity: 0.9;
        }}
        .category {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        .category h2 {{
            color: #667eea;
            font-size: 28px;
            margin-bottom: 20px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        .grid-item {{
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .grid-item:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.25);
        }}
        .grid-item img {{
            width: 100%;
            height: auto;
            display: block;
        }}
        .grid-item video {{
            width: 100%;
            height: auto;
            display: block;
        }}
        .item-title {{
            padding: 12px;
            background: #f8f9fa;
            font-size: 14px;
            color: #333;
            text-align: center;
            font-weight: 500;
        }}
        .video-section {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        .video-section h2 {{
            color: #667eea;
            font-size: 28px;
            margin-bottom: 20px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        .video-container {{
            max-width: 800px;
            margin: 0 auto;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .footer {{
            text-align: center;
            color: white;
            margin-top: 50px;
            opacity: 0.8;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🦒 长颈鹿IP系列化成果展示</h1>
            <p>生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | 共{len(images)}张高清图片 + {len(videos)}个动态短视频</p>
        </div>
"""
    
    # 添加分类内容
    for category_name, category_files in categories.items():
        if category_files:
            html_template += f"""
        <div class="category">
            <h2>{category_name}</h2>
            <div class="grid">
"""
            for file in category_files:
                title = file.replace(".jpg", "").replace(".png", "").replace("giraffe_", "").replace("_", " ").title()
                html_template += f"""
                <div class="grid-item">
                    <img src="{file}" alt="{title}">
                    <div class="item-title">{title}</div>
                </div>
"""
            html_template += """
            </div>
        </div>
"""
    
    # 添加视频部分
    if videos:
        html_template += """
        <div class="video-section">
            <h2>动态短视频</h2>
            <div class="video-container">
"""
        for video in videos:
            title = video.replace(".mp4", "").replace("giraffe_", "").replace("_", " ").title()
            html_template += f"""
                <video controls>
                    <source src="{video}" type="video/mp4">
                    您的浏览器不支持视频播放
                </video>
                <div class="item-title">{title}</div>
"""
        html_template += """
            </div>
        </div>
"""
    
    # 页脚
    html_template += """
        <div class="footer">
            <p>© 2026 IP系列化生成工具 | 所有素材均为AI生成，可商用</p>
        </div>
    </div>
</body>
</html>
"""
    
    # 保存HTML
    html_path = os.path.join(output_dir, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_template)
    
    print(f"HTML页面已生成: {html_path}")
    return html_path

def pack_files():
    """打包所有文件到压缩包"""
    output_dir = "C:/Users/User/.openclaw/workspace/skills/siri-ip-series-wanxiang/output"
    zip_path = "C:/Users/User/.openclaw/workspace/skills/siri-ip-series-wanxiang/长颈鹿IP全量素材包.zip"
    
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        # 遍历output目录
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, output_dir)
                zipf.write(file_path, arcname)
                print(f"已添加: {arcname}")
    
    print(f"全量素材包已生成: {zip_path}")
    print(f"压缩包大小: {os.path.getsize(zip_path) / 1024 / 1024:.2f} MB")
    return zip_path

if __name__ == "__main__":
    print("=== 开始生成HTML展示页面 + 文件打包 ===")
    generate_html()
    pack_files()
    print("=== 全部流程执行完成 ===")
