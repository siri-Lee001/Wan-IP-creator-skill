#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML生成和文件打包补充脚本（修正版）
修复：同时处理图片和视频资源
"""

import os
import sys
import json
import zipfile
import shutil
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

class HTMLPackagingSupplementFixed:
    """HTML生成和文件打包补充功能（修正版）"""
    
    def __init__(self, output_dir: str, role_name: str = "角色", input_type: str = "single_character"):
        """
        初始化补充功能
        
        Args:
            output_dir: 输出目录（与主工作流相同）
            role_name: 角色名称
            input_type: 输入类型
        """
        self.output_dir = output_dir
        self.role_name = role_name
        self.input_type = input_type
        
        # 创建必要的子目录
        os.makedirs(os.path.join(output_dir, "html"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "packages"), exist_ok=True)
        
        print(f"HTML和打包补充功能初始化完成（修正版）")
        print(f"输出目录: {output_dir}")
        print(f"角色: {role_name}")
    
    def generate_html(self) -> Dict[str, Any]:
        """生成HTML展示页面（同时处理图片和视频）"""
        try:
            print("生成HTML展示页面（包含图片和视频）...")
            
            # HTML文件路径
            html_path = os.path.join(self.output_dir, "html", "index.html")
            
            # 收集所有生成的图片
            images_dir = os.path.join(self.output_dir, "images")
            image_files = []
            if os.path.exists(images_dir):
                for file in os.listdir(images_dir):
                    if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                        image_files.append(file)
            
            # 收集生成的视频
            video_dir = os.path.join(self.output_dir, "video")
            video_files = []
            if os.path.exists(video_dir):
                for file in os.listdir(video_dir):
                    if file.lower().endswith(('.mp4', '.mov', '.avi', '.webm')):
                        video_files.append(file)
            
            # 按步骤顺序排序图片
            step_order = [
                "00_三视图建模参考图.jpg",
                "01_国潮风格.jpg",
                "02_Q版风格.jpg",
                "03_水彩简化风格.jpg",
                "04_动作九合一.jpg",
                "05_文创九合一.jpg",
                "06_表情包十二合一.jpg"
            ]
            
            # 过滤存在的图片
            existing_images = [img for img in step_order if img in image_files]
            
            # 生成HTML内容（包含图片和视频）
            html_content = self._generate_html_content(existing_images, video_files)
            
            # 保存HTML文件
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # 复制图片到html目录
            html_images_dir = os.path.join(self.output_dir, "html", "images")
            os.makedirs(html_images_dir, exist_ok=True)
            
            for image_file in existing_images:
                src = os.path.join(images_dir, image_file)
                dst = os.path.join(html_images_dir, image_file)
                if os.path.exists(src):
                    shutil.copy2(src, dst)
                    print(f"复制图片: {image_file}")
            
            # 复制视频到html目录
            html_video_dir = os.path.join(self.output_dir, "html", "video")
            os.makedirs(html_video_dir, exist_ok=True)
            
            for video_file in video_files:
                src = os.path.join(video_dir, video_file)
                dst = os.path.join(html_video_dir, video_file)
                if os.path.exists(src):
                    shutil.copy2(src, dst)
                    print(f"复制视频: {video_file}")
            
            result = {
                "success": True,
                "html_path": html_path,
                "image_count": len(existing_images),
                "video_count": len(video_files),
                "images": existing_images,
                "videos": video_files,
                "timestamp": datetime.now().isoformat()
            }
            
            # 保存结果到JSON
            json_path = os.path.join(self.output_dir, "json", "step_html.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            print(f"✅ HTML生成完成: {html_path}")
            print(f"   包含 {len(existing_images)} 张图片, {len(video_files)} 个视频")
            return result
            
        except Exception as e:
            print(f"❌ HTML生成失败: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _generate_html_content(self, image_files: List[str], video_files: List[str]) -> str:
        """生成HTML内容（包含图片和视频）"""
        # 图片描述映射
        image_descriptions = {
            "00_三视图建模参考图.jpg": "专业三视图建模参考图，包含正面、侧面、背面三个正交视角，用于3D建模参考",
            "01_国潮风格.jpg": "国潮艺术风格转换，传统中国风元素，水墨渲染效果",
            "02_Q版风格.jpg": "Q版可爱风格转换，二头身比例，卡通渲染效果",
            "03_水彩简化风格.jpg": "水彩画艺术风格，简化线条，水彩渲染效果",
            "04_动作九合一.jpg": "9种不同动作延展，3×3九宫格布局",
            "05_文创九合一.jpg": "9种文创产品设计，3×3九宫格布局",
            "06_表情包十二合一.jpg": "12种常用社交表情，带中文文字"
        }
        
        # 视频描述
        video_description = "角色动态展示视频，5秒时长，720P分辨率"
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>万相IP技能成果展示 - {self.role_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Microsoft YaHei', sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ font-size: 2rem; margin-bottom: 10px; }}
        .stats {{ background: #f8f9fa; padding: 15px; text-align: center; border-bottom: 1px solid #e9ecef; }}
        .stats span {{ margin: 0 15px; }}
        .section {{ padding: 30px; }}
        .section h2 {{ text-align: center; margin-bottom: 20px; color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
        .image-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .media-card {{ background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 3px 10px rgba(0,0,0,0.1); transition: transform 0.3s; }}
        .media-card:hover {{ transform: translateY(-5px); }}
        .media-card img {{ width: 100%; height: 200px; object-fit: cover; }}
        .media-card video {{ width: 100%; height: 200px; object-fit: cover; background: #000; }}
        .media-info {{ padding: 15px; }}
        .media-info h3 {{ color: #333; margin-bottom: 5px; }}
        .media-info p {{ color: #666; font-size: 0.9rem; margin-bottom: 10px; }}
        .media-tag {{ display: inline-block; background: #667eea; color: white; padding: 3px 8px; border-radius: 3px; font-size: 0.8rem; }}
        .video-section {{ background: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 20px; }}
        .video-container {{ max-width: 800px; margin: 0 auto; }}
        .video-player {{ width: 100%; border-radius: 10px; }}
        .footer {{ background: #f8f9fa; padding: 20px; text-align: center; border-top: 1px solid #e9ecef; }}
        .download-btn {{ display: inline-block; background: #667eea; color: white; padding: 12px 24px; border-radius: 5px; text-decoration: none; margin-top: 10px; font-weight: bold; }}
        .download-btn:hover {{ background: #5a67d8; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 万相IP技能成果展示</h1>
            <p>角色: {self.role_name} | 类型: {self.input_type} | 时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
        
        <div class="stats">
            <span>📷 图片: {len(image_files)}张</span>
            <span>🎬 视频: {len(video_files)}个</span>
            <span>📦 文件: {len(image_files) + len(video_files)}个</span>
        </div>
        
        <div class="section">
            <h2>📋 图片成果展示</h2>
            <div class="image-grid">
"""
        
        # 添加图片卡片
        for image_file in image_files:
            description = image_descriptions.get(image_file, "角色IP生成成果")
            step_name = image_file.replace('.jpg', '').replace('_', ' ')
            
            html += f"""
                <div class="media-card">
                    <img src="images/{image_file}" alt="{step_name}" loading="lazy">
                    <div class="media-info">
                        <h3>{step_name}</h3>
                        <p>{description}</p>
                        <span class="media-tag">图片</span>
                    </div>
                </div>
"""
        
        html += """
            </div>
        </div>
"""
        
        # 添加视频部分
        if video_files:
            html += f"""
        <div class="section">
            <h2>🎬 视频成果展示</h2>
            <div class="video-section">
                <div class="video-container">
"""
            
            for video_file in video_files:
                video_name = video_file.replace('.mp4', '').replace('_', ' ')
                html += f"""
                    <h3 style="text-align: center; margin-bottom: 15px;">{video_name}</h3>
                    <video class="video-player" controls>
                        <source src="video/{video_file}" type="video/mp4">
                        您的浏览器不支持视频播放
                    </video>
                    <div style="text-align: center; margin-top: 10px;">
                        <a href="video/{video_file}" download class="download-btn" style="font-size: 0.9rem; padding: 8px 16px;">
                            📥 下载视频
                        </a>
                    </div>
"""
            
            html += """
                </div>
            </div>
        </div>
"""
        
        html += f"""
        <div class="footer">
            <p>万相IP技能 v1.7.2 | 生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
            <p>模型: wan2.7-image (图片) / wan2.7-i2v (视频) | 分辨率: 1440*1440 / 720P</p>
            <a href="../packages/万相IP技能成果包_{datetime.now().strftime('%Y%m%d_%H%M')}.zip" class="download-btn" download>
                📦 下载完整文件包 ({len(image_files) + len(video_files)}个文件)
            </a>
        </div>
    </div>
    
    <script>
        // 图片懒加载
        document.addEventListener('DOMContentLoaded', function() {{
            const images = document.querySelectorAll('img[loading="lazy"]');
            
            if ('IntersectionObserver' in window) {{
                const imageObserver = new IntersectionObserver((entries) => {{
                    entries.forEach(entry => {{
                        if (entry.isIntersecting) {{
                            const image = entry.target;
                            const dataSrc = image.getAttribute('data-src');
                            if (dataSrc) {{
                                image.src = dataSrc;
                                image.removeAttribute('data-src');
                            }}
                            imageObserver.unobserve(image);
                        }}
                    }});
                }});
                
                images.forEach(image => {{
                    if (!image.complete) {{
                        const dataSrc = image.src;
                        image.src = '';
                        image.setAttribute('data-src', dataSrc);
                        imageObserver.observe(image);
                    }}
                }});
            }}
        }});
    </script>
</body>
</html>"""
        
        return html
    
    def create_package(self) -> Dict[str, Any]:
        """创建文件包（包含图片和视频）"""
        try:
            print("创建文件包（包含图片和视频）...")
            
            # ZIP文件路径
            zip_filename = f"万相IP技能成果包_{datetime.now().strftime('%Y%m%d_%H%M')}.zip"
            zip_path = os.path.join(self.output_dir, "packages", zip_filename)
            
            # 创建ZIP文件
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                added_files = []
                
                # 添加所有目录
                directories = ["images", "json", "html", "video", "logs"]
                for dir_name in directories:
                    dir_path = os.path.join(self.output_dir, dir_name)
                    if os.path.exists(dir_path):
                        for root, dirs, files in os.walk(dir_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, self.output_dir)
                                zipf.write(file_path, arcname)
                                added_files.append(arcname)
                                print(f"  添加: {arcname}")
                
                # 添加README
                readme_content = f"""# 万相IP技能成果包

## 基本信息
- 角色: {self.role_name}
- 类型: {self.input_type}
- 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 文件数: {len(added_files)}个

## 内容说明
### 图片文件 (images/)
1. 00_三视图建模参考图.jpg - 专业三视图建模参考图
2. 01_国潮风格.jpg - 国潮艺术风格转换
3. 02_Q版风格.jpg - Q版可爱风格转换
4. 03_水彩简化风格.jpg - 水彩画艺术风格
5. 04_动作九合一.jpg - 9种不同动作延展
6. 05_文创九合一.jpg - 9种文创产品设计
7. 06_表情包十二合一.jpg - 12种常用社交表情

### 视频文件 (video/)
1. dynamic_video.mp4 - 角色动态展示视频 (5秒, 720P)

### 其他文件
- html/index.html - 成果展示页面
- json/ - 每个步骤的JSON元数据
- logs/ - 工作流执行日志

## 使用说明
1. 解压此ZIP文件
2. 打开 html/index.html 查看完整成果展示
3. 所有图片在 images/ 目录
4. 视频在 video/ 目录
5. 查看 json/ 目录了解详细元数据

## 技术信息
- 图片模型: wan2.7-image
- 视频模型: wan2.7-i2v
- 图片分辨率: 1440*1440
- 视频参数: 5秒, 720P
- API: 阿里云万相API

## 注意事项
- 所有内容由AI生成，版权归生成者所有
- 可用于个人学习、商业设计等用途
- 建议保留原始文件以便后续修改

---
万相IP技能 v1.7.2 © 2026
生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
"""
                zipf.writestr("README.txt", readme_content)
                added_files.append("README.txt")
            
            # 计算文件大小
            file_size = os.path.getsize(zip_path)
            file_size_mb = file_size / (1024 * 1024)
            
            result = {
                "success": True,
                "zip_path": zip