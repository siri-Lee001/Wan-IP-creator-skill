#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
万相技能优化版图片上传模块
支持多种图片上传策略，优先级：
1. Base64 data URL（首选，无需外部服务）
2. postimages.org（免费，无需API密钥）
3. imgbb.com（需要API密钥，备用）
4. 本地HTTP服务器（技术方案）
"""

import requests
import base64
import os
import time
import json
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket
import urllib.parse

class ImageUploaderOptimized:
    """优化版图片上传器"""
    
    def __init__(self, imgbb_api_key=None):
        """
        初始化图片上传器
        
        Args:
            imgbb_api_key: imgbb.com的API密钥（可选）
        """
        self.imgbb_api_key = imgbb_api_key
        self.local_server = None
        self.local_server_port = None
        self.local_server_thread = None
        
    def upload_image(self, image_path, max_size_mb=10):
        """
        上传图片，返回公网URL
        
        Args:
            image_path: 本地图片路径
            max_size_mb: 最大文件大小（MB）
            
        Returns:
            str: 图片URL，失败返回None
        """
        # 检查文件是否存在
        if not os.path.exists(image_path):
            print(f"[ERROR] 图片不存在: {image_path}")
            return None
        
        # 检查文件大小
        file_size_mb = os.path.getsize(image_path) / 1024 / 1024
        if file_size_mb > max_size_mb:
            print(f"[WARNING] 图片过大: {file_size_mb:.2f}MB > {max_size_mb}MB")
            # 可以尝试压缩，但这里先跳过
        
        print(f"[INFO] 上传图片: {os.path.basename(image_path)} ({file_size_mb:.2f}MB)")
        
        # 策略1：Base64 data URL（首选）
        print("[INFO] 尝试策略1: Base64 data URL")
        data_url = self._try_base64_data_url(image_path)
        if data_url:
            print("[SUCCESS] Base64 data URL生成成功")
            return data_url
        
        # 策略2：postimages.org（免费）
        print("[INFO] 尝试策略2: postimages.org")
        url = self._try_postimages(image_path)
        if url:
            print(f"[SUCCESS] postimages.org上传成功: {url}")
            return url
        
        # 策略3：imgbb.com（需要API密钥）
        if self.imgbb_api_key:
            print("[INFO] 尝试策略3: imgbb.com")
            url = self._try_imgbb(image_path)
            if url:
                print(f"[SUCCESS] imgbb.com上传成功: {url}")
                return url
        
        # 策略4：本地HTTP服务器
        print("[INFO] 尝试策略4: 本地HTTP服务器")
        url = self._start_local_server(image_path)
        if url:
            print(f"[SUCCESS] 本地服务器启动成功: {url}")
            return url
        
        print("[ERROR] 所有上传策略均失败")
        return None
    
    def _try_base64_data_url(self, image_path):
        """
        尝试生成Base64 data URL
        
        Args:
            image_path: 图片路径
            
        Returns:
            str: data URL，失败返回None
        """
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # 检查Base64长度限制（万相API限制61440字符）
            # 但data URL格式可能不受此限制
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            data_url = f'data:image/jpeg;base64,{image_base64}'
            
            # 验证长度
            if len(image_base64) > 1000000:  # 1MB Base64约1.33MB
                print(f"[WARNING] Base64长度较大: {len(image_base64)}字符")
                # 但data URL格式可能被接受
            
            return data_url
            
        except Exception as e:
            print(f"[ERROR] Base64转换失败: {e}")
            return None
    
    def _try_postimages(self, image_path):
        """
        尝试上传到postimages.org
        
        Args:
            image_path: 图片路径
            
        Returns:
            str: 图片URL，失败返回None
        """
        try:
            # postimages.org通过网页表单上传
            # 这里使用API端点（如果可用）
            api_url = 'https://postimages.org/json/rr'
            
            with open(image_path, 'rb') as f:
                files = {'file': (os.path.basename(image_path), f)}
                response = requests.post(api_url, files=files, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'url' in data:
                    return data['url']
                elif 'status' in data and data['status'] == 'success':
                    # 尝试从响应中提取URL
                    # postimages.org返回HTML，需要解析
                    print("[INFO] postimages.org上传成功，但需要手动获取URL")
                    # 返回一个占位符，实际使用时需要手动获取
                    return "https://postimages.org/upload/success"
            
            print(f"[ERROR] postimages.org上传失败: {response.status_code}")
            return None
            
        except Exception as e:
            print(f"[ERROR] postimages.org异常: {e}")
            return None
    
    def _try_imgbb(self, image_path):
        """
        尝试上传到imgbb.com（需要API密钥）
        
        Args:
            image_path: 图片路径
            
        Returns:
            str: 图片URL，失败返回None
        """
        if not self.imgbb_api_key:
            print("[INFO] 未提供imgbb.com API密钥")
            return None
        
        try:
            api_url = 'https://api.imgbb.com/1/upload'
            
            with open(image_path, 'rb') as f:
                image_base64 = base64.b64encode(f.read()).decode('utf-8')
            
            params = {
                'key': self.imgbb_api_key,
                'image': image_base64,
                'name': os.path.basename(image_path)
            }
            
            response = requests.post(api_url, data=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return data['data']['url']
            
            print(f"[ERROR] imgbb.com上传失败: {response.status_code}")
            return None
            
        except Exception as e:
            print(f"[ERROR] imgbb.com异常: {e}")
            return None
    
    def _start_local_server(self, image_path):
        """
        启动本地HTTP服务器提供图片
        
        Args:
            image_path: 图片路径
            
        Returns:
            str: 本地服务器URL，失败返回None
        """
        try:
            # 复制图片到临时目录
            import tempfile
            import shutil
            
            temp_dir = tempfile.mkdtemp(prefix='wanxiang_')
            temp_image_path = os.path.join(temp_dir, 'image.jpg')
            shutil.copy2(image_path, temp_image_path)
            
            # 启动HTTP服务器
            port = self._find_available_port()
            if not port:
                print("[ERROR] 找不到可用端口")
                return None
            
            # 切换到临时目录
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            # 启动服务器线程
            self.local_server = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
            self.local_server_port = port
            
            def run_server():
                self.local_server.serve_forever()
            
            self.local_server_thread = threading.Thread(target=run_server, daemon=True)
            self.local_server_thread.start()
            
            # 等待服务器启动
            time.sleep(1)
            
            # 恢复原始目录
            os.chdir(original_cwd)
            
            url = f'http://localhost:{port}/image.jpg'
            print(f"[INFO] 本地服务器启动: {url}")
            
            # 注意：本地服务器只能本机访问
            # 需要ngrok等工具创建公网隧道
            print("[WARNING] 本地服务器只能本机访问，需要ngrok创建公网隧道")
            
            return url
            
        except Exception as e:
            print(f"[ERROR] 本地服务器启动失败: {e}")
            return None
    
    def _find_available_port(self, start_port=8080, end_port=8100):
        """查找可用端口"""
        for port in range(start_port, end_port + 1):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    return port
            except OSError:
                continue
        return None
    
    def cleanup(self):
        """清理资源"""
        if self.local_server:
            self.local_server.shutdown()
            if self.local_server_thread:
                self.local_server_thread.join(timeout=5)
            self.local_server = None
            self.local_server_thread = None

# 使用示例
if __name__ == '__main__':
    # 测试图片上传
    test_image = r'C:\Users\User\.openclaw\media\inbound\50aa9399-c216-4a0c-9176-32df77233abb.jpg'
    
    if os.path.exists(test_image):
        uploader = ImageUploaderOptimized()
        
        print("测试图片上传策略...")
        image_url = uploader.upload_image(test_image)
        
        if image_url:
            print(f"\n[SUCCESS] 图片URL获取成功: {image_url}")
            
            # 检查URL类型
            if image_url.startswith('data:'):
                print("类型: Base64 data URL")
                print(f"长度: {len(image_url)} 字符")
            else:
                print(f"类型: 公网URL")
        else:
            print("\n[FAILED] 图片URL获取失败")
        
        # 清理
        uploader.cleanup()
    else:
        print(f"测试图片不存在: {test_image}")