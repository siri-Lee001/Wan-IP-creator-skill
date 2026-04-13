# Wan-skills集成说明

## 📋 集成概述

**万相IP技能**现已完全集成**Wan-skills**官方技能包，所有生图及生视频动作统一使用Wan-skills处理。

## 🎯 集成目标

1. **统一技术栈**: 所有AI生成操作使用同一套技术方案
2. **解决权限问题**: 使用官方推荐的异步调用模式
3. **提高稳定性**: 基于官方代码，确保API调用的稳定性
4. **标准化流程**: 遵循Wan-skills的最佳实践

## 🔧 集成内容

### 1. 核心脚本集成
```
📁 scripts/
├── 📄 wan_skills_integrated.py      # Wan-skills集成适配器（主入口）
├── 📄 image-generation-editing.py   # Wan-skills官方图片生成脚本
├── 📄 check_wan_task_status.py      # 异步任务状态检查
└── 📄 file_to_oss.py                # 文件上传到OSS（备用）
```

### 2. 关键配置
```python
# Wan-skills标准请求头
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
    "X-DashScope-Async": "enable",           # 关键：启用异步
    "X-DashScope-OssResourceResolve": "enable"  # 关键：启用OSS资源解析
}
```

### 3. 异步调用流程
```
用户请求 → 压缩图片 → 调用Wan-skills异步API → 获取任务ID → 
轮询任务状态 → 任务完成 → 下载图片 → 发送给用户确认
```

## 🚀 已验证功能

### ✅ 图片生成（已验证）
- **模型**: `wan2.7-image`
- **调用方式**: 异步调用（`X-DashScope-Async: enable`）
- **验证状态**: ✅ 成功
- **任务ID示例**: `0e3a3bec-e22e-4ab2-bd9a-db36a3a38a1a`

### ✅ 视频生成（待验证）
- **模型**: `wan2.7-i2v`
- **调用方式**: 异步调用（`X-DashScope-Async: enable`）
- **验证状态**: ⏳ 待测试
- **参数**: 720P 5秒，无水印，开启prompt_extend

## 📊 集成优势

### 1. **权限问题解决**
- ✅ 支持异步调用权限
- ✅ 支持OSS资源解析权限
- ✅ 已验证API密钥可用性

### 2. **稳定性提升**
- ✅ 基于官方Wan-skills代码
- ✅ 异步调用避免超时问题
- ✅ 自动任务轮询机制

### 3. **标准化流程**
- ✅ 遵循官方最佳实践
- ✅ 统一的错误处理
- ✅ 标准化的请求/响应格式

### 4. **维护性**
- ✅ 代码结构清晰
- ✅ 易于调试和扩展
- ✅ 与官方更新保持同步

## 🛠️ 使用方式

### 基本调用
```python
from scripts.wan_skills_integrated import WanSkillsIntegrated

# 初始化适配器
adapter = WanSkillsIntegrated()

# 生成图片
image_urls = adapter.generate_image(
    prompt="国潮风格角色，红色为主色调",
    image_url=data_url,  # Base64 data URL
    size="2K",
    num_images=1
)

# 下载图片
if image_urls:
    adapter.download_image(image_urls[0], "output/image.jpg")
```

### 图片压缩
```python
# 自动压缩图片为Base64
data_url = adapter.compress_image_to_base64("input.jpg")
print(f"Base64长度: {len(data_url)}字符")  # 自动控制在API限制内
```

### 任务轮询
```python
# 手动轮询任务状态（适配器内部自动处理）
task_result = adapter._poll_task_status("task_id_here")
if task_result.get("status") == "SUCCEEDED":
    print("任务成功完成")
```

## 🔍 技术细节

### 1. **Base64长度控制**
- **API限制**: ≤61440字符
- **自动压缩**: 图片尺寸超过1024px时自动压缩
- **质量保持**: JPEG质量90%，保持视觉质量
- **格式**: `data:image/jpeg;base64,...`

### 2. **异步任务处理**
- **轮询间隔**: 3秒
- **最大轮询次数**: 30次（约90秒）
- **状态检查**: 自动检查任务状态变化
- **错误处理**: 完善的异常处理机制

### 3. **错误恢复**
- **网络超时**: 自动重试
- **API错误**: 详细错误信息输出
- **任务失败**: 明确的失败原因说明
- **连接问题**: 优雅降级处理

## 📝 配置要求

### 必需权限
1. **API密钥权限**:
   - `wan2.7-image` 模型权限
   - `wan2.7-i2v` 模型权限（视频生成）
   - 异步调用权限
   - OSS资源解析权限

2. **网络要求**:
   - 可访问 `dashscope.aliyuncs.com`
   - 支持HTTPS连接
   - 稳定的网络环境

### 环境变量
```bash
# 必需
export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 可选
export DASHSCOPE_REGION="beijing"  # beijing 或 singapore
export DASHSCOPE_BASE_URL="https://dashscope.aliyuncs.com/api/v1/"
```

## 🧪 测试验证

### 已执行的测试
1. **API连接测试**: ✅ 成功
2. **异步调用测试**: ✅ 成功（获取任务ID）
3. **任务轮询测试**: ✅ 成功（获取生成结果）
4. **图片下载测试**: ✅ 成功（保存到本地）
5. **Base64压缩测试**: ✅ 成功（控制在API限制内）

### 待测试功能
1. **视频生成测试**: ⏳ 待测试
2. **批量生成测试**: ⏳ 待测试
3. **错误场景测试**: ⏳ 待测试
4. **性能压力测试**: ⏳ 待测试

## 🚨 注意事项

### 1. **API密钥管理**
- 确保API密钥有正确的权限
- 定期检查密钥有效期
- 不要在代码中硬编码密钥

### 2. **成本控制**
- 异步调用可能产生额外成本
- 监控API使用量
- 设置使用限额

### 3. **网络稳定性**
- 异步调用对网络稳定性要求较高
- 确保有稳定的网络连接
- 考虑网络中断的恢复策略

### 4. **错误处理**
- 所有API调用都要有错误处理
- 记录详细的错误日志
- 提供用户友好的错误信息

## 🔮 未来规划

### 短期计划
1. **视频生成集成**: 完成wan2.7-i2v视频生成集成
2. **批量处理优化**: 支持批量图片生成
3. **错误处理增强**: 更完善的错误恢复机制

### 长期计划
1. **模型更新**: 跟进万相模型更新
2. **功能扩展**: 支持更多AI生成功能
3. **性能优化**: 提高生成速度和稳定性
4. **用户体验**: 更友好的交互界面

## 📞 支持与反馈

### 问题报告
1. **GitHub Issues**: 提交问题报告
2. **错误日志**: 提供详细的错误日志
3. **复现步骤**: 描述问题的复现步骤

### 功能建议
1. **功能需求**: 描述需要的功能
2. **使用场景**: 说明使用场景
3. **优先级**: 建议的优先级

### 贡献指南
1. **代码规范**: 遵循现有代码规范
2. **测试要求**: 新功能必须包含测试
3. **文档更新**: 更新相关文档

---

**集成状态**: ✅ 已完成图片生成部分集成

**最后更新**: 2026年4月12日

**维护团队**: 万相IP技能开发团队