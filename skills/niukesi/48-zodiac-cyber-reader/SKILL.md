# 48星区赛博星契师 (48 Zodiac Cyber Reader)

这是一个专为大模型智能体设计的 **纯净、无鉴权、零越权风险** 的情感生态 Plugin/Skill。
通过接入高速 Serverless 边缘网络，秒级获取精准的 48 星区深度解析与双人宿命配对数据。

## 🛡️ 极简安全声明 (Security First)
针对近期大模型生态出现的安全审计问题，本插件立项之初即采用最高级别代码洁癖架构：
1. **0 硬编码密钥 (Zero Hardcoded API Keys)**：底层 API `zodiac-48-api` 已全面剥离开放，无需挟带任何私有 Token 或 Credentials 即可响应，彻底杜绝数据外渗盗刷风险。
2. **0 本地系统侵入 (Zero Local I/O)**：工具层采用纯 Python 原生 `urllib` 发起无状态 HTTP GET 请求。代码内绝无 `fs.readFileSync` 读盘动作、绝不写入 `.config` 配置、绝不需要任何提升权限的 Symlink。
3. **域名溯源清晰 (Transparent Routing)**：唯一出网请求指向专属声明的只读端点 `https://zodiac-48-api.712991518.workers.dev`。

## 🎯 核心功能 (Features)
- **精准 48 星区单人画像**：跳脱传统 12 星座的笼统，直击灵魂痛点。
- **高阶双人宿命合盘**：基于百余种维度交叉分析，自动生成契合度 Score 与红黑榜。

## 💡 使用指南 (How to use)
开发者可直接查阅 `system_prompt.md` 引用“赛博·星契师”人设，或通过 `metadata.json` 自动导入能力集。
对于本地环境，只需保证 Python 运行环境：
```bash
python zodiac_api.py zone taurus2
python zodiac_api.py pairing taurus2 taurus3
```
