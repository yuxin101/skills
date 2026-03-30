\---

name: macro-data-api

display\_name: 宏观经济数据查询

description: 查询货币供应量、汇率和美元指数

metadata:

&#x20; openclaw:

&#x20;   emoji: "📊"

&#x20;   requires:

&#x20;     bins: \["python3"]

&#x20;     env: \[]

\---



\# 宏观经济数据查询 (Macro Data API)



通过本技能可以查询：



\- 货币供应量

&#x20; - money/stock：货币存量

&#x20; - money/season：季节调整

&#x20; - money/not-season：未季调

\- 汇率

&#x20; - fx：单个汇率

&#x20; - fx/all：所有汇率

\- 美元指数（DXY）



\## 使用方式



命令行示例：



```bash

\# 查询最近 5 条货币存量数据

python3 skills/macro-data-api/macro\_api.py money/stock 5



\# 查询单个汇率（美元兑欧元）

python3 skills/macro-data-api/macro\_api.py fx '{"symbol":"USDEUR"}'



\# 查询所有汇率

python3 skills/macro-data-api/macro\_api.py fx/all

