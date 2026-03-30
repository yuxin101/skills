# DeepSleep 阶段二：晨报分发指令

## 流程

1. 读取昨天（今天日期-1天）的摘要文件 ~/clawd/memory/YYYY-MM-DD.md
2. 如果文件不存在或没有"每日摘要"章节，跳过
3. 对每个有摘要的群，用 message(action='send', channel='feishu', target='chat:<chat_id>') 发送该群专属的昨日回顾
4. 发送格式：
   📋 昨日回顾（YYYY-MM-DD）
   [该群的摘要内容]
   🔮 Open Questions（如有与该群相关的）
   📋 Tomorrow（如有与该群相关的）
5. 检查 schedule.md 中今天到期的事项，一并提醒
6. 只向有内容的群发送，没有摘要的群不发
