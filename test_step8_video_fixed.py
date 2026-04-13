#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 8测试：动态短视频生成 - 修复版（直接使用阿里云公网URL）
"""

import os
import sys
import requests
import time
from pathlib import Path

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 导入Wan-skills集成工具
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))
from wan_skills_video import WanSkillsVideo

def main():
    print("=== Step 8：动态短视频生成（修复版） ===")
    
    # 直接使用之前生成的国潮风格图的阿里云公网URL（无需上传）
    image_url = "https://dashscope-7c2c.oss-accelerate.aliyuncs.com/1d/57/20260413/87c6cc91/0be46bae-54c5-4e1d-abf4-55ae1bc8d854_0.png?Expires=1776132597&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=Vq12zP8Fo9MewxUG1KsIL1YKs18%3D"
    print(f"使用公网图片URL: {image_url[:100]}...")
    
    # 初始化视频生成适配器
    wan_video = WanSkillsVideo()
    
    # 视频生成提示词
    prompt = "长颈鹿宝宝动态展示，可爱帅气动作，自然流畅的动态效果，头部微微转动，眼睛眨动，非常生动可爱"
    
    print(f"提示词长度: {len(prompt)} 字符")
    print("正在调用万相API生成动态短视频...（预计耗时60-120秒）")
    
    # 生成视频 - 固定参数：5秒 720P 无水印
    result = wan_video.generate_video(
        prompt=prompt,
        image_url=image_url,
        duration=5,
        resolution="720P"
    )
    
    if result:
        video_url = result
        print(f"生成成功！视频URL: {video_url}")
        
        # 下载视频
        output_dir = "C:/Users/User/.openclaw/workspace/skills/siri-ip-series-wanxiang/output"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "giraffe_dynamic_video.mp4")
        
        print("正在下载视频...")
        response = requests.get(video_url, timeout=120)
        response.raise_for_status()
        
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"视频已保存到: {output_path}")
        print(f"文件大小: {os.path.getsize(output_path)} 字节")
        
        # 返回结果
        print("=== Step 8执行完成 ===")
        return output_path
    else:
        print("生成失败！")
        return None

if __name__ == "__main__":
    main()
