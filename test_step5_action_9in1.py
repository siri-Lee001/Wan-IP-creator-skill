#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 5测试：动作延展九合一图
"""

import os
import sys
import base64
import requests
from pathlib import Path

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 导入Wan-skills集成工具
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))
from wan_skills_integrated import WanSkillsIntegrated

def main():
    print("=== Step 5：动作延展九合一图生成 ===")
    
    # 输入图片路径（修复版三视图）
    image_path = "C:/Users/User/.openclaw/workspace/skills/siri-ip-series-wanxiang/output/giraffe_3view_fixed_legs.jpg"
    print(f"输入图片路径: {image_path}")
    
    # 初始化适配器
    wan = WanSkillsIntegrated()
    
    # 读取图片并转换为Base64
    with open(image_path, "rb") as f:
        image_data = f.read()
    base64_data = base64.b64encode(image_data).decode("utf-8")
    image_url = f"data:image/jpeg;base64,{base64_data}"
    print(f"Base64长度: {len(base64_data)} 字符")
    
    # 动作延展九合一提示词
    prompt = """生成角色9种不同动作，排列成3×3九宫格布局：
1. 打招呼 2. 敬礼 3. 比心 4. 认真工作 5. 可爱pose
6. 挥手 7. 歪头 8. 点赞 9. 害羞

要求：单张大图，九宫格布局，每个动作清晰可辨，生成单一角色正面主体图，去掉三视图的多视图布局，只保留单个完整的角色，100%保留角色核心视觉特征。"""
    
    print(f"提示词长度: {len(prompt)} 字符")
    print("正在调用万相API生成动作延展九合一图...（预计耗时30-60秒）")
    
    # 生成图片
    result = wan.generate_image(
        prompt=prompt,
        image_url=image_url,
        size="1440*1440",
        num_images=1
    )
    
    if result and len(result) > 0:
        image_url = result[0]
        print(f"生成成功！图片URL: {image_url}")
        
        # 下载图片
        output_dir = "C:/Users/User/.openclaw/workspace/skills/siri-ip-series-wanxiang/output"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "giraffe_action_9in1.jpg")
        
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"图片已保存到: {output_path}")
        print(f"文件大小: {os.path.getsize(output_path)} 字节")
        
        # 返回结果
        print("=== Step 5执行完成 ===")
        return output_path
    else:
        print("生成失败！")
        return None

if __name__ == "__main__":
    main()
