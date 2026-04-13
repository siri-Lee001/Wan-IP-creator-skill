#!/usr/bin/env python3
# 万相IP技能工作流执行器
# 基于Wan-skills集成的全流程执行器

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from wan_skills_integrated import WanSkillsIntegrated
from wan_skills_video import WanSkillsVideo

class WanIPWorkflowExecutor:
    """万相IP技能工作流执行器"""
    
    def __init__(self, api_key: Optional[str] = None, region: str = "beijing"):
        """
        初始化工作流执行器
        
        Args:
            api_key: API密钥
            region: 地域
        """
        self.api_key = api_key
        self.region = region
        
        # 初始化适配器
        self.image_adapter = WanSkillsIntegrated(api_key=api_key, region=region)
        self.video_adapter = WanSkillsVideo(api_key=api_key, region=region)
        
        # 输出目录
        self.output_dir = r"C:\Users\User\.openclaw\workspace\output"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 工作流状态
        self.workflow_state = {
            "current_step": 0,
            "total_steps": 0,
            "completed_steps": [],
            "failed_steps": [],
            "output_files": []
        }
        
        print(f"万相IP工作流执行器初始化完成")
        print(f"输出目录: {self.output_dir}")
    
    def set_input_image(self, image_path: str) -> bool:
        """
        设置输入图片
        
        Args:
            image_path: 图片路径
            
        Returns:
            是否成功
        """
        if not os.path.exists(image_path):
            print(f"错误: 输入图片不存在: {image_path}")
            return False
        
        self.input_image = image_path
        print(f"输入图片设置: {image_path}")
        
        # 压缩图片为Base64
        print("压缩输入图片...")
        self.input_data_url = self.image_adapter.compress_image_to_base64(image_path)
        
        if not self.input_data_url:
            print("图片压缩失败")
            return False
        
        print(f"Base64 data URL长度: {len(self.input_data_url)}字符")
        return True
    
    def execute_workflow(self, workflow_type: str = "single_character", 
                        step_by_step: bool = True, confirm_each: bool = True) -> Dict[str, Any]:
        """
        执行工作流
        
        Args:
            workflow_type: 工作流类型
                - "three_views": 三视图输入
                - "single_character": 单角色图输入  
                - "text_description": 文字描述输入
            step_by_step: 是否分步执行
            confirm_each: 是否每步确认
            
        Returns:
            执行结果
        """
        print(f"开始执行工作流: {workflow_type}")
        print(f"分步模式: {step_by_step}")
        print(f"每步确认: {confirm_each}")
        
        # 根据工作流类型设置步骤
        if workflow_type == "three_views":
            steps = self._get_three_views_steps()
        elif workflow_type == "single_character":
            steps = self._get_single_character_steps()
        elif workflow_type == "text_description":
            steps = self._get_text_description_steps()
        else:
            print(f"错误: 未知的工作流类型: {workflow_type}")
            return {"success": False, "error": f"未知的工作流类型: {workflow_type}"}
        
        self.workflow_state["total_steps"] = len(steps)
        
        results = []
        
        for i, step in enumerate(steps, 1):
            self.workflow_state["current_step"] = i
            
            print(f"\n{'='*60}")
            print(f"步骤 {i}/{len(steps)}: {step['name']}")
            print(f"{'='*60}")
            
            # 执行步骤
            step_result = self._execute_step(step)
            
            if step_result["success"]:
                self.workflow_state["completed_steps"].append(step["name"])
                results.append(step_result)
                
                print(f"✅ 步骤完成: {step['name']}")
                
                # 分步确认模式
                if step_by_step and confirm_each and i < len(steps):
                    print(f"\n等待确认后继续执行下一步...")
                    # 在实际使用中，这里应该等待用户确认
                    # 为了测试，我们自动继续
                    time.sleep(2)
            else:
                self.workflow_state["failed_steps"].append(step["name"])
                print(f"❌ 步骤失败: {step['name']}")
                print(f"错误: {step_result.get('error', '未知错误')}")
                
                # 如果步骤失败，根据配置决定是否继续
                if not step.get("continue_on_failure", False):
                    print("工作流因步骤失败而终止")
                    break
        
        # 汇总结果
        total_success = len(self.workflow_state["completed_steps"])
        total_failed = len(self.workflow_state["failed_steps"])
        
        print(f"\n{'='*60}")
        print(f"工作流执行完成")
        print(f"成功步骤: {total_success}/{len(steps)}")
        print(f"失败步骤: {total_failed}/{len(steps)}")
        print(f"输出文件: {len(self.workflow_state['output_files'])}个")
        print(f"{'='*60}")
        
        return {
            "success": total_failed == 0,
            "completed_steps": self.workflow_state["completed_steps"],
            "failed_steps": self.workflow_state["failed_steps"],
            "output_files": self.workflow_state["output_files"],
            "results": results
        }
    
    def _get_three_views_steps(self) -> List[Dict]:
        """获取三视图输入的工作流步骤"""
        return [
            {
                "name": "国潮风格转换",
                "type": "image_generation",
                "prompt": "将角色转换为国潮风格，红色为主色调，加入传统纹样和现代设计元素，保持角色特征不变",
                "output_name": "style_guochao.jpg"
            },
            {
                "name": "Q版风格转换", 
                "type": "image_generation",
                "prompt": "将角色转换为Q版可爱风格，大眼睛，简化线条，卡通化，保持角色特征",
                "output_name": "style_q_version.jpg"
            },
            {
                "name": "水彩简化风格转换",
                "type": "image_generation",
                "prompt": "将角色转换为水彩简化风格，柔和色彩，笔触感，艺术化，保持角色特征",
                "output_name": "style_watercolor.jpg"
            },
            {
                "name": "动作延伸（九合一）",
                "type": "image_generation",
                "prompt": "生成角色9种不同动作：打招呼、敬礼、比心、认真工作、可爱pose、握手、摇头、点赞、害羞，排列成3×3九宫格布局的单张大图",
                "output_name": "actions_9in1.jpg"
            },
            {
                "name": "文创设计（九合一）",
                "type": "image_generation",
                "prompt": "设计商业化文创产品：杯子+水瓶组合、抱枕、背包+挎包组合、手机壳、小挂件、手办、眼罩、T恤、4张多动作贴纸集合，排列成3×3九宫格布局的单张大图",
                "output_name": "products_9in1.jpg"
            },
            {
                "name": "表情包制作（九合一）",
                "type": "image_generation",
                "prompt": "制作12种常用社交表情：比心、对不起、大笑、伤心、生气、累了、疑问、炫耀、吃瓜、震惊、使坏、晚安，每个表情带中文标签，排列成单张大图整齐排列",
                "output_name": "emojis_9in1.jpg"
            },
            {
                "name": "动态视频生成",
                "type": "video_generation",
                "prompt": "角色动起来，自然的动作，适合IP角色的动态表现",
                "output_name": "dynamic_video.mp4",
                "duration": 5,
                "resolution": "720P"
            }
        ]
    
    def _get_single_character_steps(self) -> List[Dict]:
        """获取单角色图输入的工作流步骤"""
        steps = self._get_three_views_steps()
        
        # 在第一位置插入三视图生成步骤
        three_view_step = {
            "name": "三视图生成",
            "type": "image_generation",
            "prompt": "生成角色三视图：正面、侧面、背面，保持角色所有视觉属性、质感、光影、特征不变",
            "output_name": "character_three_views.jpg"
        }
        
        steps.insert(0, three_view_step)
        return steps
    
    def _get_text_description_steps(self) -> List[Dict]:
        """获取文字描述输入的工作流步骤"""
        # 这里需要用户提供文字描述，暂时返回空列表
        # 在实际使用中，应该先让用户提供文字描述
        return []
    
    def _execute_step(self, step: Dict) -> Dict[str, Any]:
        """
        执行单个步骤
        
        Args:
            step: 步骤配置
            
        Returns:
            执行结果
        """
        try:
            step_type = step["type"]
            
            if step_type == "image_generation":
                return self._execute_image_generation(step)
            elif step_type == "video_generation":
                return self._execute_video_generation(step)
            else:
                return {"success": False, "error": f"未知的步骤类型: {step_type}"}
                
        except Exception as e:
            return {"success": False, "error": f"步骤执行异常: {e}"}
    
    def _execute_image_generation(self, step: Dict) -> Dict[str, Any]:
        """执行图片生成步骤"""
        prompt = step["prompt"]
        output_name = step["output_name"]
        
        print(f"生成图片: {step['name']}")
        print(f"提示词: {prompt}")
        
        # 生成图片
        image_urls = self.image_adapter.generate_image(
            prompt=prompt,
            image_url=self.input_data_url,
            size="2K",
            num_images=1
        )
        
        if not image_urls or len(image_urls) == 0:
            return {"success": False, "error": "图片生成失败"}
        
        # 下载图片
        output_path = os.path.join(self.output_dir, output_name)
        if self.image_adapter.download_image(image_urls[0], output_path):
            self.workflow_state["output_files"].append(output_path)
            
            # 获取图片信息
            try:
                from PIL import Image
                img_info = Image.open(output_path)
                file_size = os.path.getsize(output_path)
                
                return {
                    "success": True,
                    "output_path": output_path,
                    "image_url": image_urls[0],
                    "file_size": file_size,
                    "image_size": img_info.size,
                    "step_name": step["name"]
                }
            except:
                return {
                    "success": True,
                    "output_path": output_path,
                    "image_url": image_urls[0],
                    "step_name": step["name"]
                }
        else:
            return {"success": False, "error": "图片下载失败"}
    
    def _execute_video_generation(self, step: Dict) -> Dict[str, Any]:
        """执行视频生成步骤"""
        prompt = step["prompt"]
        output_name = step["output_name"]
        duration = step.get("duration", 5)
        resolution = step.get("resolution", "720P")
        
        print(f"生成视频: {step['name']}")
        print(f"提示词: {prompt}")
        print(f"时长: {duration}秒")
        print(f"分辨率: {resolution}")
        
        # 生成视频
        video_url = self.video_adapter.generate_video(
            image_url=self.input_data_url,
            prompt=prompt,
            duration=duration,
            resolution=resolution
        )
        
        if not video_url:
            return {"success": False, "error": "视频生成失败"}
        
        # 下载视频
        output_path = os.path.join(self.output_dir, output_name)
        if self.video_adapter.download_video(video_url, output_path):
            self.workflow_state["output_files"].append(output_path)
            file_size = os.path.getsize(output_path)
            
            return {
                "success": True,
                "output_path": output_path,
                "video_url": video_url,
                "file_size": file_size,
                "step_name": step["name"]
            }
        else:
            return {"success": False, "error": "视频下载失败"}


