---
name: mzu-news-briefing
displayName: 每日要闻（可定制版）· Customizable Daily Briefing
description: "多源 AI / 科技 / 全球宏观智能聚合简报。每天 09:00 / 22:00 写入待发标记，用户上线时推送（无论何时上线，到手都是当天简报）；追踪 X 账号 Timeline + 多维度覆盖，实时过滤 + 热度分级。安装后自动读取用户 X following 列表生成专属追踪清单，支持自定义触发时间、内容比重、输出格式。Multi-source AI/Tech/Global Macro news aggregator. Smart on-demand delivery: writes pending flag at 09:00/22:00, delivers when you come online — always fresh. X Timeline tracking, real-time filtering, hot ranking. After install: auto-reads your X following to build personalized watch list."
version: 1.2.0
tags: ["AI", "news", "briefing", "科技", "简报", "aggregation", "可定制"]
allowList:
  - cmd: bird          # Twitter/X CLI (agent-reach package)
  - env: TWITTER_AUTH_TOKEN  # Twitter auth token for bird CLI
  - path: "~/.agent-reach-twitter.env"  # Twitter credentials file
  - path: "~/.openclaw/skills/mzu-news-briefing/X_ACCOUNTS.md"  # X accounts list
---

# Mzu News Briefing
## 每日科技简报 · Daily AI/Tech Briefing

---

## Overview | 功能总览

| | |
|---|---|
| **定时生成** | 每日 09:00 + 22:00 写入待发标记，上线时推送（不过期） |
| **X Timeline 追踪** | 安装后自动读取你的 X 关注列表，生成专属账号追踪清单 |
| **多维度覆盖** | X/Twitter · Newsletter · HN · 中文媒体 · 全球宏观 · 市场信号 |
| **实时过滤** | 仅收录 24 小时内新闻，超过 48 小时一律不选 |
| **热度分级** | 🔥 高 / ⚡ 中 / 💤 低，自动分类 + 深度分析 |
| **安装即用** | 无需配置，安装后告之 X 用户名，Agent 自动初始化 |

---

## Key Changes in v1.2 | 重大更新（按需推送机制）

- **按需推送替代定时推送**：09:00 / 22:00 只写入待发标记，用户上线时才推送简报
- **不过期**：即使你凌晨 3 点才看到消息，收到的也是今天的简报，不是过期的
- **自动补发询问**：漏发时会问你要不要补昨天的（仅限昨天），超过1天自动跳过

## Key Changes in v1.1 | 重大更新（历史）

- **X Timeline 优先**：27 个账号直接抓取，替代关键词搜索，告别搜索延迟
- **全球宏观替代融资**：去掉公司融资新闻，聚焦央行政策、股市、大宗、加密
- **HN 踢出新闻源**：HN 帖子属于社区讨论，不作为独立新闻条目
- **Newsletter 日期过滤**：抓取后逐条核对原始发布时间，只选近 24 小时内容
- **X Following 动态初始化**：安装后 Agent 自动读你的关注列表，生成个性化账号清单

---

## Coverage | 覆盖维度

| 维度 | 类型 | 数据来源 |
|------|------|---------|
| A | Newsletter / 精选信源 | NeuralBuddies · Labla · GTMAI |
| B | 社区热度信号 | Hacker News · Reddit · GitHub Trending |
| C | X 账号 Timeline | 27 个 AI 大V / 独立开发者 / KOL |
| D | 中文专业媒体 | 36氪 · 机器之心 · 量子位 · 虎嗅 · IT之家 |
| E | 全球宏观经济 | 央行政策 · 利率 · 汇率 · 通胀预期 |
| F | 监管 / 政策 | Reuters · Politico · NYT AI |
| G | 股市 / 大宗 / 加密 | 指数异动 · 个股 · BTC · 黄金 · 原油 |

---

## Output Format | 输出格式

```
📰 Mzu 每日简报 2026-03-25 08:00

本班共收录 12 条 | 搜索 12 次 | 覆盖维度：A B C D E F G
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 高热度
1. [新闻标题](链接)
   来源：媒体名 | 时间：YYYY-MM-DD | 标签：#AI #Agent
   摘要：（50字以内）

   ▶ 深度：为什么重要
   · 分析点1
   · 分析点2

⚡ 中热度
2. [新闻标题](链接)
   来源：媒体名 | 标签：...

💤 低热度（如有）
3. [新闻标题](链接)
   来源：...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
维度覆盖：A(X) B(X) C(X) D(X) E(X) F(X) G(X)
下一班：22:00（定时 cron 触发）
```

