#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真实工作流脚本 - 使用真正的阿里云百炼API
更新版：使用开源包中的正确提示词
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
    
    def __init__(self, role_image_path: str, role_name: str = "角色", output_dir: str = "real_output"):
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
        """加载工作流步骤配置 - 使用开源包中的正确提示词"""
        base_prompt_suffix = "生成单一角色正面主体图，去掉三视图的多视图布局，只保留单个完整的角色，100%保留角色核心视觉特征"
        
        return [
            {
                "id": 1,
                "name": "风格转换-国潮",
                "description": "国潮风格转换",
                "prompt": "转换为国潮艺术风格，传统中国风，水墨渲染效果，传统色彩搭配，保留角色核心特征",
                "filename": "01_国潮风格.jpg"
            },
            {
                "id": 2,
                "name": "风格转换-Q版",
                "description": "Q版风格转换",
                "prompt": "转换为Q版可爱风格，二头身比例，卡通渲染效果，萌系表情，保留角色核心特征",
                "filename": "02_Q版风格.jpg"
            },
            {
                "id": 3,
                "name": "风格转换-水彩简化",
                "description": "水彩简化风格转换",
                "prompt": "转换为水彩画艺术风格，简化线条，水彩渲染效果，柔和色彩，保留角色核心特征",
                "filename": "03_水彩简化风格.jpg"
            },
            {
                "id": 4,
                "name": "动作延展-九合一",
                "description": "九合一动作大图",
                "prompt": """生成角色9种不同动作，排列成3×3九宫格布局：
1. 打招呼 2. 敬礼 3. 比心 4. 认真工作 5. 可爱pose
6. 挥手 7. 歪头 8. 点赞 9. 害羞

要求：单张大图，九宫格布局，每个动作清晰可辨，保留角色核心特征。""",
                "filename": "04_动作九合一.jpg"
            },
            {
                "id": 5,
                "name": "文创设计-九合一",
                "description": "九合一文创产品大图",
                "prompt": """设计商业化文创产品，生成单张3×3九宫格布局的文创产品集合大图：
1. 杯子+水壶组合展示 2. 抱枕设计 3. 背包+挎包组合展示
4. 手机壳设计 5. 小挂件设计 6. 手办设计
7. 眼罩设计 8. T恤设计 9. 4张多动作贴纸集合

要求：单张大图，九宫格布局，产品设计美观实用，保留角色核心特征。""",
                "filename": "05_文创九合一.jpg"
            },
            {
                "id": 6,
                "name": "表情包-十二合一",
                "description": "十二合一表情包大图",
                "prompt": """制作12种常用社交表情，每个表情都要带中文文字，排列成单张大图整齐排列：
1. 比心❤️ 2. 对不起😔 3. 大笑😂 4. 伤心😢 5. 生气😠 6. 累了😫
7. 疑问❓ 8. 拜托🙏 9. 吃瓜🍉 10. 震惊😲 11. 使坏😈 12. 晚安🌙

要求：单张大图，整齐排列，每个表情清晰可辨，带中文文字，保留角色核心特征。""",
                "filename": "06_表情包十二合一.jpg"
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
                size="1440*1440",  # 2K分辨率
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
                    self.log(f"步骤 {step['id']} 失败: 图片下载失败")
                    return {
                        "step_id": step["id"],
                        "name": step["name"],
                        "success": False,
                        "error": "图片下载失败",
                        "timestamp": datetime.now().isoformat()
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
    
    def execute_video_step(self) -> Optional[Dict[str, Any]]:
        """执行视频生成步骤"""
        self.log("开始执行视频生成步骤")
        
        try:
            # 使用角色正面图作为视频输入
            from wanxiang_api_optimized import generate_video_wanxiang, wait_for_video_completion
            
            # 视频提示词
            video_prompt = "角色动态展示，帅气动作，自然流畅"
            
            # 生成视频
            task_id = generate_video_wanxiang(
                prompt=video_prompt,
                image_url=self.role_image_path,  # 注意：这里需要是URL，不是本地路径
                duration=5,
                resolution="720P"
            )
            
            if task_id:
                self.log(f"视频任务创建成功，任务ID: {task_id}")
                
                # 等待视频完成
                self.log("等待视频生成完成...")
                video_result = wait_for_video_completion(task_id, timeout=300)
                
                if video_result and video_result.get("video_url"):
                    video_url = video_result["video_url"]
                    
                    # 下载视频
                    video_path = os.path.join(self.output_dir, "video", "dynamic_video.mp4")
                    from wanxiang_api_optimized import download_video
                    success = download_video(video_url, video_path)
                    
                    if success:
                        video_step_result = {
                            "step_id": "video",
                            "name": "动态视频生成",
                            "success": True,
                            "video_url": video_url,
                            "local_path": video_path,
                            "prompt": video_prompt,
                            "task_id": task_id,
                            "timestamp": datetime.now().isoformat()
                        }
                        
                        # 保存结果到JSON
                        json_path = os.path.join(self.output_dir, "json", "step_video.json")
                        with open(json_path, "w", encoding="utf-8") as f:
                            json.dump(video_step_result, f, ensure_ascii=False, indent=2)
                        
                        self.log("视频生成步骤完成")
                        return video_step_result
                    else:
                        self.log("视频生成步骤失败: 视频下载失败")
                        return {
                            "step_id": "video",
                            "name": "动态视频生成",
                            "success": False,
                            "error": "视频下载失败",
                            "task_id": task_id,
                            "timestamp": datetime.now().isoformat()
                        }
                else:
                    self.log("视频生成步骤失败: 视频生成失败")
                    return {
                        "step_id": "video",
                        "name": "动态视频生成",
                        "success": False,
                        "error": "视频生成失败",
                        "task_id": task_id,
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                self.log("视频生成步骤失败: 任务创建失败")
                return {
                    "step_id": "video",
                    "name": "动态视频生成",
                    "success": False,
                    "error": "任务创建失败",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            self.log(f"视频生成步骤异常: {str(e)}")
            return {
                "step_id": "video",
                "name": "动态视频生成",
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def run_full_workflow(self, skip_video: bool = False):
        """运行完整工作流"""
        self.log("开始运行完整工作流")
        
        all_results = []
        
        # 执行所有图片生成步骤
        for step in self.workflow_steps:
            result = self.execute_step(step)
            all_results.append(result)
            
            # 如果步骤失败，可以决定是否继续
            if not result.get("success", False):
                self.log(f"步骤 {step['id']} 失败，继续执行后续步骤")
        
        # 执行视频生成步骤（如果不跳过）
        if not skip_video:
            video_result = self.execute_video_step()
            if video_result:
                all_results.append(video_result)
        
        # 生成汇总报告
        summary = {
            "total_steps": len(all_results),
            "successful_steps": sum(1 for r in all_results if r.get("success", False)),
            "failed_steps": sum(1 for r in all_results if not r.get("success", True)),
            "results": all_results,
            "timestamp": datetime.now().isoformat()
        }
        
        # 保存汇总报告
        summary_path = os.path.join(self.output_dir, "workflow_summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        self.log(f"工作流执行完成，成功 {summary['successful_steps']}/{summary['total_steps']} 个步骤")
        return summary

if __name__ == "__main__":
    # 示例用法
    workflow = RealWorkflow(
        role_image_path="path/to/your/role/image.jpg",
        role_name="测试角色",
        output_dir="test_output"
    )
    
    # 运行完整工作流（跳过视频）
    result = workflow.run_full_workflow(skip_video=True)
    print(f"工作流执行结果: {result['successful_steps']}/{result['total_steps']} 成功")