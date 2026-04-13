#!/usr/bin/env python3
# 万相IP技能 - 第一步：生成角色三视图
# 输入：单角色图片
# 输出：角色三视图

import os
import sys
import time
from pathlib import Path

# 添加scripts目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/scripts')

from wan_skills_integrated import WanSkillsIntegrated

def main():
    print("=" * 60)
    print("万相IP技能 - 第一步：生成角色三视图")
    print("=" * 60)
    
    # 输入图片路径
    input_image_path = r"C:\Users\User\.openclaw\media\inbound\d3e6712e-0e04-4348-a240-a6f2a028ce6f.jpg"
    
    if not os.path.exists(input_image_path):
        print(f"错误：输入图片不存在: {input_image_path}")
        return
    
    print(f"输入图片: {input_image_path}")
    print(f"图片大小: {os.path.getsize(input_image_path) / 1024:.1f} KB")
    
    # 初始化Wan-skills适配器
    print("\n初始化Wan-skills适配器...")
    adapter = WanSkillsIntegrated()
    
    # 生成角色三视图的提示词
    prompt = """生成这个兽人战士角色的三视图（正面、侧面、背面）。
    
角色特征：
1. 强壮有力的兽人战士
2. 头上有角，面部有兽人特征
3. 身穿战斗装备，有护甲
4. 肌肉发达，战斗姿态
    
要求：
1. 生成标准的三视图布局：正面在中间，侧面在两边
2. 保持角色核心特征一致
3. 高质量2K分辨率
4. 无水印
    
请生成这个兽人战士角色的完整三视图。"""
    
    print(f"\n提示词长度: {len(prompt)} 字符")
    print(f"模型: wan2.7-image")
    print(f"分辨率: 2K")
    print(f"水印: 无水印")
    
    # 调用API生成图片
    print("\n开始调用Wan-skills API生成角色三视图...")
    print("注意：这是异步调用，需要轮询任务状态")
    
    try:
        # 调用Wan-skills生成图片
        image_urls = adapter.generate_image(
            prompt=prompt,
            image_path=input_image_path,
            size="2K",
            num_images=1,
            thinking_mode=True
        )
        
        if image_urls:
            print(f"\n✅ 图片生成成功！")
            print(f"获取到 {len(image_urls)} 张图片")
            
            # 下载第一张图片
            output_path = r"C:\Users\User\.openclaw\workspace\skills\siri-ip-series-wanxiang\output\step1_character_3view.jpg"
            saved_path = adapter.download_image(image_urls[0], output_path)
            
            if saved_path and os.path.exists(saved_path):
                print(f"✅ 图片已保存到: {saved_path}")
                print(f"文件大小: {os.path.getsize(saved_path) / 1024:.1f} KB")
                
                # 返回成功信息
                return {
                    "status": "success",
                    "step": "step1_character_3view",
                    "output_path": saved_path,
                    "message": "角色三视图生成成功"
                }
            else:
                print("❌ 图片下载失败")
                return {
                    "status": "error",
                    "step": "step1_character_3view",
                    "message": "图片下载失败"
                }
        else:
            print("❌ 图片生成失败，未获取到图片URL")
            return {
                "status": "error",
                "step": "step1_character_3view",
                "message": "未获取到图片URL"
            }
            
    except Exception as e:
        print(f"❌ API调用失败: {str(e)}")
        return {
            "status": "error",
            "step": "step1_character_3view",
            "message": f"API调用失败: {str(e)}"
        }

if __name__ == "__main__":
    result = main()
    print("\n" + "=" * 60)
    if result["status"] == "success":
        print("✅ 第一步执行完成！")
        print(f"输出文件: {result['output_path']}")
    else:
        print("❌ 第一步执行失败")
        print(f"错误信息: {result['message']}")
    print("=" * 60)