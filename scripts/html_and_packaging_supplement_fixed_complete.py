            # 计算文件大小
            file_size = os.path.getsize(zip_path)
            file_size_mb = file_size / (1024 * 1024)
            
            result = {
                "success": True,
                "zip_path": zip_path,
                "zip_filename": zip_filename,
                "file_count": len(added_files),
                "file_size_mb": round(file_size_mb, 2),
                "timestamp": datetime.now().isoformat()
            }
            
            # 保存结果到JSON
            json_path = os.path.join(self.output_dir, "json", "step_package.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 文件包创建完成: {zip_path}")
            print(f"   包含 {len(added_files)} 个文件, {round(file_size_mb, 2)} MB")
            return result
            
        except Exception as e:
            print(f"❌ 文件包创建失败: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def run_supplement(self) -> Dict[str, Any]:
        """运行补充功能（HTML生成 + 文件打包）"""
        print("=" * 50)
        print("运行HTML生成和文件打包补充功能（修正版）")
        print("=" * 50)
        
        results = {}
        
        # 1. 生成HTML（包含图片和视频）
        html_result = self.generate_html()
        results["html"] = html_result
        
        if not html_result.get("success", False):
            print("⚠️ HTML生成失败，继续尝试打包...")
        
        # 2. 创建文件包（包含图片和视频）
        package_result = self.create_package()
        results["package"] = package_result
        
        # 汇总结果
        summary = {
            "html_success": html_result.get("success", False),
            "package_success": package_result.get("success", False),
            "total_success": html_result.get("success", False) and package_result.get("success", False),
            "image_count": html_result.get("image_count", 0),
            "video_count": html_result.get("video_count", 0),
            "total_files": html_result.get("image_count", 0) + html_result.get("video_count", 0),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
        # 保存汇总
        summary_path = os.path.join(self.output_dir, "json", "supplement_summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print("=" * 50)
        print("补充功能执行完成（修正版）")
        print(f"HTML生成: {'✅ 成功' if html_result.get('success') else '❌ 失败'}")
        print(f"文件打包: {'✅ 成功' if package_result.get('success') else '❌ 失败'}")
        print(f"图片数量: {html_result.get('image_count', 0)}张")
        print(f"视频数量: {html_result.get('video_count', 0)}个")
        print(f"总文件数: {summary['total_files']}个")
        print("=" * 50)
        
        return summary

if __name__ == "__main__":
    # 示例用法
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
        role_name = sys.argv[2] if len(sys.argv) > 2 else "测试角色"
        input_type = sys.argv[3] if len(sys.argv) > 3 else "single_character"
    else:
        # 默认值
        output_dir = "real_output"
        role_name = "测试角色"
        input_type = "single_character"
    
    # 运行补充功能
    supplement = HTMLPackagingSupplementFixed(output_dir, role_name, input_type)
    result = supplement.run_supplement()
    
    if result.get("total_success", False):
        print("🎉 所有补充功能执行成功！")
        print(f"HTML页面: {output_dir}/html/index.html")
        print(f"文件包: {output_dir}/packages/")
        print(f"包含: {result.get('image_count', 0)}张图片 + {result.get('video_count', 0)}个视频")
    else:
        print("⚠️ 部分功能执行失败，请检查日志")