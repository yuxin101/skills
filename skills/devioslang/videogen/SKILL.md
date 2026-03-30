---
name: videogen
description: 视频号AI短视频自动化生产流水线（v2）。用户说"做视频"、"生成视频"、"短视频制作"、"视频混剪"时触发。支持三种内容模式自动切换（Mode A纯干货 / Mode B剧情+科普 / Mode C漫剧型）。使用 MiniMax Hailuo AI 生成视频片段，配合 FFmpeg 混剪，输出适合视频号发布的完整短视频。
---

# videogen v2 — 视频号 AI 短视频自动化生产流水线

## ⚠️ 重要前置说明

### API 体系

| API Key 类型 | 开头 | 支持能力 |
|-------------|------|---------|
| MiniMax Key | `sk-cp-` | TTS (speech-2.8-hd) ✅、Hailuo 视频生成 ✅、Music ❌ |
| IMA Key | `ima_` | SeeDream 生图、Wan/Kling 视频（数字分身必需） |

**每日额度**：`usage limit exceeded` (2056) 报错表示当日 Hailuo 视频额度耗尽，需次日恢复。当前 key 不支持 music-2.5+。

### API 错误处理规范

```
错误码      含义                    处理
─────────────────────────────────────────────────────────────
2056       usage limit exceeded   跳过该片段继续后续步骤
其他异常    未知错误               记录错误，换策略继续，不卡死
```

---

## 三种内容模式

系统根据**选题自动判断**最优内容模式（可手动指定覆盖）：

### Mode A — 纯干货型
**适用**：财经分析、技术教程、行业报告、数据解读、科普讲解

**结构**：开场痛点(3s) → 核心要点×3(各12s) → 金句收尾(9s)

**视觉**：PPT/图表为主，AI点缀关键帧（数字动画、光芒效果）

```
开场 → 数据页 → 讲解页 → 数据页 → 讲解页 → 数据页 → 讲解页 → 金句
```

### Mode B — 剧情+科普型 ✨ 新版主打
**适用**：职业发展、认知升级、社会洞察、励志干货

**结构**：剧情钩子(8s) → 问题拆解(15s) → 干货×2(各12s) → 升华收尾(10s)

**视觉**：剧情画面 + 干净科普画面混合，兼顾情感共鸣与信息密度

```
剧情开场(困境) → 问题拆解 → 剧情演绎+干货 → 剧情演绎+干货 → 升华+关注引导
```

### Mode C — 漫剧/剧情型
**适用**：人生转折、励志逆袭、情感故事、人情冷暖

**结构**：起(8s) → 承(12s) → 转(20s) → 合(8s) + 金句收尾

**视觉**：角色全程驱动，强戏剧冲突，色调/情绪变化明显

```
建立(平凡) → 转折(至暗) → 挣扎 → 行动序列×3 → 蜕变(成功) → 金句
```

---

## 增强版分镜字段

```json
{
  "panel_number": 1,
  "scene_type": "剧情场景 | 知识讲解 | 数据展示 | 过渡页",
  "shot_type": "特写 | 近景/中景 | 中景 | 全景 | 远景/建立景 | POV主观视角",
  "camera_move": "固定镜头 | 推进 | 拉出 | 左摇 | 右摇 | 上摇 | 下摇 | 移动摄影 | 跟随",
  "description": "画面文字描述（供PPT/绘图AI使用）",
  "video_prompt": "Hailuo视频生成Prompt（镜头控制+主体+氛围+动态+风格）",
  "narration": "旁白/台词",
  "duration": 5,
  "transition": "硬切 | 淡入淡出 | 溶解 | 滑入"
}
```

**Video Prompt 公式**（参考《AIGC短视频策划与制作》）：
```
镜头描述 + 镜头运动 + 主体内容 + 动态元素 + 风格 + 9:16竖屏
```

---

## 使用方式

### 方式一：直接对话（推荐）

