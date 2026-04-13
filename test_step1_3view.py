#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 1测试：生成三视图
"""

import os
import sys
import base64
from pathlib import Path

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 导入Wan-skills集成工具
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))
from wan_skills_integrated import WanSkillsIntegrated

def main():
    print("=== Step 1：生成三视图测试 ===")
    
    # 用户上传的图片路径
    image_path = "C:/Users/User/.openclaw/media/inbound/9dbf3fb9-6ea5-4415-984a-c4786e8e90eb.jpg"
    print(f"输入图片路径: {image_path}")
    
    # 初始化适配器
    wan = WanSkillsIntegrated()
    
    # 读取图片并转换为Base64
    with open(image_path, "rb") as f:
        image_data = f.read()
    base64_data = base64.b64encode(image_data).decode("utf-8")
    image_url = f"data:image/jpeg;base64,{base64_data}"
    print(f"Base64长度: {len(base64_data)} 字符")
    
    # 三视图提示词
    prompt = """-modeling-sheet

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
        *   **背景**：统一使用上述定义的**白底+浅灰网格线**。"""
    
    print(f"提示词长度: {len(prompt)} 字符")
    print("正在调用万相API生成三视图...（预计耗时30-60秒）")
    
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
        import requests
        response = requests.get(image_url)
        output_path = "./output/test_3view_giraffe.jpg"
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"图片已保存到: {output_path}")
        
        # 返回结果
        print("=== Step 1执行完成 ===")
        return output_path
    else:
        print("生成失败！")
        return None

if __name__ == "__main__":
    main()