---

## Auto Setup | 安装即用

安装后，Agent 会自动询问你的 X 用户名，然后：
1. 读取你的 X 关注列表
2. 识别其中 AI / 科技相关账号
3. 生成专属追踪清单并保存
4. 后续简报按你的关注动态生成

---

## Customization | 安装后可定制

| 定制项 | 修改方式 |
|--------|---------|
| 触发时间 | 修改 cron 表达式 |
| 内容比重 | 调整 SKILL.md 内容优先级表 |
| 覆盖维度 | 增删工作流第一步的维度 |
| 输出条数 | 调整 SKILL.md 输出格式 |
| 信源替换 | 更换各维度搜索词 |
| 热度阈值 | 调整第四步热度分级标准 |

> 修改后保存，重新触发即可生效。

---

## 定位

多源新闻聚合与智能简报生成工具。
当用户请求新闻简报、天下大事、AI动态，或定时触发（每日 08:00 / 22:00）时调用。

## 安装后可定制

技能安装后可直接修改以下内容，无需懂代码：

| 定制项 | 说明 | 修改位置 |
|--------|------|---------|
| 触发时间 | 改为每天任意时间点 | cron 表达式或 SKILL.md 中的 schedule |
| 内容比重 | 调整 AI/科技/财经/天下的占比 | SKILL.md 内容优先级表 |
| 覆盖维度 | 增删搜索维度（如去掉财经专注 AI） | 工作流第一步的维度 |
| 输出条数 | 调整为 5 条简报或 20 条全量 | SKILL.md 输出格式 |
| 信源替换 | 换成自己常用的新闻源 | 工作流各维度搜索词 |
| 热度阈值 | 调整高中低热度的判定标准 | 工作流第四步热度分级 |

> 修改后保存文件，重新触发即可生效。

## 首次安装时自动初始化

**首次安装时，Agent 自动进行 X 账号初始化**（无需用户手动配置）：

1. Agent 询问用户 X/Twitter 用户名
2. 用 bird 读取用户的 following 列表（`bird following --json`）
3. 识别其中 AI/科技相关的账号，生成专属追踪清单
4. 将清单写入 `~/.openclaw/skills/mzu-news-briefing/X_ACCOUNTS.md`
5. 之后的每日简报 → 读取 `X_ACCOUNTS.md`，按该用户关注的账号动态生成

> 每次简报也会更新清单（新增关注的 AI 账号自动加入，长期无更新的账号自动移除）

---

## 内容优先级

按比重从高到低，覆盖四个层次，资源有限时按顺序取舍：

| 层次 | 比重 | 覆盖范围 |
|------|------|---------|
| 核心 | 50% | AI / 大模型 / Agent / 工具 / 融资 |
| 构建 | 30% | 科技行业 / 大厂动态 / 产品发布 / 平台新闻 |
| 补充 | 20% | 全球宏观 / 股市 / 大宗商品 / 加密货币 / 货币 |
| 背景 | 10% | 天下大事 / 地缘博弈 / 重大突发事件 |

> 重大新闻：少而精，只当事件对科技/财经/AI领域产生实质性影响时入选。重大例表：若军事事件直接冲击科技供应链、能源市场或AI行业格局，可突破比重限制。

---

## 工作流程

### 第一步：检查偏好配置

读取偏好文件：
```
~/.openclaw/skills/mzu-news-briefing/X_ACCOUNTS.md
```

**如果文件存在** → 按文件中保存的偏好生成简报
**如果文件不存在** → 向主人发送偏好询问消息，等待回复后保存偏好，**本次不生成简报**

偏好询问消息内容见"安装后自动初始化流程"环节。

### 第二步：多维度分布搜索

搜索是一切的基础。单一维度覆盖率不超过 30%，必须覆盖至少 **6 个维度**。

> **并发限制**：Brave Free Plan 同时只接受 1 个请求。切勿并发发出多个搜索——逐一串行执行，每次间隔 ≥2 秒。

