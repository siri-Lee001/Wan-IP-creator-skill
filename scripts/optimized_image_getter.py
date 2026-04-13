#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化版图片获取器 - 基于API文档分析
四层策略：Base64 → 压缩Base64 → 缩略图Base64 → 备用CDN
"""

import os
import re
import base64
import mimetypes
import time
from typing import Optional, Tuple, Dict, Any
from PIL import Image
import io

class OptimizedImageGetter:
    """优化版图片获取器 - 基于千问API文档"""
    
    def __init__(self):
        """
        初始化优化获取器
        
        基于API文档：
        - 图片大小限制：10MB
        - Base64支持：data:image/jpeg;base64,...格式
        - 建议分辨率：384px-3072px
        """
        # API限制
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.max_base64_length = 13_300_000  # 10MB图片对应的Base64约13.3M字符
        
        # 优化参数
        self.thumbnail_size = (512, 512)  # 缩略图尺寸
        self.thumbnail_quality = 85  # JPEG质量
        
        # 支持的图片扩展名
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp', '.tiff'}
        
        # 日志
        self.logs = []
    
    def log(self, message: str):
        """记录日志"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f'[{timestamp}] {message}'
        self.logs.append(log_entry)
        print(log_entry)
    
    def get_image_url(self, image_input: str, strategy: str = 'optimized') -> Tuple[Optional[str], Dict[str, Any]]:
        """
        获取图片URL（主函数）
        
        Args:
            image_input: 图片输入（本地路径、URL、Base64）
            strategy: 策略选择
                'optimized': 优化策略（Base64优先）
                'base64_only': 只使用Base64
                'cdn_only': 只使用CDN（最后手段）
        
        Returns:
            (image_url, metadata)
        """
        metadata = {
            'input_type': 'unknown',
            'strategy_used': strategy,
            'success': False,
            'error': None,
            'steps': [],
            'file_size': 0,
            'base64_length': 0,
            'optimization_applied': None
        }
        
        try:
            # 检测输入类型
            input_type = self._detect_input_type(image_input)
            metadata['input_type'] = input_type
            self.log(f'输入类型: {input_type}')
            
            # 策略选择
            if strategy == 'optimized':
                return self._optimized_strategy(image_input, input_type, metadata)
            elif strategy == 'base64_only':
                return self._base64_only_strategy(image_input, input_type, metadata)
            elif strategy == 'cdn_only':
                return self._cdn_only_strategy(image_input, input_type, metadata)
            else:
                metadata['error'] = f'未知策略: {strategy}'
                return None, metadata
                
        except Exception as e:
            metadata['error'] = str(e)
            self.log(f'获取图片URL失败: {e}')
            return None, metadata
    
    def _detect_input_type(self, image_input: str) -> str:
        """检测输入类型"""
        # 检查是否是data URL
        if image_input.startswith('data:image/'):
            self.log(f'检测到data URL输入，长度: {len(image_input)}')
            return 'data_url'
        
        # 检查是否是URL
        if re.match(r'^https?://', image_input):
            self.log(f'检测到URL输入: {image_input[:50]}...')
            return 'url'
        
        # 检查是否是本地文件路径
        if os.path.exists(image_input):
            ext = os.path.splitext(image_input)[1].lower()
            if ext in self.image_extensions:
                self.log(f'检测到本地图片文件: {image_input}')
                return 'local_path'
        
        # 检查是否是纯Base64（长字符串）
        if len(image_input) > 1000 and self._looks_like_base64(image_input):
            self.log(f'检测到纯Base64输入，长度: {len(image_input)}')
            return 'base64'
        
        self.log(f'未知输入类型: {image_input[:50]}...')
        return 'unknown'
    
    def _looks_like_base64(self, text: str) -> bool:
        """检查字符串是否像Base64编码"""
        base64_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=')
        sample = text[:100]
        base64_count = sum(1 for c in sample if c in base64_chars)
        return base64_count / len(sample) > 0.9 if sample else False
    
    def _optimized_strategy(self, image_input: str, input_type: str, metadata: Dict[str, Any]) -> Tuple[Optional[str], Dict[str, Any]]:
        """优化策略：四层方案"""
        
        # 第1层：如果已经是URL，直接使用（但注意API可能无法访问某些CDN）
        if input_type == 'url':
            metadata['steps'].append('使用已有URL')
            metadata['success'] = True
            self.log('第1层: 使用已有URL')
            return image_input, metadata
        
        # 第2层：Base64 data URL（优先）
        base64_result = self._get_base64_url(image_input, input_type, metadata)
        if base64_result:
            base64_url, base64_len = base64_result
            
            # 检查是否超限
            if base64_len <= self.max_base64_length:
                metadata['steps'].append('使用Base64 data URL')
                metadata['success'] = True
                metadata['base64_length'] = base64_len
                self.log(f'第2层: 使用Base64 data URL (长度: {base64_len:,})')
                return base64_url, metadata
            else:
                metadata['steps'].append(f'Base64超限 ({base64_len:,} > {self.max_base64_length:,})')
                self.log(f'Base64超限，尝试第3层')
        
        # 第3层：压缩或缩略图Base64
        compressed_result = self._get_compressed_base64(image_input, input_type, metadata)
        if compressed_result:
            compressed_url, compressed_len, optimization = compressed_result
            
            if compressed_len <= self.max_base64_length:
                metadata['steps'].append(f'使用{optimization}Base64')
                metadata['success'] = True
                metadata['base64_length'] = compressed_len
                metadata['optimization_applied'] = optimization
                self.log(f'第3层: 使用{optimization}Base64 (长度: {compressed_len:,})')
                return compressed_url, metadata
            else:
                metadata['steps'].append(f'{optimization}Base64仍然超限')
                self.log(f'{optimization}Base64仍然超限，尝试第4层')
        
        # 第4层：备用CDN（最后手段）
        cdn_result = self._get_cdn_url(image_input, input_type, metadata)
        if cdn_result:
            metadata['steps'].append('使用备用CDN')
            metadata['success'] = True
            self.log(f'第4层: 使用备用CDN')
            return cdn_result, metadata
        
        # 所有策略都失败
        metadata['error'] = '所有图片URL获取策略均失败'
        metadata['steps'].append('所有策略失败')
        self.log('所有图片URL获取策略均失败')
        return None, metadata
    
    def _get_base64_url(self, image_input: str, input_type: str, metadata: Dict[str, Any]) -> Tuple[Optional[str], int]:
        """获取Base64 data URL"""
        try:
            if input_type == 'data_url':
                return image_input, len(image_input)
            
            elif input_type == 'local_path':
                # 读取文件
                with open(image_input, 'rb') as f:
                    image_data = f.read()
                
                file_size = len(image_data)
                metadata['file_size'] = file_size
                
                # 检查文件大小
                if file_size > self.max_file_size:
                    self.log(f'文件过大 ({file_size:,} > {self.max_file_size:,})')
                    return None, 0
                
                # 获取MIME类型
                mime_type, _ = mimetypes.guess_type(image_input)
                if not mime_type or not mime_type.startswith('image/'):
                    mime_type = 'image/jpeg'
                
                # 转换为Base64
                image_base64 = base64.b64encode(image_data).decode('utf-8')
                data_url = f'data:{mime_type};base64,{image_base64}'
                
                self.log(f'本地文件转Base64: {file_size:,}字节 → {len(image_base64):,}字符')
                return data_url, len(data_url)
            
            elif input_type == 'base64':
                data_url = f'data:image/jpeg;base64,{image_input}'
                return data_url, len(data_url)
            
            else:
                return None, 0
                
        except Exception as e:
            self.log(f'获取Base64 URL失败: {e}')
            return None, 0
    
    def _get_compressed_base64(self, image_input: str, input_type: str, metadata: Dict[str, Any]) -> Tuple[Optional[str], int, str]:
        """获取压缩或缩略图Base64"""
        try:
            # 首先尝试获取原始图片数据
            image_data = None
            if input_type == 'local_path':
                with open(image_input, 'rb') as f:
                    image_data = f.read()
            elif input_type in ['data_url', 'base64']:
                # 提取Base64数据
                if input_type == 'data_url':
                    if 'base64,' in image_input:
                        base64_str = image_input.split('base64,', 1)[1]
                        image_data = base64.b64decode(base64_str)
                elif input_type == 'base64':
                    image_data = base64.b64decode(image_input)
            
            if not image_data:
                return None, 0, ""
            
            # 尝试1: 压缩图片（如果已经是JPEG，压缩效果有限）
            try:
                img = Image.open(io.BytesIO(image_data))
                
                # 检查是否需要缩略图
                if img.size[0] > 1024 or img.size[1] > 1024:
                    # 创建缩略图
                    img.thumbnail(self.thumbnail_size, Image.Resampling.LANCZOS)
                    
                    # 保存为JPEG
                    output = io.BytesIO()
                    img.save(output, format='JPEG', quality=self.thumbnail_quality, optimize=True)
                    compressed_data = output.getvalue()
                    
                    compressed_size = len(compressed_data)
                    compression_ratio = compressed_size / len(image_data)
                    
                    self.log(f'缩略图优化: {img.size}，压缩率: {compression_ratio:.1%}')
                    
                    # 转换为Base64
                    compressed_base64 = base64.b64encode(compressed_data).decode('utf-8')
                    data_url = f'data:image/jpeg;base64,{compressed_base64}'
                    
                    return data_url, len(data_url), "缩略图"
                    
                else:
                    # 图片已经较小，直接使用
                    return None, 0, ""
                    
            except Exception as e:
                self.log(f'图片处理失败: {e}')
                return None, 0, ""
                
        except Exception as e:
            self.log(f'获取压缩Base64失败: {e}')
            return None, 0, ""
    
    def _get_cdn_url(self, image_input: str, input_type: str, metadata: Dict[str, Any]) -> Optional[str]:
        """获取CDN URL（备用方案）"""
        # 注意：Catbox.moe可能被API服务屏蔽
        # 这里可以集成其他CDN服务，如imgbb、imgur等
        self.log('CDN方案: 当前Catbox.moe可能被API屏蔽，需要测试其他CDN')
        
        # 暂时返回None，需要主人提供可用的CDN方案
        return None
    
    def _base64_only_strategy(self, image_input: str, input_type: str, metadata: Dict[str, Any]) -> Tuple[Optional[str], Dict[str, Any]]:
        """只使用Base64策略"""
        base64_result = self._get_base64_url(image_input, input_type, metadata)
        if base64_result:
            base64_url, base64_len = base64_result
            
            if base64_len <= self.max_base64_length:
                metadata['steps'].append('Base64策略成功')
                metadata['success'] = True
                metadata['base64_length'] = base64_len
                self.log(f'Base64策略: 使用Base64 data URL (长度: {base64_len:,})')
                return base64_url, metadata
            else:
                metadata['error'] = f'Base64超限 ({base64_len:,} > {self.max_base64_length:,})'
                metadata['steps'].append('Base64策略失败: 超限')
                self.log(f'Base64策略失败: 超限')
        else:
            metadata['error'] = '无法获取Base64 URL'
            metadata['steps'].append('Base64策略失败')
            self.log('Base64策略失败')
        
        return None, metadata
    
    def _cdn_only_strategy(self, image_input: str, input_type: str, metadata: Dict[str, Any]) -> Tuple[Optional[str], Dict[str, Any]]:
        """只使用CDN策略"""
        cdn_url = self._get_cdn_url(image_input, input_type, metadata)
        if cdn_url:
            metadata['steps'].append('CDN策略成功')
            metadata['success'] = True
            self.log('CDN策略成功')
            return cdn_url, metadata
        else:
            metadata['error'] = 'CDN获取失败'
            metadata['steps'].append('CDN策略失败')
            self.log('CDN策略失败')
            return None, metadata
    
    def get_logs(self) -> str:
        """获取所有日志"""
        return '\n'.join(self.logs)
    
    def clear_logs(self):
        """清空日志"""
        self.logs = []


