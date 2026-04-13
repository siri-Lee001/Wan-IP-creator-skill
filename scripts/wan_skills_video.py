#!/usr/bin/env python3
# Wan-skills视频生成适配器
# 基于Wan-skills异步调用模式的视频生成适配器

import os
import sys
import requests
import time
import json
from typing import Optional, Dict, Any
from pathlib import Path

class WanSkillsVideo:
    """Wan-skills视频生成适配器"""
    
    def __init__(self, api_key: Optional[str] = None, region: str = "beijing"):
        """
        初始化视频生成适配器
        
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
        
        print(f"WanSkillsVideo初始化完成")
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
        轮询任务状态直到完成
        
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
        max_checks = 60  # 视频生成需要更长时间，最多检查60次（约3分钟）
        
        print(f"开始轮询视频任务状态: {task_id}")
        
        while status not in ("SUCCEEDED", "FAILED", "CANCELLED"):
            if check_count >= max_checks:
                return {"status": status, "content": [], "error": "轮询超时"}
            
            print(f"轮询 #{check_count+1}, 当前状态: {status} ...")
            time.sleep(5)  # 视频生成需要更长时间，等待5秒
            
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
                    print("视频任务成功完成！")
                    
                    # 提取结果
                    output = poll_res.get("output", {})
                    
                    # 尝试多种结果格式
                    if "results" in output:
                        results = output.get("results", [])
                        if results and len(results) > 0:
                            return {"status": status, "content": results}
                    
                    if "output_video" in output:
                        video_url = output.get("output_video")
                        if video_url:
                            return {"status": status, "content": [{"video_url": video_url}]}
                    
                    # 直接返回整个输出
                    return {"status": status, "content": [output]}
                    
                elif status == "FAILED":
                    failed_code = poll_res.get("output", {}).get("code", "")
                    failed_message = poll_res.get("output", {}).get("message", "")
                    detail_error = f"视频任务失败，代码: {failed_code}, 消息: {failed_message}"
                    print(f"视频任务失败: {detail_error}")
                    return {"status": status, "error": detail_error}
                    
            except Exception as e:
                print(f"轮询异常: {e}")
                check_count += 1
                continue
            
            check_count += 1
        
        return {"status": status, "error": f"视频任务结束，状态: {status}"}
    
    def generate_video(self, image_url: str, prompt: str, 
                      duration: int = 5, resolution: str = "720P") -> Optional[str]:
        """
        生成视频（基于Wan-skills异步模式）
        
        Args:
            image_url: 输入图片URL（Base64 data URL或公网URL）
            prompt: 视频描述提示词
            duration: 视频时长（秒），固定为5秒
            resolution: 视频分辨率，固定为720P
            
        Returns:
            视频URL 或 None
        """
        try:
            headers = self._get_headers()
            api_url = f"{self.base_url}services/aigc/video-generation/video-synthesis"
            
            # 构建请求体（基于Wan2.7-i2v官方文档）
            payload = {
                "model": "wan2.7-i2v",
                "input": {
                    "media": [
                        {
                            "type": "first_frame",
                            "url": image_url
                        }
                    ],
                    "prompt": prompt
                },
                "parameters": {
                    "duration": duration,
                    "resolution": resolution,
                    "watermark": False,
                    "prompt_extend": True  # 开启智能改写
                }
            }
            
            print(f"生成视频请求:")
            print(f"图片URL长度: {len(image_url)}字符")
            print(f"提示词: {prompt}")
            print(f"时长: {duration}秒")
            print(f"分辨率: {resolution}")
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=60)
            
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"API响应代码: {result.get('code', '成功')}")
                
                # 检查是否有任务ID（异步模式）
                if "output" in result and "task_id" in result["output"]:
                    task_id = result["output"]["task_id"]
                    print(f"异步视频任务创建成功，任务ID: {task_id}")
                    
                    # 轮询任务状态
                    task_result = self._poll_task_status(task_id)
                    
                    if task_result.get("status") == "SUCCEEDED":
                        content = task_result.get("content", [])
                        
                        # 提取视频URL
                        video_url = None
                        for item in content:
                            if isinstance(item, dict):
                                if "video_url" in item:
                                    video_url = item["video_url"]
                                    break
                                elif "url" in item and item["url"].endswith(('.mp4', '.mov', '.avi')):
                                    video_url = item["url"]
                                    break
                            elif isinstance(item, str) and item.endswith(('.mp4', '.mov', '.avi')):
                                video_url = item
                                break
                        
                        if video_url:
                            print(f"视频生成成功，视频URL: {video_url}")
                            return video_url
                        else:
                            print("未找到视频URL")
                    else:
                        print(f"视频任务失败: {task_result.get('error', '未知错误')}")
                else:
                    print(f"响应格式异常，未找到任务ID: {result}")
            else:
                print(f"API调用失败: {response.status_code}")
                print(f"错误信息: {response.text[:500]}")
                
                # 尝试解析错误
                try:
                    error_data = response.json()
                    print(f"错误代码: {error_data.get('code', '未知')}")
                    print(f"错误信息: {error_data.get('message', '未知')}")
                    
                    if error_data.get('code') == 'AccessDenied':
                        print("\nAPI密钥权限不足")
                        print("可能原因:")
                        print("1. API密钥没有 wan2.7-i2v 模型权限")
                        print("2. API密钥已过期")
                        print("3. 需要开通异步调用权限")
                        print("4. 需要开通OSS资源解析权限")
                        
                except:
                    pass
            
            return None
            
        except Exception as e:
            print(f"生成视频失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def download_video(self, video_url: str, output_path: str) -> bool:
        """
        下载视频到本地
        
        Args:
            video_url: 视频URL
            output_path: 输出路径
            
        Returns:
            是否成功
        """
        try:
            response = requests.get(video_url, timeout=60, stream=True)
            if response.status_code == 200:
                # 确保输出目录存在
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            # 显示下载进度
                            if total_size > 0:
                                percent = (downloaded / total_size) * 100
                                print(f"下载进度: {percent:.1f}% ({downloaded}/{total_size}字节)", end='\r')
                
                print(f"\n视频下载成功: {output_path}")
                print(f"文件大小: {os.path.getsize(output_path)} 字节")
                return True
            else:
                print(f"下载失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"下载失败: {e}")
            return False


# 测试函数
def test_video_generation():
    """测试视频生成适配器"""
    print("测试WanSkillsVideo适配器...")
    
    # 初始化适配器
    video_adapter = WanSkillsVideo()
    
    # 测试图片路径
    test_image = r"C:\Users\User\.openclaw\workspace\output\style_guochao_wan_skills.jpg"
    
    if not os.path.exists(test_image):
        print(f"测试图片不存在: {test_image}")
        return False
    
    # 使用Wan-skills集成适配器压缩图片
    from wan_skills_integrated import WanSkillsIntegrated
    
    image_adapter = WanSkillsIntegrated()
    data_url = image_adapter.compress_image_to_base64(test_image)
    
    if not data_url:
        print("图片压缩失败")
        return False
    
    print(f"Base64 data URL长度: {len(data_url)}字符")
    
    # 生成视频
    prompt = "角色动起来，自然的动作，适合IP角色的动态表现"
    video_url = video_adapter.generate_video(
        image_url=data_url,
        prompt=prompt,
        duration=5,
        resolution="720P"
    )
    
    if video_url:
        print(f"视频生成成功: {video_url}")
        
        # 下载视频
        output_dir = r"C:\Users\User\.openclaw\workspace\output"
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, "test_video_wan_skills.mp4")
        if video_adapter.download_video(video_url, output_path):
            print(f"视频已保存: {output_path}")
            return True
        else:
            print("视频下载失败")
            return False
    else:
        print("视频生成失败")
        return False

if __name__ == "__main__":
    print("开始测试Wan-skills视频生成...")
    success = test_video_generation()
    
    if success:
        print("\nWan-skills视频生成测试成功！")
    else:
        print("\nWan-skills视频生成测试失败")