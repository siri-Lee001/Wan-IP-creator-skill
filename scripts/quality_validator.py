#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
质量验证器 - 验证IP创建各步骤的输出质量
"""

import json
import os
import re
from typing import Dict, List, Any, Tuple
from datetime import datetime

class QualityValidator:
    """质量验证器"""
    
    def __init__(self):
        self.quality_standards = self.load_quality_standards()
        self.validation_rules = self.load_validation_rules()
        
    def load_quality_standards(self) -> Dict[str, Dict[str, Any]]:
        """加载质量标准"""
        return {
            "角色建模": {
                "dimensions": ["一致性", "创意性", "技术性", "商业化"],
                "weights": [0.3, 0.3, 0.2, 0.2],
                "thresholds": {
                    "excellent": 4.5,
                    "good": 4.0,
                    "average": 3.5,
                    "poor": 3.0
                }
            },
            "三视图": {
                "dimensions": ["准确性", "完整性", "专业性", "实用性"],
                "weights": [0.4, 0.3, 0.2, 0.1],
                "thresholds": {
                    "excellent": 4.5,
                    "good": 4.0,
                    "average": 3.5,
                    "poor": 3.0
                }
            },
            "风格转换": {
                "dimensions": ["风格一致性", "创意表达", "技术实现", "应用适配"],
                "weights": [0.3, 0.3, 0.2, 0.2],
                "thresholds": {
                    "excellent": 4.5,
                    "good": 4.0,
                    "average": 3.5,
                    "poor": 3.0
                }
            },
            "动作延展": {
                "dimensions": ["动作自然度", "表情丰富度", "构图合理性", "应用价值"],
                "weights": [0.3, 0.3, 0.2, 0.2],
                "thresholds": {
                    "excellent": 4.5,
                    "good": 4.0,
                    "average": 3.5,
                    "poor": 3.0
                }
            },
            "文创设计": {
                "dimensions": ["设计美感", "实用性", "生产可行性", "商业价值"],
                "weights": [0.3, 0.3, 0.2, 0.2],
                "thresholds": {
                    "excellent": 4.5,
                    "good": 4.0,
                    "average": 3.5,
                    "poor": 3.0
                }
            },
            "表情包": {
                "dimensions": ["表情夸张度", "识别度", "传播性", "平台适配"],
                "weights": [0.3, 0.3, 0.2, 0.2],
                "thresholds": {
                    "excellent": 4.5,
                    "good": 4.0,
                    "average": 3.5,
                    "poor": 3.0
                }
            },
            "动态化": {
                "dimensions": ["动作流畅度", "节奏控制", "技术实现", "用户体验"],
                "weights": [0.4, 0.3, 0.2, 0.1],
                "thresholds": {
                    "excellent": 4.5,
                    "good": 4.0,
                    "average": 3.5,
                    "poor": 3.0
                }
            }
        }
    
    def load_validation_rules(self) -> Dict[str, List[Dict[str, Any]]]:
        """加载验证规则"""
        return {
            "角色建模": [
                {
                    "rule": "角色特征一致性",
                    "description": "角色特征与需求描述一致",
                    "check_method": "text_analysis",
                    "weight": 0.3
                },
                {
                    "rule": "风格统一性",
                    "description": "视觉风格统一协调",
                    "check_method": "style_check",
                    "weight": 0.3
                },
                {
                    "rule": "技术实现质量",
                    "description": "渲染质量和技术实现达标",
                    "check_method": "technical_check",
                    "weight": 0.2
                },
                {
                    "rule": "商业化潜力",
                    "description": "具备商业化应用价值",
                    "check_method": "commercial_check",
                    "weight": 0.2
                }
            ],
            "三视图": [
                {
                    "rule": "视图准确性",
                    "description": "三视图比例和结构准确",
                    "check_method": "accuracy_check",
                    "weight": 0.4
                },
                {
                    "rule": "视图完整性",
                    "description": "包含所有必要视图",
                    "check_method": "completeness_check",
                    "weight": 0.3
                },
                {
                    "rule": "专业标准符合",
                    "description": "符合专业设计标准",
                    "check_method": "standard_check",
                    "weight": 0.2
                },
                {
                    "rule": "实际应用价值",
                    "description": "具有实际应用价值",
                    "check_method": "utility_check",
                    "weight": 0.1
                }
            ]
        }
    
    def validate_step(self, step_type: str, step_data: Dict[str, Any]) -> Dict[str, Any]:
        """验证单个步骤"""
        if step_type not in self.quality_standards:
            return self.create_error_result(f"未知步骤类型: {step_type}")
        
        standards = self.quality_standards[step_type]
        validation_result = {
            "step_type": step_type,
            "validation_time": datetime.now().isoformat(),
            "dimension_scores": {},
            "rule_validations": [],
            "overall_score": 0,
            "quality_level": "unknown",
            "pass_fail": False,
            "issues": [],
            "recommendations": []
        }
        
        # 计算维度分数
        dimension_scores = {}
        for dimension in standards["dimensions"]:
            score = self.evaluate_dimension(step_type, dimension, step_data)
            dimension_scores[dimension] = score
        
        validation_result["dimension_scores"] = dimension_scores
        
        # 计算总体分数
        overall_score = self.calculate_overall_score(dimension_scores, standards["weights"])
        validation_result["overall_score"] = overall_score
        
        # 确定质量等级
        quality_level = self.determine_quality_level(overall_score, standards["thresholds"])
        validation_result["quality_level"] = quality_level
        
        # 确定通过/失败
        validation_result["pass_fail"] = overall_score >= standards["thresholds"]["poor"]
        
        # 执行规则验证
        if step_type in self.validation_rules:
            rule_results = self.validate_rules(step_type, step_data)
            validation_result["rule_validations"] = rule_results
            
            # 从规则验证中提取问题和建议
            for rule_result in rule_results:
                if not rule_result.get("passed", True):
                    validation_result["issues"].append({
                        "rule": rule_result["rule"],
                        "issue": rule_result.get("issue", "规则验证失败"),
                        "severity": rule_result.get("severity", "medium")
                    })
                
                if "recommendation" in rule_result:
                    validation_result["recommendations"].append(rule_result["recommendation"])
        
        # 如果没有规则验证，生成通用建议
        if not validation_result["recommendations"]:
            validation_result["recommendations"] = self.generate_general_recommendations(
                step_type, overall_score, quality_level
            )
        
        return validation_result
    
    def evaluate_dimension(self, step_type: str, dimension: str, step_data: Dict[str, Any]) -> float:
        """评估单个维度"""
        # 基础评分逻辑
        base_score = 4.0  # 基础分4分
        
        # 根据步骤类型和维度调整
        adjustment_factors = {
            "角色建模": {
                "一致性": self.check_consistency(step_data),
                "创意性": self.check_creativity(step_data),
                "技术性": self.check_technical_quality(step_data),
                "商业化": self.check_commercial_potential(step_data)
            },
            "三视图": {
                "准确性": self.check_accuracy(step_data),
                "完整性": self.check_completeness(step_data),
                "专业性": self.check_professionalism(step_data),
                "实用性": self.check_utility(step_data)
            }
        }
        
        # 获取调整因子
        if step_type in adjustment_factors and dimension in adjustment_factors[step_type]:
            adjustment = adjustment_factors[step_type][dimension]
        else:
            adjustment = 0.0
        
        # 计算最终分数
        final_score = base_score + adjustment
        
        # 限制在1-5分之间
        return max(1.0, min(5.0, final_score))
    
    def check_consistency(self, step_data: Dict[str, Any]) -> float:
        """检查一致性"""
        consistency_score = 0.0
        
        # 检查需求一致性
        if "requirements" in step_data and "output" in step_data:
            requirements = step_data["requirements"]
            output = step_data["output"]
            
            # 简单关键词匹配
            requirement_keywords = self.extract_keywords(str(requirements))
            output_keywords = self.extract_keywords(str(output))
            
            match_count = len(set(requirement_keywords) & set(output_keywords))
            total_count = len(set(requirement_keywords) | set(output_keywords))
            
            if total_count > 0:
                consistency_score = match_count / total_count * 2.0  # 最多加2分
        
        return consistency_score - 1.0  # 调整为-1到+1
    
    def check_creativity(self, step_data: Dict[str, Any]) -> float:
        """检查创意性"""
        creativity_score = 0.0
        
        if "output" in step_data:
            output = str(step_data["output"])
            
            # 检查创意关键词
            creative_keywords = ["独特", "创新", "新颖", "突破", "创意", "原创"]
            creative_count = sum(1 for keyword in creative_keywords if keyword in output)
            
            creativity_score = min(creative_count * 0.3, 1.0)  # 最多加1分
        
        return creativity_score - 0.5  # 调整为-0.5到+0.5
    
    def check_technical_quality(self, step_data: Dict[str, Any]) -> float:
        """检查技术质量"""
        technical_score = 0.0
        
        if "technical_details" in step_data:
            tech_details = step_data["technical_details"]
            
            # 检查技术参数
            tech_params = ["分辨率", "渲染", "材质", "光影", "细节"]
            param_count = sum(1 for param in tech_params if param in str(tech_details))
            
            technical_score = min(param_count * 0.2, 1.0)  # 最多加1分
        
        return technical_score - 0.5  # 调整为-0.5到+0.5
    
    def check_commercial_potential(self, step_data: Dict[str, Any]) -> float:
        """检查商业化潜力"""
        commercial_score = 0.0
        
        if "application_scenarios" in step_data:
            scenarios = step_data["application_scenarios"]
            
            # 检查应用场景数量
            if isinstance(scenarios, list):
                scenario_count = len(scenarios)
                commercial_score = min(scenario_count * 0.2, 1.0)  # 最多加1分
        
        return commercial_score - 0.5  # 调整为-0.5到+0.5
    
    def check_accuracy(self, step_data: Dict[str, Any]) -> float:
        """检查准确性"""
        return 0.0  # 简化实现
    
    def check_completeness(self, step_data: Dict[str, Any]) -> float:
        """检查完整性"""
        return 0.0  # 简化实现
    
    def check_professionalism(self, step_data: Dict[str, Any]) -> float:
        """检查专业性"""
        return 0.0  # 简化实现
    
    def check_utility(self, step_data: Dict[str, Any]) -> float:
        """检查实用性"""
        return 0.0  # 简化实现
    
    def extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简单的中文关键词提取
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]{2,4}')
        keywords = chinese_pattern.findall(text)
        
        # 去重
        return list(set(keywords))
    
    def calculate_overall_score(self, dimension_scores: Dict[str, float], weights: List[float]) -> float:
        """计算总体分数"""
        if not dimension_scores:
            return 0.0
        
        dimensions = list(dimension_scores.keys())
        
        # 确保权重和维度数量匹配
        if len(weights) != len(dimensions):
            weights = [1.0 / len(dimensions)] * len(dimensions)
        
        # 计算加权平均
        weighted_sum = 0.0
        weight_sum = 0.0
        
        for i, dimension in enumerate(dimensions):
            weight = weights[i] if i < len(weights) else 1.0 / len(dimensions)
            score = dimension_scores[dimension]
            
            weighted_sum += score * weight
            weight_sum += weight
        
        overall_score = weighted_sum / weight_sum if weight_sum > 0 else 0.0
        
        return round(overall_score, 2)
    
    def determine_quality_level(self, score: float, thresholds: Dict[str, float]) -> str:
        """确定质量等级"""
        if score >= thresholds.get("excellent", 4.5):
            return "excellent"
        elif score >= thresholds.get("good", 4.0):
            return "good"
        elif score >= thresholds.get("average", 3.5):
            return "average"
        elif score >= thresholds.get("poor", 3.0):
            return "poor"
        else:
            return "unacceptable"
    
    def validate_rules(self, step_type: str, step_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """验证规则"""
        if step_type not in self.validation_rules:
            return []
        
        rules = self.validation_rules[step_type]
        results = []
        
        for rule_config in rules:
            rule_name = rule_config["rule"]
            check_method = rule_config["check_method"]
            
            # 执行检查
            passed, details = self.execute_rule_check(check_method, step_data)
            
            result = {
                "rule": rule_name,
                "description": rule_config["description"],
                "passed": passed,
                "weight": rule_config["weight"],
                "check_method": check_method,
                "checked_at": datetime.now().isoformat()
            }
            
            if not passed and "issue" in details:
                result["issue"] = details["issue"]
                result["severity"] = details.get("severity", "medium")
            
            if "recommendation" in details:
                result["recommendation"] = details["recommendation"]
            
            results.append(result)
        
        return results
    
    def execute_rule_check(self, check_method: str, step_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """执行规则检查"""
        # 简化实现，实际使用时需要根据具体检查方法实现
        if check_method == "text_analysis":
            return self.text_analysis_check(step_data)
        elif check_method == "style_check":
            return self.style_check(step_data)
        elif check_method == "technical_check":
            return self.technical_check(step_data)
        elif check_method == "commercial_check":
            return self.commercial_check(step_data)
        else:
            # 默认检查
            return True, {"note": f"检查方法 {check_method} 未实现，默认通过"}
    
    def text_analysis_check(self, step_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """文本分析检查"""
        if "prompt" not in step_data or "output_description" not in step_data:
            return False, {
                "issue": "缺少必要的文本数据",
                "severity": "high",
                "recommendation": "提供完整的提示词和输出描述"
            }
        
        prompt = str(step_data["prompt"])
        output = str(step_data["output_description"])
        
        # 简单的一致性检查
        prompt_keywords = self.extract_keywords(prompt)
        output_keywords = self.extract_keywords(output)
        
        match_count = len(set(prompt_keywords) & set(output_keywords))
        
        if match_count < 3:  # 至少匹配3个关键词
            return False, {
                "issue": "输出与提示词一致性较低",
                "severity": "medium",
                "recommendation": "优化提示词或重新生成以更好匹配需求"
            }
        
        return True, {"match_keywords": match_count}
    
    def style_check(self, step_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """风格检查"""
        if "style_requirements" not in step_data:
            return True, {"note": "未指定风格要求，跳过风格检查"}
        
        return True, {"style_consistent": True}
    
    def technical_check(self, step_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """技术检查"""
        if "technical_specs" not in step_data:
            return True, {"note": "未指定技术规格，跳过技术检查"}
        
        return True, {"technical_adequate": True}
    
    def commercial_check(self, step_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """商业化检查"""
        if "commercial_potential" not in step_data:
            return True, {"note": "未指定商业化要求，跳过商业化检查"}
        
        return True, {"commercial_viable": True}
    
    def generate_general_recommendations(self, step_type: str, score: float, quality_level: str) -> List[str]:
        """生成通用建议"""
        recommendations = []
        
        # 基于分数和质量等级的建议
        if quality_level == "excellent":
            recommendations.append(f"{step_type}质量优秀，可直接用于商业化应用")
            recommendations.append("建议保持当前质量标准，可考虑申请设计专利")
        
        elif quality_level == "good":
            recommendations.append(f"{step_type}质量良好，适合大多数应用场景")
            recommendations.append("建议进行小范围测试，收集用户反馈")
        
        elif quality_level == "average":
            recommendations.append(f"{step_type}质量一般，建议进行优化")
            recommendations.append("可考虑重新生成或调整生成参数")
        
        elif quality_level == "poor":
            recommendations.append(f"{step_type}质量较差，需要重新评估")
            recommendations.append("建议重新分析需求，调整生成策略")
        
        else:  # unacceptable
            recommendations.append(f"{step_type}质量不合格，必须重新生成")
            recommendations.append("建议与需求方重新确认需求细节")
        
        # 基于步骤类型的特定建议
        type_specific = {
            "角色建模": [
                "确保角色特征清晰明确",
                "考虑角色的扩展性和系列化潜力"
            ],
            "三视图": [
                "检查视图比例和结构准确性",
                "确保视图符合生产制造标准"
            ],
            "风格转换": [
                "保持风格转换的一致性",
                "考虑目标平台的技术限制"
            ],
            "动作延展": [
                "确保动作自然流畅",
                "考虑动作的实用性和应用场景"
            ],
            "文创设计": [
                "检查产品的生产可行性",
                "考虑成本控制和市场定价"
            ],
            "表情包": [
                "确保表情夸张且易于识别",
                "考虑不同平台的表情包规范"
            ],
            "动态化": [
                "检查动画的流畅度和循环",
                "考虑文件大小和加载性能"
            ]
        }
        
        if step_type in type_specific:
            recommendations.extend(type_specific[step_type][:2])
        
        return recommendations
    
    def create_error_result(self, error_message: str) -> Dict[str, Any]:
        """创建错误结果"""
        return {
            "step_type": "unknown",
            "validation_time": datetime.now().isoformat(),
            "error": error_message,
            "overall_score": 0,
            "quality_level": "error",
            "pass_fail": False,
            "issues": [{"issue": error_message, "severity": "high"}],
            "recommendations": ["检查步骤类型和数据格式", "重新运行验证"]
        }
    
    def validate_workflow(self, workflow_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """验证完整工作流"""
        workflow_validation = {
            "workflow_id": f"validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "validation_time": datetime.now().isoformat(),
            "step_validations": [],
            "overall_score": 0,
            "workflow_quality": "unknown",
            "passed_steps": 0,
            "failed_steps": 0,
            "critical_issues": [],
            "workflow_recommendations": []
        }
        
        step_scores = []
        
        for step_result in workflow_results:
            if "step_type" in step_result and "step_data" in step_result:
                step_type = step_result["step_type"]
                step_data = step_result["step_data"]
                
                # 验证单个步骤
                step_validation = self.validate_step(step_type, step_data)
                workflow_validation["step_validations"].append(step_validation)
                
                # 记录分数
                step_scores.append(step_validation["overall_score"])
                
                # 统计通过/失败
                if step_validation["pass_fail"]:
                    workflow_validation["passed_steps"] += 1
                else:
                    workflow_validation["failed_steps"] += 1
                
                # 收集严重问题
                for issue in step_validation.get("issues", []):
                    if issue.get("severity") == "high":
                        workflow_validation["critical_issues"].append({
                            "step": step_type,
                            "issue": issue["issue"]
                        })
        
        # 计算工作流总体分数
        if step_scores:
            workflow_validation["overall_score"] = round(sum(step_scores) / len(step_scores), 2)
            
            # 确定工作流质量
            if workflow_validation["overall_score"] >= 4.5:
                workflow_validation["workflow_quality"] = "excellent"
            elif workflow_validation["overall_score"] >= 4.0:
                workflow_validation["workflow_quality"] = "good"
            elif workflow_validation["overall_score"] >= 3.5:
                workflow_validation["workflow_quality"] = "average"
            elif workflow_validation["overall_score"] >= 3.0:
                workflow_validation["workflow_quality"] = "poor"
            else:
                workflow_validation["workflow_quality"] = "unacceptable"
        
        # 生成工作流建议
        workflow_validation["workflow_recommendations"] = self.generate_workflow_recommendations(
            workflow_validation
        )
        
        return workflow_validation
    
    def generate_workflow_recommendations(self, workflow_validation: Dict[str, Any]) -> List[str]:
        """生成工作流建议"""
        recommendations = []
        
        overall_score = workflow_validation.get("overall_score", 0)
        workflow_quality = workflow_validation.get("workflow_quality", "unknown")
        failed_steps = workflow_validation.get("failed_steps", 0)
        critical_issues = workflow_validation.get("critical_issues", [])
        
        # 基于总体质量的建议
        if workflow_quality == "excellent":
            recommendations.append("工作流质量优秀，所有步骤均达到高标准")
            recommendations.append("建议直接推进商业化，可考虑申请完整IP保护")
        
        elif workflow_quality == "good":
            recommendations.append("工作流质量良好，适合商业化应用")
            recommendations.append("建议进行市场测试，收集用户反馈")
        
        elif workflow_quality == "average":
            recommendations.append("工作流质量一般，建议优化关键步骤")
            recommendations.append("可考虑重新生成质量较低的步骤")
        
        elif workflow_quality == "poor":
            recommendations.append("工作流质量较差，需要系统性优化")
            recommendations.append("建议重新评估需求，调整生成策略")
        
        else:  # unacceptable
            recommendations.append("工作流质量不合格，必须重新执行")
            recommendations.append("建议与需求方重新确认所有需求")
        
        # 基于失败步骤的建议
        if failed_steps > 0:
            recommendations.append(f"有{failed_steps}个步骤验证失败，需要重点关注")
        
        # 基于严重问题的建议
        if critical_issues:
            recommendations.append(f"发现{len(critical_issues)}个严重问题，必须优先解决")
            for i, issue in enumerate(critical_issues[:3], 1):
                recommendations.append(f"  问题{i}: {issue['step']} - {issue['issue']}")
        
        # 通用建议
        recommendations.append("建议建立质量监控机制，定期评估输出质量")
        recommendations.append("可考虑建立质量数据库，积累质量评估经验")
        
        return recommendations

def main():
    """主函数 - 测试质量验证器"""
    print("=== 质量验证器测试 ===\n")
    
    # 创建验证器
    validator = QualityValidator()
    
    # 测试数据
    test_steps = [
        {
            "step_type": "角色建模",
            "step_data": {
                "requirements": "赛博朋克风格猫娘，机械义体，霓虹色彩",
                "output_description": "一个赛博朋克风格的猫娘角色，带有银色机械义体和蓝色霓虹灯光",
                "technical_details": "C4D渲染，PVC材质，2048x2048分辨率",
                "application_scenarios": ["游戏角色", "虚拟主播", "文创产品"]
            }
        },
        {
            "step_type": "三视图",
            "step_data": {
                "requirements": "标准三视图，正面侧面背面",
                "output_description": "角色三视图，包含正面、侧面、背面视角",
                "technical_details": "BLENDER建模，Octane渲染，32K分辨率"
            }
        }
    ]
    
    # 验证单个步骤
    print("验证单个步骤:")
    for i, step in enumerate(test_steps, 1):
        step_type = step["step_type"]
        step_data = step["step_data"]
        
        print(f"\n步骤{i}: {step_type}")
        validation_result = validator.validate_step(step_type, step_data)
        
        print(f"  总体分数: {validation_result['overall_score']}/5")
        print(f"  质量等级: {validation_result['quality_level']}")
        print(f"  通过/失败: {'通过' if validation_result['pass_fail'] else '失败'}")
        
        if validation_result["issues"]:
            print(f"  问题: {len(validation_result['issues'])}个")
        
        if validation_result["recommendations"]:
            print(f"  建议: {validation_result['recommendations'][0]}")
    
    # 验证完整工作流
    print("\n\n验证完整工作流:")
    workflow_validation = validator.validate_workflow(test_steps)
    
    print(f"工作流总体分数: {workflow_validation['overall_score']}/5")
    print(f"工作流质量: {workflow_validation['workflow_quality']}")
    print(f"通过步骤: {workflow_validation['passed_steps']}")
    print(f"失败步骤: {workflow_validation['failed_steps']}")
    
    if workflow_validation["critical_issues"]:
        print(f"严重问题: {len(workflow_validation['critical_issues'])}个")
    
    print("\n工作流建议:")
    for i, recommendation in enumerate(workflow_validation["workflow_recommendations"][:3], 1):
        print(f"{i}. {recommendation}")

if __name__ == "__main__":
    main()