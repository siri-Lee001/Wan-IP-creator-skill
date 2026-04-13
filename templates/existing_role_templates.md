# 已有角色专用模板库

## 🎯 模板设计原则

**基于分析，保持一致，智能扩展**:
1. **一致性优先**: 保持与原角色特征一致
2. **智能适配**: 基于分析结果自动适配模板
3. **质量保证**: 确保生成结果达到商业化标准
4. **扩展价值**: 显著扩展原角色的应用场景

## 🔧 模板参数系统

### 基础参数占位符
```python
# 从角色分析中提取的参数
base_params = {
    "{style}": "检测到的风格 (如: cyberpunk, ancient_chinese, cute)",
    "{character_type}": "角色类型 (如: human, animal, robot, fantasy)",
    "{color_scheme}": "色彩方案 (如: cool_tone, warm_tone, neon)",
    "{key_features}": "关键特征列表 (如: 银色短发、机械义体)",
    "{color_mood}": "色彩情绪 (如: energetic, calm, elegant)",
    "{quality_level}": "质量等级 (如: excellent, good, average)"
}
```

### 动态参数生成
```python
def generate_template_params(analysis_result):
    """基于分析结果生成模板参数"""
    params = {
        "style": analysis_result["detected_style"],
        "character_type": analysis_result["character_type"],
        "color_scheme": analysis_result["color_analysis"]["detected_color_scheme"],
        "key_features_text": format_features(analysis_result["key_features"]),
        "color_mood": analysis_result["color_analysis"]["detected_color_mood"],
        "quality_adjective": get_quality_adjective(analysis_result["quality_assessment"]["overall_score"])
    }
    return params
```

## 🎨 三视图生成模板

### 标准三视图模板
**适用场景**: 大多数角色类型
**模板内容**:
```
基于参考图生成标准三视图，即正面视角、侧面视角、背面视角。
保持{style}风格一致，{key_features_text}特征清晰。
线条流畅，结构准确，比例协调。
纯白背景，超级细节，专业设计标准。
使用{quality_adjective}质量渲染。
```

**参数填充示例**:
```
基于参考图生成标准三视图，即正面视角、侧面视角、背面视角。
保持赛博朋克风格一致，银色短发、机械义体、霓虹灯光特征清晰。
线条流畅，结构准确，比例协调。
纯白背景，超级细节，专业设计标准。
使用优秀质量渲染。
```

### 风格化三视图模板
**适用场景**: 特定风格强化
**模板内容**:
```
基于参考图生成{style}风格三视图。
强化{style}风格特征，如{style_specific_elements}。
保持{key_features_text}核心特征。
{color_scheme}色彩方案，{color_mood}情绪表达。
专业{style}风格设计，适合商业化应用。
```

**风格特定元素**:
- **赛博朋克**: 机械细节、霓虹灯光、数据界面
- **古风**: 传统纹样、水墨效果、古典构图
- **可爱**: 圆润线条、明亮色彩、萌系元素
- **科技**: 简洁线条、未来感、智能元素

## 🌈 风格转换模板

### 同风格强化模板
**适用场景**: 强化原有风格
**模板内容**:
```
将参考图角色强化为更强烈的{style}风格。
增加{style}典型元素，如{style_elements}。
提升{color_scheme}色彩方案的饱和度/对比度。
保持{key_features_text}特征识别度。
专业{style}风格插画，适合{target_application}。
```

### 跨风格转换模板
**适用场景**: 尝试不同风格
**模板内容**:
```
将参考图的{original_style}风格角色转换为{target_style}风格。
保持{key_features_text}核心特征不变。
使用{target_style}的典型表现手法，如{target_style_elements}。
{target_color_scheme}色彩方案，{target_color_mood}情绪。
专业风格转换，保持角色识别度。
```

**风格转换矩阵**:
| 原风格 → 目标风格 | 转换重点 |
|-----------------|----------|
| 赛博朋克 → 古风 | 机械→传统、霓虹→水墨、未来→古典 |
| 古风 → 赛博朋克 | 传统→机械、水墨→霓虹、古典→未来 |
| 可爱 → 科技 | 圆润→简洁、明亮→冷色、萌系→智能 |
| 写实 → 卡通 | 细节→简化、真实→夸张、复杂→简洁 |

## 🏃 动作延展模板

### 基础动作模板
**适用场景**: 日常动作延展
**模板内容**:
```
基于参考图角色，生成{action_count}个不同的{action_type}动作。
动作包括{action_list}。
保持{style}风格一致，{key_features_text}特征清晰。
动作自然流畅，表情生动恰当。
{background_setting}背景，适合{application_scenario}。
```

