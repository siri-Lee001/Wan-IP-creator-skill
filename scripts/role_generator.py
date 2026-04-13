#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
角色图生成器 - 基于确认需求生成角色图变体
"""

import json
import os
import sys
from typing import Dict, List, Any, Tuple
from datetime import datetime

class RoleImageGenerator:
    """角色图生成器"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        self.prompt_templates = self.load_prompt_templates()
        self.style_configs = self.load_style_configs()
        
        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_prompt_templates(self) -> Dict[str, str]:
        """加载提示词模板"""
        return {
            "cyberpunk_cute": "纯白背景前站立{材质}材质Q版动漫{角色类型}。{发型描述}，{头部特征}，{服装描述}，{配饰细节}。C4D渲染强调材质特性:高反光{材质}表面精确呈现饱和色块冲突，{纹理细节}极清晰。光影简洁突出先锋艺术感。赛博朋克元素:{赛博元素}，色彩方案:{色彩方案}。",
            
            "ancient_chinese": "纯白背景前{姿势}{材质}材质古风{角色类型}。{发型描述}，{头部特征}，{服装描述}，{配饰细节}。水墨渲染强调{材质}质感，{纹理细节}细腻。光影柔和突出古典美感。古风元素:{古风元素}，色彩方案:{色彩方案}。",
            
            "tech_futuristic": "纯白背景前站立{材质}材质未来科技{角色类型}。{发型描述}，{头部特征}，{服装描述}，{配饰细节}。3D渲染强调科技质感:{材质}表面带有发光元素，{纹理细节}清晰。光影强烈突出科技感。科技元素:{科技元素}，色彩方案:{色彩方案}。",
            
            "fantasy_magic": "纯白背景前{姿势}{材质}材质奇幻{角色类型}。{发型描述}，{头部特征}，{服装描述}，{配饰细节}。魔法渲染强调{材质}魔力效果，{纹理细节}带有魔法光泽。光影梦幻突出奇幻感。魔法元素:{魔法元素}，色彩方案:{色彩方案}。"
        }
    
    def load_style_configs(self) -> Dict[str, Dict[str, Any]]:
        """加载风格配置"""
        return {
            "cyberpunk": {
                "materials": ["PVC", "金属", "玻璃", "发光材料"],
                "colors": ["冷色调", "霓虹色", "金属色", "荧光色"],
                "elements": ["机械义体", "数据线", "全息投影", "霓虹灯光", "代码流"],
                "textures": ["电路板纹理", "金属拉丝", "玻璃反光", "发光边缘"]
            },
            "ancient_chinese": {
                "materials": ["丝绸", "陶瓷", "玉石", "木材"],
                "colors": ["传统色彩", "水墨色", "金色", "红色"],
                "elements": ["传统纹样", "古典配饰", "水墨效果", "书法元素"],
                "textures": ["丝绸质感", "陶瓷光泽", "木纹", "水墨晕染"]
            },
            "tech": {
                "materials": ["金属", "碳纤维", "玻璃", "发光聚合物"],
                "colors": ["科技蓝", "银色", "黑色", "发光色"],
                "elements": ["LED灯带", "全息界面", "机械结构", "数据可视化"],
                "textures": ["金属抛光", "碳纤维纹理", "玻璃透光", "发光效果"]
            },
            "fantasy": {
                "materials": ["水晶", "魔法材料", "发光宝石", "神秘金属"],
                "colors": ["魔法紫", "精灵绿", "神秘蓝", "金色"],
                "elements": ["魔法阵", "精灵翅膀", "魔法光效", "神秘符文"],
                "textures": ["水晶折射", "魔法光泽", "宝石闪光", "符文发光"]
            }
        }
    
    def analyze_requirements(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """分析需求，确定生成参数"""
        analysis = {
            "primary_style": "cyberpunk",
            "secondary_styles": [],
            "color_scheme": "cool_tone",
            "key_elements": [],
            "character_type": "角色",
            "complexity": "medium"
        }
        
        # 从需求中提取风格信息
        if "generation_parameters" in requirements:
            params = requirements["generation_parameters"]
            
            if "style" in params:
                style_map = {
                    "cyberpunk": "cyberpunk",
                    "ancient_chinese": "ancient_chinese",
                    "tech": "tech",
                    "cute": "cyberpunk",  # 可爱风格映射到赛博可爱
                    "minimalist": "tech",  # 简约映射到科技
                    "retro": "ancient_chinese"  # 复古映射到古风
                }
                analysis["primary_style"] = style_map.get(params["style"], "cyberpunk")
            
            if "color_scheme" in params:
                analysis["color_scheme"] = params["color_scheme"]
        
        # 从具体细节中提取关键元素
        if "specific_details" in requirements:
            details = requirements["specific_details"]
            for detail in details.values():
                # 提取角色类型
                if any(word in detail for word in ["猫", "狗", "动物", "兽人"]):
                    analysis["character_type"] = "动物角色"
                elif any(word in detail for word in ["机器人", "AI", "机械"]):
                    analysis["character_type"] = "机械角色"
                elif any(word in detail for word in ["精灵", "魔法", "奇幻"]):
                    analysis["character_type"] = "奇幻角色"
                
                # 提取关键元素
                for element in ["机械", "魔法", "科技", "传统", "可爱", "帅气"]:
                    if element in detail:
                        analysis["key_elements"].append(element)
        
        # 确定复杂度
        if len(analysis["key_elements"]) > 3:
            analysis["complexity"] = "high"
        elif len(analysis["key_elements"]) > 1:
            analysis["complexity"] = "medium"
        else:
            analysis["complexity"] = "low"
        
        return analysis
    
    def generate_variants(self, analysis: Dict[str, Any], requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成3个角色图变体"""
        variants = []
        primary_style = analysis["primary_style"]
        style_config = self.style_configs.get(primary_style, self.style_configs["cyberpunk"])
        
        # 变体1: 标准版 - 完全按照分析结果
        variant1 = self.create_variant(
            variant_id=1,
            style=primary_style,
            style_config=style_config,
            analysis=analysis,
            requirements=requirements,
            variation_type="standard"
        )
        variants.append(variant1)
        
        # 变体2: 强化版 - 强化关键元素
        variant2 = self.create_variant(
            variant_id=2,
            style=primary_style,
            style_config=style_config,
            analysis=analysis,
            requirements=requirements,
            variation_type="enhanced"
        )
        variants.append(variant2)
        
        # 变体3: 混合版 - 混合其他风格元素
        variant3 = self.create_variant(
            variant_id=3,
            style=primary_style,
            style_config=style_config,
            analysis=analysis,
            requirements=requirements,
            variation_type="hybrid"
        )
        variants.append(variant3)
        
        return variants
    
    def create_variant(self, variant_id: int, style: str, style_config: Dict[str, Any], 
                      analysis: Dict[str, Any], requirements: Dict[str, Any], 
                      variation_type: str) -> Dict[str, Any]:
        """创建单个变体"""
        # 选择模板
        template_map = {
            "cyberpunk": "cyberpunk_cute",
            "ancient_chinese": "ancient_chinese",
            "tech": "tech_futuristic",
            "fantasy": "fantasy_magic"
        }
        template_key = template_map.get(style, "cyberpunk_cute")
        template = self.prompt_templates[template_key]
        
        # 生成变体参数
        variant_params = self.generate_variant_parameters(
            style_config=style_config,
            analysis=analysis,
            variation_type=variation_type
        )
        
        # 填充模板
        prompt = template.format(**variant_params)
        
        # 生成变体描述
        description = self.generate_variant_description(
            variant_id=variant_id,
            style=style,
            params=variant_params,
            variation_type=variation_type
        )
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"role_variant_{variant_id}_{style}_{timestamp}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        # 保存提示词
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# 角色图变体 {variant_id}\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"风格: {style} ({variation_type}版)\n")
            f.write(f"描述: {description}\n\n")
            f.write("提示词:\n")
            f.write(prompt)
        
        return {
            "id": variant_id,
            "name": f"变体{variant_id}: {description}",
            "style": style,
            "variation_type": variation_type,
            "prompt": prompt,
            "description": description,
            "parameters": variant_params,
            "filepath": filepath,
            "preview_prompt": self.generate_preview_prompt(prompt)
        }
    
    def generate_variant_parameters(self, style_config: Dict[str, Any], 
                                   analysis: Dict[str, Any], 
                                   variation_type: str) -> Dict[str, str]:
        """生成变体参数"""
        params = {
            "角色类型": analysis.get("character_type", "角色"),
            "材质": self.select_random(style_config["materials"]),
            "发型描述": self.generate_hair_description(style_config, variation_type),
            "头部特征": self.generate_head_features(style_config, variation_type),
            "服装描述": self.generate_clothing_description(style_config, variation_type),
            "配饰细节": self.generate_accessories(style_config, variation_type),
            "纹理细节": self.select_random(style_config["textures"]),
            "色彩方案": self.generate_color_scheme(style_config, analysis),
            "姿势": self.select_pose(variation_type)
        }
        
        # 添加风格特定元素
        style_element_key = {
            "cyberpunk": "赛博元素",
            "ancient_chinese": "古风元素",
            "tech": "科技元素",
            "fantasy": "魔法元素"
        }
        
        for style_name, element_key in style_element_key.items():
            if style_name in str(style_config):
                params[element_key] = ", ".join(style_config["elements"][:3])
                break
        
        # 根据变体类型调整
        if variation_type == "enhanced":
            # 强化版：更多元素，更复杂
            params["配饰细节"] += f", 额外添加{self.select_random(style_config['elements'])}"
            params["纹理细节"] += f"和{self.select_random(style_config['textures'])}"
        
        elif variation_type == "hybrid":
            # 混合版：混合其他风格元素
            other_styles = [s for s in self.style_configs.keys() if s != list(self.style_configs.keys())[0]]
            if other_styles:
                mixed_style = self.select_random(other_styles)
                mixed_elements = self.style_configs[mixed_style]["elements"][:2]
                params["配饰细节"] += f", 融合{mixed_style}风格元素: {', '.join(mixed_elements)}"
        
        return params
    
    def generate_variant_description(self, variant_id: int, style: str, 
                                   params: Dict[str, str], variation_type: str) -> str:
        """生成变体描述"""
        style_names = {
            "cyberpunk": "赛博朋克",
            "ancient_chinese": "古风",
            "tech": "未来科技",
            "fantasy": "奇幻魔法"
        }
        
        variation_names = {
            "standard": "标准版",
            "enhanced": "强化版",
            "hybrid": "混合版"
        }
        
        style_name = style_names.get(style, style)
        variation_name = variation_names.get(variation_type, variation_type)
        
        # 提取关键特征
        key_features = []
        if "材质" in params:
            key_features.append(params["材质"])
        if "色彩方案" in params:
            key_features.append(params["色彩方案"])
        if "赛博元素" in params:
            key_features.extend(params["赛博元素"].split(", ")[:2])
        elif "古风元素" in params:
            key_features.extend(params["古风元素"].split(", ")[:2])
        elif "科技元素" in params:
            key_features.extend(params["科技元素"].split(", ")[:2])
        elif "魔法元素" in params:
            key_features.extend(params["魔法元素"].split(", ")[:2])
        
        description = f"{style_name}{variation_name}"
        if key_features:
            description += f" - {', '.join(key_features[:3])}"
        
        return description
    
    def generate_preview_prompt(self, full_prompt: str) -> str:
        """生成预览用简版提示词"""
        # 提取关键信息
        lines = full_prompt.split("。")
        key_lines = []
        
        for line in lines:
            if any(keyword in line for keyword in ["材质", "发型", "服装", "色彩", "元素"]):
                key_lines.append(line.strip())
        
        preview = "。".join(key_lines[:4]) + "。"
        
        # 简化长度
        if len(preview) > 200:
            preview = preview[:197] + "..."
        
        return preview
    
    # 辅助方法
    def select_random(self, items: List[str]) -> str:
        """随机选择列表中的项目"""
        import random
        return random.choice(items) if items else ""
    
    def generate_hair_description(self, style_config: Dict[str, Any], variation_type: str) -> str:
        """生成发型描述"""
        base_hairs = ["长发", "短发", "中长发", "双马尾", "单马尾"]
        style_hairs = {
            "cyberpunk": ["霓虹染发", "数据流发型", "机械发饰"],
            "ancient_chinese": ["发髻", "发簪", "步摇"],
            "tech": ["发光发型", "全息发饰", "几何剪裁"],
            "fantasy": ["魔法光泽发", "精灵尖耳", "水晶发饰"]
        }
        
        # 确定风格
        style = list(style_config.keys())[0] if isinstance(style_config, dict) else "cyberpunk"
        
        hair_options = base_hairs + style_hairs.get(style, [])
        
        if variation_type == "enhanced":
            # 强化版：组合多个元素
            hair = f"{self.select_random(base_hairs)}搭配{self.select_random(style_hairs.get(style, ['']))}"
        else:
            hair = self.select_random(hair_options)
        
        return hair
    
    def generate_head_features(self, style_config: Dict[str, Any], variation_type: str) -> str:
        """生成头部特征"""
        base_features = ["大眼睛", "精致五官", "可爱表情"]
        style_features = {
            "cyberpunk": ["机械义眼", "数据接口", "霓虹妆容"],
            "ancient_chinese": ["古典妆容", "花钿", "细眉"],
            "tech": ["全息眼镜", "面部LED", "科技面纹"],
            "fantasy": ["魔法印记", "精灵尖耳", "宝石额饰"]
        }
        
        style = list(style_config.keys())[0] if isinstance(style_config, dict) else "cyberpunk"
        
        features = base_features + style_features.get(style, [])
        selected = self.select_random(features)
        
        if variation_type == "enhanced" and len(features) > 1:
            # 添加第二个特征
            second = self.select_random([f for f in features if f != selected])
            selected = f"{selected}和{second}"
        
        return selected
    
    def generate_clothing_description(self, style_config: Dict[str, Any], variation_type: str) -> str:
        """生成服装描述"""
        base_clothing = ["时尚服装", "个性穿搭", "特色服饰"]
        style_clothing = {
            "cyberpunk": ["机械装甲", "霓虹外套", "数据线装饰"],
            "ancient_chinese": ["汉服", "旗袍", "古风长袍"],
            "tech": ["科技战衣", "发光服装", "智能织物"],
            "fantasy": ["魔法长袍", "精灵服饰", "奇幻装备"]
        }
        
        style = list(style_config.keys())[0] if isinstance(style_config, dict) else "cyberpunk"
        
        clothing_options = base_clothing + style_clothing.get(style, [])
        clothing = self.select_random(clothing_options)
        
        if variation_type == "enhanced":
            clothing += f"，带有{self.select_random(style_config.get('elements', ['']))}装饰"
        
        return clothing
    
    def generate_accessories(self, style_config: Dict[str, Any], variation_type: str) -> str:
        """生成配饰细节"""
        base_accessories = ["个性配饰", "特色装饰", "时尚配件"]
        style_accessories = {
            "cyberpunk": ["机械臂", "数据背包", "霓虹首饰"],
            "ancient_chinese": ["玉佩", "香囊", "古典首饰"],
            "tech": ["全息设备", "科技配件", "智能手表"],
            "fantasy": ["魔法杖", "精灵首饰", "符文装备"]
        }
        
        style = list(style_config.keys())[0] if isinstance(style_config, dict) else "cyberpunk"
        
        accessory_options = base_accessories + style_accessories.get(style, [])
        accessories = self.select_random(accessory_options)
        
        if variation_type == "enhanced":
            # 添加多个配饰
            second = self.select_random([a for a in accessory_options if a != accessories])
            accessories = f"{accessories}和{second}"
        
        return accessories
    
    def generate_color_scheme(self, style_config: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """生成色彩方案"""
        color_scheme = analysis.get("color_scheme", "cool_tone")
        
        color_map = {
            "cool_tone": "冷色调为主，搭配霓虹色点缀",
            "warm_tone": "暖色调为主，搭配金色点缀",
            "neon": "霓虹色系，高饱和撞色",
            "pastel": "马卡龙色系，柔和温暖",
            "monochrome": "黑白灰色调，简约现代"
        }
        
        return color_map.get(color_scheme, "冷色调为主，搭配霓虹色点缀")
    
    def select_pose(self, variation_type: str) -> str:
        """选择姿势"""
        poses = ["站立", "坐姿", "行走", "奔跑", "跳跃"]
        
        if variation_type == "enhanced":
            return "动态" + self.select_random(poses)
        else:
            return self.select_random(poses)
    
    def format_variants_for_display(self, variants: List[Dict[str, Any]]) -> str:
        """格式化变体用于显示"""
        output = "基于您的需求，我生成了3个不同方向的角色图变体：\n\n"
        
        for variant in variants:
            output += f"## {variant['name']}\n"
            output += f"**风格**: {variant['style']} ({variant['variation_type']}版)\n"
            output += f"**描述**: {variant['description']}\n"
            output += f"**关键特征**: \n"
            
            # 提取关键参数
            params = variant['parameters']
            key_params = ["材质", "发型描述", "服装描述", "色彩方案"]
            
            for key in key_params:
                if key in params:
                    output += f"  - {key}: {params[key]}\n"
            
            output += f"**预览提示词**: {variant['preview_prompt']}\n\n"
        
        output += "请选择最接近您想象的变体，或告诉我需要调整的方向：\n"
        output += "1. 选择变体1/2/3\n"
        output += "2. 需要修改某个变体的特定元素\n"
        output += "3. 都不满意，需要重新生成\n"
        output += "4. 混合多个变体的元素\n"
        
        return output
    
    def process_user_feedback(self, variants: List[Dict[str, Any]], feedback: str) -> Dict[str, Any]:
        """处理用户反馈"""
        feedback_analysis = {
            "selected_variant": None,
            "modification_requests": [],
            "regenerate_requested": False,
            "mix_requested": False,
            "mix_elements": []
        }
        
        # 简单关键词分析
        feedback_lower = feedback.lower()
        
        # 检查选择
        for i in range(1, 4):
            if f"变体{i}" in feedback or f"variant{i}" in feedback_lower or str(i) in feedback:
                feedback_analysis["selected_variant"] = i
                break
        
        # 检查修改请求
        modification_keywords = ["修改", "调整", "改变", "去掉", "增加", "减少"]
        for keyword in modification_keywords:
            if keyword in feedback:
                feedback_analysis["modification_requests"].append(feedback)
                break
        
        # 检查重新生成
        if any(word in feedback_lower for word in ["重新", "都不", "不满意", "重来"]):
            feedback_analysis["regenerate_requested"] = True
        
        # 检查混合请求
        if any(word in feedback for word in ["混合", "结合", "融合", "组合"]):
            feedback_analysis["mix_requested"] = True
            
            # 提取混合元素
            for variant in variants:
                variant_id = variant['id']
                if str(variant_id) in feedback:
                    feedback_analysis["mix_elements"].append(variant_id)
        
        return feedback_analysis

def main():
    """主函数 - 测试角色图生成器"""
    print("=== 角色图生成器测试 ===\n")
    
    # 创建生成器
    generator = RoleImageGenerator(output_dir="test_output")
    
    # 测试需求
    test_requirements = {
        "generation_parameters": {
            "style": "cyberpunk",
            "color_scheme": "neon",
            "platforms": ["sticker", "red_note"]
        },
        "specific_details": {
            "detail_0": "一个生活在赛博都市的猫娘，白天是程序员，晚上是黑客",
            "detail_1": "希望有机械义体和数据线元素",
            "detail_2": "用于微信表情包和小红书内容"
        }
    }
    
    # 分析需求
    analysis = generator.analyze_requirements(test_requirements)
    print("需求分析结果:")
    print(f"  主要风格: {analysis['primary_style']}")
    print(f"  色彩方案: {analysis['color_scheme']}")
    print(f"  角色类型: {analysis['character_type']}")
    print(f"  关键元素: {analysis['key_elements']}")
    print(f"  复杂度: {analysis['complexity']}")
    
    # 生成变体
    print("\n生成角色图变体...")
    variants = generator.generate_variants(analysis, test_requirements)
    
    # 显示变体
    display_text = generator.format_variants_for_display(variants)
    print(display_text)
    
    # 测试用户反馈处理
    print("\n测试用户反馈处理...")
    test_feedbacks = [
        "我选择变体2，但希望把发型改成短发",
        "都不满意，重新生成",
        "混合变体1的服装和变体3的色彩"
    ]
    
    for feedback in test_feedbacks:
        print(f"\n反馈: {feedback}")
        analysis = generator.process_user_feedback(variants, feedback)
        print(f"分析结果: {analysis}")

if __name__ == "__main__":
    main()