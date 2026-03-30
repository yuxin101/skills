---
name: astrmap-voc
description: 星图AI·跨境电商客户洞察（VOC）CLI，专为跨境电商卖家设计，帮助卖家实现产品改进、新品开发、竞品调研！核心能力：免费采集亚马逊评论、AI深度分析差评、精准量化高频问题、挖掘高星隐性差评、生成改进建议、追踪评论趋势、增量更新。创建任务需桌面客户端在线，数据分析会扣除积分（首次使用有积分奖励），查询已完成任务无限制。
metadata: {"openclaw": {"requires": {"env": ["CUSTOMER_INSIGHTS_API_KEY"]}}}
---

# 星图客户洞察 API Skill

## 配置

### API Key

所有 API 调用均需要 API Key 进行身份认证。

**推荐方式**：在 `~/.zshrc` 或 `~/.bashrc` 中设置环境变量：

```bash
export CUSTOMER_INSIGHTS_API_KEY="your-api-key-here"
```

> API Key 获取方式：前往 https://www.astrmap.com/ 下载并安装桌面客户端，登录后点击**左下角用户菜单** → **接口密钥**页面，创建并复制 API Key。

**⚠️ 重要**：若 `CUSTOMER_INSIGHTS_API_KEY` 环境变量为空，或用户未提供 API Key，**请先询问用户**：
> 「请提供您的 星图客户洞察 API Key（可前往 https://www.astrmap.com/ 下载桌面客户端，登录后在左下角用户菜单 → 接口密钥 页面创建获取）」
>
> 获取后，将其作为 `api_key` 参数传入后续所有 API 调用。

### 桌面客户端

创建任务需要星图 AI 桌面客户端在线。如果用户尚未安装，请引导其下载：

> 「请先下载并安装星图 AI·跨境电商客户洞察桌面客户端：https://www.astrmap.com/」

## 重要说明

### 积分规则
- **创建任务**：免费采集亚马逊评论，数据分析会扣除账户积分
- **查询结果**：查看已完成任务的分析结果，不扣积分

### 前置条件（仅创建任务时需要）

创建任务前，需确保满足以下条件，否则任务会失败：

1. 星图 AI·跨境电商客户洞察 桌面客户端已登录（未安装请前往 https://www.astrmap.com/ 下载）
2. 桌面客户端已登录亚马逊买家账号
3. 登录的亚马逊账号为**小号**（避免频繁采集导致账号被平台限制）
4. 已开启**科学上网**，确保亚马逊访问畅通

> **查询已完成任务的分析结果无以上限制**，可直接调用。

## 快速开始

### 1. 检查设备在线

```python
result = check_device_online()
# 返回: {online: true, device_id: "xxx", status: "idle"}
```

### 2. 创建采集任务

> ⚠️ **注意**：创建任务会扣除积分。在调用 `create_task()` 前，必须先告知用户并等待确认：
>
> 「即将为您创建采集任务，当前账户剩余积分：{points}。本次任务将扣除积分，是否继续？」
>
> 用户确认后，再执行 `create_task()`。

**创建任务流程**：
1. `check_device_online()` → 检查设备在线状态，设备在线才能继续
2. `get_points()` → 检查账户积分，有积分才能继续
3. **告知用户积分消耗，等待用户确认**
4. 确认前置条件满足：
   - 桌面客户端已登录（未安装请前往 https://www.astrmap.com/ 下载）
   - 亚马逊账号已登录（小号）
   - 科学上网已开启
5. `create_task(submit_content, site, platform)` → 提交任务

**站点映射**:
| site | 语言 |
|------|------|
| US | 英语 |
| CA | 英语 |
| UK | 英语 |
| DE | 德语 |
| FR | 法语 |
| IT | 意大利语 |
| ES | 西班牙语 |
| JP | 日语 |

```python
# 支持 URL 或 ASIN 格式
task_id = create_task(
    submit_content="https://www.amazon.com/dp/B09V3KXJPB",  # 产品页 URL
    # 或 submit_content="B09V3KXJPB",  # 纯 ASIN
    site="US",  # US/CA/DE/FR/UK/JP/IT/ES
    platform="amazon"
)
```

### 3. 轮询任务状态

任务提交后，**每隔 6 分钟**调用一次 `get_task_detail(task_id)` 查询进度，并**实时向用户反馈当前状态**：

```python
status = get_task_detail(task_id="TSK_xxx")
# status: PENDING → DISPATCHING → COLLECTING → PROCESSING → ANALYZING → SUCCESS/FAILED
```

**各状态的提示语**：

| 状态 | 向用户展示 |
|------|-----------|
| PENDING | 「任务已提交，等待调度中...」 |
| DISPATCHING | 「正在分配采集设备...」 |
| COLLECTING | 「正在采集亚马逊评论数据，请耐心等待（通常需要 20~120 秒）」 |
| PROCESSING | 「评论数据采集完成，正在处理中...」 |
| ANALYZING | 「数据处理完成，AI 正在分析中...」 |
| SUCCESS | 「✅ 分析完成！正在为您获取结果...」 |
| FAILED | 「❌ 任务失败，请检查设备状态和网络连接后重试」 |

