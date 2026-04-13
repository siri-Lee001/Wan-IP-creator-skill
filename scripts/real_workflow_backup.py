#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真实工作流脚本 - 使用真正的阿里云百炼API
"""

import json
import os
import sys
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# 使用优化版API
from wanxiang_api_optimized import generate_image_wanxiang, generate_video_wanxiang, wait_for_video_completion

class RealWorkflow:
    """真实工作流管理器"""
    
    def __init__(self, role_image_path: str, role_name: str = "兽人战士", output_dir: str = "real_output"):
        """
        初始化工作流
        
        Args:
            role_image_path: 角色图片路径
            role_name: 角色名称
            output_dir: 输出目录
        """
        self.role_image_path = role_image_path
        self.role_name = role_name
        self.output_dir = output_dir
        
        # 初始化API客户端
        self.api = None
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "json"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "video"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "logs"), exist_ok=True)
        
        # 工作流步骤
        self.workflow_steps = self.load_workflow_steps()
        self.results = {}
        
        # 日志文件
        self.log_file = os.path.join(output_dir, "logs", "workflow.log")
        self.log(f"真实工作流初始化完成 - 角色: {role_name}")
    
    def load_workflow_steps(self) -> List[Dict[str, Any]]:
        """加载工作流步骤配置"""
        base_prompt_suffix = "生成单一角色正面主体图，去掉三视图的多视图布局，只保留单个完整的角色，100%保留角色核心视觉特征"
        
        return [
            {
                "id": 1,
                "name": "风格转换-国潮",
                "description": "国潮风格转换",
                "prompt": f"兽人战士，绿色皮肤，黑色龙鳞铠甲，金色发光眼睛，国潮风格，传统中国风元素，祥云、海浪、水墨效果，红色金色配色，{base_prompt_suffix}，超高清8K，细节丰富",
                "filename": "01_国潮风格.jpg"
            },
            {
                "id": 2,
                "name": "风格转换-赛博",
                "description": "赛博风格转换",
                "prompt": f"兽人战士，绿色皮肤，黑色龙鳞铠甲，金色发光眼睛，赛博朋克风格，未来科技感，霓虹灯光，机械义体，数据流效果，{base_prompt_suffix}，超高清8K，细节丰富",
                "filename": "02_赛博风格.jpg"
            },
            {
                "id": 3,
                "name": "风格转换-Q版",
                "description": "Q版风格转换",
                "prompt": f"兽人战士，绿色皮肤，黑色龙鳞铠甲，金色发光眼睛，Q版风格，二头身可爱萌化，大眼睛，简化细节，卡通渲染，{base_prompt_suffix}，超高清8K，细节丰富",
                "filename": "03_Q版风格.jpg"
            },
            {
                "id": 4,
                "name": "风格转换-极简",
                "description": "极简风格转换",
                "prompt": f"兽人战士，绿色皮肤，黑色龙鳞铠甲，金色发光眼睛，极简风格，扁平化设计，简约线条，几何形状，矢量风格，{base_prompt_suffix}，超高清8K，细节丰富",
                "filename": "04_极简风格.jpg"
            },
            {
                "id": 5,
                "name": "动作延展-九合一",
                "description": "九合一动作大图",
                "prompt": f"兽人战士，绿色皮肤，黑色龙鳞铠甲，金色发光眼睛，生成9种不同动作：打招呼、敬礼、比心、认真工作、可爱pose、挥手、歪头、点赞、害羞，排列成单张3×3九宫格布局的高清大图，{base_prompt_suffix}，超高清8K",
                "filename": "05_动作九合一.jpg"
            },
            {
                "id": 6,
                "name": "文创设计-T恤",
                "description": "T恤设计",
                "prompt": f"兽人战士，绿色皮肤，黑色龙鳞铠甲，金色发光眼睛，T恤设计，潮流服饰，{base_prompt_suffix}，超高清8K",
                "filename": "06_文创_T恤.jpg"
            },
            {
                "id": 7,
                "name": "文创设计-手办",
                "description": "手办设计",
                "prompt": f"兽人战士，绿色皮肤，黑色龙鳞铠甲，金色发光眼睛，手办模型，可动手办，{base_prompt_suffix}，超高清8K",
                "filename": "07_文创_手办.jpg"
            },
            {
                "id": 8,
                "name": "文创设计-海报",
                "description": "海报设计",
                "prompt": f"兽人战士，绿色皮肤，黑色龙鳞铠甲，金色发光眼睛，宣传海报，电影海报风格，{base_prompt_suffix}，超高清8K",
                "filename": "08_文创_海报.jpg"
            },
            {
                "id": 9,
                "name": "文创设计-挂件",
                "description": "挂件设计",
                "prompt": f"兽人战士，绿色皮肤，黑色龙鳞铠甲，金色发光眼睛，钥匙扣挂件，{base_prompt_suffix}，超高清8K",
                "filename": "09_文创_挂件.jpg"
            },
            {
                "id": 10,
                "name": "文创设计-12合一贴纸",
                "description": "12合一贴纸大图",
                "prompt": f"兽人战士，绿色皮肤，黑色龙鳞铠甲，金色发光眼睛，12个不同设计的贴纸，排列到同一张展示图中，{base_prompt_suffix}，超高清8K",
                "filename": "10_文创_12合一贴纸.jpg"
            },
            {
                "id": 11,
                "name": "文创设计-三合一背包",
                "description": "三合一背包大图",
                "prompt": f"兽人战士，绿色皮肤，黑色龙鳞铠甲，金色发光眼睛，背包/挎包/小包三款产品展示在同一张图，{base_prompt_suffix}，超高清8K",
                "filename": "11_文创_三合一背包.jpg"
            },
            {
                "id": 12,
                "name": "文创设计-二合一杯子",
                "description": "二合一杯子大图",
                "prompt": f"兽人战士，绿色皮肤，黑色龙鳞铠甲，金色发光眼睛，杯子/水壶两款产品展示在同一张图，{base_prompt_suffix}，超高清8K",
                "filename": "12_文创_二合一杯子.jpg"
            },
            {
                "id": 13,
                "name": "表情包-九合一",
                "description": "九合一表情包大图",
                "prompt": f"兽人战士，绿色皮肤，黑色龙鳞铠甲，金色发光眼睛，制作9种常用社交表情：收到、OK、加油、谢谢、疑惑、开心、抱歉、点赞、委屈，每个动作配上对应的表情文字，排列成单张3×3九宫格布局的带文字高清表情包大图，{base_prompt_suffix}，超高清8K",
                "filename": "13_表情包九合一.jpg"
            }
        ]
    
    def log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    
    def execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """执行单个步骤"""
        self.log(f"开始执行步骤 {step['id']}: {step['name']}")
        
        try:
            # 生成图片 - 使用优化版万相API
            from wanxiang_api_optimized import generate_image_wanxiang, download_image
            
            # 调用万相API
            image_urls = generate_image_wanxiang(
                prompt=step["prompt"],
                reference_image_path=self.role_image_path,
                size="1920*1080",  # 正确格式：星号*
                n=1
            )
            
            if image_urls:
                image_url = image_urls[0]
                
                # 下载图片
                image_path = os.path.join(self.output_dir, "images", step["filename"])
                success = download_image(image_url, image_path)
                
                if success:
                
                step_result = {
                    "step_id": step["id"],
                    "name": step["name"],
                    "success": True,
                    "image_url": image_url,
                    "local_path": image_path,
                    "prompt": step["prompt"],
                    "timestamp": datetime.now().isoformat()
                }
                
                # 保存结果到JSON
                json_path = os.path.join(self.output_dir, "json", f"step_{step['id']}.json")
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(step_result, f, ensure_ascii=False, indent=2)
                
                self.log(f"步骤 {step['id']} 完成: {step['name']}")
                return step_result
            else:
                raise Exception("API调用失败，未返回图片URL")
                
        except Exception as e:
            self.log(f"步骤 {step['id']} 失败: {str(e)}")
            return {
                "step_id": step["id"],
                "name": step["name"],
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def generate_video(self, image_path: str) -> Dict[str, Any]:
        """生成视频 - 使用阿里云万相wan2.7-i2v模型"""
        self.log("开始生成视频（万相wan2.7-i2v模型）")
        
        try:
            # 1. 上传图片到img402.dev获得公网URL
            from image_uploader import upload_to_img402
            
            self.log(f"上传图片到img402.dev: {image_path}")
            image_url = upload_to_img402(image_path)
            
            if not image_url:
                return {
                    "success": False,
                    "error": "图片上传到图床失败",
                    "timestamp": datetime.now().isoformat()
                }
            
            self.log(f"图片上传成功，公网URL: {image_url}")
            
            # 调用万相视频API
            task_id = generate_video_wanxiang(
                image_url=image_url,
                prompt=f"{self.role_name} 动态展示，帅气动作",
                duration=4,  # 4秒视频
                resolution="720P",
                watermark=False
            )
            
            if not task_id:
                self.log("视频任务创建失败")
                return {"success": False, "error": "任务创建失败"}
            
            self.log(f"视频任务创建成功，task_id: {task_id}")
            
            # 等待视频生成完成
            video_url = wait_for_video_completion(task_id, max_attempts=40, interval=15)
            
            if video_url:
                # 下载视频
                video_path = os.path.join(self.output_dir, "video", f"{self.role_name}_dynamic.mp4")
                import requests
                response = requests.get(video_url, timeout=60)
                if response.status_code == 200:
                    with open(video_path, "wb") as f:
                        f.write(response.content)
                    self.log(f"视频下载成功: {video_path}")
                    
                    video_result = {
                        "success": True,
                        "task_id": task_id,
                        "video_url": video_url,
                        "local_path": video_path,
                        "duration": 4,
                        "resolution": "720P",
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    self.log(f"视频下载失败: {response.status_code}")
                    video_result = {"success": False, "error": "视频下载失败"}
            else:
                self.log("视频生成失败或超时")
                video_result = {"success": False, "error": "视频生成失败或超时"}
            
            # 保存结果
            json_path = os.path.join(self.output_dir, "json", "video_task.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(video_result, f, ensure_ascii=False, indent=2)
            
            self.log("视频任务创建成功")
            return video_result
            
        except Exception as e:
            self.log(f"视频生成失败: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def create_html(self):
        """创建HTML展示页面"""
        self.log("创建HTML展示页面")
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.role_name} IP系列化设计</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        h1 {{ color: #333; text-align: center; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .section {{ margin: 30px 0; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h2 {{ color: #555; border-bottom: 2px solid #ddd; padding-bottom: 10px; }}
        .image-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }}
        .image-card {{ border: 1px solid #ddd; border-radius: 5px; overflow: hidden; }}
        .image-card img {{ width: 100%; height: 300px; object-fit: cover; }}
        .image-title {{ padding: 10px; text-align: center; background: #f9f9f9; }}
        .status {{ background: #e8f4fd; padding: 15px; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{self.role_name} IP系列化设计</h1>
        
        <div class="status">
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>总图片数: {len(self.workflow_steps)}张</p>
            <p>输出目录: {self.output_dir}</p>
        </div>
        
        <div class="section">
            <h2>原始三视图</h2>
            <div class="image-grid">
                <div class="image-card">
                    <img src="{self.role_image_path}" alt="原始三视图">
                    <div class="image-title">原始三视图</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>风格转换 (4张)</h2>
            <div class="image-grid">
                <div class="image-card">
                    <img src="./images/01_国潮风格.jpg" alt="国潮风格">
                    <div class="image-title">国潮风格</div>
                </div>
                <div class="image-card">
                    <img src="./images/02_赛博风格.jpg" alt="赛博风格">
                    <div class="image-title">赛博风格</div>
                </div>
                <div class="image-card">
                    <img src="./images/03_Q版风格.jpg" alt="Q版风格">
                    <div class="image-title">Q版风格</div>
                </div>
                <div class="image-card">
                    <img src="./images/04_极简风格.jpg" alt="极简风格">
                    <div class="image-title">极简风格</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>动作延展 (1张九合一)</h2>
            <div class="image-grid">
                <div class="image-card">
                    <img src="./images/05_动作九合一.jpg" alt="动作九合一">
                    <div class="image-title">九合一动作大图</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>文创设计 (7张)</h2>
            <div class="image-grid">
                <div class="image-card">
                    <img src="./images/06_文创_T恤.jpg" alt="T恤设计">
                    <div class="image-title">T恤设计</div>
                </div>
                <div class="image-card">
                    <img src="./images/07_文创_手办.jpg" alt="手办设计">
                    <div class="image-title">手办设计</div>
                </div>
                <div class="image-card">
                    <img src="./images/08_文创_海报.jpg" alt="海报设计">
                    <div class="image-title">海报设计</div>
                </div>
                <div class="image-card">
                    <img src="./images/09_文创_挂件.jpg" alt="挂件设计">
                    <div class="image-title">挂件设计</div>
                </div>
                <div class="image-card">
                    <img src="./images/10_文创_12合一贴纸.jpg" alt="12合一贴纸">
                    <div class="image-title">12合一贴纸</div>
                </div>
                <div class="image-card">
                    <img src="./images/11_文创_三合一背包.jpg" alt="三合一背包">
                    <div class="image-title">三合一背包</div>
                </div>
                <div class="image-card">
                    <img src="./images/12_文创_二合一杯子.jpg" alt="二合一杯子">
                    <div class="image-title">二合一杯子</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>表情包 (1张九合一)</h2>
            <div class="image-grid">
                <div class="image-card">
                    <img src="./images/13_表情包九合一.jpg" alt="表情包九合一">
                    <div class="image-title">九合一表情包</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>视频生成</h2>
            <div class="status">
                <p>视频任务已创建，请查看 video_task.json 获取任务ID</p>
                <p>视频生成需要时间，请稍后检查任务状态</p>
            </div>
        </div>
        
        <div class="section">
            <h2>下载链接</h2>
            <ul>
                <li><