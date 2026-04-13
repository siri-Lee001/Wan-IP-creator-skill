#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片上传到img402.dev模块
用于将本地图片上传到img402.dev图床，获得公网URL
"""

import requests
import os
import mimetypes
import base64

def upload_to_img402(file_path):
    """
    上传图片到img402.dev
    
    Args:
        file_path: 本地图片文件路径
        
    Returns:
        str: 图片的公网URL，失败返回None
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"错误：文件不存在 {file_path}")
            return None
        
        # 获取文件信息
        file_size = os.path.getsize(file_path)
        if file_size > 1 * 1024 * 1024:  # 1MB限制
            print(f"警告：文件大小 {file_size/1024/1024:.2f}MB 超过1MB限制")
            # 可以在这里添加压缩逻辑
        
        # 读取文件
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # 获取MIME类型
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type or not mime_type.startswith('image/'):
            mime_type = 'image/jpeg'
        
        # 转换为base64
        file_base64 = base64.b64encode(file_content).decode('utf-8')
        
        # 构建请求数据
        data = {
            'file': file_base64,
            'mime': mime_type
        }
        
        # 上传到img402.dev
        print(f"上传图片到img402.dev: {os.path.basename(file_path)}")
        response = requests.post('https://img402.dev/api/upload', json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                image_url = result.get('url')
                print(f"上传成功: {image_url}")
                return image_url
            else:
                print(f"上传失败: {result.get('error', '未知错误')}")
        else:
            print(f"HTTP错误: {response.status_code}")
            print(f"响应内容: {response.text[:200]}")
            
    except Exception as e:
        print(f"上传异常: {e}")
    
    return None

def upload_multiple_images(image_paths):
    """
    批量上传图片
    
    Args:
        image_paths: 图片路径列表
        
    Returns:
        dict: {文件路径: URL} 映射
    """
    results = {}
    
    for image_path in image_paths:
        if os.path.exists(image_path):
            url = upload_to_img402(image_path)
            if url:
                results[image_path] = url
            else:
                print(f"上传失败: {image_path}")
        else:
            print(f"文件不存在: {image_path}")
    
    return results

def get_best_front_image(image_dir):
    """
    从图片目录中选择最佳的正面角色图用于视频生成
    
    Args:
        image_dir: 图片目录路径
        
    Returns:
        str: 最佳正面图片路径，找不到返回None
    """
    if not os.path.exists(image_dir):
        return None
    
    # 优先选择的文件名模式
    preferred_patterns = [
        '正面', 'front', '主体', 'main', '角色', 'character',
        '01_', '02_', '03_',  # 按序号
    ]
    
    image_files = []
    for file in os.listdir(image_dir):
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            image_files.append(os.path.join(image_dir, file))
    
    if not image_files:
        return None
    
    # 按优先级排序
    def get_priority(filepath):
        filename = os.path.basename(filepath).lower()
        for i, pattern in enumerate(preferred_patterns):
            if pattern.lower() in filename:
                return i
        return len(preferred_patterns)  # 最低优先级
    
    image_files.sort(key=get_priority)
    return image_files[0] if image_files else None

if __name__ == '__main__':
    # 测试代码
    test_image = r"C:\Users\User\.openclaw\workspace\test_image.jpg"
    
    # 创建测试图片（如果不存在）
    if not os.path.exists(test_image):
        print(f"测试图片不存在: {test_image}")
        print("请提供真实的图片路径进行测试")
    else:
        url = upload_to_img402(test_image)
        if url:
            print(f"测试成功！图片URL: {url}")
        else:
            print("测试失败")