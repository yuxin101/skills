# aidso_geo_brand_report（无 Cron 继续查询版）

这版不依赖 openclaw cron。

流程：
1. 用户发起品牌诊断
2. 若未绑定 API key，提示先绑定
3. 绑定后提示“此次诊断将消耗20积分，是否确认？”
4. 用户确认后，调同一个接口
   - 如果返回处理中：回复“诊断报告生成中，大约需要3~10分钟，请稍后...”
   - 同时保存 pending_brand
   - 用户后续发送“继续 / 查看结果 / 查询结果”时，再次用同一个 brandName 查询
   - 如果返回成功：立即返回文件

仍然保留：
- 首次成功时只输出一行 MEDIA:/tmp/xxx
- 所有调试日志都写到 stderr
- PDF 链接直接下载
- MD 链接下载后渲染为 PDF

依赖：
pip install requests markdown weasyprint
