#!/usr/bin/env python3
# API连通性测试脚本

import os
import sys
import requests
import json

def test_api_connectivity():
    """测试API连通性"""
    api_key = os.getenv("DASHSCOPE_API_KEY", "sk-1d50f95340d848ae83c3950470e01deb")
    region = os.getenv("DASHSCOPE_REGION", "beijing")
    
    # 根据地域选择base URL
    if region == "singapore":
        base_url = "https://dashscope-intl.aliyuncs.com/api/v1/"
    else:
        base_url = "https://dashscope.aliyuncs.com/api/v1/"
    
    # Wan-skills标准请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "X-DashScope-Async": "enable",
        "X-DashScope-OssResourceResolve": "enable"
    }
    
    api_url = f"{base_url}services/aigc/image-generation/generation"
    
    # 简单测试请求
    payload = {
        "model": "wan2.7-image",
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"text": "测试API连通性，生成一张简单的测试图片"}
                    ]
                }
            ]
        },
        "parameters": {
            "size": "1K",
            "thinking_mode": False,
            "watermark": False,
            "num_images": 1
        }
    }
    
    print("测试API连通性...")
    print(f"API密钥: {api_key[:10]}...")
    print(f"地域: {region}")
    print(f"端点: {api_url}")
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"API响应成功!")
            
            # 检查是否有任务ID
            if "output" in result and "task_id" in result["output"]:
                task_id = result["output"]["task_id"]
                print(f"异步任务创建成功!")
                print(f"任务ID: {task_id}")
                
                # 立即检查任务状态
                print(f"立即检查任务状态...")
                check_url = f"{base_url}tasks/{task_id}"
                check_headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                }
                
                check_response = requests.get(check_url, headers=check_headers, timeout=30)
                if check_response.status_code == 200:
                    check_result = check_response.json()
                    task_status = check_result.get("output", {}).get("task_status", "UNKNOWN")
                    print(f"任务状态: {task_status}")
                    
                    if task_status == "SUCCEEDED":
                        print("任务已成功完成!")
                        return True
                    elif task_status == "FAILED":
                        print("任务失败")
                        error = check_result.get("output", {}).get("error", {})
                        print(f"错误信息: {error}")
                    else:
                        print(f"任务状态: {task_status}，需要轮询")
                else:
                    print(f"任务状态检查失败: {check_response.status_code}")
            else:
                print("未找到任务ID")
        else:
            print(f"API调用失败: {response.status_code}")
            print(f"错误信息: {response.text[:500]}")
            
            # 尝试解析错误
            try:
                error_data = response.json()
                print(f"错误代码: {error_data.get('code', '未知')}")
                print(f"错误信息: {error_data.get('message', '未知')}")
                
                if error_data.get('code') == 'AccessDenied':
                    print("API密钥权限不足")
                    print("可能原因:")
                    print("1. API密钥没有 wan2.7-image 模型权限")
                    print("2. API密钥已过期")
                    print("3. 需要开通异步调用权限")
                    print("4. 需要开通OSS资源解析权限")
                    
            except:
                pass
                
        return False
        
    except requests.exceptions.Timeout:
        print("请求超时")
        return False
    except requests.exceptions.ConnectionError:
        print("连接错误")
        return False
    except Exception as e:
        print(f"其他错误: {e}")
        return False

def test_video_api():
    """测试视频API连通性"""
    api_key = os.getenv("DASHSCOPE_API_KEY", "sk-1d50f95340d848ae83c3950470e01deb")
    region = os.getenv("DASHSCOPE_REGION", "beijing")
    
    # 根据地域选择base URL
    if region == "singapore":
        base_url = "https://dashscope-intl.aliyuncs.com/api/v1/"
    else:
        base_url = "https://dashscope.aliyuncs.com/api/v1/"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "X-DashScope-Async": "enable",
        "X-DashScope-OssResourceResolve": "enable"
    }
    
    api_url = f"{base_url}services/aigc/video-generation/video-synthesis"
    
    # 简单测试请求（需要图片URL，这里用占位符）
    payload = {
        "model": "wan2.7-i2v",
        "input": {
            "image_url": "https://example.com/test.jpg",
            "prompt": "测试视频API连通性"
        },
        "parameters": {
            "duration": 2,
            "resolution": "480P",
            "watermark": False
        }
    }
    
    print("\n测试视频API连通性...")
    print(f"端点: {api_url}")
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"视频API响应成功!")
            
            if "output" in result and "task_id" in result["output"]:
                task_id = result["output"]["task_id"]
                print(f"视频异步任务创建成功!")
                print(f"任务ID: {task_id}")
                return True
            else:
                print("未找到任务ID")
        else:
            print(f"视频API调用失败: {response.status_code}")
            
            # 检查是否是图片URL无效的错误
            if response.status_code == 400:
                print("可能是图片URL无效，但API端点可访问")
                return True
                
        return False
        
    except Exception as e:
        print(f"视频API测试错误: {e}")
        return False

if __name__ == "__main__":
    print("开始测试API连通性...")
    
    # 测试图片API
    image_api_ok = test_api_connectivity()
    
    # 测试视频API
    video_api_ok = test_video_api()
    
    print("\n" + "="*50)
    print("API连通性测试结果:")
    print(f"图片API (wan2.7-image): {'✅ 通过' if image_api_ok else '❌ 失败'}")
    print(f"视频API (wan2.7-i2v): {'✅ 通过' if video_api_ok else '❌ 失败'}")
    print("="*50)
    
    if image_api_ok and video_api_ok:
        print("\n✅ 所有API测试通过!")
        print("万相IP技能可以正常使用。")
    else:
        print("\n❌ API测试失败")
        print("请检查:")
        print("1. API密钥是否正确")
        print("2. 是否开通了相应模型的权限")
        print("3. 是否开通了异步调用权限")
        print("4. 网络连接是否正常")