> **日期计算基准**（执行前必须先算好）：
> - 今日日期：YYYY-MM-DD（从系统时钟获取）
> - 近 24 小时：`after:YYYY-MM-DD`（今日 - 1 天）
> - 例如：2026-03-25 执行时 → `after:2026-03-24`，`pushed:>2026-03-24`，`-since:1days`
> - **超过 2 天的新闻一律不选**，除非是今日才被大规模报道的旧闻（热度二次爆发）

#### 维度 A：Newsletter / 精选信源

信息密度高，但注意：Web Fetch 抓到的文章里的内容**日期以原始发布时间为准**，不是抓取时间。

> **时间过滤**：只抓近 1 天内发布的 Newsletter；抓取后逐条核对原始发布时间，跳过无日期或超过 24 小时的条目
> **排除 HN**：HN 帖子是社区讨论，不是新闻，不计入维度 B；如需引用 HN 内容，仅作辅助线索，不作为独立新闻条目

```
搜索词：
- after:YYYY-MM-DD "AI weekly roundup" OR "this week in AI"
- after:YYYY-MM-DD "the batch AI newsletter"
- after:YYYY-MM-DD site:substack.com "AI news"
```

发现 Newsletter 后，用 `web_fetch` 抓取全文，逐条核对原始发布日期并过滤。

**推荐周报源（实测有效）：**
- https://www.neuralbuddies.com
- https://www.gtmaipodcast.com
- https://www.labla.org

#### 维度 B：社区热度信号（关键）

自下而上的社区爆款，泛搜索几乎无法触达。

> **时间过滤**：HN 和 Reddit 默认按热度排，必须加 `after:YYYY-MM-DD` 强制只看近 24 小时；GitHub Trending 加 `pushed:>YYYY-MM-DD`（近 1 天）

```
搜索词：
- after:YYYY-MM-DD site:news.ycombinator.com AI（HN 近 24 小时热帖）
- after:YYYY-MM-DD site:reddit.com/r/MachineLearning OR site:reddit.com/r/artificial "AI"
- pushed:>YYYY-MM-DD site:github.com/trending AI
- after:YYYY-MM-DD "most popular AI tool"
```

**推荐信源：**
- Hacker News（news.ycombinator.com）— 技术开发者社区，能抓到工具冷启动爆款
- Reddit r/MachineLearning、r/LocalLLaMA — 真实用户讨论
- GitHub Trending — AI 开源项目实时热度

#### 维度 C：AI 大厂动态 / 账号 Timeline（最优先）

使用 **bird** CLI 追踪账号 Timeline，这是最精准的一手信息来源。

> **每次简报都要读**，不依赖关键词搜索，直接抓账号 timeline

**追踪账号清单（按优先级）：**
```
# AI 大厂 / 官方账号
bird user-tweets AnthropicAI -n 5 --json
bird user-tweets claudeai -n 5 --json
bird user-tweets OpenAI -n 5 --json
bird user-tweets Kimi_Moonshot -n 5 --json
bird user-tweets Ali_TongyiLab -n 5 --json
bird user-tweets Alibaba_Wan -n 5 --json
bird user-tweets XiaomiMiMo -n 5 --json
bird user-tweets antigravity -n 5 --json
bird user-tweets odysseyml -n 5 --json

# 独立开发者 / AI 工具
bird user-tweets yetone -n 5 --json
bird user-tweets vllm_project -n 5 --json
bird user-tweets bourneliu66 -n 5 --json
bird user-tweets jakevin7 -n 5 --json
bird user-tweets levelsio -n 5 --json
bird user-tweets akokoi1 -n 5 --json
bird user-tweets axisacat -n 5 --json
bird user-tweets mulerun_ai -n 5 --json

# 中文 AI KOL
bird user-tweets xiaohu -n 5 --json
bird user-tweets op7418 -n 5 --json
bird user-tweets lyc_zh -n 5 --json
bird user-tweets wangray -n 5 --json
bird user-tweets aiwarts -n 5 --json
bird user-tweets iammattx -n 5 --json

# 英文 AI KOL / 媒体
bird user-tweets wshuyi -n 5 --json

# 工具 / 平台
bird user-tweets OpenRouter -n 5 --json
bird user-tweets immersivetran -n 5 --json

# OpenClaw 生态
bird user-tweets steipete -n 5 --json
bird user-tweets openclaw -n 5 --json
```