# 测试函数
def test_optimized_getter():
    """测试优化获取器"""
    print("测试优化版图片获取器")
    print("=" * 60)
    
    getter = OptimizedImageGetter()
    
    # 测试图片路径
    test_image = r"C:\Users\User\.openclaw\media\inbound\65dcfec4-72c0-47d3-84f2-a7c118730324.jpg"
    
    if not os.path.exists(test_image):
        print(f"[ERROR] 测试图片不存在: {test_image}")
        return
    
    print(f"[INFO] 测试图片: {test_image}")
    file_size = os.path.getsize(test_image)
    print(f"[INFO] 文件大小: {file_size:,} 字节 ({file_size/1024/1024:.2f} MB)")
    
    # 测试优化策略
    print("\n[测试优化策略]")
    url, metadata = getter.get_image_url(test_image, strategy='optimized')
    
    print(f"\n[结果]")
    print(f"成功: {metadata.get('success')}")
    print(f"步骤: {metadata.get('steps', [])}")
    
    if metadata.get('success'):
        print(f"URL类型: {'Base64' if url.startswith('data:') else 'HTTP'}")
        if url.startswith('data:'):
            print(f"Base64长度: {metadata.get('base64_length', 0):,} 字符")
            print(f"优化方案: {metadata.get('optimization_applied', '无')}")
        print(f"URL预览: {url[:80]}...")
    else:
        print(f"错误: {metadata.get('error')}")
    
    print("\n[日志]")
    print(getter.get_logs())

if __name__ == "__main__":
    test_optimized_getter()