#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能提问引擎 - 基于用户创意动态生成提问问题
"""

import json
import sys
from typing import Dict, List, Any

class IntelligentQuestionnaire:
    """智能提问引擎"""
    
    def __init__(self):
        self.question_templates = self.load_question_templates()
        self.creative_types = self.load_creative_types()
        
    def load_question_templates(self) -> Dict[str, List[Dict]]:
        """加载提问模板"""
        return {
            "创意概念": [
                {
                    "question": "请详细描述您的IP创意核心概念",
                    "follow_up": "这个创意的独特之处是什么？",
                    "examples": ["一个会魔法的外卖小哥", "未来世界的垃圾分类机器人"]
                },
                {
                    "question": "这个IP的世界观或背景设定是什么？",
                    "follow_up": "有什么特殊的规则或设定吗？",
                    "examples": ["近未来赛博都市", "古代神话与现代科技结合"]
                }
            ],
            "目标用户": [
                {
                    "question": "这个IP的目标用户群体是什么？",
                    "follow_up": "用户的年龄、性别、兴趣有什么特点？",
                    "examples": ["Z世代年轻人", "二次元爱好者", "科技产品用户"]
                },
                {
                    "question": "用户会在什么场景下使用或接触这个IP？",
                    "follow_up": "使用频率和接触深度如何？",
                    "examples": ["日常社交聊天", "游戏角色", "文创产品收藏"]
                }
            ],
            "风格调性": [
                {
                    "question": "期望的视觉风格和情感基调是什么？",
                    "follow_up": "有什么具体的视觉参考或灵感来源？",
                    "examples": ["赛博朋克+可爱风", "极简主义+科技感", "复古像素+现代设计"]
                },
                {
                    "question": "色彩偏好和视觉元素偏好？",
                    "follow_up": "有什么需要避免的颜色或元素？",
                    "examples": ["冷色调为主，霓虹色点缀", "马卡龙色系，柔和温暖"]
                }
            ],
            "应用场景": [
                {
                    "question": "IP的主要应用场景和平台是什么？",
                    "follow_up": "不同场景下需要什么不同的表现形式？",
                    "examples": ["微信表情包", "小红书内容", "游戏角色", "文创产品"]
                },
                {
                    "question": "需要哪些具体的输出形式？",
                    "follow_up": "优先级排序是怎样的？",
                    "examples": ["角色图 > 表情包 > 文创设计", "三视图 > 动作图 > 动态图"]
                }
            ],
            "商业化": [
                {
                    "question": "IP的商业化方向和变现路径？",
                    "follow_up": "短期和长期的商业化计划？",
                    "examples": ["表情包付费下载", "文创产品销售", "品牌授权合作"]
                },
                {
                    "question": "对IP的扩展性和可持续性有什么考虑？",
                    "follow_up": "未来可能的发展方向？",
                    "examples": ["系列化角色开发", "故事内容扩展", "跨平台运营"]
                }
            ]
        }
    
    def load_creative_types(self) -> Dict[str, Dict[str, Any]]:
        """加载创意类型特征"""
        return {
            "角色IP": {
                "priority": ["创意概念", "风格调性", "目标用户"],
                "special_questions": ["角色性格设定", "角色背景故事", "角色关系网络"]
            },
            "品牌IP": {
                "priority": ["商业化", "应用场景", "目标用户"],
                "special_questions": ["品牌价值观", "品牌识别元素", "品牌传播策略"]
            },
            "内容IP": {
                "priority": ["创意概念", "应用场景", "商业化"],
                "special_questions": ["内容形式", "更新频率", "互动方式"]
            },
            "文创IP": {
                "priority": ["商业化", "应用场景", "风格调性"],
                "special_questions": ["产品类型", "定价策略", "销售渠道"]
            }
        }
    
    def analyze_creative_input(self, user_input: str) -> Dict[str, Any]:
        """分析用户创意输入"""
        analysis = {
            "detected_type": "通用IP",
            "key_themes": [],
            "specificity_score": 0,
            "missing_info": []
        }
        
        # 简单关键词检测
        keywords = {
            "角色IP": ["角色", "人物", "形象", "人设", "角色设计"],
            "品牌IP": ["品牌", "商标", "企业", "产品", "商业"],
            "内容IP": ["故事", "内容", "漫画", "动画", "视频"],
            "文创IP": ["文创", "周边", "产品", "商品", "衍生品"]
        }
        
        for ip_type, words in keywords.items():
            for word in words:
                if word in user_input:
                    analysis["detected_type"] = ip_type
                    break
        
        # 提取关键主题
        theme_keywords = ["赛博", "古风", "可爱", "科技", "奇幻", "现实", "未来", "复古"]
        for theme in theme_keywords:
            if theme in user_input:
                analysis["key_themes"].append(theme)
        
        # 计算详细度评分
        word_count = len(user_input.split())
        if word_count > 100:
            analysis["specificity_score"] = 3  # 非常详细
        elif word_count > 50:
            analysis["specificity_score"] = 2  # 详细
        elif word_count > 20:
            analysis["specificity_score"] = 1  # 一般
        else:
            analysis["specificity_score"] = 0  # 简略
        
        return analysis
    
    def generate_questions(self, user_input: str, analysis: Dict[str, Any]) -> List[Dict]:
        """基于分析结果生成提问问题"""
        questions = []
        
        # 确定创意类型
        ip_type = analysis["detected_type"]
        creative_config = self.creative_types.get(ip_type, self.creative_types["角色IP"])
        
        # 按优先级添加问题
        for category in creative_config["priority"]:
            if category in self.question_templates:
                for template in self.question_templates[category][:2]:  # 每个类别取前2个
                    question = {
                        "category": category,
                        "question": template["question"],
                        "follow_up": template["follow_up"],
                        "examples": template["examples"]
                    }
                    questions.append(question)
        
        # 添加特殊问题
        for special_q in creative_config.get("special_questions", [])[:2]:
            question = {
                "category": "特殊需求",
                "question": special_q,
                "follow_up": f"关于{special_q}，有什么具体的要求或想法？",
                "examples": []
            }
            questions.append(question)
        
        # 根据详细度调整问题数量
        if analysis["specificity_score"] < 1:  # 简略输入，需要更多澄清
            questions = questions[:6]  # 取前6个关键问题
        elif analysis["specificity_score"] < 2:  # 一般输入
            questions = questions[:8]  # 取前8个问题
        else:  # 详细输入
            questions = questions[:10]  # 取前10个问题
        
        return questions
    
    def format_questions_for_display(self, questions: List[Dict]) -> str:
        """格式化问题用于显示"""
        output = "基于您的创意，我需要确认以下关键点：\n\n"
        
        for i, q in enumerate(questions, 1):
            output += f"{i}. **{q['category']}**: {q['question']}\n"
            
            if q['examples']:
                examples_str = "、".join(q['examples'])
                output += f"   示例参考：{examples_str}\n"
            
            output += "\n"
        
        output += "请逐一回答这些问题，我会基于您的回答生成更精准的角色图。\n"
        output += "如果您对某个问题不确定，可以先跳过，我会根据已有信息生成。"
        
        return output
    
    def process_user_answers(self, questions: List[Dict], answers: Dict[str, str]) -> Dict[str, Any]:
        """处理用户回答，生成需求摘要"""
        summary = {
            "confirmed_categories": {},
            "missing_categories": [],
            "specific_details": {},
            "generation_parameters": {}
        }
        
        for q in questions:
            category = q['category']
            question_key = q['question'][:30]  # 用问题前30字符作为key
            
            if question_key in answers and answers[question_key].strip():
                answer = answers[question_key].strip()
                
                # 记录确认的信息
                if category not in summary["confirmed_categories"]:
                    summary["confirmed_categories"][category] = []
                summary["confirmed_categories"][category].append({
                    "question": q['question'],
                    "answer": answer
                })
                
                # 提取生成参数
                self.extract_generation_parameters(category, answer, summary["generation_parameters"])
                
                # 记录具体细节
                if len(answer) > 20:  # 较详细的回答
                    key = f"{category}_detail_{len(summary['specific_details'])}"
                    summary["specific_details"][key] = answer
            else:
                if category not in summary["missing_categories"]:
                    summary["missing_categories"].append(category)
        
        return summary
    
    def extract_generation_parameters(self, category: str, answer: str, params: Dict):
        """从回答中提取生成参数"""
        # 风格相关参数
        if category == "风格调性":
            style_keywords = {
                "赛博": "cyberpunk",
                "古风": "ancient_chinese",
                "可爱": "cute",
                "科技": "tech",
                "简约": "minimalist",
                "复古": "retro"
            }
            
            for keyword, param_value in style_keywords.items():
                if keyword in answer:
                    params["style"] = param_value
                    break
        
        # 色彩相关参数
        if category == "风格调性" or "色彩" in answer:
            color_keywords = {
                "冷色调": "cool_tone",
                "暖色调": "warm_tone", 
                "霓虹": "neon",
                "马卡龙": "pastel",
                "黑白": "monochrome"
            }
            
            for keyword, param_value in color_keywords.items():
                if keyword in answer:
                    params["color_scheme"] = param_value
                    break
        
        # 应用场景参数
        if category == "应用场景":
            platform_keywords = {
                "表情包": "sticker",
                "小红书": "red_note", 
                "游戏": "game",
                "文创": "cultural_creative"
            }
            
            for keyword, param_value in platform_keywords.items():
                if keyword in answer:
                    if "platforms" not in params:
                        params["platforms"] = []
                    params["platforms"].append(param_value)

def main():
    """主函数 - 测试智能提问引擎"""
    print("=== 智能提问引擎测试 ===\n")
    
    # 创建提问引擎
    engine = IntelligentQuestionnaire()
    
    # 测试用户输入
    test_inputs = [
        "我想做一个赛博朋克风格的猫娘IP",
        "需要设计一个品牌吉祥物，用于产品包装",
        "创作一个关于未来垃圾分类的科普IP"
    ]
    
    for i, user_input in enumerate(test_inputs, 1):
        print(f"测试用例 {i}: {user_input}")
        print("-" * 50)
        
        # 分析创意输入
        analysis = engine.analyze_creative_input(user_input)
        print(f"检测到的类型: {analysis['detected_type']}")
        print(f"关键主题: {analysis['key_themes']}")
        print(f"详细度评分: {analysis['specificity_score']}")
        
        # 生成问题
        questions = engine.generate_questions(user_input, analysis)
        formatted = engine.format_questions_for_display(questions)
        
        print("\n生成的问题:")
        print(formatted)
        
        # 模拟用户回答
        print("\n模拟用户回答处理...")
        answers = {
            "请详细描述您的IP创意核心概念": "一个生活在赛博都市的猫娘，白天是程序员，晚上是黑客",
            "期望的视觉风格和情感基调是什么？": "赛博朋克风格，带点可爱元素，冷色调为主",
            "IP的主要应用场景和平台是什么？": "主要用于微信表情包和小红书内容"
        }
        
        summary = engine.process_user_answers(questions, answers)
        print(f"确认的类别: {list(summary['confirmed_categories'].keys())}")
        print(f"缺失的类别: {summary['missing_categories']}")
        print(f"生成参数: {summary['generation_parameters']}")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()