**动作类型库**:
- **日常动作**: 站立、行走、坐姿、挥手、打招呼
- **情绪动作**: 大笑、生气、伤心、困惑、惊喜
- **职业动作**: 工作、学习、运动、表演、创作
- **互动动作**: 拥抱、握手、击掌、对话、合作

### 风格化动作模板
**适用场景**: 风格特定动作
**模板内容**:
```
基于参考图的{style}风格角色，生成{action_count}个{style}风格动作。
动作体现{style}特色，如{style_action_elements}。
{key_features_text}特征在动作中自然呈现。
{color_scheme}色彩动态，{color_mood}情绪表达。
专业{style}动作设计，适合动画或游戏。
```

**风格动作元素**:
- **赛博朋克**: 数据交互、机械运动、霓虹特效
- **古风**: 传统礼仪、武术动作、古典舞姿
- **可爱**: 萌系动作、夸张表情、活泼姿态
- **科技**: 智能交互、未来感动作、科技特效

## 🛍️ 文创设计模板

### 产品设计模板
**适用场景**: 文创产品设计
**模板内容**:
```
基于参考图角色设计文创产品，包括{product_list}。
产品设计保持{style}风格，{key_features_text}特征清晰。
{color_scheme}色彩方案，{color_mood}情绪表达。
考虑实际生产可行性，设计美观实用。
适合{target_market}市场，具有商业价值。
```

**产品类型库**:
- **数码产品**: 手机壳、平板套、电脑贴纸、充电宝
- **服饰配件**: T恤、卫衣、帽子、背包、钥匙扣
- **生活用品**: 马克杯、水杯、抱枕、鼠标垫、笔记本
- **办公用品**: 文具套装、文件夹、便签纸、书签

### 应用场景模板
**适用场景**: 角色应用展示
**模板内容**:
```
展示参考图角色在{scene_count}个不同应用场景中的使用。
场景包括{scene_list}。
每个场景中角色自然融入，{key_features_text}特征保持。
{style}风格与环境协调，{color_scheme}色彩适配。
专业应用展示，适合商业推广。
```

**应用场景库**:
- **数字媒体**: 社交媒体头像、直播背景、视频贴纸
- **实体产品**: 产品包装、宣传物料、店面装饰
- **活动宣传**: 海报设计、活动吉祥物、宣传动画
- **品牌合作**: 联名产品、品牌形象、合作推广

## 😊 表情包制作模板

### 基础表情模板
**适用场景**: 通用表情包
**模板内容**:
```
基于参考图角色制作一套表情包，包括{expression_count}个表情。
表情包括{expression_list}。
保持{style}风格，{key_features_text}特征夸张表现。
表情生动夸张，易于识别，适合{platform}平台。
简洁背景，重点突出表情。
```

**表情库**:
- **基础情绪**: 😊微笑、😢伤心、😠生气、😮惊讶、😴困倦
- **社交互动**: 👍点赞、❤️爱心、🙏拜托、🎉庆祝、🤝合作
- **日常表达**: 💡想法、❓疑问、✅完成、⏰等待、🎯目标
- **趣味表达**: 🐶卖萌、🔥厉害、💪加油、🎨创意、🚀冲鸭

### 平台优化模板
**适用场景**: 特定平台优化
**模板内容**:
```
为{platform}平台优化设计表情包。
符合{platform}平台规范：{platform_specs}。
{expression_count}个表情，包括{platform_popular_expressions}。
{style}风格适配{platform}用户喜好。
文件格式和大小符合{platform}要求。
```

**平台规范**:
- **微信**: 240×240像素，GIF格式，≤100KB
- **QQ**: 200×200像素，GIF格式，≤200KB
- **抖音**: 多种尺寸，MP4/GIF，≤5MB
- **小红书**: 正方形比例，高清静态，适合图文

## 🎬 动态化处理模板

### 基础动画模板
**适用场景**: 简单动态化
**模板内容**:
```
让参考图的{animation_target}流畅自然地动起来。
动画类型：{animation_type}。
保持{style}风格一致，{key_features_text}特征动态自然。
动画流畅循环，节奏适中，适合{usage_scenario}。
技术实现符合{technical_requirements}。
```

**动画类型**:
- **简单动画**: 呼吸效果、轻微摆动、眨眼循环
- **中等动画**: 走路循环、简单动作、表情变化
- **复杂动画**: 完整动作序列、交互动画、特效动画

