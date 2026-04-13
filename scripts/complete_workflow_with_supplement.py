#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整工作流脚本：现有工作流 + HTML生成 + 文件打包
最小改动原则：不修改现有工作流，只添加补充功能
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, Any

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_complete_workflow():
    """运行完整工作流（现有工作流 + 补充功能）"""
    print("=" * 60)
    print("万相IP技能完整工作流")
    print("=" * 60)
    
    # 参数配置
    role_image_path = input("请输入角色图片路径: ").strip()
    if not role_image_path:
        role_image_path = r"C:\Users\User\.openclaw\media\inbound\d3e6712e-0e04-4348-a240-a6f2a028ce6f.jpg"
        print(f"使用默认图片: {role_image_path}")
    
    role_name = input("请输入角色名称 [默认: 测试角色]: ").strip() or "测试角色"
    input_type = input("请输入输入类型 (single_character/three_views) [默认: single_character]: ").strip() or "single_character"
    output_dir = input("请输入输出目录 [默认: complete_output]: ").strip() or "complete_output"
    skip_video = input("是否跳过视频生成? (y/n) [默认: y]: ").strip().lower() == 'y'
    
    print("\n" + "=" * 60)
    print("配置确认:")
    print(f"  角色图片: {role_image_path}")
    print(f"  角色名称: {role_name}")
    print(f"  输入类型: {input_type}")
    print(f"  输出目录: {output_dir}")
    print(f"  跳过视频: {skip_video}")
    print("=" * 60)
    
    # 确认执行
    confirm = input("\n确认执行? (y/n): ").strip().lower()
    if confirm != 'y':
        print("取消执行")
        return
    
    print("\n" + "=" * 60)
    print("开始执行完整工作流")
    print("=" * 60)
    
    all_results = {}
    
    try:
        # 1. 执行现有工作流
        print("\n[阶段1] 执行现有工作流...")
        from real_workflow import RealWorkflow
        
        workflow = RealWorkflow(
            role_image_path=role_image_path,
            role_name=role_name,
            output_dir=output_dir,
            input_type=input_type
        )
        
        workflow_result = workflow.run_full_workflow(skip_video=skip_video)
        all_results["main_workflow"] = workflow_result
        
        print(f"✅ 现有工作流完成: {workflow_result.get('successful_steps', 0)}/{workflow_result.get('total_steps', 0)} 成功")
        
        # 2. 执行补充功能（HTML生成 + 文件打包）
        print("\n[阶段2] 执行补充功能...")
        from html_and_packaging_supplement import HTMLPackagingSupplement
        
        supplement = HTMLPackagingSupplement(
            output_dir=output_dir,
            role_name=role_name,
            input_type=input_type
        )
        
        supplement_result = supplement.run_supplement()
        all_results["supplement"] = supplement_result
        
        # 3. 生成最终报告
        print("\n[阶段3] 生成最终报告...")
        final_summary = {
            "role_name": role_name,
            "input_type": input_type,
            "output_dir": output_dir,
            "main_workflow_success": workflow_result.get("successful_steps", 0),
            "main_workflow_total": workflow_result.get("total_steps", 0),
            "html_success": supplement_result.get("html_success", False),
            "package_success": supplement_result.get("package_success", False),
            "total_success": supplement_result.get("total_success", False),
            "timestamp": datetime.now().isoformat(),
            "results": all_results
        }
        
        # 保存最终报告
        summary_path = os.path.join(output_dir, "complete_workflow_summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(final_summary, f, ensure_ascii=False, indent=2)
        
        # 生成文本报告
        report_path = os.path.join(output_dir, "complete_workflow_report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("万相IP技能完整工作流执行报告\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"执行时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n")
            f.write(f"角色名称: {role_name}\n")
            f.write(f"输入类型: {input_type}\n")
            f.write(f"输出目录: {output_dir}\n\n")
            
            f.write("[阶段1] 现有工作流结果:\n")
            f.write(f"  成功步骤: {workflow_result.get('successful_steps', 0)}/{workflow_result.get('total_steps', 0)}\n")
            f.write(f"  失败步骤: {workflow_result.get('failed_steps', 0)}\n\n")
            
            f.write("[阶段2] 补充功能结果:\n")
            f.write(f"  HTML生成: {'✅ 成功' if supplement_result.get('html_success') else '❌ 失败'}\n")
            f.write(f"  文件打包: {'✅ 成功' if supplement_result.get('package_success') else '❌ 失败'}\n\n")
            
            f.write("[输出文件]\n")
            f.write(f"  1. 图片文件: {output_dir}/images/\n")
            f.write(f"  2. JSON元数据: {output_dir}/json/\n")
            f.write(f"  3. HTML展示: {output_dir}/html/index.html\n")
            f.write(f"  4. 文件包: {output_dir}/packages/\n")
            f.write(f"  5. 日志文件: {output_dir}/logs/\n")
            f.write(f"  6. 视频文件: {output_dir}/video/\n\n")
            
            f.write("[使用说明]\n")
            f.write("  1. 打开 html/index.html 查看成果展示\n")
            f.write("  2. 下载 packages/ 目录下的ZIP文件获取完整成果包\n")
            f.write("  3. 查看 json/ 目录了解每个步骤的详细信息\n\n")
            
            f.write("=" * 60 + "\n")
            f.write("万相IP技能 v1.7.2 | 完整工作流执行完成\n")
            f.write("=" * 60 + "\n")
        
        print("\n" + "=" * 60)
        print("🎉 完整工作流执行完成！")
        print("=" * 60)
        print(f"\n📁 输出目录: {output_dir}")
        print(f"📊 工作流结果: {workflow_result.get('successful_steps', 0)}/{workflow_result.get('total_steps', 0)} 成功")
        print(f"🌐 HTML页面: {output_dir}/html/index.html")
        print(f"📦 文件包: {output_dir}/packages/")
        print(f"📝 完整报告: {output_dir}/complete_workflow_report.txt")
        print("\n" + "=" * 60)
        
        return final_summary
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保以下文件存在:")
        print("  - real_workflow.py (现有工作流)")
        print("  - html_and_packaging_supplement.py (补充功能)")
        return None
    except Exception as e:
        print(f"❌ 执行错误: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    run_complete_workflow()