**账号 timeline 抓不到时（备用搜索）：**
```
bird search "@OpenAI OR @AnthropicAI" -n 10 -since:1days
bird search "Sora OR AI video generation" -n 5 -since:1days
bird search "Claude Code OR Computer Use" -n 5 -since:1days
```

**固定页面抓取（web_fetch）：**
```
- https://releasebot.io/updates/openai — OpenAI 官方发布记录
- https://llm-stats.com/llm-updates — AI 模型发布追踪
```

**Twitter/X 认证配置（每次 bird 调用前必须先加载）：**
认证信息存储在 `~/.agent-reach-twitter.env`（跨平台），执行 bird 前先加载：
```powershell
# Windows: 逐行读取 env 文件并设置环境变量（关键：必须用 $env: 而非 [Environment]::SetEnvironmentVariable）
Get-Content "$env:USERPROFILE\.agent-reach-twitter.env" | ForEach-Object { if ($_ -match '^(.+?)=(.*)$') { Set-Content -Path "env:$($Matches[1])" -Value $Matches[2] } }
# 添加 npm 全局路径（isolated session PATH 不含 npm）
$env:PATH = "C:\Users\admin\AppData\Roaming\npm;$env:PATH"
# Linux/macOS
# source ~/.agent-reach-twitter.env && export PATH="$HOME/.npm-global/bin:$PATH"
```
> 加载后即可直接运行 `bird search ...`，无需每次传参。

**备用搜索（Brave，不依赖 bird）：**
```
- after:YYYY-MM-DD "GPT-5" OR "Claude 4" OR "Gemini 3"
- after:YYYY-MM-DD "MiniMo" OR "DeepSeek" OR "Llama model release"
- after:YYYY-MM-DD "AI product launch" OR "AI model release" OR "AI feature"
```

**优先级**：bird 搜索 > 固定页面抓取 > Brave 搜索引擎

#### 维度 D：中文专业媒体

> **时间过滤**：必须加 `after:YYYY-MM-DD` 限制为近 24 小时

```
搜索词：
- after:YYYY-MM-DD site:36kr.com AI 大模型
- after:YYYY-MM-DD site:jiqizhixin.com AI
- after:YYYY-MM-DD "量子位" OR "机器之心" AI
- after:YYYY-MM-DD 昆仑万维 OR Mureka OR 音乐模型
- after:YYYY-MM-DD site:leiphone.com AI
```

**实测有效固定信源：**
- 36氪（36kr.com）— 速度快，有AI和大厂动态
- 机器之心（jiqizhixin.com）
- 量子位（1baijia.com）
- 虎嗅（huxiu.com）— AI 产品和大厂动态
- IT之家（ithome.com）— AI 产品发布速报

#### 维度 E：全球宏观经济与资本市场

> **时间过滤**：加 `after:YYYY-MM-DD` 限制为近 24 小时

```
搜索词：
- after:YYYY-MM-DD Fed interest rate OR ECB policy OR 央行
- after:YYYY-MM-DD stock market crash OR rally OR 股市大涨 OR 股市暴跌
- after:YYYY-MM-DD oil price OR gold price OR 黄金 OR 原油 大幅
- after:YYYY-MM-DD recession OR inflation OR CPI OR GDP forecast
- after:YYYY-MM-DD 美联储 OR 人民币汇率 OR 比特币 大幅波动
```

**推荐固定信源：**
- Reuters 财经频道
- Bloomberg Markets
- FT 市场数据

#### 维度 F：监管 / 政策

> **时间过滤**：加 `after:YYYY-MM-DD` 限制为近 24 小时

```
搜索词：
- after:YYYY-MM-DD AI regulation policy
- after:YYYY-MM-DD AI law government
- after:YYYY-MM-DD 白宫 AI 政策 OR Trump AI 立法
```

**实测有效固定信源：**
- Reuters AI 政策报道
- Politico / Nextgov（美国政策）
- NYT AI 政策报道

#### 维度 G：股市 / 大宗商品 / 加密货币

当本日有重大市场事件（股市大幅波动、大宗商品异动）时补充搜索：
> **时间过滤**：加 `after:YYYY-MM-DD` 限制为近 24 小时

