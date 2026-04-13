#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
角色图智能分析器 - 分析已有角色图片，提取生成参数
"""

import json
import os
import re
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime

class RoleImageAnalyzer:
    """角色图智能分析器"""
    
    def __init__(self):
        self.style_classifier = self.load_style_classifier()
        self.feature_extractor = self.load_feature_extractor()
        self.color_analyzer = self.load_color_analyzer()
        self.quality_assessor = self.load_quality_assessor()
        
    def load_style_classifier(self) -> Dict[str, List[str]]:
        """加载风格分类器"""
        return {
            "cyberpunk": ["机械", "霓虹", "未来", "科技", "赛博", "数据", "义体", "发光"],
            "ancient_chinese": ["古风", "传统", "汉服", "水墨", "古典", "仙侠", "武侠", "发髻"],
            "cute": ["可爱", "萌", "Q版", "圆润", "大眼睛", "卡通", "软萌", "甜美"],
            "tech": ["科技", "未来", "智能", "数据", "界面", "发光", "金属", "简约"],
            "fantasy": ["奇幻", "魔法", "精灵", "神秘", "幻想", "神话", "魔法阵", "翅膀"],
            "realistic": ["写实", "真实", "细节", "质感", "光影", "逼真", "照片", "现实"]
        }
    
    def load_feature_extractor(self) -> Dict[str, List[str]]:
        """加载特征提取器"""
        return {
            "hair_styles": ["长发", "短发", "马尾", "双马尾", "卷发", "直发", "刘海", "发饰"],
            "clothing_types": ["西装", "连衣裙", "T恤", "外套", "盔甲", "长袍", "制服", "休闲服"],
            "accessories": ["眼镜", "耳机", "背包", "武器", "首饰", "帽子", "围巾", "手套"],
            "facial_features": ["大眼睛", "小眼睛", "圆脸", "尖脸", "笑容", "严肃", "眼镜", "妆容"]
        }
    
    def load_color_analyzer(self) -> Dict[str, List[str]]:
        """加载色彩分析器"""
        return {
            "color_schemes": {
                "cool_tone": ["蓝色", "紫色", "青色", "银色", "黑色", "白色", "灰色"],
                "warm_tone": ["红色", "黄色", "橙色", "粉色", "棕色", "金色", "米色"],
                "neon": ["霓虹粉", "荧光绿", "亮蓝色", "荧光黄", "亮紫色", "荧光橙"],
                "pastel": ["淡粉色", "浅蓝色", "米白色", "淡黄色", "浅紫色", "淡绿色"],
                "monochrome": ["黑色", "白色", "灰色", "深灰", "浅灰", "银灰"]
            },
            "color_moods": {
                " energetic": ["红色", "橙色", "黄色", "霓虹色"],
                "calm": ["蓝色", "绿色", "紫色", "淡色"],
                "elegant": ["黑色", "白色", "金色", "银色"],
                "cute": ["粉色", "淡蓝", "淡紫", "淡黄"]
            }
        }
    
    def load_quality_assessor(self) -> Dict[str, Any]:
        """加载质量评估器"""
        return {
            "resolution_standards": {
                "excellent": 2048,
                "good": 1024,
                "average": 512,
                "poor": 256
            },
            "aspect_ratios": ["1:1", "3:4", "4:3", "16:9", "9:16"],
            "file_formats": ["png", "jpg", "jpeg", "webp"]
        }
    
    def analyze_image(self, image_path: str, user_description: str = "") -> Dict[str, Any]:
        """
        分析角色图片
        
        Args:
            image_path: 图片文件路径
            user_description: 用户提供的描述（可选）
            
        Returns:
            分析结果字典
        """
        # 检查文件是否存在
        if not os.path.exists(image_path):
            return self.create_error_result(f"图片文件不存在: {image_path}")
        
        # 基础分析
        analysis = {
            "image_info": self.get_image_info(image_path),
            "detected_style": "unknown",
            "key_features": [],
            "color_analysis": {},
            "character_type": "unknown",
            "quality_assessment": {},
            "extracted_parameters": {},
            "suggestions": [],
            "analysis_time": datetime.now().isoformat()
        }
        
        # 从文件名和路径提取信息
        filename = os.path.basename(image_path)
        analysis["filename_analysis"] = self.analyze_filename(filename)
        
        # 文本分析（简化版，实际需要CV）
        if user_description:
            analysis["user_description_analysis"] = self.analyze_user_description(user_description)
        
        # 风格检测
        analysis["detected_style"] = self.detect_style(filename, user_description)
        
        # 特征提取
        analysis["key_features"] = self.extract_features(filename, user_description)
        
        # 色彩分析
        analysis["color_analysis"] = self.analyze_colors(filename, user_description)
        
        # 角色类型判断
        analysis["character_type"] = self.determine_character_type(analysis)
        
        # 质量评估
        analysis["quality_assessment"] = self.assess_quality(image_path, analysis)
        
        # 提取生成参数
        analysis["extracted_parameters"] = self.extract_generation_parameters(analysis)
        
        # 生成建议
        analysis["suggestions"] = self.generate_suggestions(analysis)
        
        return analysis
    
    def get_image_info(self, image_path: str) -> Dict[str, Any]:
        """获取图片基本信息"""
        # 简化实现，实际需要图像处理库
        filename = os.path.basename(image_path)
        file_size = os.path.getsize(image_path) if os.path.exists(image_path) else 0
        
        return {
            "filename": filename,
            "file_size_bytes": file_size,
            "file_size_mb": round(file_size / (1024 * 1024), 2) if file_size > 0 else 0,
            "file_extension": os.path.splitext(filename)[1].lower().replace(".", ""),
            "file_path": image_path,
            "last_modified": datetime.fromtimestamp(os.path.getmtime(image_path)).isoformat() if os.path.exists(image_path) else ""
        }
    
    def analyze_filename(self, filename: str) -> Dict[str, Any]:
        """分析文件名"""
        name_lower = filename.lower()
        
        analysis = {
            "contains_style_keywords": [],
            "contains_feature_keywords": [],
            "filename_pattern": "unknown"
        }
        
        # 检查风格关键词
        for style, keywords in self.style_classifier.items():
            for keyword in keywords:
                if keyword in name_lower:
                    if style not in analysis["contains_style_keywords"]:
                        analysis["contains_style_keywords"].append(style)
        
        # 检查特征关键词
        for category, keywords in self.feature_extractor.items():
            for keyword in keywords:
                if keyword in name_lower:
                    feature_entry = f"{category}:{keyword}"
                    if feature_entry not in analysis["contains_feature_keywords"]:
                        analysis["contains_feature_keywords"].append(feature_entry)
        
        # 判断文件名模式
        patterns = {
            "role_design": ["角色", "人设", "形象", "design", "character"],
            "illustration": ["插画", "绘画", "画作", "illustration", "art"],
            "reference": ["参考", "原画", "设定", "reference", "concept"],
            "final": ["最终", "定稿", "完成", "final", "completed"]
        }
        
        for pattern_name, pattern_keywords in patterns.items():
            for keyword in pattern_keywords:
                if keyword in name_lower:
                    analysis["filename_pattern"] = pattern_name
                    break
        
        return analysis
    
    def analyze_user_description(self, description: str) -> Dict[str, Any]:
        """分析用户描述"""
        analysis = {
            "word_count": len(description.split()),
            "contains_style_keywords": [],
            "contains_feature_keywords": [],
            "key_phrases": [],
            "description_quality": "unknown"
        }
        
        # 提取关键短语（简单实现）
        sentences = re.split(r'[。！？!?]', description)
        for sentence in sentences:
            if len(sentence.strip()) > 10:  # 长度大于10字符的句子
                analysis["key_phrases"].append(sentence.strip())
        
        # 检查风格关键词
        for style, keywords in self.style_classifier.items():
            for keyword in keywords:
                if keyword in description:
                    if style not in analysis["contains_style_keywords"]:
                        analysis["contains_style_keywords"].append(style)
        
        # 检查特征关键词
        for category, keywords in self.feature_extractor.items():
            for keyword in keywords:
                if keyword in description:
                    feature_entry = f"{category}:{keyword}"
                    if feature_entry not in analysis["contains_feature_keywords"]:
                        analysis["contains_feature_keywords"].append(feature_entry)
        
        # 评估描述质量
        word_count = analysis["word_count"]
        if word_count > 100:
            analysis["description_quality"] = "excellent"
        elif word_count > 50:
            analysis["description_quality"] = "good"
        elif word_count > 20:
            analysis["description_quality"] = "average"
        else:
            analysis["description_quality"] = "poor"
        
        return analysis
    
    def detect_style(self, filename: str, description: str = "") -> str:
        """检测风格"""
        all_text = f"{filename} {description}".lower()
        
        style_scores = {}
        
        # 计算风格匹配分数
        for style, keywords in self.style_classifier.items():
            score = 0
            for keyword in keywords:
                if keyword in all_text:
                    score += 1
            
            if score > 0:
                style_scores[style] = score
        
        # 选择最高分风格
        if style_scores:
            best_style = max(style_scores.items(), key=lambda x: x[1])
            return best_style[0]
        
        return "general"  # 通用风格
    
    def extract_features(self, filename: str, description: str = "") -> List[str]:
        """提取特征"""
        all_text = f"{filename} {description}"
        features = []
        
        # 提取发型特征
        for hair_style in self.feature_extractor["hair_styles"]:
            if hair_style in all_text:
                features.append(f"发型:{hair_style}")
        
        # 提取服装特征
        for clothing in self.feature_extractor["clothing_types"]:
            if clothing in all_text:
                features.append(f"服装:{clothing}")
        
        # 提取配饰特征
        for accessory in self.feature_extractor["accessories"]:
            if accessory in all_text:
                features.append(f"配饰:{accessory}")
        
        # 提取面部特征
        for facial in self.feature_extractor["facial_features"]:
            if facial in all_text:
                features.append(f"面部:{facial}")
        
        return features
    
    def analyze_colors(self, filename: str, description: str = "") -> Dict[str, Any]:
        """分析色彩"""
        all_text = f"{filename} {description}".lower()
        
        color_analysis = {
            "detected_color_scheme": "unknown",
            "detected_color_mood": "unknown",
            "color_keywords": [],
            "color_confidence": 0
        }
        
        # 检测色彩方案
        for scheme, colors in self.color_analyzer["color_schemes"].items():
            for color in colors:
                if color in all_text:
                    color_analysis["detected_color_scheme"] = scheme
                    color_analysis["color_keywords"].append(color)
                    color_analysis["color_confidence"] += 1
        
        # 检测色彩情绪
        for mood, colors in self.color_analyzer["color_moods"].items():
            for color in colors:
                if color in all_text:
                    color_analysis["detected_color_mood"] = mood
                    break
        
        return color_analysis
    
    def determine_character_type(self, analysis: Dict[str, Any]) -> str:
        """确定角色类型"""
        features = analysis.get("key_features", [])
        style = analysis.get("detected_style", "")
        
        # 基于特征判断
        character_types = {
            "human": ["发型:", "服装:", "面部:"],
            "animal": ["动物", "兽人", "猫", "狗", "熊", "兔"],
            "robot": ["机械", "机器人", "AI", "机甲", "义体"],
            "fantasy": ["精灵", "魔法", "奇幻", "神话", "翅膀"]
        }
        
        # 检查特征匹配
        for char_type, indicators in character_types.items():
            for indicator in indicators:
                if any(indicator in feature for feature in features) or indicator in style:
                    return char_type
        
        return "human"  # 默认人类角色
    
    def assess_quality(self, image_path: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """评估质量"""
        quality = {
            "file_quality": "unknown",
            "content_quality": "unknown",
            "suitability": "unknown",
            "overall_score": 0,
            "issues": [],
            "strengths": []
        }
        
        # 文件质量评估
        file_info = analysis.get("image_info", {})
        file_size_mb = file_info.get("file_size_mb", 0)
        file_extension = file_info.get("file_extension", "")
        
        if file_size_mb > 5:
            quality["file_quality"] = "excellent"
            quality["strengths"].append("文件大小充足，适合高质量处理")
        elif file_size_mb > 1:
            quality["file_quality"] = "good"
        elif file_size_mb > 0.1:
            quality["file_quality"] = "average"
        else:
            quality["file_quality"] = "poor"
            quality["issues"].append("文件大小可能不足，影响处理质量")
        
        # 文件格式检查
        if file_extension in self.quality_assessor["file_formats"]:
            quality["strengths"].append(f"文件格式{file_extension}支持良好")
        else:
            quality["issues"].append(f"文件格式{file_extension}可能不兼容")
        
        # 内容质量评估
        description_analysis = analysis.get("user_description_analysis", {})
        desc_quality = description_analysis.get("description_quality", "unknown")
        
        if desc_quality == "excellent":
            quality["content_quality"] = "excellent"
            quality["strengths"].append("描述详细，有助于精准分析")
        elif desc_quality == "good":
            quality["content_quality"] = "good"
        elif desc_quality == "average":
            quality["content_quality"] = "average"
        else:
            quality["content_quality"] = "poor"
            quality["issues"].append("描述信息不足，可能影响分析精度")
        
        # 适用性评估
        style = analysis.get("detected_style", "")
        features = analysis.get("key_features", [])
        
        if style != "unknown" and len(features) > 2:
            quality["suitability"] = "high"
            quality["strengths"].append("风格明确，特征丰富，适合系列化设计")
        elif style != "unknown" or len(features) > 0:
            quality["suitability"] = "medium"
        else:
            quality["suitability"] = "low"
            quality["issues"].append("风格和特征信息不足，可能影响设计效果")
        
        # 计算总体分数
        score_map = {"excellent": 5, "good": 4, "average": 3, "poor": 2, "unknown": 1}
        
        file_score = score_map.get(quality["file_quality"], 1)
        content_score = score_map.get(quality["content_quality"], 1)
        suitability_score = {"high": 5, "medium": 3, "low": 1}.get(quality["suitability"], 1)
        
        quality["overall_score"] = round((file_score + content_score + suitability_score) / 3, 1)
        
        return quality
    
    def extract_generation_parameters(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """提取生成参数"""
        params = {
            "style": analysis.get("detected_style", "general"),
            "character_type": analysis.get("character_type", "human"),
            "color_scheme": analysis.get("color_analysis", {}).get("detected_color_scheme", "general"),
            "key_features": analysis.get("key_features", []),
            "base_prompt": self.generate_base_prompt(analysis),
            "wanxiang_parameters": self.generate_wanxiang_parameters(analysis)
        }
        
        return params
    
    def generate_base_prompt(self, analysis: Dict[str, Any]) -> str:
        """生成基础提示词"""
        style = analysis.get("detected_style", "通用")
        features = analysis.get("key_features", [])
        color_scheme = analysis.get("color_analysis", {}).get("detected_color_scheme", "通用")
        
        # 提取特征描述
        feature_descriptions = []
        for feature in features[:5]:  # 取前5个特征
            if ":" in feature:
                _, desc = feature.split(":", 1)
                feature_descriptions.append(desc)
        
        features_text = "、".join(feature_descriptions) if feature_descriptions else "精致设计"
        
        # 构建基础提示词
        prompt = f"{style}风格角色，{features_text}，{color_scheme}色彩方案"
        
        return prompt
    
    def generate_wanxiang_parameters(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """生成Wanxiang 4.5参数"""
        style = analysis.get("detected_style", "general")
        
        # Wanxiang参数映射
        wanxiang_params = {
            "model": "wanxiang-4.5",
            "width": 2048,
            "height": 2048,
            "steps": 30,
            "cfg_scale": 7.5,
            "sampler": "DPM++ 2M Karras",
            "seed": -1,  # 随机种子
            "style_preset": self.map_style_to_wanxiang(style),
            "quality": "high",
            "aspect_ratio": "1:1"
        }
        
        return wanxiang_params
    
    def map_style_to_wanxiang(self, style: str) -> str:
        """映射风格到Wanxiang预设"""
        style_map = {
            "cyberpunk": "cyberpunk",
            "ancient_chinese": "anime",
            "cute": "cute",
            "tech": "futuristic",
            "fantasy": "fantasy",
            "realistic": "realistic",
            "general": "general"
        }
        
        return style_map.get(style, "general")
    
    def generate_suggestions(self, analysis: Dict[str, Any]) -> List[str]:
        """生成建议"""
        suggestions = []
        
        quality = analysis.get("quality_assessment", {})
        overall_score = quality.get("overall_score", 0)
        issues = quality.get("issues", [])
        strengths = quality.get("strengths", [])
        
        # 基于质量评分的建议
        if overall_score >= 4.5:
            suggestions.append("图片质量优秀，可直接用于高质量系列化设计")
            suggestions.append("建议进行完整的7步流程，最大化IP价值")
        
        elif overall_score >= 4.0:
            suggestions.append("图片质量良好，适合大多数系列化应用")
            suggestions.append("建议重点优化关键步骤，如三视图和表情包")
        
        elif overall_score >= 3.5:
            suggestions.append("图片质量一般，建议先进行基础优化")
            suggestions.append("可考虑风格强化或特征补充")
        
        elif overall_score >= 3.0:
            suggestions.append("图片质量有待提高，建议重新评估")
            suggestions.append("可能需要重新拍摄或寻找更高质量的图片")
        
        else:
            suggestions.append("图片质量不足，不建议直接使用")
            suggestions.append("建议重新获取高质量图片或考虑从零创建")
        
        # 基于问题的建议
        for issue in issues[:3]:  # 取前3个问题
            suggestions.append(f"注意: {issue}")
        
        # 基于优势的建议
        for strength in strengths[:2]:  # 取前2个优势
            suggestions.append(f"优势: {strength}，可充分利用")
        
        # 基于风格的建议
        style = analysis.get("detected_style", "")
        if style in ["cyberpunk", "tech"]:
            suggestions.append("赛博/科技风格适合动态化和未来感设计")
        elif style in ["ancient_chinese", "fantasy"]:
            suggestions.append("古风/奇幻风格适合文创产品和故事化扩展")
        elif style == "cute":
            suggestions.append("可爱风格适合表情包和萌系文创")
        
        return suggestions
    
    def create_error_result(self, error_message: str) -> Dict[str, Any]:
        """创建错误结果"""
        return {
            "error": error_message,
            "analysis_time": datetime.now().isoformat(),
            "suggestions": [
                "检查图片文件路径是否正确",
                "确保图片文件格式支持（PNG/JPG/WebP）",
                "尝试重新上传或提供图片描述"
            ]
        }
    
    def format_analysis_for_display(self, analysis: Dict[str, Any]) -> str:
        """格式化分析结果用于显示"""
        if "error" in analysis:
            return f"分析失败: {analysis['error']}"
        
        output = "## 角色图分析结果\n\n"
        
        # 基本信息
        image_info = analysis.get("image_info", {})
        output += f"**文件信息**: {image_info.get('filename', '未知')} "
        output += f"({image_info.get('file_size_mb', 0)}MB)\n\n"
        
        # 检测结果
        output += "### 检测结果\n"
        output += f"- **风格**: {analysis.get('detected_style', '未知')}\n"
        output += f"- **角色类型**: {analysis.get('character_type', '未知')}\n"
        
        color_analysis = analysis.get("color_analysis", {})
        output += f"- **色彩方案**: {color_analysis.get('detected_color_scheme', '未知')}\n"
        output += f"- **色彩情绪**: {color_analysis.get('detected_color_mood', '未知')}\n\n"
        
        # 关键特征
        features = analysis.get("key_features", [])
        if features:
            output += "### 关键特征\n"
            for feature in features[:5]:  # 显示前5个特征
                output += f"- {feature}\n"
            output += "\n"
        
        # 质量评估
        quality = analysis.get("quality_assessment", {})
        output += "### 质量评估\n"
        output += f"- **文件质量**: {quality.get('file_quality', '未知')}\n"
        output += f"- **内容质量**: {quality.get('content_quality', '未知')}\n"
        output += f"- **适用性**: {quality.get('suitability', '未知')}\n"
        output += f"- **总体评分**: {quality.get('overall_score', 0)}/5\n\n"
        
        # 建议
        suggestions = analysis.get("suggestions", [])
        if suggestions:
            output += "### 优化建议\n"
            for i, suggestion in enumerate(suggestions[:5], 1):  # 显示前5个建议
                output += f"{i}. {suggestion}\n"
        
        return output

def main():
    """主函数 - 测试角色分析器"""
    print("=== 角色图智能分析器测试 ===\n")
    
    # 创建分析器
    analyzer = RoleImageAnalyzer()
    
    # 测试用例
    test_cases = [
        {
            "filename": "赛博猫娘_机械义体_霓虹色彩.png",
            "description": "一个赛博朋克风格的猫娘角色，带有银色机械义体和蓝色霓虹灯光，未来感十足"
        },
        {
            "filename": "古风仙侠女剑客.jpg",
            "description": "古风仙侠风格的女剑客，穿着汉服，手持长剑，气质清冷"
        },
        {
            "filename": "可爱萌宠Q版角色.webp",
            "description": "Q版可爱风格的萌宠角色，大眼睛圆脸，适合表情包"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"测试用例 {i}:")
        print(f"文件名: {test_case['filename']}")
        print(f"描述: {test_case['description']}")
        
        # 模拟分析
        analysis = analyzer.analyze_image(
            image_path=test_case['filename'],  # 模拟路径
            user_description=test_case['description']
        )
        
        # 显示格式化结果
        formatted = analyzer.format_analysis_for_display(analysis)
        print(formatted)
        
        # 显示提取的参数
        if "extracted_parameters" in analysis:
            params = analysis["extracted_parameters"]
            print("### 提取的生成参数")
            print(f"- 风格: {params.get('style', '未知')}")
            print(f"- 角色类型: {params.get('character_type', '未知')}")
            print(f"- 色彩方案: {params.get('color_scheme', '未知')}")
            print(f"- 基础提示词: {params.get('base_prompt', '未知')}")
            
            wanxiang_params = params.get("wanxiang_parameters", {})
            print(f"- Wanxiang模型: {wanxiang_params.get('model', '未知')}")
            print(f"- 分辨率: {wanxiang_params.get('width', 0)}x{wanxiang_params.get('height', 0)}")
            print(f"- 风格预设: {wanxiang_params.get('style_preset', '未知')}")
        
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()