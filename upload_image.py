#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上传图片到img402.dev获取公网URL
"""

import os
import requests
import base64

def upload_image(image_path):
    url = "https://img402.dev/api/upload"
    with open(image_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                return result.get("data", {}).get("url")
    return None

if __name__ == "__main__":
    image_path = "C:/Users/User/.openclaw/workspace/skills/siri-ip-series-wanxiang/output/giraffe_guochao_style.jpg"
    public_url = upload_image(image_path)
    print(f"公网URL: {public_url}")
