                <li><a href="./images/">所有图片文件夹</a></li>
                <li><a href="./json/">所有JSON配置文件</a></li>
                <li><a href="./logs/workflow.log">工作流日志</a></li>
                <li><a href="./兽人战士IP系列化设计.html">HTML页面(本文件)</a></li>
            </ul>
        </div>
    </div>
</body>
</html>"""
        
        html_path = os.path.join(self.output_dir, f"{self.role_name}IP系列化设计.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        self.log(f"HTML页面创建完成: {html_path}")
        return html_path
    
    def execute_all(self):
        """执行所有步骤"""
        self.log("开始执行所有工作流步骤")
        
        # 执行所有图片生成步骤
        for step in self.workflow_steps:
            result = self.execute_step(step)
            self.results[step["id"]] = result
            
            # 等待一下，避免API限制
            time.sleep(2)
        
        # 生成视频
        video_result = self.generate_video(self.role_image_path)
        self.results["video"] = video_result
        
        # 创建HTML
        html_path = self.create_html()
        
        # 保存总结果
        summary = {
            "role_name": self.role_name,
            "role_image": self.role_image_path,
            "output_dir": self.output_dir,
            "total_steps": len(self.workflow_steps),
            "completed_steps": sum(1 for r in self.results.values() if isinstance(r, dict) and r.get("success", False)),
            "results": self.results,
            "html_path": html_path,
            "completion_time": datetime.now().isoformat()
        }
        
        summary_path = os.path.join(self.output_dir, "summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        self.log(f"所有步骤执行完成! 总结文件: {summary_path}")
        return summary

# 主函数
def main():
    """主函数"""
    # 使用提供的角色三视图
    role_image_path = "C:\\Users\\User\\.openclaw\\media\\inbound\\1e67db41-51d5-45a1-8e75-a68d35f186eb.jpg"
    
    if not os.path.exists(role_image_path):
        print(f"错误: 角色图片不存在: {role_image_path}")
        return
    
    # 创建工作流
    workflow = RealWorkflow(
        role_image_path=role_image_path,
        role_name="兽人战士",
        output_dir="C:\\Users\\User\\.openclaw\\workspace\\orc_ip_real"
    )
    
    # 执行所有步骤
    try:
        summary = workflow.execute_all()
        print(f"\n✅ 工作流执行完成!")
        print(f"   输出目录: {summary['output_dir']}")
        print(f"   HTML页面: {summary['html_path']}")
        print(f"   完成步骤: {summary['completed_steps']}/{summary['total_steps']}")
        
    except Exception as e:
        print(f"\n❌ 工作流执行失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()