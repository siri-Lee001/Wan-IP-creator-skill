#!/usr/bin/env python3
# Wan-skills适配器
# 基于Wan-skills文档创建的适配器，解决同步调用权限问题

import os
import requests
import json
import time
import base64
from typing import Optional, List, Dict, Any
from pathlib import Path

class WanSkillsAdapter:
    """Wan-skills适配器 - 解决同步调用权限问题"""
    
    def __init__(self, api_key: Optional[str] = None, region: str = "beijing"):
        """
        初始化Wan-skills适配器
        
        Args:
            api_key: API密钥，不传则使用环境变量
            region: 地域，beijing或singapore
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY", "sk-1d50f95340d848ae83c3950470e01deb")
        self.region = region
        
        # 根据地域选择base URL
        if region == "singapore":
            self.base_url = "https://dashscope-intl.aliyuncs.com/api/v1/"
        else:
            self.base_url = "https://dashscope.aliyuncs.com/api/v1/"
        
        # 图片生成端点
        self.image_endpoint = f"{self.base_url}services/aigc/image-generation/generation"
        
        # 视频生成端点
        self.video_endpoint = f"{self.base_url}services/aigc/video-generation/video-synthesis"
        
        # 任务状态查询端点
        self.task_endpoint = f"{self.base_url}services/aigc/async-task"
        
        print(f"WanSkillsAdapter初始化完成")
        print(f"地域: {region}")
        print(f"Base URL: {self.base_url}")
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def _compress_image_for_api(self, image_path: str) -> Optional[str]:
        """
        压缩图片以适应API限制
        
        Args:
            image_path: 图片路径
            
        Returns:
            Base64 data URL 或 None
        """
        try:
            from PIL import Image
            import io
            
            # 打开图片
            img = Image.open(image_path)
            
            # 获取原始尺寸
            original_size = img.size
            print(f"原始尺寸: {original_size}")
            
            # 计算压缩比例
            max_dimension = 768  # 最大尺寸
            if max(original_size) > max_dimension:
                # 等比例缩放
                ratio = max_dimension / max(original_size)
                new_size = (int(original_size[0] * ratio), int(original_size[1] * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
                print(f"压缩后尺寸: {new_size}")
            
            # 转换为JPEG并压缩质量
            output_buffer = io.BytesIO()
            img.save(output_buffer, format='JPEG', quality=85, optimize=True)
            compressed_data = output_buffer.getvalue()
            
            print(f"压缩后大小: {len(compressed_data)}字节")
            
            # 转换为Base64
            base64_str = base64.b64encode(compressed_data).decode('utf-8')
            data_url = f"data:image/jpeg;base64,{base64_str}"
            
            print(f"Base64长度: {len(data_url)}字符")
            
            if len(data_url) > 61440:
                print("警告: Base64 URL仍然较长，但尝试使用")
            
            return data_url
            
        except Exception as e:
            print(f"图片压缩失败: {e}")
            return None
    
    def generate_image_text_to_image(self, prompt: str, size: str = "2K", 
                                     num_images: int = 1) -> Optional[List[str]]:
        """
        文生图 - 生成图片
        
        Args:
            prompt: 提示词
            size: 图片尺寸 (1K, 2K, 或 宽x高)
            num_images: 生成数量
            
        Returns:
            图片URL列表 或 None
        """
        try:
            headers = self._get_headers()
            
            payload = {
                "model": "wan2.7-image",
                "input": {
                    "prompt": prompt
                },
                "parameters": {
                    "size": size,
                    "thinking_mode": True,  # 开启思考模式
                    "watermark": False,
                    "num_images": num_images
                }
            }
            
            print(f"文生图请求:")
            print(f"提示词: {prompt}")
            print(f"尺寸: {size}")
            print(f"数量: {num_images}")
            
            response = requests.post(self.image_endpoint, headers=headers, 
                                    json=payload, timeout=60)
            
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"API响应代码: {result.get('code', '成功')}")
                
                if "output" in result and "results" in result["output"]:
                    image_urls = []
                    for item in result["output"]["results"]:
                        if "url" in item:
                            image_urls.append(item["url"])
                    
                    if image_urls:
                        print(f"生成成功，获取到 {len(image_urls)} 张图片")
                        return image_urls
                    else:
                        print("未找到图片URL")
                else:
                    print(f"响应格式异常: {result}")
            else:
                print(f"API调用失败: {response.status_code}")
                print(f"错误信息: {response.text[:500]}")
            
            return None
            
        except Exception as e:
            print(f"文生图失败: {e}")
            return None
    
    def generate_image_image_to_image(self, image_path: str, prompt: str, 
                                      size: str = "2K", num_images: int = 1) -> Optional[List[str]]:
        """
        图生图 - 基于图片生成新图片
        
        Args:
            image_path: 输入图片路径
            prompt: 提示词
            size: 图片尺寸
            num_images: 生成数量
            
        Returns:
            图片URL列表 或 None
        """
        try:
            # 压缩图片
            data_url = self._compress_image_for_api(image_path)
            if not data_url:
                print("图片压缩失败，尝试文生图模式")
                return self.generate_image_text_to_image(prompt, size, num_images)
            
            headers = self._get_headers()
            
            payload = {
                "model": "wan2.7-image",
                "input": {
                    "image_url": data_url,
                    "prompt": prompt
                },
                "parameters": {
                    "size": size,
                    "thinking_mode": True,
                    "watermark": False,
                    "num_images": num_images
                }
            }
            
            print(f"图生图请求:")
            print(f"输入图片: {image_path}")
            print(f"提示词: {prompt}")
            
            response = requests.post(self.image_endpoint, headers=headers, 
                                    json=payload, timeout=60)
            
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"API响应代码: {result.get('code', '成功')}")
                
                if "output" in result and "results" in result["output"]:
                    image_urls = []
                    for item in result["output"]["results"]:
                        if "url" in item:
                            image_urls.append(item["url"])
                    
                    if image_urls:
                        print(f"生成成功，获取到 {len(image_urls)} 张图片")
                        return image_urls
                    else:
                        print("未找到图片URL")
                else:
                    print(f"响应格式异常: {result}")
            else:
                print(f"API调用失败: {response.status_code}")
                print(f"错误信息: {response.text[:500]}")
                
                # 如果图生图失败，尝试文生图
                print("尝试文生图模式...")
                return self.generate_image_text_to_image(prompt, size, num_images)
            
            return None
            
        except Exception as e:
            print(f"图生图失败: {e}")
            # 失败时尝试文生图
            return self.generate_image_text_to_image(prompt, size, num_images)
    
    def generate_video(self, image_path: str, prompt: str, 
                       duration: int = 5, resolution: str = "720P") -> Optional[str]:
        """
        生成视频 - 图生视频
        
        Args:
            image_path: 输入图片路径
            prompt: 视频描述
            duration: 视频时长（秒）
            resolution: 视频分辨率
            
        Returns:
            任务ID 或 None
        """
        try:
            # 压缩图片
            data_url = self._compress_image_for_api(image_path)
            if not data_url:
                print("图片压缩失败，无法生成视频")
                return None
            
            headers = self._get_headers()
            
            payload = {
                "model": "wan2.7-i2v",
                "input": {
                    "image_url": data_url,
                    "prompt": prompt
                },
                "parameters": {
                    "resolution": resolution,
                    "duration": duration,
                    "prompt_extend": True,  # 开启智能改写
                    "watermark": False
                }
            }
            
            print(f"视频生成请求:")
            print(f"输入图片: {image_path}")
            print(f"视频描述: {prompt}")
            print(f"时长: {duration}秒")
            print(f"分辨率: {resolution}")
            
            response = requests.post(self.video_endpoint, headers=headers, 
                                    json=payload, timeout=60)
            
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"API响应代码: {result.get('code', '成功')}")
                
                if "output" in result and "task_id" in result["output"]:
                    task_id = result["output"]["task_id"]
                    print(f"视频任务创建成功，任务ID: {task_id}")
                    return task_id
                else:
                    print(f"响应格式异常: {result}")
            else:
                print(f"API调用失败: {response.status_code}")
                print(f"错误信息: {response.text[:500]}")
            
            return None
            
        except Exception as e:
            print(f"视频生成失败: {e}")
            return None
    
    def check_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        检查任务状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务状态信息 或 None
        """
        try:
            headers = self._get_headers()
            
            url = f"{self.task_endpoint}/{task_id}"
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"任务状态查询失败: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"任务状态查询失败: {e}")
            return None
    
    def download_image(self, image_url: str, output_path: str) -> bool:
        """
        下载图片到本地
        
        Args:
            image_url: 图片URL
            output_path: 输出路径
            
        Returns:
            是否成功
        """
        try:
            response = requests.get(image_url, timeout=30)
            if response.status_code == 200:
                # 确保输出目录存在
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"图片下载成功: {output_path}")
                print(f"文件大小: {os.path.getsize(output_path)} 字节")
                return True
            else:
                print(f"下载失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"下载失败: {e}")
            return False


# 测试函数
def test_wan_skills_adapter():
    """测试WanSkillsAdapter"""
    print("测试WanSkillsAdapter...")
    
    # 初始化适配器
    adapter = WanSkillsAdapter()
    
    # 测试文生图
    print("\n1. 测试文生图...")
    prompt = "国潮风格角色，红色为主色调，传统纹样，现代设计，高质量"
    image_urls = adapter.generate_image_text_to_image(prompt, size="2K", num_images=1)
    
    if image_urls:
        print(f"文生图成功: {image_urls[0]}")
        
        # 下载图片
        output_dir = r"C:\Users\User\.openclaw\workspace\output"
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, "test_text_to_image.jpg")
        if adapter.download_image(image_urls[0], output_path):
            print(f"图片已保存: {output_path}")
    else:
        print("文生图失败")
    
    # 测试图生图（如果有输入图片）
    test_image = r"C:\Users\User\.openclaw\media\inbound\b7e7a959-27c0-47da-95be-2cd3e3152639.jpg"
    if os.path.exists(test_image):
        print("\n2. 测试图生图...")
        prompt = "将角色转换为国潮风格，红色为主色调，加入传统纹样"
        image_urls = adapter.generate_image_image_to_image(test_image, prompt, size="2K", num_images=1)
        
        if image_urls:
            print(f"图生图成功: {image_urls[0]}")
            
            output_path = os.path.join(output_dir, "test_image_to_image.jpg")
            if adapter.download_image(image_urls[0], output_path):
                print(f"图片已保存: {output_path}")
        else:
            print("图生图失败")
    
    print("\n测试完成！")

if __name__ == "__main__":
    test_wan_skills_adapter()