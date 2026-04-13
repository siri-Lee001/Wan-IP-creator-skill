#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真实工作流脚本 - 使用真正的阿里云百炼API
最终版：包含正确的三视图提示词和其他节点提示词
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
    
    def __init__(self, role_image_path: str, role_name: str = "角色", output_dir: str = "real_output", 
                 input_type: str = "single_character"):
        """
        初始化工作流
        
        Args:
            role_image_path: 角色图片路径
            role_name: 角色名称
            output_dir: 输出目录
            input_type: 输入类型 (single_character: 单角色图, three_views: 三视图)
        """
        self.role_image_path = role_image_path
        self.role_name = role_name
        self.output_dir = output_dir
        self.input_type = input_type
        
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
        self.log(f"真实工作流初始化完成 - 角色: {role_name}, 输入类型: {input_type}")
    
    def load_workflow_steps(self) -> List[Dict[str, Any]]:
        """加载工作流步骤配置 - 根据输入类型返回不同的步骤"""
        
        if self.input_type == "single_character":
            # 单角色图输入：先生成三视图，再进行其他步骤
            return self._get_single_character_steps()
        elif self.input_type == "three_views":
            # 三视图输入：跳过三视图生成，直接进行其他步骤
            return self._get_three_views_steps()
        else:
            self.log(f"未知的输入类型: {self.input_type}")
            return []
    
    def _get_single_character_steps(self) -> List[Dict[str, Any]]:
        """获取单角色图输入的工作流步骤"""
        base_prompt_suffix = "生成单一角色正面主体图，去掉三视图的多视图布局，只保留单个完整的角色，100%保留角色核心视觉特征"
        
        steps = [
            # 步骤0：三视图生成（单角色图输入时添加）
            {
                "id": 0,
                "name": "三视图生成",
                "description": "生成专业三视图建模参考图",
                "prompt": """-modeling-sheet

# 角色：3D建模技术支持
你是一位为建模部门提供精确视觉规范的专家。你的唯一任务是将用户上传的**单张角色图片**，转化成一幅可直接导入3D软件作为参照的**纯技术蓝图**。

# 核心原则：零创作，纯转换
1.  **数据锁定**：原图中角色的**所有视觉属性**已被锁定，包括：**服饰（款式、褶皱、纹理）、身材、五官、发型、配色**。严禁任何修改、增删或重新设计。
2.  **背景规范**：使用**纯白色（#FFFFFF）背景**，并叠加一层**浅灰色（#F0F0F0）的等距网格线**。**禁止出现任何其他环境、颜色或装饰性元素**。
3.  **姿态与补全**：
    *   主体保持**原始静态姿态**。
    *   **仅在绝对必要时**（如原图明显缺脚），才依据已有结构进行**最保守、无缝的几何延伸**，以形成可用于建模的完整闭合形体。

# 输出规范：单页建模参考图
生成**单张**横版画面，风格与原图一致，渲染精度为**8K，专业级**。

**【画面布局与内容】**

*   **A. 主体区：标准三视图（占据画面至少75%的宽度）**
    *   **内容**：严格生成且仅生成以下三个**正交视角**，在**同一水平基线上**从左至右**一字水平排列**：
        1.  **正面图 (FRONT VIEW)**
        2.  **侧面图 (SIDE VIEW)**：通常为角色左侧视图。
        3.  **背面图 (BACK VIEW)**
    *   **关键要求**：
        *   **比例绝对对齐**：三个视图并排水平对齐，三个视图的**头顶、眼线、肩线、肘点、腰线、膝点、脚底**必须严格对齐。
        *   **细节绝对一致**：三个视图中的角色，必须是**同一个3D模型在三个正交视窗中的渲染结果**。所有细节（如口袋位置、图案、配饰形状）必须完全相同。
        *   **背景**：统一使用上述定义的**白底+浅灰网格线**。""",
                "filename": "00_三视图建模参考图.jpg"
            },
            # 其他步骤（从步骤1开始）
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
        
        return steps
    
    def _get_three_views_steps(self) -> List[Dict[str, Any]]:
        """获取三视图输入的工作流步骤"""
        base_prompt_suffix = "生成单一角色正面主体图，去掉三视图的多视图布局，只保留单个完整的角色，100%保留角色核心视觉特征"
        
        steps = [
            # 三视图输入时，跳过三视图生成，直接从风格转换开始
            {
                "id": 1,
                "name": "风格转换-国潮",
                "description": "国潮风格转换",
                "prompt": f"转换为国潮艺术风格，传统中国风，水墨渲染效果，传统色彩搭配，{base_prompt_suffix}",
                "filename": "01_国潮风格.jpg"
            },
            {
                "id": 2,
                "name": "风格转换-Q版",
                "description": "Q版风格转换",
                "prompt": f"转换为Q版可爱风格，二头身比例，卡通渲染效果，萌系表情，{base_prompt_suffix}",
                "filename": "02_Q版风格.jpg"
            },
            {
                "id": 3,
                "name": "风格转换-水彩简化",
                "description": "水彩简化风格转换",
                "prompt": f"转换为水彩画艺术风格，简化线条，水彩渲染效果，柔和色彩，{base_prompt_suffix}",
                "filename": "03_水彩简化风格.jpg"
            },
            {
                "id": 4,
                "name": "动作延展-九合一",
                "description": "九合一动作大图",
                "prompt": f"""生成角色9种不同动作，排列成3×3九宫格布局：
1. 打招呼 2. 敬礼 3. 比心 4. 认真工作 5. 可爱pose
6. 挥手 7. 歪头 8. 点赞 9. 害羞

要求：单张大图，九宫格布局，每个动作清晰可辨，{base_prompt_suffix}""",
                "filename": "04_动作九合一.jpg"
            },
            {
                "id": 5,
                "name": "文创设计-九合一",
                "description": "九合一文创产品大图",
                "prompt": f"""设计商业化文创产品，生成单张3×3九宫格布局的文创产品集合大图：
1. 杯子+水壶组合展示 2. 抱枕设计 3. 背包+挎包组合展示
4. 手机壳设计 5. 小挂件设计 6. 手办设计
7. 眼罩设计 8. T恤设计 9. 4张多动作贴纸集合

要求：单张大图，九宫格布局，产品设计美观实用，{base_prompt_suffix}""",
                "filename": "05_文创九合一.jpg"
            },
            {
                "id": 6,
                "name": "表情包-十二合一",
                "description": "十二合一表情包大图",
                "prompt": f"""制作12种常用社交表情，每个表情都要带中文文字，排列成单张大图整齐排列：
1. 比心❤️ 2. 对不起😔 3. 大笑😂 4. 伤心😢 5. 生气😠 6. 累了😫
7. 疑问❓ 8. 拜托🙏 9. 吃瓜🍉 10. 震惊😲 11. 使坏😈 12. 晚安🌙

要求：单张大图，整齐排列，每个表情清晰可辨，带中文文字，{base_prompt_suffix}""",
                "filename": "06_表情包十二合一.jpg"
            }
        ]
        
        return steps
    
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
                            "error