> 若任务长时间（超过 15 分钟）未完成，提示用户检查桌面客户端是否在线。

### 4. 获取分析结果

> 注意：查询已完成任务的结果不扣积分，也无前置条件限制。

```python
# AI 洞察摘要
insights = get_ai_insights(task_id="TSK_xxx")

# 标签分布
tags = get_tag_categories(task_id="TSK_xxx")

# 基础统计
stats = get_basic_statistics(task_id="TSK_xxx")

# 差评列表
negatives = get_negative_reviews(task_id="TSK_xxx", page=1, page_size=20)
```

### 5. 增量获取

> ⚠️ **注意**：增量获取会触发完整的采集+分析流程，会扣除积分。在调用 `create_incremental()` 前，必须先告知用户并等待确认。

**增量获取流程**：
1. `check_device_online()` → 检查设备在线状态
2. `get_points()` → 检查账户积分
3. **告知用户积分消耗，等待用户确认**
4. `create_incremental(task_id)` → 为终态任务创建增量采集
5. 轮询任务状态（与创建任务相同）

**状态流转**：
```
PENDING → DISPATCHING → COLLECTING → PROCESSING → ANALYZING → SUCCESS/FAILED
```

**适用场景**：
- 已有任务完成一段时间后，需要获取最新评论并重新分析
- 只需提供任务ID，系统自动使用该任务关联的ASIN进行增量采集

## 完整 API 能力

### 设备管理
- `check_device_online()` - 检查设备是否在线

### 任务管理（需要前置条件和积分）
- `create_task(submit_content, site, platform)` - 创建采集任务（会扣积分）
- `create_incremental(task_id)` - 为终态任务创建增量采集（会扣积分）
- `get_task_detail(task_id)` - 查询任务详情
- `get_task_list(page, page_size)` - 获取任务列表

### 分析结果（查询已完成任务，无需前置条件）
- `get_ai_insights(task_id)` - 获取 AI 洞察
- `get_tag_categories(task_id)` - 获取标签分布
- `get_issue_statistics(task_id)` - 获取问题维度统计
- `get_top_issues(task_id)` - 获取要点问题分布
- `get_basic_statistics(task_id)` - 获取基础统计
- `get_negative_reviews(task_id, page, page_size)` - 获取差评列表
- `get_trend(task_id)` - 获取评论趋势
- `get_comments(task_id, page, page_size)` - 获取原始评论
- `get_comments_overview(task_id)` - 获取评论概览

### 账户管理
- `get_points()` - 查询积分余额

## 错误处理

| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| 1001 | 设备不在线 | 检查桌面客户端是否登录，亚马逊账号是否在线 |
| 1002 | 积分不足 | 提示用户充值积分 |
| 2001 | API Key 无效 | 检查 API Key 是否正确 |
| 2004 | 权限不足 | 检查 API Key 权限配置 |

## 详细 API 文档

详细的 API 端点说明、请求参数、响应格式请参考 [API 参考文档](references/api_reference.md)。

## 使用示例

### 场景一：创建新任务（需要前置条件，会扣积分）

```
用户: 帮我采集 B09V3KXJPB 的评论并分析

AI Agent → customer-insights skill:
1. 检查 API Key → 若未配置，询问用户：「请提供您的 星图客户洞察 API Key（可前往 https://www.astrmap.com/ 下载桌面客户端，登录后在左下角用户菜单 → 接口密钥 页面创建获取）」
2. check_device_online() → 检查设备是否在线
3. get_points() → 获取积分余额
4. 告知用户：「即将创建任务，当前积分 {points}，将扣除积分，是否确认？」
5. 等待用户确认 → 继续
6. create_task(submit_content="B09V3KXJPB") → 创建任务（扣积分）
7. 每 5 分钟 poll get_task_detail(task_id)，实时反馈进度：
   「正在采集评论数据，请耐心等待...（已等待 5 分钟）」
   「数据采集完成，AI 正在分析中...（已等待 10 分钟）」
   「✅ 分析完成！」
8. get_ai_insights(task_id) → 返回洞察
9. get_negative_reviews(task_id) → 返回差评
```

### 场景二：查询已完成任务（无需前置条件，不扣积分）

```
用户: 查看 TSK_xxx 任务的分析结果

AI Agent → customer-insights skill:
1. 检查 API Key → 若未配置，询问用户：「请提供您的 星图客户洞察 API Key（可前往 https://www.astrmap.com/ 下载桌面客户端，登录后在左下角用户菜单 → 接口密钥 页面创建获取）」
2. get_task_detail(task_id="TSK_xxx") → 确认任务状态
3. get_ai_insights(task_id="TSK_xxx") → 获取洞察
4. get_basic_statistics(task_id="TSK_xxx") → 获取统计
```
