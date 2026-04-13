#!/usr/bin/env python3
# 万相IP技能 - 第一步：生成角色三视图（修复版）
# 输入：单角色图片
# 输出：角色三视图

import os
import sys
import time
import base64
from pathlib import Path

# 添加scripts目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/scripts')

from wan_skills_integrated import WanSkillsIntegrated

def image_to_data_url(image_path: str, max_size: int = 1024) -> str:
    """将本地图片转换为Base64 data URL，自动压缩"""
    try:
        from PIL import Image
        from io import BytesIO
        
        # 打开图片
        img = Image.open(image_path)
        width, height = img.size
        
        # 如果图片太大，调整尺寸
        if width > max_size or height > max_size:
            ratio = min(max_size/width, max_size/height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            print(f"图片压缩: {width}x{height} -> {new_width}x{new_height}")
        
        # 转换为JPEG格式（兼容性最好）
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 保存到内存缓冲区
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=90, optimize=True)
        buffer.seek(0)
        
        # 转换为Base64
        img_data = buffer.getvalue()
        base64_str = base64.b64encode(img_data).decode('utf-8')
        data_url = f'data:image/jpeg;base64,{base64_str}'
        
        print(f"Base64 data URL长度: {len(data_url)} 字符")
        return data_url
        
    except ImportError:
        # 如果没有PIL，使用简单方法（不压缩）
        print("警告: PIL未安装，使用简单Base64转换（不压缩）")
        with open(image_path, 'rb') as f:
            img_data = f.read()
            base64_str = base64.b64encode(img_data).decode('utf-8')
            data_url = f'data:image/jpeg;base64,{base64_str}'
            print(f"Base64 data URL长度: {len(data_url)} 字符")
            return data_url
    except Exception as e:
        print(f"图片转换失败: {e}")
        raise

def main():
    print("=" * 60)
    print("万相IP技能 - 第一步：生成角色三视图")
    print("=" * 60)
    
    # 输入图片路径
    input_image_path = r"C:\Users\User\.openclaw\media\inbound\d3e6712e-0e04-4348-a240-a6f2a028ce6f.jpg"
    
    if not os.path.exists(input_image_path):
        print(f"错误：输入图片不存在: {input_image_path}")
        return
    
    print(f"输入图片: {input_image_path}")
    print(f"图片大小: {os.path.getsize(input_image_path) / 1024:.1f} KB")
    
    # 将图片转换为Base64 data URL
    print("\n转换图片为Base64 data URL...")
    try:
        data_url = image_to_data_url(input_image_path)
        print("✅ 图片转换成功")
    except Exception as e:
        print(f"❌ 图片转换失败: {e}")
        return {
            "status": "error",
            "step": "step1_character_3view",
            "message": f"图片转换失败: {str(e)}"
        }
    
    # 初始化Wan-skills适配器
    print("\n初始化Wan-skills适配器...")
    adapter = WanSkillsIntegrated()
    
    # 生成角色三视图的提示词
    prompt = """生成这个兽人战士角色的三视图（正面、侧面、背面）。
    
角色特征：
1. 强壮有力的兽人战士
2. 头上有角，面部有兽人特征
3. 身穿战斗装备，有护甲
4. 肌肉发达，战斗姿态
    
要求：
1. 生成标准的三视图布局：正面在中间，侧面在两边
2. 保持角色核心特征一致
3. 高质量2K分辨率
4. 无水印
    
请生成这个兽人战士角色的完整三视图。"""
    
    print(f"\n提示词长度: {len(prompt)} 字符")
    print(f"模型: wan2.7-image")
    print(f"分辨率: 2K")
    print(f"水印: 无水印")
    
    # 调用API生成图片
    print("\n开始调用Wan-skills API生成角色三视图...")
    print("注意：这是异步调用，需要轮询任务状态")
    
    try:
        # 调用Wan-skills生成图片
        image_urls = adapter.generate_image(
            prompt=prompt,
            image_url=data_url,
            size="2K",
            num_images=1
        )
        
        if image_urls:
            print(f"\n✅ 图片生成成功！")
            print(f"获取到 {len(image_urls)} 张图片")
            
            # 下载第一张图片
            output_path = r"C:\Users\User\.openclaw\workspace\skills\siri-ip-series-wanxiang\output\step1_character_3view.jpg"
            saved_path = adapter.download_image(image_urls[0], output_path)
            
            if saved_path and os.path.exists(saved_path):
                print(f"✅ 图片已保存到: {saved_path}")
                print(f"文件大小: {os.path.getsize(saved_path) / 1024:.1f} KB")
                
                # 返回成功信息
                return {
                    "status": "success",
                    "step": "step1_character_3view",
                    "output_path": saved_path,
                    "message": "角色三视图生成成功"
                }
            else:
                print("❌ 图片下载失败")
                return {
                    "status": "error",
                    "step": "step1_character_3view",
                    "message": "图片下载失败"
                }
        else:
            print("❌ 图片生成失败，未获取到图片URL")
            return {
                "status": "error",
                "step": "step1_character_3view",
                "message": "未获取到图片URL"
            }
            
    except Exception as e:
        print(f"❌ API调用失败: {str(e)}")
        return {
            "status": "error",
            "step": "step1_character_3view",
            "message": f"API调用失败: {str(e)}"
        }

if __name__ == "__main__":
    result = main()
    print("\n" + "=" * 60)
    if result["status"] == "success":
        print("✅ 第一步执行完成！")
        print(f"输出文件: {result['output_path']}")
    else:
        print("❌ 第一步执行失败")
        print(f"错误信息: {result['message']}")
    print("=" * 60)