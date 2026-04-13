#!/usr/bin/env python3
# Wan-skills异步适配器
# 支持异步调用的适配器

import os
import requests
import json
import time
import base64
from typing import Optional, List, Dict, Any
from pathlib import Path

class WanSkillsAsyncAdapter:
    """Wan-skills异步适配器 - 支持异步调用"""
    
    def __init__(self, api_key: Optional[str] = None, region: str = "beijing"):
        """
        初始化异步适配器
        
        Args:
            api_key: API密钥
            region: 地域
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY", "sk-1d50f95340d848ae83c3950470e01deb")
        self.region = region
        
        # 根据地域选择base URL
        if region == "singapore":
            self.base_url = "https://dashscope-intl.aliyuncs.com/api/v1/"
        else:
            self.base_url = "https://dashscope.aliyuncs.com/api/v1/"
        
        # 异步任务端点
        self.async_endpoint = f"{self.base_url}services/aigc/async-task"
        
        print(f"WanSkillsAsyncAdapter初始化完成")
        print(f"地域: {region}")
        print(f"Base URL: {self.base_url}")
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def create_async_image_task(self, prompt: str, image_url: Optional[str] = None,
                               size: str = "2K", num_images: int = 1) -> Optional[str]:
        """
        创建异步图片生成任务
        
        Args:
            prompt: 提示词
            image_url: 输入图片URL（可选，图生图时使用）
            size: 图片尺寸
            num_images: 生成数量
            
        Returns:
            任务ID 或 None
        """
        try:
            headers = self._get_headers()
            
            # 构建输入
            input_data = {"prompt": prompt}
            if image_url:
                input_data["image_url"] = image_url
            
            payload = {
                "model": "wan2.7-image",
                "input": input_data,
                "parameters": {
                    "size": size,
                    "thinking_mode": True,
                    "watermark": False,
                    "num_images": num_images
                }
            }
            
            print(f"创建异步图片任务:")
            print(f"提示词: {prompt}")
            print(f"尺寸: {size}")
            print(f"数量: {num_images}")
            if image_url:
                print(f"输入图片: {image_url[:100]}...")
            
            response = requests.post(self.async_endpoint, headers=headers, 
                                    json=payload, timeout=60)
            
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"API响应代码: {result.get('code', '成功')}")
                
                if "output" in result and "task_id" in result["output"]:
                    task_id = result["output"]["task_id"]
                    print(f"异步任务创建成功，任务ID: {task_id}")
                    return task_id
                else:
                    print(f"响应格式异常: {result}")
            else:
                print(f"API调用失败: {response.status_code}")
                print(f"错误信息: {response.text[:500]}")
            
            return None
            
        except Exception as e:
            print(f"创建异步任务失败: {e}")
            return None
    
    def create_async_video_task(self, image_url: str, prompt: str,
                               duration: int = 5, resolution: str = "720P") -> Optional[str]:
        """
        创建异步视频生成任务
        
        Args:
            image_url: 输入图片URL
            prompt: 视频描述
            duration: 视频时长
            resolution: 视频分辨率
            
        Returns:
            任务ID 或 None
        """
        try:
            headers = self._get_headers()
            
            payload = {
                "model": "wan2.7-i2v",
                "input": {
                    "image_url": image_url,
                    "prompt": prompt
                },
                "parameters": {
                    "resolution": resolution,
                    "duration": duration,
                    "prompt_extend": True,
                    "watermark": False
                }
            }
            
            print(f"创建异步视频任务:")
            print(f"输入图片: {image_url[:100]}...")
            print(f"视频描述: {prompt}")
            print(f"时长: {duration}秒")
            print(f"分辨率: {resolution}")
            
            response = requests.post(self.async_endpoint, headers=headers, 
                                    json=payload, timeout=60)
            
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"API响应代码: {result.get('code', '成功')}")
                
                if "output" in result and "task_id" in result["output"]:
                    task_id = result["output"]["task_id"]
                    print(f"异步视频任务创建成功，任务ID: {task_id}")
                    return task_id
                else:
                    print(f"响应格式异常: {result}")
            else:
                print(f"API调用失败: {response.status_code}")
                print(f"错误信息: {response.text[:500]}")
            
            return None
            
        except Exception as e:
            print(f"创建异步视频任务失败: {e}")
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
            
            url = f"{self.async_endpoint}/{task_id}"
            
            print(f"检查任务状态: {task_id}")
            
            response = requests.get(url, headers=headers, timeout=30)
            
            print(f"状态响应码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"任务状态: {result.get('output', {}).get('task_status', '未知')}")
                return result
            else:
                print(f"任务状态查询失败: {response.status_code}")
                print(f"错误信息: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"任务状态查询失败: {e}")
            return None
    
    def wait_for_task_completion(self, task_id: str, max_wait: int = 300, 
                                poll_interval: int = 10) -> Optional[Dict[str, Any]]:
        """
        等待任务完成
        
        Args:
            task_id: 任务ID
            max_wait: 最大等待时间（秒）
            poll_interval: 轮询间隔（秒）
            
        Returns:
            完成后的任务结果 或 None
        """
        print(f"等待任务完成: {task_id}")
        print(f"最大等待时间: {max_wait}秒")
        print(f"轮询间隔: {poll_interval}秒")
        
        start_time = time.time()
        poll_count = 0
        
        while time.time() - start_time < max_wait:
            poll_count += 1
            print(f"\n轮询 #{poll_count}...")
            
            status = self.check_task_status(task_id)
            if not status:
                print("获取状态失败")
                return None
            
            task_status = status.get('output', {}).get('task_status', 'UNKNOWN')
            print(f"任务状态: {task_status}")
            
            if task_status == 'SUCCEEDED':
                print("任务成功完成！")
                return status
            elif task_status == 'FAILED':
                print("任务失败")
                error = status.get('output', {}).get('task_metrics', {}).get('error', {})
                print(f"错误信息: {error}")
                return None
            elif task_status == 'CANCELED':
                print("任务已取消")
                return None
            
            # 任务还在进行中，等待后继续轮询
            print(f"等待 {poll_interval} 秒后继续检查...")
            time.sleep(poll_interval)
        
        print(f"等待超时（{max_wait}秒）")
        return None
    
    def get_task_results(self, task_result: Dict[str, Any]) -> Optional[List[str]]:
        """
        从任务结果中提取图片URL
        
        Args:
            task_result: 任务结果
            
        Returns:
            图片URL列表 或 None
        """
        try:
            output = task_result.get('output', {})
            
            # 检查是否有results
            if 'results' in output:
                image_urls = []
                for item in output['results']:
                    if 'url' in item:
                        image_urls.append(item['url'])
                
                if image_urls:
                    print(f"提取到 {len(image_urls)} 个图片URL")
                    return image_urls
            
            # 检查是否有output_url（视频任务）
            if 'output_url' in output:
                video_url = output['output_url']
                print(f"提取到视频URL: {video_url}")
                return [video_url]
            
            print("未找到结果URL")
            return None
            
        except Exception as e:
            print(f"提取结果失败: {e}")
            return None
    
    def compress_image_to_base64(self, image_path: str) -> Optional[str]:
        """
        压缩图片并转换为Base64
        
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
            original_size = img.size
            print(f"原始尺寸: {original_size}")
            
            # 压缩到合适大小
            max_dimension = 512  # 进一步压缩
            if max(original_size) > max_dimension:
                ratio = max_dimension / max(original_size)
                new_size = (int(original_size[0] * ratio), int(original_size[1] * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
                print(f"压缩后尺寸: {new_size}")
            
            # 转换为JPEG
            output_buffer = io.BytesIO()
            img.save(output_buffer, format='JPEG', quality=80, optimize=True)
            compressed_data = output_buffer.getvalue()
            
            print(f"压缩后大小: {len(compressed_data)}字节")
            
            # 转换为Base64
            base64_str = base64.b64encode(compressed_data).decode('utf-8')
            data_url = f"data:image/jpeg;base64,{base64_str}"
            
            print(f"Base64长度: {len(data_url)}字符")
            return data_url
            
        except Exception as e:
            print(f"图片压缩失败: {e}")
            return None


# 测试函数
def test_async_adapter():
    """测试异步适配器"""
    print("测试WanSkillsAsyncAdapter...")
    
    # 初始化适配器
    adapter = WanSkillsAsyncAdapter()
    
    # 测试1: 创建异步文生图任务
    print("\n1. 测试异步文生图任务...")
    prompt = "国潮风格角色，红色为主色调，传统纹样，现代设计"
    task_id = adapter.create_async_image_task(prompt, size="2K", num_images=1)
    
    if task_id:
        print(f"任务创建成功: {task_id}")
        
        # 等待任务完成（缩短等待时间用于测试）
        print("等待任务完成（测试模式，只检查一次状态）...")
        status = adapter.check_task_status(task_id)
        if status:
            print(f"任务状态: {status.get('output', {}).get('task_status', '未知')}")
            
            # 如果是完成状态，提取结果
            task_status = status.get('output', {}).get('task_status', '')
            if task_status == 'SUCCEEDED':
                image_urls = adapter.get_task_results(status)
                if image_urls:
                    print(f"图片URL: {image_urls[0]}")
    else:
        print("任务创建失败")
    
    # 测试2: 如果有输入图片，测试图生图
    test_image = r"C:\Users\User\.openclaw\media\inbound\b7e7a959-27c0-47da-95be-2cd3e3152639.jpg"
    if os.path.exists(test_image):
        print("\n2. 测试异步图生图任务...")
        
        # 压缩图片为Base64
        data_url = adapter.compress_image_to_base64(test_image)
        if data_url:
            prompt = "将角色转换为国潮风格，红色为主色调"
            task_id = adapter.create_async_image_task(prompt, image_url=data_url, 
                                                     size="2K", num_images=1)
            
            if task_id:
                print(f"图生图任务创建成功: {task_id}")
                status = adapter.check_task_status(task_id)
                if status:
                    print(f"任务状态: {status.get('output', {}).get('task_status', '未知')}")
    
    print("\n测试完成！")

if __name__ == "__main__":
    test_async_adapter()