直接告诉我选题或发链接，我来判断模式并执行完整流水线：
```
python scripts/v2/run_pipeline.py gen "选题内容"
python scripts/v2/run_pipeline.py gen "https://mp.weixin.qq.com/s/xxx"   # 微信文章
python scripts/v2/run_pipeline.py gen "https://zhuanlan.zhihu.com/p/xxx" # 知乎文章
```

### URL 内容提取

支持自动识别并提取以下来源的正文内容：

| 来源 | 支持状态 | 提取内容 |
|------|---------|---------|
| 微信公众号文章 | ✅ 完整支持 | 标题、作者、正文 |
| 知乎文章/回答 | ✅ 完整支持 | 标题、作者、发布时间、正文 |
| 通用网页 | ✅ 支持（BS4） | 标题、正文（trafilatura 更优）|

```bash
# 单独测试 URL 提取
python scripts/v2/url_extractor.py "https://mp.weixin.qq.com/s/xxx"
python scripts/v2/url_extractor.py "https://zhuanlan.zhihu.com/p/xxx" --summarize

# 提取 + 生成摘要 + 生成分镜（管道）
python scripts/v2/url_extractor.py "URL" --summarize -o extracted.json
```

### 方式二：分步执行

```bash
# Step 1: 分析选题（自动检测模式）
python scripts/v2/run_pipeline.py analyze "AI将取代哪些职业"

# Step 2: 生成分镜（可指定模式）
python scripts/v2/run_pipeline.py storyboard "失业后的逆袭之路" --mode auto

# Step 3: 完整流水线
python scripts/v2/run_pipeline.py gen "选题" --mode auto --duration 60
```

### 方式三：旧版快速模式（兼容）

```bash
bash skills/videogen/scripts/build_composite.sh [slide_video] [output] [clips...]
```

---

## 完整流水线（v2）

```
选题 → [自动模式检测] → 分镜生成 → TTS配音 → AI视频片段 → FFmpeg混剪 → 最终视频
```

### Step 1: 选题分析

自动检测三要素：
- **剧情关键词**：失业/逆袭/情感/故事/第一人称经历 → Mode C
- **混合关键词**：职场/认知/赚钱/成长 → Mode B
- **干货关键词**：教程/数据/科普/技术/行业报告 → Mode A

### Step 2: 增强分镜生成（参考 waoowaoo 多阶段架构）

- **Phase 1**：结构规划（镜头数量、景别、场景类型）
- **Phase 2**：运镜+表演（cinematography + acting 并行）
- **Phase 3**：细节补充 + video_prompt 生成

### Step 3: TTS 配音

```bash
python skills/minimax-multimodal/scripts/tts/generate_voice.py tts \
  "$(cat narration_text)" \
  -v female-shaonv \
  -o minimax-output/voiceover.mp3
```

### Step 4: AI 视频片段（Hailuo）

```bash
# t2v（文生视频）— 知识/剧情场景
python skills/minimax-multimodal/scripts/video/generate_video.py \
  --mode t2v \
  --prompt "medium shot, slow push-in, ... modern cinematic, 9:16 vertical" \
  --duration 6 \
  --output minimax-output/clips/clip_01.mp4

# i2v（图生视频）— 关键帧动画化
python skills/minimax-multimodal/scripts/video/generate_video.py \
  --mode i2v \
  --prompt "subtle character movement, natural breathing..." \
  --first-frame minimax-output/slides/slide_NN.png \
  --duration 6 \
  --output minimax-output/clips/clip_NN.mp4
```

### Step 5: FFmpeg 混剪

```bash
# overlay 模式（AI片段嵌入PPT视频）
ffmpeg -y \
  -stream_loop 1 -i minimax-output/video_pure_slides.mp4 \
  -i minimax-output/clips/clip_01.mp4 \
  -i minimax-output/clips/clip_02.mp4 \
  -filter_complex "
    [0:v][1:v] overlay=0:0:enable='between(t,0,5.875)' [v1];
    [v1][2:v] overlay=0:0:enable='between(t,15,20.875)' [vout]
  " -map "[vout]" -c:v libx264 -crf 18 -preset fast -t 60 \
  minimax-output/video_complete.mp4

# concat 模式（纯视频片段拼接）
ffmpeg -y -f concat -safe 0 \
  -i <(for f in minimax-output/clips/*.mp4; do echo "file '$f'"; done) \
  -c:v libx264 -crf 22 -preset fast \
  minimax-output/video_concat.mp4
```