# 测试函数
def test_workflow():
    """测试工作流执行器"""
    print("测试万相IP工作流执行器...")
    
    # 初始化执行器
    executor = WanIPWorkflowExecutor()
    
    # 设置输入图片
    test_image = r"C:\Users\User\.openclaw\media\inbound\b7e7a959-27c0-47da-95be-2cd3e3152639.jpg"
    
    if not os.path.exists(test_image):
        print(f"测试图片不存在: {test_image}")
        return False
    
    if not executor.set_input_image(test_image):
        print("输入图片设置失败")
        return False
    
    # 执行工作流（三视图输入场景）
    print("\n执行三视图输入工作流...")
    result = executor.execute_workflow(
        workflow_type="three_views",
        step_by_step=True,
        confirm_each=True
    )
    
    if result["success"]:
        print("\n✅ 工作流执行成功！")
        print(f"输出文件:")
        for file_path in result["output_files"]:
            print(f"  - {file_path}")
        return True
    else:
        print("\n❌ 工作流执行失败")
        print(f"失败步骤: {result.get('failed_steps', [])}")
        return False

if __name__ == "__main__":
    print("开始测试万相IP工作流...")
    success = test_workflow()
    
    if success:
        print("\n万相IP工作流测试成功！")
    else:
        print("\n万相IP工作流测试失败")