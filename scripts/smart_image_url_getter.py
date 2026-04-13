#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能图片URL获取模块
三层策略：1.已有URL直接使用 2.Base64 data URL 3.备用免费图床
"""

import os
import re
import base64
import requests
import mimetypes
import time
from typing import Optional, Tuple, Dict, Any
from urllib.parse import urlparse


class SmartImageUrlGetter:
    """智能图片URL获取器"""
    
    def __init__(self, max_base64_length=61440, enable_free_cdn=True):
        """
        初始化智能获取器
        
        Args:
            max_base64_length: Base64最大长度限制（万相API限制）
            enable_free_cdn: 是否启用免费CDN备用方案
        """
        self.max_base64_length = max_base64_length
        self.enable_free_cdn = enable_free_cdn
        
        # 支持的图片扩展名
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp'}
        
        # URL模式检测
        self.url_pattern = re.compile(
            r'^(https?://|data:image/)'  # http/https或data URL
            r'([a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,})'  # 域名
            r'(:\d+)?'  # 端口
            r'(/[^\s]*)?$',  # 路径
            re.IGNORECASE
        )
        
        # data URL模式
        self.data_url_pattern = re.compile(r'^data:image/[a-zA-Z]+;base64,', re.IGNORECASE)
        
        # 日志
        self.logs = []
    
    def log(self, message: str):
        """记录日志"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f'[{timestamp}] {message}'
        self.logs.append(log_entry)
        print(log_entry)
    
    def detect_input_type(self, image_input: str) -> str:
        """
        检测输入类型
        
        Returns:
            'url': 公网URL
            'data_url': Base64 data URL
            'local_path': 本地文件路径
            'base64': 纯Base64字符串
            'unknown': 未知类型
        """
        # 1. 检查是否是data URL
        if self.data_url_pattern.match(image_input):
            self.log(f'检测到data URL输入，长度: {len(image_input)}')
            return 'data_url'
        
        # 2. 检查是否是URL
        if self.url_pattern.match(image_input):
            self.log(f'检测到URL输入: {image_input[:50]}...')
            return 'url'
        
        # 3. 检查是否是纯Base64（较长字符串）
        if len(image_input) > 1000 and self._looks_like_base64(image_input):
            self.log(f'检测到纯Base64输入，长度: {len(image_input)}')
            return 'base64'
        
        # 4. 检查是否是本地文件路径
        if os.path.exists(image_input):
            # 检查是否是图片文件
            ext = os.path.splitext(image_input)[1].lower()
            if ext in self.image_extensions:
                self.log(f'检测到本地图片文件: {image_input}')
                return 'local_path'
        
        self.log(f'未知输入类型: {image_input[:50]}...')
        return 'unknown'
    
    def _looks_like_base64(self, text: str) -> bool:
        """检查字符串是否像Base64编码"""
        # Base64字符集
        base64_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=')
        
        # 检查前100个字符
        sample = text[:100]
        base64_count = sum(1 for c in sample if c in base64_chars)
        
        # 如果90%以上是Base64字符，认为是Base64
        return base64_count / len(sample) > 0.9 if sample else False
    
    def get_image_url(self, image_input: str, strategy: str = 'auto') -> Tuple[Optional[str], Dict[str, Any]]:
        """
        获取图片URL（主函数）
        
        Args:
            image_input: 图片输入（本地路径、URL、Base64）
            strategy: 策略选择
                'auto': 自动选择最佳策略
                'url_only': 只使用URL（不转换）
                'base64_only': 只使用Base64
                'cdn_only': 只使用CDN
        
        Returns:
            (image_url, metadata)
        """
        metadata = {
            'input_type': 'unknown',
            'strategy_used': strategy,
            'success': False,
            'error': None,
            'steps': []
        }
        
        try:
            # 检测输入类型
            input_type = self.detect_input_type(image_input)
            metadata['input_type'] = input_type
            self.log(f'输入类型: {input_type}')
            
            # 策略选择
            if strategy == 'auto':
                return self._auto_strategy(image_input, input_type, metadata)
            elif strategy == 'url_only':
                return self._url_only_strategy(image_input, input_type, metadata)
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
    
    def _auto_strategy(self, image_input: str, input_type: str, metadata: Dict[str, Any]) -> Tuple[Optional[str], Dict[str, Any]]:
        """自动策略：URL → Base64 → CDN"""
        
        # 步骤1: 如果已经是URL，直接使用
        if input_type == 'url':
            metadata['steps'].append('使用已有URL')
            metadata['success'] = True
            self.log('策略1: 使用已有URL')
            return image_input, metadata
        
        # 步骤2: 如果已经是data URL，检查长度
        if input_type == 'data_url':
            if len(image_input) <= self.max_base64_length:
                metadata['steps'].append('使用data URL')
                metadata['success'] = True
                self.log(f'策略2: 使用data URL (长度: {len(image_input)})')
                return image_input, metadata
            else:
                metadata['steps'].append('data URL过长，尝试压缩')
                self.log(f'data URL过长 ({len(image_input)} > {self.max_base64_length})，尝试压缩')
        
        # 步骤3: 如果是本地文件，尝试转换为Base64
        if input_type == 'local_path':
            data_url = self._local_to_data_url(image_input, metadata)
            if data_url and len(data_url) <= self.max_base64_length:
                metadata['steps'].append('本地文件转Base64成功')
                metadata['success'] = True
                self.log(f'策略3: 本地文件转Base64成功 (长度: {len(data_url)})')
                return data_url, metadata
            elif data_url:
                metadata['steps'].append('Base64过长，需要CDN')
                self.log(f'Base64过长 ({len(data_url)} > {self.max_base64_length})，需要CDN')
        
        # 步骤4: 如果是纯Base64，检查长度
        if input_type == 'base64':
            data_url = f'data:image/jpeg;base64,{image_input}'
            if len(data_url) <= self.max_base64_length:
                metadata['steps'].append('使用纯Base64')
                metadata['success'] = True
                self.log(f'策略4: 使用纯Base64 (长度: {len(data_url)})')
                return data_url, metadata
            else:
                metadata['steps'].append('Base64过长，需要CDN')
                self.log(f'Base64过长 ({len(data_url)} > {self.max_base64_length})，需要CDN')
        
        # 步骤5: 使用免费CDN备用方案
        if self.enable_free_cdn:
            cdn_url = self._upload_to_free_cdn(image_input, input_type, metadata)
            if cdn_url:
                metadata['steps'].append('使用免费CDN成功')
                metadata['success'] = True
                self.log(f'策略5: 使用免费CDN成功: {cdn_url}')
                return cdn_url, metadata
        
        # 所有策略都失败
        metadata['error'] = '所有图片URL获取策略均失败'
        metadata['steps'].append('所有策略失败')
        self.log('所有图片URL获取策略均失败')
        return None, metadata
    
    def _url_only_strategy(self, image_input: str, input_type: str, metadata: Dict[str, Any]) -> Tuple[Optional[str], Dict[str, Any]]:
        """只使用URL策略"""
        if input_type == 'url':
            metadata['steps'].append('URL策略: 使用已有URL')
            metadata['success'] = True
            self.log('URL策略: 使用已有URL')
            return image_input, metadata
        else:
            metadata['error'] = f'输入类型不是URL: {input_type}'
            metadata['steps'].append('URL策略失败')
            self.log(f'URL策略失败: 输入类型不是URL')
            return None, metadata
    
    def _base64_only_strategy(self, image_input: str, input_type: str, metadata: Dict[str, Any]) -> Tuple[Optional[str], Dict[str, Any]]:
        """只使用Base64策略"""
        # 如果是本地文件，转换为Base64
        if input_type == 'local_path':
            data_url = self._local_to_data_url(image_input, metadata)
            if data_url:
                metadata['steps'].append('Base64策略: 本地文件转Base64')
                metadata['success'] = True
                self.log('Base64策略: 本地文件转Base64成功')
                return data_url, metadata
        
        # 如果是纯Base64，包装为data URL
        elif input_type == 'base64':
            data_url = f'data:image/jpeg;base64,{image_input}'
            metadata['steps'].append('Base64策略: 使用纯Base64')
            metadata['success'] = True
            self.log('Base64策略: 使用纯Base64')
            return data_url, metadata
        
        # 如果是data URL，直接使用
        elif input_type == 'data_url':
            metadata['steps'].append('Base64策略: 使用data URL')
            metadata['success'] = True
            self.log('Base64策略: 使用data URL')
            return image_input, metadata
        
        else:
            metadata['error'] = f'无法转换为Base64: {input_type}'
            metadata['steps'].append('Base64策略失败')
            self.log(f'Base64策略失败: 无法转换类型 {input_type}')
            return None, metadata
    
    def _cdn_only_strategy(self, image_input: str, input_type: str, metadata: Dict[str, Any]) -> Tuple[Optional[str], Dict[str, Any]]:
        """只使用CDN策略"""
        if not self.enable_free_cdn:
            metadata['error'] = '免费CDN未启用'
            metadata['steps'].append('CDN策略失败: 未启用')
            self.log('CDN策略失败: 免费CDN未启用')
            return None, metadata
        
        cdn_url = self._upload_to_free_cdn(image_input, input_type, metadata)
        if cdn_url:
            metadata['steps'].append('CDN策略: 上传成功')
            metadata['success'] = True
            self.log('CDN策略: 上传成功')
            return cdn_url, metadata
        else:
            metadata['error'] = 'CDN上传失败'
            metadata['steps'].append('CDN策略失败')
            self.log('CDN策略失败: 上传失败')
            return None, metadata
    
    def _local_to_data_url(self, image_path: str, metadata: Dict[str, Any]) -> Optional[str]:
        """本地文件转换为Base64 data URL"""
        try:
            # 检测MIME类型
            mime_type, _ = mimetypes.guess_type(image_path)
            if not mime_type or not mime_type.startswith('image/'):
                mime_type = 'image/jpeg'
            
            # 读取文件
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # 转换为Base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            data_url = f'data:{mime_type};base64,{image_base64}'
            
            metadata['file_size'] = len(image_data)
            metadata['base64_length'] = len(image_base64)
            metadata['data_url_length'] = len(data_url)
            
            self.log(f'本地文件转换: {image_path} → Base64 ({len(image_base64)}字符)')
            return data_url
            
        except Exception as e:
            metadata['error'] = f'本地文件转Base64失败: {e}'
            self.log(f'本地文件转Base64失败: {e}')
            return None
    
    def _upload_to_free_cdn(self, image_input: str, input_type: str, metadata: Dict[str, Any]) -> Optional[str]:
        """
        上传到免费CDN（Catbox.moe - 已验证可用）
        使用litterbox.catbox.moe临时存储（24小时）
        """
        try:
            self.log('尝试使用免费CDN (Catbox.moe)')
            
            # 准备本地文件路径
            local_path = None
            
            if input_type == 'local_path':
                local_path = image_input
            elif input_type in ['base64', 'data_url', 'unknown']:
                # 需要先保存为本地文件
                temp_path = self._save_to_temp_file(image_input, input_type, metadata)
                if temp_path:
                    local_path = temp_path
                    metadata['temp_file'] = temp_path
                else:
                    metadata['error'] = '无法创建临时文件'
                    return None
            
            if not local_path or not os.path.exists(local_path):
                metadata['error'] = f'本地文件不存在: {local_path}'
                return None
            
            # 调用Catbox上传
            cdn_url = self._upload_to_catbox(local_path, metadata)
            
            # 清理临时文件
            if 'temp_file' in metadata and os.path.exists(metadata['temp_file']):
                try:
                    os.remove(metadata['temp_file'])
                    self.log(f'清理临时文件: {metadata["temp_file"]}')
                except:
                    pass
            
            return cdn_url
            
        except Exception as e:
            metadata['error'] = f'CDN上传失败: {e}'
            self.log(f'CDN上传失败: {e}')
            return None
    
    def _save_to_temp_file(self, image_input: str, input_type: str, metadata: Dict[str, Any]) -> Optional[str]:
        """将非本地文件输入保存为临时文件"""
        import tempfile
        import base64
        
        try:
            # 创建临时文件
            temp_dir = tempfile.gettempdir()
            temp_filename = f'catbox_upload_{int(time.time())}.jpg'
            temp_path = os.path.join(temp_dir, temp_filename)
            
            if input_type == 'data_url':
                # 提取Base64部分
                if 'base64,' in image_input:
                    base64_str = image_input.split('base64,', 1)[1]
                    image_data = base64.b64decode(base64_str)
                else:
                    metadata['error'] = '无效的data URL格式'
                    return None
                    
            elif input_type == 'base64':
                # 直接解码Base64
                image_data = base64.b64decode(image_input)
                
            else:
                metadata['error'] = f'无法处理的输入类型: {input_type}'
                return None
            
            # 保存文件
            with open(temp_path, 'wb') as f:
                f.write(image_data)
            
            self.log(f'创建临时文件: {temp_path} ({len(image_data)}字节)')
            return temp_path
            
        except Exception as e:
            metadata['error'] = f'创建临时文件失败: {e}'
            self.log(f'创建临时文件失败: {e}')
            return None
    
    def _upload_to_catbox(self, local_path: str, metadata: Dict[str, Any]) -> Optional[str]:
        """上传到Catbox.moe（使用litterbox临时存储）"""
        try:
            self.log(f'上传到Catbox.moe: {local_path}')
            
            # 导入Catbox上传模块
            catbox_skill_path = r'C:\Users\User\.openclaw\workspace\skills\catbox-upload'
            if not os.path.exists(catbox_skill_path):
                metadata['error'] = f'Catbox技能未安装: {catbox_skill_path}'
                self.log('错误: Catbox技能未安装')
                return None
            
            # 添加路径到sys.path
            import sys
            sys.path.append(catbox_skill_path)
            
            # 导入上传函数
            from upload import upload_to_litterbox
            
            # 上传文件（使用litterbox，24小时有效期）
            cdn_url = upload_to_litterbox(local_path, time="24h")
            
            metadata['cdn_method'] = 'catbox.moe (litterbox)'
            metadata['cdn_url'] = cdn_url
            metadata['cdn_expiry'] = '24小时'
            
            self.log(f'Catbox上传成功: {cdn_url}')
            return cdn_url
            
        except ImportError as e:
            metadata['error'] = f'无法导入Catbox模块: {e}'
            self.log(f'导入Catbox模块失败: {e}')
            
            # 备用方案：直接调用命令行
            return self._upload_to_catbox_cli(local_path, metadata)
            
        except Exception as e:
            metadata['error'] = f'Catbox上传异常: {e}'
            self.log(f'Catbox上传异常: {e}')
            return None
    
    def _upload_to_catbox_cli(self, local_path: str, metadata: Dict[str, Any]) -> Optional[str]:
        """通过命令行调用Catbox上传（备用方案）"""
        try:
            self.log(f'通过命令行上传到Catbox: {local_path}')
            
            import subprocess
            import sys
            
            catbox_script = r'C:\Users\User\.openclaw\workspace\skills\catbox-upload\upload.py'
            
            if not os.path.exists(catbox_script):
                metadata['error'] = f'Catbox脚本不存在: {catbox_script}'
                return None
            
            # 执行上传命令
            cmd = [sys.executable, catbox_script, local_path, '--service', 'litterbox', '--time', '24h']
            
            self.log(f'执行命令: {" ".join(cmd)}')
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                cdn_url = result.stdout.strip()
                if cdn_url.startswith('http'):
                    metadata['cdn_method'] = 'catbox.moe (cli)'
                    metadata['cdn_url'] = cdn_url
                    self.log(f'命令行上传成功: {cdn_url}')
                    return cdn_url
                else:
                    metadata['error'] = f'无效的URL返回: {cdn_url}'
            else:
                metadata['error'] = f'命令行上传失败: {result.stderr}'
                
        except Exception as e:
            metadata['error'] = f'命令行上传异常: {e}'
        
        return None
    
    def get_logs(self) -> str:
        """获取所有日志"""
        return '\n'.join(self.logs)
    
    def clear_logs(self):
        """清空日志"""
        self.logs = []


# 使用示例（仅用于说明，不执行）
def example_usage():
    """使用示例（不执行）"""
    getter = SmartImageUrlGetter()
    
    # 示例1: 本地文件
    local_image = '/path/to/image.jpg'
    url1, meta1 = getter.get_image_url(local_image, strategy='auto')
    
    # 示例2: 公网URL
    web_url = 'https://example.com/image.jpg'
    url2, meta2 = getter.get_image_url(web_url, strategy='auto')
    
    # 示例3: 纯Base64
    with open('/path/to/image.jpg', 'rb') as f:
        base64_str = base64.b64encode(f.read()).decode('utf-8')
    url3, meta3 = getter.get_image_url(base64_str, strategy='auto')
    
    print(getter.get_logs())


if __name__ == '__main__':
    print('智能图片URL获取模块 - 仅用于代码分析，不执行测试')
    print('=' * 60)
    print('模块功能:')
    print('1. 自动检测图片输入类型')
    print('2. 三层策略: URL → Base64 → 免费CDN')
    print('3. 支持多种策略选择')
    print('4. 详细日志记录')
    print('=' * 60)
    print('注意: 不执行任何API调用或测试')