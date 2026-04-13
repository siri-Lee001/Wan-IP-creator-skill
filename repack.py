#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import zipfile

output_dir = "C:/Users/User/.openclaw/workspace/skills/siri-ip-series-wanxiang/output"
zip_path = "C:/Users/User/.openclaw/workspace/skills/siri-ip-series-wanxiang/长颈鹿IP全量素材包.zip"

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file == "step1_character_3view.jpg":
                continue  # 跳过无关图片
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, output_dir)
            zipf.write(file_path, arcname)
            print(f"已添加: {arcname}")

print(f"\n✅ 打包完成！压缩包路径: {zip_path}")
print(f"📦 压缩包大小: {os.path.getsize(zip_path) / 1024 / 1024:.2f} MB")
