# bb-browser 支持平台速查

> 完整列表来源：[bb-sites](https://github.com/epiral/bb-sites)
> 本文档仅列出最常用的适配器命令格式。

## 获取账号列表的方式

目前 bb-browser 不支持自动获取"我关注的人"列表，需要用户手动提供要追踪的账号用户名。

用户可以在配置文件中填写多个账号。

## Twitter/X 适配器

| 命令 | 说明 | 关键字段 |
|------|------|---------|
| `twitter/user <handle>` | 获取用户 profile | followers, following, bio |
| `twitter/tweets <handle>` | 获取用户推文（默认20条，上限100） | text, likes, retweets, created_at, type(tweet/retweet) |
| `twitter/thread <url>` | 获取推文对话线程 | full thread with replies |
| `twitter/bookmarks` | 获取书签列表 | |
| `twitter/notifications` | 获取通知 | |

**Twitter 增量抓取注意**：`twitter/tweets` 不支持时间范围参数，通过 `count` 参数控制每次抓取条数。依赖 state.json 时间戳做增量过滤。

## 其他常用平台

| 平台 | 命令 | 说明 |
|------|------|------|
| Reddit | `reddit/posts <user>` | 用户帖子 |
| | `reddit/hot` | 热门帖子 |
| | `reddit/thread <url>` | 帖子详情 |
| Weibo | `weibo/user_posts <uid>` | 用户微博 |
| | `weibo/feed` | 首页时间线 |
| Bilibili | `bilibili/user_posts <uid>` | 用户投稿 |
| | `bilibili/feed` | 动态（关注用户） |
| 小红书 | `xiaohongshu/user_posts <uid>` | 用户笔记 |
| | `xiaohongshu/note <id>` | 笔记详情 |
| GitHub | `github/repo <owner/repo>` | 仓库信息 |
| | `github/issues <owner/repo>` | issue 列表 |
| HackerNews | `hackernews/top [count]` | 热门帖子 |
| | `hackernews/thread <id>` | 帖子评论 |
| V2EX | `v2ex/hot` | 热门主题 |
| | `v2ex/latest` | 最新主题 |
| 知乎 | `zhihu/hot` | 热榜 |
| | `zhihu/question <id>` | 问题+回答 |
| 雪球 | `xueqiu/hot` | 热门动态 |
| | `xueqiu/stock <code>` | 股票行情 |
| | `xueqiu/feed` | 首页时间线 |
| YouTube | `youtube/video <id>` | 视频详情 |
| | `youtube/transcript <id>` | 字幕（需在视频页） |

## 适配器适配情况

| 平台 | 适配器状态 | 备注 |
|------|-----------|------|
| Twitter | ✅ 完整支持 | tweets/user/thread 均可用 |
| Reddit | ✅ 可用 | posts/hot/thread |
| GitHub | ✅ 可用 | repo/issues |
| HackerNews | ✅ 可用 | top/thread |
| V2EX | ✅ 可用 | hot/latest |
| Weibo | ✅ 可用 | user_posts/feed |
| Bilibili | ✅ 可用 | user_posts/feed |
| 小红书 | ✅ 可用 | user_posts/note |
| 知乎 | ⚠️ 部分可用 | hot 可用，search 可能不稳定 |
| 雪球 | ✅ 可用 | hot/stock/feed |
| YouTube | ⚠️ 受限 | 需 video id，transcript 需在视频页 |

## 添加新平台

如需添加新平台适配：
1. 查看 bb-browser 支持列表：`bb-browser site list`
2. 参考 `bb-browser site info <platform>` 查看命令参数
3. 更新 `fetch_save.py` 中的 `get_adapter_cmd()` 函数
