#!/usr/bin/env python3
# Wan-skills集成适配器
# 基于Wan-skills核心代码的集成适配器

import os
import sys
import requests
import time
import json
import base64
from typing import Optional, List, Dict, Any
from pathlib import Path

class WanSkillsIntegrated:
    """Wan-skills集成适配器 - 基于官方Wan-skills代码"""
    
    def __init__(self, api_key: Optional[str] = None, region: str = "beijing"):
        """
        初始化集成适配器
        
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
        
        print(f"WanSkillsIntegrated初始化完成")
        print(f"地域: {region}")
        print(f"Base URL: {self.base_url}")
        print(f"API密钥: {self.api_key[:10]}...")
    
    def _get_headers(self) -> Dict[str, str]:
        """获取Wan-skills标准请求头"""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "X-DashScope-Async": "enable",  # 关键：启用异步
            "X-DashScope-OssResourceResolve": "enable"  # 关键：启用OSS资源解析
        }
    
    def _poll_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        轮询任务状态直到完成（基于Wan-skills代码）
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务结果
        """
        check_url = f"{self.base_url}tasks/{task_id}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        status = "PENDING"
        check_count = 0
        max_checks = 30  # 最多检查30次（约90秒）
        
        print(f"开始轮询任务状态: {task_id}")
        
        while status not in ("SUCCEEDED", "FAILED", "CANCELLED"):
            if check_count >= max_checks:
                return {"status": status, "content": [], "error": "轮询超时"}
            
            print(f"轮询 #{check_count+1}, 当前状态: {status} ...")
            time.sleep(3)  # 等待3秒
            
            try:
                poll_response = requests.get(check_url, headers=headers, timeout=30)
                
                if poll_response.status_code != 200:
                    error_message = f"HTTP {poll_response.status_code}"
                    try:
                        error_data = poll_response.json()
                        error_message = error_data.get("error", error_message)
                    except:
                        pass
                    
                    print(f"轮询失败: {error_message}")
                    check_count += 1
                    continue
                
                poll_res = poll_response.json()
                status = poll_res.get("output", {}).get("task_status", "UNKNOWN")
                
                if status == "SUCCEEDED":
                    print("任务成功完成！")
                    
                    # 提取结果（根据Wan-skills格式）
                    output = poll_res.get("output", {})
                    
                    # 尝试多种结果格式
                    if "choices" in output:
                        choices = output.get("choices", [])
                        if choices and len(choices) > 0:
                            message = choices[0].get("message", {})
                            content = message.get("content", [])
                            if content and isinstance(content, list):
                                return {"status": status, "content": content}
                    
                    # 尝试其他格式
                    if "results" in output:
                        results = output.get("results", [])
                        if results and len(results) > 0:
                            return {"status": status, "content": results}
                    
                    # 直接返回整个输出
                    return {"status": status, "content": [output]}
                    
                elif status == "FAILED":
                    failed_code = poll_res.get("output", {}).get("code", "")
                    failed_message = poll_res.get("output", {}).get("message", "")
                    detail_error = f"任务失败，代码: {failed_code}, 消息: {failed_message}"
                    print(f"任务失败: {detail_error}")
                    return {"status": status, "error": detail_error}
                    
            except Exception as e:
                print(f"轮询异常: {e}")
                check_count += 1
                continue
            
            check_count += 1
        
        return {"status": status, "error": f"任务结束，状态: {status}"}
    
    def generate_image(self, prompt: str, image_url: Optional[str] = None,
                      size: str = "2K", num_images: int = 1) -> Optional[List[str]]:
        """
        生成图片（基于Wan-skills的generate函数）
        
        Args:
            prompt: 提示词
            image_url: 输入图片URL（可选，图生图时使用）
            size: 图片尺寸
            num_images: 生成数量
            
        Returns:
            图片URL列表 或 None
        """
        try:
            headers = self._get_headers()
            # 对齐Wan-skills报文规范，使用多模态生成接口
            api_url = f"{self.base_url}services/aigc/multimodal-generation/generation"
            
            # 构建输入（基于Wan-skills格式）
            if image_url:
                # 图生图模式
                input_data = {
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"image": image_url},
                                {"text": prompt}
                            ]
                        }
                    ]
                }
            else:
                # 文生图模式
                input_data = {
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"text": prompt}
                            ]
                        }
                    ]
                }
            
            # 从环境变量读取模型名称，适配wan2.7-image-pro
            model_name = os.getenv("IMAGE_MODEL", "wan2.7-image-pro")
            payload = {
                "model": model_name,
                "input": input_data,
                "parameters": {
                    "size": size,
                    "thinking_mode": True,
                    "watermark": False,
                    "n": num_images
                }
            }
            
            print(f"生成图片请求:")
            print(f"提示词: {prompt}")
            print(f"尺寸: {size}")
            print(f"数量: {num_images}")
            if image_url:
                print(f"输入图片: {image_url[:100]}...")
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=60)
            
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"API响应代码: {result.get('code', '成功')}")
                
                # 检查是否有任务ID（异步模式）
                if "output" in result and "task_id" in result["output"]:
                    task_id = result["output"]["task_id"]
                    print(f"异步任务创建成功，任务ID: {task_id}")
                    
                    # 轮询任务状态
                    task_result = self._poll_task_status(task_id)
                    
                    if task_result.get("status") == "SUCCEEDED":
                        content = task_result.get("content", [])
                        
                        # 提取图片URL
                        image_urls = []
                        for item in content:
                            if isinstance(item, dict):
                                if "url" in item:
                                    image_urls.append(item["url"])
                                elif "image" in item:
                                    image_urls.append(item["image"])
                            elif isinstance(item, str) and item.startswith("http"):
                                image_urls.append(item)
                        
                        if image_urls:
                            print(f"生成成功，获取到 {len(image_urls)} 张图片")
                            return image_urls
                        else:
                            print("未找到图片URL")
                    else:
                        print(f"任务失败: {task_result.get('error', '未知错误')}")
                else:
                    print(f"响应格式异常，未找到任务ID: {result}")
            else:
                print(f"API调用失败: {response.status_code}")
                print(f"错误信息: {response.text[:500]}")
            
            return None
            
        except Exception as e:
            print(f"生成图片失败: {e}")
            import traceback
            traceback.print_exc()
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
            
            # 压缩到合适大小（Wan-skills建议）
            max_dimension = 1024
            if max(original_size) > max_dimension:
                ratio = max_dimension / max(original_size)
                new_size = (int(original_size[0] * ratio), int(original_size[1] * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
                print(f"压缩后尺寸: {new_size}")
            
            # 转换为JPEG
            output_buffer = io.BytesIO()
            img.save(output_buffer, format='JPEG', quality=90, optimize=True)
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
def test_integrated_adapter():
    """测试集成适配器"""
    print("测试WanSkillsIntegrated适配器...")
    
    # 初始化适配器
    adapter = WanSkillsIntegrated()
    
    # 测试文生图
    print("\n1. 测试文生图...")
    prompt = "国潮风格角色，红色为主色调，传统纹样，现代设计，高质量"
    image_urls = adapter.generate_image(prompt, size="2K", num_images=1)
    
    if image_urls:
        print(f"文生图成功: {image_urls[0]}")
        
        # 下载图片
        output_dir = r"C:\Users\User\.openclaw\workspace\output"
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, "test_integrated_text_to_image.jpg")
        if adapter.download_image(image_urls[0], output_path):
            print(f"图片已保存: {output_path}")
    else:
        print("文生图失败")
    
    # 测试图生图（如果有输入图片）
    test_image = r"C:\Users\User\.openclaw\media\inbound\b7e7a959-27c0-47da-95be-2cd3e3152639.jpg"
    if os.path.exists(test_image):
        print("\n2. 测试图生图...")
        
        # 压缩图片为Base64
        data_url = adapter.compress_image_to_base64(test_image)
        if data_url:
            prompt = "将角色转换为国潮风格，红色为主色调，加入传统纹样"
            image_urls = adapter.generate_image(prompt, image_url=data_url, size="2K", num_images=1)
            
            if image_urls:
                print(f"图生图成功: {image_urls[0]}")
                
                output_path = os.path.join(output_dir, "test_integrated_image_to_image.jpg")
                if adapter.download_image(image_urls[0], output_path):
                    print(f"图片已保存: {output_path}")
            else:
                print("图生图失败")
    
    print("\n测试完成！")

if __name__ == "__main__":
    test_integrated_adapter()