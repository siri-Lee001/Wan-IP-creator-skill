#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
万相IP技能配置验证脚本
"""

import os
import sys
import json

def validate_config():
    """验证技能配置"""
    print("=" * 60)
    print("万相IP技能配置验证")
    print("=" * 60)
    
    # 检查配置文件
    config_files = [
        "wanxiang_api_optimized.py",
        "smart_image_url_getter.py",
        "real_workflow.py"
    ]
    
    print("\n[1. 检查配置文件存在性]")
    for file in config_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (缺失)")
    
    # 读取主要配置
    print("\n[2. 读取API配置]")
    try:
        with open("wanxiang_api_optimized.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 提取配置
        import re
        
        # API密钥
        api_key_match = re.search(r'DASHSCOPE_API_KEY = "(.*?)"', content)
        if api_key_match:
            key = api_key_match.group(1)
            masked = key[:8] + "*" * (len(key)-12) + key[-4:] if len(key) > 12 else "***"
            print(f"  ✅ API密钥: {masked}")
        else:
            print("  ❌ 未找到API密钥")
        
        # 图片模型
        image_model_match = re.search(r'QWEN_IMAGE_MODEL = "(.*?)"', content)
        if image_model_match:
            print(f"  ✅ 图片模型: {image_model_match.group(1)}")
        else:
            print("  ❌ 未找到图片模型")
        
        # 视频模型
        video_model_match = re.search(r'WANXIANG_VIDEO_MODEL = "(.*?)"', content)
        if video_model_match:
            print(f"  ✅ 视频模型: {video_model_match.group(1)}")
        else:
            print("  ❌ 未找到视频模型")
        
        # 固定参数
        size_match = re.search(r'IMAGE_SIZE = "(.*?)"', content)
        if size_match:
            print(f"  ✅ 图片尺寸: {size_match.group(1)}")
        
        duration_match = re.search(r'VIDEO_DURATION = (\d+)', content)
        if duration_match:
            print(f"  ✅ 视频时长: {duration_match.group(1)}秒")
        
        resolution_match = re.search(r'VIDEO_RESOLUTION = "(.*?)"', content)
        if resolution_match:
            print(f"  ✅ 视频分辨率: {resolution_match.group(1)}")
        
        watermark_match = re.search(r'VIDEO_WATERMARK = (True|False)', content)
        if watermark_match:
            watermark = "无水印" if watermark_match.group(1) == "False" else "有水印"
            print(f"  ✅ 水印设置: {watermark}")
        
        # API端点
        image_url_match = re.search(r'self\.image_url = "(.*?)"', content)
        if image_url_match:
            print(f"  ✅ 图片API端点: {image_url_match.group(1)}")
        
        video_url_match = re.search(r'self\.video_url = "(.*?)"', content)
        if video_url_match:
            print(f"  ✅ 视频API端点: {video_url_match.group(1)}")
            
    except Exception as e:
        print(f"  ❌ 读取配置失败: {e}")
    
    print("\n[3. 检查智能获取器]")
    try:
        with open("smart_image_url_getter.py", "r", encoding="utf-8") as f:
            getter_content = f.read()
        
        # 检查关键函数
        functions = [
            "get_image_url",
            "_auto_strategy",
            "_url_only_strategy",
            "_base64_only_strategy",
            "_cdn_only_strategy",
            "_upload_to_free_cdn"
        ]
        
        for func in functions:
            if f"def {func}" in getter_content:
                print(f"  ✅ {func}()")
            else:
                print(f"  ❌ {func}() (缺失)")
                
    except Exception as e:
        print(f"  ❌ 检查智能获取器失败: {e}")
    
    print("\n[4. 检查工作流脚本]")
    try:
        with open("real_workflow.py", "r", encoding="utf-8") as f:
            workflow_content = f.read()
        
        # 检查导入
        imports = [
            "wanxiang_api",
            "generate_image_wanxiang",
            "generate_video_wanxiang"
        ]
        
        for imp in imports:
            if imp in workflow_content:
                print(f"  ✅ 导入: {imp}")
            else:
                print(f"  ❌ 导入: {imp} (缺失)")
                
    except Exception as e:
        print(f"  ❌ 检查工作流脚本失败: {e}")
    
    print("\n" + "=" * 60)
    print("配置验证完成")
    print("=" * 60)

if __name__ == "__main__":
    # 切换到脚本目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    validate_config()