### 平台动态模板
**适用场景**: 平台动态内容
**模板内容**:
```
为{platform}平台创建动态内容。
内容类型：{content_type}。
基于参考图角色，{animation_description}。
符合{platform}动态内容规范：{platform_animation_specs}。
适合{platform}用户观看习惯，具有传播性。
```

**动态内容类型**:
- **短视频**: 15-60秒动态展示，故事性内容
- **动态贴纸**: 可交互动态元素，增强表达
- **动态壁纸**: 手机/电脑动态背景，个性化
- **互动内容**: 用户可参与的动态体验

## 🔧 技术参数模板

### 万相 4.5 参数模板
**基础参数**:
```json
{
  "model": "wanxiang-4.5",
  "width": 2048,
  "height": 2048,
  "steps": 30,
  "cfg_scale": 7.5,
  "sampler": "DPM++ 2M Karras",
  "seed": -1,
  "style_preset": "{style_preset}",
  "quality": "{quality_level}",
  "aspect_ratio": "{aspect_ratio}"
}
```

**风格预设映射**:
```python
style_preset_map = {
    "cyberpunk": "cyberpunk",
    "ancient_chinese": "anime",
    "cute": "cute", 
    "tech": "futuristic",
    "fantasy": "fantasy",
    "realistic": "realistic",
    "general": "general"
}
```

**质量等级映射**:
```python
quality_map = {
    "excellent": "high",
    "good": "high",
    "average": "medium",
    "poor": "low"
}
```

### 批量生成模板
**场景**: 需要生成多个变体
**模板**:
```python
batch_params = {
    "base_prompt": "{base_prompt}",
    "variations": [
        {"modifier": "版本1描述", "weight": 1.0},
        {"modifier": "版本2描述", "weight": 0.8},
        {"modifier": "版本3描述", "weight": 0.6}
    ],
    "common_params": {
        "model": "wanxiang-4.5",
        "width": 2048,
        "height": 2048,
        "steps": 30
    }
}
```

## 📊 质量控制模板

### 质量检查清单
```python
quality_checklist = {
    "一致性检查": [
        "风格与原图一致",
        "特征保持清晰",
        "色彩方案协调",
        "比例结构准确"
    ],
    "技术检查": [
        "分辨率达标",
        "文件格式正确",
        "文件大小合理",
        "渲染质量良好"
    ],
    "应用检查": [
        "适合目标应用",
        "具有商业价值",
        "符合平台规范",
        "用户体验良好"
    ]
}
```

### 质量评分模板
```python
def calculate_quality_score(analysis_result, generated_result):
    """计算质量评分"""
    scores = {
        "style_consistency": compare_style(analysis_result, generated_result),
        "feature_preservation": compare_features(analysis_result, generated_result),
        "technical_quality": assess_technical(generated_result),
        "application_value": assess_application(generated_result)
    }
    
    weights = {"style": 0.3, "features": 0.3, "technical": 0.2, "application": 0.2}
    overall_score = sum(scores[k] * weights[k] for k in scores)
    
    return {
        "dimension_scores": scores,
        "overall_score": round(overall_score, 2),
        "quality_level": get_quality_level(overall_score)
    }
```

## 🚀 快速使用指南

### 模板选择流程
```
分析结果 → 匹配模板 → 参数填充 → 生成执行 → 质量验证
```

### 模板匹配规则
1. **风格优先**: 选择与检测风格最匹配的模板
2. **特征适配**: 根据关键特征数量选择详细程度
3. **质量适配**: 根据质量等级选择参数精度
4. **应用导向**: 根据目标应用选择专用模板

### 参数填充示例
```python
# 输入: 分析结果
analysis = {
    "detected_style": "cyberpunk",
    "key_features": ["发型:银色短发", "服装:机械义体"],
    "color_scheme": "cool_tone",
    "quality_level": "excellent"
}

# 选择模板
template = select_template(analysis["detected_style"], "三视图")

# 填充参数
filled_template = template.format(
    style=analysis["detected_style"],
    key_features_text=format_features(analysis["key_features"]),
    color_scheme=analysis["color_scheme"],
    quality_adjective=get_quality_adjective(analysis["quality_level"])
)

# 输出: 填充后的提示词
print(filled_template)
```

---

**模板状态**: 完整可用
**版本**: 1.0.0
**最后更新**: 2026-03-28
**维护者**: 小狐狸助手