```
- after:YYYY-MM-DD Nvidia OR Apple OR Tesla OR Microsoft stock
- after:YYYY-MM-DD Nasdaq OR S&P 500 OR Dow Jones
- after:YYYY-MM-DD 比特币 OR BTC OR crypto crash OR crypto rally
- after:YYYY-MM-DD AI stock market
```

---

### 第三步：交叉验证与补漏

初轮搜索完成后，检查：

- Newsletter 提到但初轮未覆盖的项目 → 专项搜索
- 同一事件被 **3+ 个不同来源**提及 → 确认热点，深入挖掘
- 中文源与英文源热点完全不同 → 两边各保留最有代表性的条目
- **日期守卫**：收集的新闻如超过 1/3 早于 24 小时前 → 扩大 `after:` 范围重新搜索最新结果；**任何超过 2 天的新闻一律不选**，除非是今日才被大规模报道的旧闻（热度二次爆发）
- 搜索不足 **8 次** 不开始输出
- 串行执行，每次搜索间隔 ≥2 秒（Brave Free 并发限制）

---

### 第四步：去重与合并

同一事件被多渠道报道，合并为一条：
- 选最高权威/最详细的信息源作为主来源
- 标注"多家媒体报道"若有争议
- 同一项目（如 DeepSeek）多账号提及，合并

---

### 第五步：热度分级

每条新闻按热度分为三级：

| 等级 | 特征 | 输出 |
|------|------|------|
| 高 | 3+ 来源确认 / 社区热烈传播 / 大厂官方公告 / 重大政策 | 深度分析分栏（为什么重要+分析层次） |
| 中 | 2 个来源 / 有数据支撑 / 行业影响明确 | 标准摘要，标注关键数据 |
| 低 | 单来源 / 泛泛报道 / 边缘信息 | 仅标题入选，或直接略过 |

> 边缘信息（如某创业公司发布无关产品的 PR稿）直接略过，不占用篇幅。

---

### 第六步：输出

输出语言：**中文为主**
专业术语处理：首次出现保留英文原词（中文翻译）"格式，后续统一用中文。
---

## 输出格式

```
📰 Mzu 每日简报 YYYY-MM-DD HH:MM

本班共收录 XX 条 | 搜索 XX 次 | 覆盖维度：A/B/C/D/E/F
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 高热度
1. [新闻标题](https://...)
   来源：媒体名 | 时间：YYYY-MM-DD | 标签：#AI #Agent
   摘要：（50字以内，说明发生了什么）

   ▶ 深度：为什么重要
   · （分析点1）
   · （分析点2）

⚡ 中热度
2. [新闻标题](https://...)
   来源：媒体名 | 标签：...
   摘要：（关键数据）

💤 低热度（如有）
3. [新闻标题](https://...)
   来源：...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
维度覆盖：A(X) B(X) C(X) D(X) E(X) F(X)
下一班：HH:MM（定时 cron 触发）
```

---

## 信息源优先级

当同一事件多个来源可选时，按以下顺序选主来源：

1. **X / Twitter** — 大厂官方、核心开发者第一时间发布（时效最快）
2. **Reuters / BBC** — 突发事件、实事报道
3. **Hacker News** — 技术社区反响、工具热度
4. **36Kr / 机器之心 / 量子位** — 中文科技专业报道
5. **The Verge / Wired / TechCrunch** — 产品评测与行业分析
6. **MIT Tech Review / Nature AI** — 研究与深度报道
7. **周报 / Newsletter** — 信息密度最高的综合内容

---

## 反向正确清零（必读）：

> **不要这样做：**
> - `"AI news today"` — 大量 SEO 聚合，噪声
> - `"artificial intelligence breaking news"` — 太宽泛
> - 夹杂年与日 — 错误倾向/预测性内容
> - 只搜 3 次就开始写 — 覆盖率不够

> **正确做法：**
> - 按维度分类搜索，每次至少覆盖一个维度
> - 用 this week / latest 替换具体日期
> - 至少 8 次搜索后才开始输出

---

## 注意事项

- 优先使用 HTTPS 链接
- 遇到付费/无法访问的内容，注明、仍需浏览
- 保持客观，不对新闻内容做主观评分
- 输出总量控制：**10-15 条**，高热度占 3-5 条，其余偏低热度
- 重大事件只在产生实质影响科技/财经/AI领域时入选
- 全程保留来源标注，每条新闻均需可溯源
