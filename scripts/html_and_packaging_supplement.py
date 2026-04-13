#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML生成和文件打包补充脚本
最小改动原则：不修改现有工作流，只添加缺失功能
"""

import os
import sys
import json
import zipfile
import shutil
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

class HTMLPackagingSupplement:
    """HTML生成和文件打包补充功能"""
    
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
        
        print(f"HTML和打包补充功能初始化完成")
        print(f"输出目录: {output_dir}")
        print(f"角色: {role_name}")
    
    def generate_html(self) -> Dict[str, Any]:
        """生成HTML展示页面"""
        try:
            print("生成HTML展示页面...")
            
            # HTML文件路径
            html_path = os.path.join(self.output_dir, "html", "index.html")
            
            # 收集所有生成的图片
            images_dir = os.path.join(self.output_dir, "images")
            image_files = []
            if os.path.exists(images_dir):
                for file in os.listdir(images_dir):
                    if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                        image_files.append(file)
            
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
            
            # 生成HTML内容
            html_content = self._generate_html_content(existing_images)
            
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
            
            result = {
                "success": True,
                "html_path": html_path,
                "image_count": len(existing_images),
                "images": existing_images,
                "timestamp": datetime.now().isoformat()
            }
            
            # 保存结果到JSON
            json_path = os.path.join(self.output_dir, "json", "step_html.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            print(f"✅ HTML生成完成: {html_path}")
            print(f"   包含 {len(existing_images)} 张图片")
            return result
            
        except Exception as e:
            print(f"❌ HTML生成失败: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _generate_html_content(self, image_files: List[str]) -> str:
        """生成HTML内容"""
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
        .gallery {{ padding: 30px; }}
        .gallery h2 {{ text-align: center; margin-bottom: 20px; color: #333; }}
        .image-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
        .image-card {{ background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 3px 10px rgba(0,0,0,0.1); }}
        .image-card img {{ width: 100%; height: 200px; object-fit: cover; }}
        .image-info {{ padding: 15px; }}
        .image-info h3 {{ color: #333; margin-bottom: 5px; }}
        .image-info p {{ color: #666; font-size: 0.9rem; }}
        .footer {{ background: #f8f9fa; padding: 20px; text-align: center; border-top: 1px solid #e9ecef; }}
        .download-btn {{ display: inline-block; background: #667eea; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 万相IP技能成果展示</h1>
            <p>角色: {self.role_name} | 类型: {self.input_type} | 时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
        
        <div class="gallery">
            <h2>📋 生成成果 ({len(image_files)}个)</h2>
            <div class="image-grid">
"""
        
        # 添加图片卡片
        for image_file in image_files:
            description = image_descriptions.get(image_file, "角色IP生成成果")
            step_name = image_file.replace('.jpg', '').replace('_', ' ')
            
            html += f"""
                <div class="image-card">
                    <img src="images/{image_file}" alt="{step_name}">
                    <div class="image-info">
                        <h3>{step_name}</h3>
                        <p>{description}</p>
                    </div>
                </div>
"""
        
        html += f"""
            </div>
        </div>
        
        <div class="footer">
            <p>万相IP技能 v1.7.2 | 生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
            <a href="../packages/万相IP技能成果包_{datetime.now().strftime('%Y%m%d')}.zip" class="download-btn" download>
                📦 下载完整文件包
            </a>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def create_package(self) -> Dict[str, Any]:
        """创建文件包"""
        try:
            print("创建文件包...")
            
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

## 使用说明
1. 解压后打开 html/index.html 查看成果
2. 所有图片在 images/ 目录
3. 元数据在 json/ 目录
4. 日志在 logs/ 目录

## 技术信息
- 模型: wan2.7-image / wan2.7-i2v
- 分辨率: 1440*1440 (图片) / 720P (视频)
- API: 阿里云万相API

万相IP技能 © 2026
"""
                zipf.writestr("README.txt", readme_content)
                added_files.append("README.txt")
            
            # 计算文件大小
            file_size = os.path.getsize(zip_path)
            file_size_mb = file_size / (1024 * 1024)
            
            result = {
                "success": True,
                "zip_path": zip_path,
                "zip_filename": zip_filename,
                "file_count": len(added_files),
                "file_size_mb": round(file_size_mb, 2),
                "timestamp": datetime.now().isoformat()
            }
            
            # 保存结果到JSON
            json_path = os.path.join(self.output_dir, "json", "step_package.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 文件包创建完成: {zip_path}")
            print(f"   包含 {len(added_files)} 个文件, {round(file_size_mb, 2)} MB")
            return result
            
        except Exception as e:
            print(f"❌ 文件包创建失败: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def run_supplement(self) -> Dict[str, Any]:
        """运行补充功能（HTML生成 + 文件打包）"""
        print("=" * 50)
        print("运行HTML生成和文件打包补充功能")
        print("=" * 50)
        
        results = {}
        
        # 1. 生成HTML
        html_result = self.generate_html()
        results["html"] = html_result
        
        if not html_result.get("success", False):
            print("⚠️ HTML生成失败，继续尝试打包...")
        
        # 2. 创建文件包
        package_result = self.create_package()
        results["package"] = package_result
        
        # 汇总结果
        summary = {
            "html_success": html_result.get("success", False),
            "package_success": package_result.get("success", False),
            "total_success": html_result.get("success", False) and package_result.get("success", False),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
        # 保存汇总
        summary_path = os.path.join(self.output_dir, "json", "supplement_summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print("=" * 50)
        print("补充功能执行完成")
        print(f"HTML生成: {'✅ 成功' if html_result.get('success') else '❌ 失败'}")
        print(f"文件打包: {'✅ 成功' if package_result.get('success') else '❌ 失败'}")
        print("=" * 50)
        
        return summary

if __name__ == "__main__":
    # 示例用法
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
        role_name = sys.argv[2] if len(sys.argv) > 2 else "测试角色"
        input_type = sys.argv[3] if len(sys.argv) > 3 else "single_character"
    else:
        # 默认值
        output_dir = "real_output"
        role_name = "测试角色"
        input_type = "single_character"
    
    # 运行补充功能
    supplement = HTMLPackagingSupplement(output_dir, role_name, input_type)
    result = supplement.run_supplement()
    
    if result.get("total_success", False):
        print("🎉 所有补充功能执行成功！")
        print(f"HTML页面: {output_dir}/html/index.html")
        print(f"文件包: {output_dir}/packages/")
    else:
        print("⚠️ 部分功能执行失败，请检查日志")