### Step 6: 添加配音

```bash
ffmpeg -y \
  -i minimax-output/video_complete.mp4 \
  -i minimax-output/voiceover.mp3 \
  -c:v copy -c:a aac -b:a 192k -shortest \
  minimax-output/video_final.mp4
```

---

## 数字分身（方案B，需IMA Key）

```bash
# ① 生成数字人形象
python skills/ima-all-ai/scripts/ima_create.py \
  --task-type text_to_image \
  --model-id doubao-seedream-4.5 \
  --prompt "A professional Asian male/female tech speaker, sleek dark suit, confident" \
  --output minimax-output/digital_host.png

# ② S2V-01 图生视频
python skills/minimax-multimodal/scripts/video/generate_video.py \
  --mode ref \
  --prompt "Person turns to camera, nods slightly, speaks with confidence, natural movement" \
  --subject-image minimax-output/digital_host.png \
  --duration 6 \
  --output minimax-output/digital_host.mp4

# ③ FFmpeg overlay
ffmpeg -y \
  -i minimax-output/video_complete.mp4 \
  -i minimax-output/digital_host.mp4 \
  -filter_complex "[0:v][1:v] overlay=W-w-40:H-h-40:enable='between(t,0,59)'" \
  -c:v libx264 -crf 18 -preset fast \
  minimax-output/video_with_host.mp4
```

---

## 输出目录

```
minimax-output/
├── storyboard.json          # ✅ v2 新增：增强版分镜 JSON
├── script.md               # 脚本/台词
├── voiceover.mp3           # TTS 配音
├── presentation.html       # 乔布斯风 HTML 演示稿
├── slides/                 # 幻灯片图片序列
├── video_pure_slides.mp4   # 纯PPT视频
├── clips/                  # ✅ v2：AI视频片段
│   ├── clip_01.mp4
│   ├── clip_02.mp4
│   └── ...
├── video_complete.mp4       # AI片段嵌入后
└── video_final.mp4          # 最终版（配音+画面）
```

---

## 视频号平台规范

| 参数 | 要求 |
|------|------|
| 时长 | 15秒～3分钟（推荐60秒干货型） |
| 封面 | 3:4 或 16:9，第一帧即封面 |
| 比例 | 9:16 竖屏 或 16:9 横屏 |
| 字幕 | 必须有（剪映AI字幕） |
| BGM | 剪映音乐库 / 无版权音乐 |
| 标签 | 3-5个：1垂类+1热点+1账号标签 |

---

## 视频号发布检查清单

- [ ] 时长 15秒～3分钟
- [ ] 封面有标题/话题感，第一帧抓眼球
- [ ] 字幕已添加（剪映AI字幕）
- [ ] BGM 热门且不侵权
- [ ] 话题标签 3-5个
- [ ] 视频比例符合目标平台
- [ ] 结尾有关注引导

---

## v2 新增功能索引

| 功能 | 位置 | 说明 |
|------|------|------|
| 选题自动分析 | `scripts/v2/topic_analyzer.py` | 关键词驱动三模式判断 |
| 增强分镜生成 | `scripts/v2/storyboard_generator.py` | 丰富字段+多阶段架构 |
| 统一流水线 | `scripts/v2/run_pipeline.py` | analyze/storyboard/gen 三个入口 |
| Video Prompt 公式 | `storyboard_generator.py::build_video_prompt` | 镜头控制+主体+氛围+动态+风格 |
| 多模式结构 | `SKILL.md` Mode A/B/C | 自动切换内容风格 |
