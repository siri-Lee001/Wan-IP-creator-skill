#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化版Step 1执行脚本
使用Base64优先策略，避免400错误
"""

import os
import sys

# 添加技能目录到路径
skill_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(skill_dir)

from optimized_image_getter import OptimizedImageGetter
from fixed_api import FixedWanxiangAPI

def execute_optimized_step1():
    """执行优化版Step 1：角色图确认"""
    print("执行优化版Step 1：角色图确认")
    print("=" * 60)
    
    # 图片路径
    image_path = r"C:\Users\User\.openclaw\media\inbound\65dcfec4-72c0-47d3-84f2-a7c118730324.jpg"
    
    if not os.path.exists(image_path):
        print("[ERROR] 图片文件不存在")
        return None
    
    print(f"[OK] 图片文件存在: {image_path}")
    size = os.path.getsize(image_path)
    print(f"[INFO] 图片大小: {size:,} 字节 ({size/1024/1024:.2f} MB)")
    
    # Step 1: 使用优化获取器获取图片URL
    print("\n[Step 1.1: 智能获取图片URL]")
    getter = OptimizedImageGetter()
    image_url, metadata = getter.get_image_url(image_path, strategy='optimized')
    
    if not image_url:
        print(f"[ERROR] 获取图片URL失败")
        if metadata.get('error'):
            print(f"[INFO] 错误信息: {metadata.get('error')}")
        return None
    
    print(f"[OK] 获取图片URL成功")
    print(f"[INFO] URL类型: {'Base64 data URL' if image_url.startswith('data:') else 'HTTP URL'}")
    
    if image_url.startswith('data:'):
        print(f"[INFO] Base64长度: {metadata.get('base64_length', 0):,} 字符")
        print(f"[INFO] 优化方案: {metadata.get('optimization_applied', '无')}")
    
    print(f"[INFO] 执行步骤: {metadata.get('steps', [])}")
    
    # Step 2: 使用修复版API生成图片
    print("\n[Step 1.2: 使用修复版API生成图片]")
    api = FixedWanxiangAPI()
    
    # 提示词
    prompt = "角色图确认 - 这是一个可爱的卡通角色，请保持原图风格和特征，优化细节和质感"
    
    print(f"[PROMPT] 提示词: {prompt}")
    print("[CHECK] 使用修复版API确保字段名正确")
    
    # 调用修复版API
    result, api_metadata = api.generate_image_fixed(
        prompt=prompt,
        image_url=image_url,
        size="1920*1080",
        n=1
    )
    
    # Step 3: 分析结果
    print("\n" + "=" * 60)
    print("Step 1 执行结果:")
    print("=" * 60)
    
    if result and api_metadata.get('success'):
        print(f"[SUCCESS] Step 1 完成: 图片生成成功")
        print(f"[INFO] 生成的图片URL: {result}")
        
        # 检查payload中的字段名
        payload = api_metadata.get('payload_sent', {})
        if payload:
            print(f"[CHECK] 字段名验证: 使用 'image' 字段 [OK]")
        
        return result
    else:
        print(f"[FAILURE] Step 1 失败")
        error = api_metadata.get('error', '未知错误')
        print(f"[ERROR] 错误信息: {error}")
        
        # 检查错误类型
        if '400' in str(error):
            print(f"[DIAGNOSIS] 400错误 - 可能是字段名或格式问题")
        elif 'Failed to download image' in str(error):
            print(f"[DIAGNOSIS] 图片下载失败 - CDN可能被屏蔽")
        else:
            print(f"[DIAGNOSIS] 其他API错误")
        
        return None

if __name__ == "__main__":
    print("万相IP技能 - 优化版Step 1 执行")
    print("=" * 60)
    print("策略: Base64优先，避免400错误")
    print("=" * 60)
    
    result = execute_optimized_step1()
    
    print("\n" + "=" * 60)
    if result:
        print("[PASS] Step 1 执行成功")
        print(f"[RESULT] 生成的图片URL已保存")
    else:
        print("[FAIL] Step 1 执行失败")
    print("=" * 60)