# 万相IP技能包结构说明

## 📁 目录结构

```
siri-ip-series-wanxiang/
├── 📄 SKILL_FIXED_NEW.md          # 技能文档（核心）
├── 📄 README_NEW.md               # 使用说明文档
├── 📄 PACKAGE_STRUCTURE.md        # 包结构说明（本文件）
├── 📄 .env.example                # 环境变量模板
├── 📄 requirements.txt            # Python依赖
├── 📁 scripts/                    # 脚本目录
│   ├── 📄 wan_skills_integrated.py    # Wan-skills集成适配器（核心）
│   ├── 📄 wan_skills_video.py         # 视频生成适配器
│   ├── 📄 workflow_executor.py        # 工作流执行器
│   └── 📄 test_api_connectivity.py    # API连通性测试
├── 📁 examples/                   # 示例文件目录
│   ├── 📄 sample_character.jpg    # 示例角色图
│   └── 📁 sample_output/          # 示例输出目录
└── 📁 output/                     # 输出目录（自动创建）
```

## 📄 文件说明

### 核心文档
1. **SKILL_FIXED_NEW.md** - 技能核心文档
   - 技能描述和使用场景
   - 前置确认对话流程
   - 三种输入场景的工作流
   - 技术栈配置和API调用规范
   - 版本历史

2. **README_NEW.md** - 详细使用说明
   - 快速开始指南
   - 环境配置说明
   - 核心组件介绍
   - 使用流程示例
   - 故障排除指南

3. **PACKAGE_STRUCTURE.md** - 包结构说明（本文件）
   - 目录结构说明
   - 文件功能说明
   - 使用指南

### 配置文件
4. **.env.example** - 环境变量模板
   - API密钥配置
   - 模型参数配置
   - 工作流配置
   - 输出配置

5. **requirements.txt** - Python依赖
   - 核心依赖包
   - 版本要求

### 核心脚本
6. **scripts/wan_skills_integrated.py** - Wan-skills集成适配器
   - 基于官方Wan-skills代码
   - 支持异步图片生成
   - 任务轮询机制
   - 图片压缩和Base64转换
   - 错误处理和重试机制

7. **scripts/wan_skills_video.py** - 视频生成适配器
   - 基于Wan2.7-i2v模型
   - 异步视频生成
   - 固定参数：5秒 720P 无水印
   - 智能特性：thinking_mode + prompt_extend

8. **scripts/workflow_executor.py** - 工作流执行器
   - 自动化执行全流程
   - 支持三种输入场景
   - 分步确认模式
   - 状态管理和错误恢复

9. **scripts/test_api_connectivity.py** - API连通性测试
   - 测试API密钥有效性
   - 测试网络连接
   - 测试模型权限

### 示例和输出
10. **examples/** - 示例文件目录
    - 示例输入图片
    - 示例输出结果

11. **output/** - 输出目录
    - 自动创建
    - 存储生成的结果文件

## 🚀 快速使用指南

### 1. 环境准备
```bash
# 克隆或复制技能包
cd siri-ip-series-wanxiang

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入您的API密钥
```

### 2. 测试API连通性
```bash
python scripts/test_api_connectivity.py
```

### 3. 使用技能
```python
# 示例代码
from scripts.wan_skills_integrated import WanSkillsIntegrated
from scripts.workflow_executor import WanIPWorkflowExecutor

# 初始化适配器
adapter = WanSkillsIntegrated()

# 生成图片
image_urls = adapter.generate_image(
    prompt="国潮风格角色",
    size="2K",
    num_images=1
)

# 或使用工作流执行器
executor = WanIPWorkflowExecutor()
executor.set_input_image("input.jpg")
result = executor.execute_workflow(
    workflow_type="single_character",
    step_by_step=True,
    confirm_each=True
)
```

## 🔧 技术特性

### Wan-skills集成
- ✅ 基于官方Wan-skills代码
- ✅ 异步调用模式（X-DashScope-Async: enable）
- ✅ OSS资源解析（X-DashScope-OssResourceResolve: enable）
- ✅ 任务轮询机制
- ✅ 完善的错误处理

### 模型配置
- **图片生成**：wan2.7-image
- **视频生成**：wan2.7-i2v
- **固定参数**：
  - 图片：2K分辨率，无水印，开启thinking_mode
  - 视频：5秒 720P，无水印，开启prompt_extend和thinking_mode

### 工作流支持
- **场景1**：三视图输入 → 直接扩展
- **场景2**：单角色图输入 → 先生成三视图 → 再扩展
- **场景3**：文字描述输入 → 先生成角色图 → 再生成三视图 → 最后扩展

## 📊 输出内容

### 三视图输入场景（8件素材）
1. 风格转换：3张（国潮、Q版、水彩简化）
2. 动作延伸：1张（九合一动作大图）
3. 文创设计：1张（九合一产品大图）
4. 表情包：1张（九合一表情大图）
5. 动态视频：1个（5秒 720P）
6. 展示页面：1个（HTML）

### 单角色图输入场景（9件素材）
1. 三视图生成：1张
2. + 三视图输入场景所有8件素材

### 文字描述输入场景（12件素材）
1. 角色图生成：3张不同风格
2. 三视图生成：1张
3. + 三视图输入场景所有8件素材

## 💰 成本预估

基于万相API计费规则：
- **图片生成**：约0.1元/张（2K分辨率）
- **视频生成**：约1.0元/个（5秒 720P）

**场景成本估算**：
- 场景1（8件素材）：约1.8元
- 场景2（9件素材）：约1.9元  
- 场景3（12件素材）：约2.2元

## 🐛 故障排除

### 常见问题
1. **API调用返回403错误**
   - 检查API密钥权限
   - 检查是否开通异步调用权限
   - 检查是否开通OSS资源解析权限

2. **Base64 data URL过长**
   - 使用压缩功能自动处理
   - 调整图片尺寸和质量

3. **任务轮询超时**
   - 增加轮询次数
   - 检查网络连接

4. **视频生成失败**
   - 确保使用单角色正面主体图
   - 禁止使用三视图、组合图

### 调试工具
```bash
# 测试API连通性
python scripts/test_api_connectivity.py

# 测试图片生成
python -c "from scripts.wan_skills_integrated import WanSkillsIntegrated; adapter = WanSkillsIntegrated(); adapter.generate_image('测试', size='1K')"

# 测试视频生成
python -c "from scripts.wan_skills_video import WanSkillsVideo; adapter = WanSkillsVideo(); print('视频适配器初始化成功')"
```

## 📝 版本信息

### v1.7.3 (2026.04.12 Wan-skills集成版)
- ✅ 所有生图及生视频动作统一使用万相skill处理
- ✅ 基于官方Wan-skills代码的集成适配器
- ✅ 统一使用异步调用模式
- ✅ 解决API权限问题
- ✅ 固定视频参数：5秒 720P 无水印
- ✅ 开启智能特性：thinking_mode + prompt_extend
- ✅ 完全更新技能文档

### 系统要求
- Python 3.8+
- 阿里云万相API访问权限
- 至少2GB可用内存

## 📞 支持

如有问题或建议，请参考：
- **技能文档**：SKILL_FIXED_NEW.md
- **使用说明**：README_NEW.md
- **API文档**：阿里云DashScope官方文档

---

**最后更新**: 2026年4月12日  
**版本**: v1.7.3 (Wan-skills集成版)  
**状态**: ✅ 生产就绪