                    }
            else:
                self.log(f"步骤 {step['id']} 失败: API调用失败")
                return {
                    "step_id": step["id"],
                    "name": step["name"],
                    "success": False,
                    "error": "API调用失败",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            self.log(f"步骤 {step['id']} 异常: {str(e)}")
            return {
                "step_id": step["id"],
                "name": step["name"],
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _execute_html_generation(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """执行HTML生成步骤"""
        try:
            self.log(f"生成HTML展示页面...")
            
            # HTML文件路径
            html_path = os.path.join(self.output_dir, "html", step["filename"])
            
            # 收集所有生成的图片
            images_dir = os.path.join(self.output_dir, "images")
            image_files = []
            if os.path.exists(images_dir):
                for file in os.listdir(images_dir):
                    if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                        image_files.append(file)
            
            # 生成HTML内容
            html_content = self._generate_html_content(image_files)
            
            # 保存HTML文件
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # 复制图片到html目录
            html_images_dir = os.path.join(self.output_dir, "html", "images")
            os.makedirs(html_images_dir, exist_ok=True)
            
            for image_file in image_files:
                src = os.path.join(images_dir, image_file)
                dst = os.path.join(html_images_dir, image_file)
                shutil.copy2(src, dst)
            
            step_result = {
                "step_id": step["id"],
                "name": step["name"],
                "success": True,
                "html_path": html_path,
                "image_count": len(image_files),
                "timestamp": datetime.now().isoformat()
            }
            
            # 保存结果到JSON
            json_path = os.path.join(self.output_dir, "json", f"step_{step['id']}.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(step_result, f, ensure_ascii=False, indent=2)
            
            self.log(f"HTML生成完成: {html_path}, 包含 {len(image_files)} 张图片")
            return step_result
            
        except Exception as e:
            self.log(f"HTML生成异常: {str(e)}")
            return {
                "step_id": step["id"],
                "name": step["name"],
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _generate_html_content(self, image_files: List[str]) -> str:
        """生成HTML内容"""
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
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>万相IP技能成果展示 - {self.role_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header .subtitle {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}
        
        .metadata {{
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .metadata-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}
        
        .metadata-item {{
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .metadata-item .label {{
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .gallery {{
            padding: 40px;
        }}
        
        .gallery h2 {{
            text-align: center;
            margin-bottom: 30px;
            color: #333;
            font-size: 2rem;
        }}
        
        .image-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }}
        
        .image-card {{
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .image-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.2);
        }}
        
        .image-card img {{
            width: 100%;
            height: 250px;
            object-fit: cover;
            border-bottom: 1px solid #eee;
        }}
        
        .image-info {{
            padding: 20px;
        }}
        
        .image-info h3 {{
            color: #333;
            margin-bottom: 10px;
            font-size: 1.3rem;
        }}
        
        .image-info p {{
            color: #666;
            font-size: 0.9rem;
            line-height: 1.5;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            border-top: 1px solid #e9ecef;
        }}
        
        .footer p {{
            color: #666;
            margin-bottom: 10px;
        }}
        
        .download-btn {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: bold;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .download-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.6);
        }}
        
        @media (max-width: 768px) {{
            .container {{
                border-radius: 10px;
            }}
            
            .header {{
                padding: 30px 20px;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
            
            .gallery {{
                padding: 20px;
            }}
            
            .image-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 万相IP技能成果展示</h1>
            <p class="subtitle">角色IP系列化全流程生成结果</p>
        </div>
        
        <div class="metadata">
            <div class="metadata-grid">
                <div class="metadata-item">
                    <div class="label">角色名称</div>
                    <div>{self.role_name}</div>
                </div>
                <div class="metadata-item">
                    <div class="label">输入类型</div>
                    <div>{self.input_type}</div>
                </div>
                <div class="metadata-item">
                    <div class="label">生成时间</div>
                    <div>{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</div>
                </div>
                <div class="metadata-item">
                    <div class="label">成果数量</div>
                    <div>{len(existing_images)} 个文件</div>
                </div>
            </div>
        </div>
        
        <div class="gallery">
            <h2>📋 生成成果展示</h2>
            <div class="image-grid">
"""
        
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
        
        # 添加图片卡片
        for image_file in existing_images:
            description = image_descriptions.get(image_file, "角色IP生成成果")
            step_name = image_file.replace('.jpg', '').replace('_', ' ')
            
            html += f"""
                <div class="image-card">
                    <img src="images/{image_file}" alt="{step_name}" loading="lazy">
                    <div class="image-info">
                        <h3>{step_name}</h3>
                        <p>{description}</p>
                    </div>
                </div>
"""
        
        html += """
            </div>
        </div>
        
        <div class="footer">
            <p>万相IP技能 v1.7.2 | 基于阿里云万相API生成</p>
            <p>© 2026 万相IP技能 | 所有图片由AI生成</p>
            <a href="../packages/万相IP技能成果包_""" + datetime.now().strftime('%Y%m%d') + """.zip" class="download-btn" download>
                📦 下载完整文件包
            </a>
        </div>
    </div>
    
    <script>
        // 图片懒加载
        document.addEventListener('DOMContentLoaded', function() {
            const images = document.querySelectorAll('img[loading="lazy"]');
            
            if ('IntersectionObserver' in window) {
                const imageObserver = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const image = entry.target;
                            image.src = image.getAttribute('data-src') || image.src;
                            imageObserver.unobserve(image);
                        }
                    });
                });
                
                images.forEach(image => {
                    if (!image.complete) {
                        const dataSrc = image.src;
                        image.src = '';
                        image.setAttribute('data-src', dataSrc);
                        imageObserver.observe(image);
                    }
                });
            }
        });
    </script>
</body>
</html>"""
        
        return html
    
    def _execute_packaging(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """执行文件打包步骤"""
        try:
            self.log(f"开始文件打包...")
            
            # ZIP文件路径
            zip_path = os.path.join(self.output_dir, "packages", step["filename"])
            
            # 创建ZIP文件
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # 添加图片文件
                images_dir = os.path.join(self.output_dir, "images")
                if os.path.exists(images_dir):
                    for root, dirs, files in os.walk(images_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, self.output_dir)
                            zipf.write(file_path, arcname)
                            self.log(f"添加文件到ZIP: {arcname}")
                
                # 添加JSON文件
                json_dir = os.path.join(self.output_dir, "json")
                if os.path.exists(json_dir):
                    for root, dirs, files in os.walk(json_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, self.output_dir)
                            zipf.write(file_path, arcname)
                            self.log(f"添加文件到ZIP: {arcname}")
                
                # 添加HTML文件
                html_dir = os.path.join(self.output_dir, "html")
                if os.path.exists(html_dir):
                    for root, dirs, files in os.walk(html_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, self.output_dir)
                            zipf.write(file_path, arcname)
                            self.log(f"添加文件到ZIP: {arcname}")
                
                # 添加日志文件
                logs_dir = os.path.join(self.output_dir, "logs")
                if os.path.exists(logs_dir):
                    for root, dirs, files in os.walk(logs_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, self.output_dir)
                            zipf.write(file_path, arcname)
                            self.log(f"添加文件到ZIP: {arcname}")
                
                # 添加视频文件（如果存在）
                video_dir = os.path.join(self.output_dir, "video")
                if os.path.exists(video_dir):
                    for root, dirs, files in os.walk(video_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, self.output_dir)
                            zipf.write(file_path, arcname)
                            self.log(f"添加文件到ZIP: {arcname}")
                
                # 添加README文件
                readme_content = f"""# 万相IP技能成果包

## 基本信息
- 角色名称: {self.role_name}
- 输入类型: {self.input_type}
- 生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
- 技能版本: v1.7.2

## 文件说明
1. images/ - 所有生成的图片文件
2. json/ - 每个步骤的JSON元数据
3. html/ - HTML展示页面
4. video/ - 生成的视频文件（如果存在）
5. logs/ - 工作流执行日志
6. packages/ - 本ZIP文件

## 使用说明
1. 解压此ZIP文件
2. 打开 html/index.html 查看成果展示
3. 查看 json/ 目录了解每个步骤的详细信息
4. 查看 logs/workflow.log 了解执行过程

## 技术信息
- 生成模型: wan2.7-image (图片), wan2.7-i2v (视频)
- 分辨率: 1440*1440 (图片), 720P (视频)
- API: 阿里云万相API

## 注意事项
- 所有图片由AI生成，版权归生成者所有
- 可用于个人学习、商业设计等用途
- 建议保留原始文件以便后续修改

---
万相IP技能 © 2026
"""
                
                zipf.writestr("README.txt", readme_content)
                self.log("添加README.txt到ZIP")
            
            # 计算文件大小
            file_size = os.path.getsize(zip_path)
            file_size_mb = file_size / (1024 * 1024)
            
            step_result = {
                "step_id": step["id"],
                "name": step["name"],
                "success": True,
                "zip_path": zip_path,
                "file_size_bytes": file_size,
                "file_size_mb": round(file_size_mb, 2),
                "timestamp": datetime.now().isoformat()
            }
