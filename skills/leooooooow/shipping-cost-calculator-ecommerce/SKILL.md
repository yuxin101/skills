---
name: shipping-cost-calculator-ecommerce
description: Estimate ecommerce shipping cost per order across weight, zones, carrier rules, and free-shipping policies. Use when teams need to understand how shipping affects margin and offer design.
---

# Shipping Cost Calculator Ecommerce

运费不是一个固定值，而是一整套会吞利润的变量。

## 先交互，再计算

开始时先问：
1. 你们想按什么维度算 shipping？
   - 单笔订单
   - 分区域
   - 分重量段
   - 包邮门槛策略
2. 你们平时 shipping 成本里包含哪些部分？
   - carrier fee
   - 包材
   - 仓配处理费
   - 补寄 / 丢件 / 退货相关成本
3. 是否要一起模拟 free shipping threshold 或 bundle 情况？
4. 要沿用现有逻辑，还是让我给推荐框架？

## Python script guidance

有结构化输入时：
- 生成 Python 脚本计算 shipping 成本
- 输出单笔 / 分区 / 政策影响
- 展示关键阈值
- 返回可复用脚本

## 解决的问题

很多团队在设“包邮”“满额包邮”或选物流商时，只看了表面报价，没算清：
- 不同地区 / 重量段的差异；
- 包材和履约费；
- 满额包邮对单均利润的影响；
- 退货或补寄带来的额外成本。

这个 skill 的目标是：
**把 shipping 成本从模糊印象，变成可用于定价和包邮策略的决策输入。**

## 何时使用

- 调整包邮门槛；
- 更换物流商或仓配方案；
- 想知道某些地区是否持续亏损；
- 做 bundle / 提升客单价策略前。

## 输入要求

- 发货区域或国家 / 州
- 包裹重量、尺寸、材积重规则
- 物流商报价 / 仓配费用
- 包材与处理费
- 包邮政策 / 促销规则
- 可选：退货、补寄、丢件损耗假设

## 工作流

1. 明确 shipping 计算口径。
2. 计算单笔基础 shipping 成本。
3. 区分区域、重量段和政策差异。
4. 评估包邮 / 满额包邮的利润影响。
5. 给出阈值和策略建议。
6. 返回可复用 Python 脚本。

## 输出格式

1. Shipping 成本假设表
2. 单笔 / 分区成本结果
3. 包邮政策影响
4. 建议动作
5. Python 脚本

## 质量标准

- 区分 carrier 报价与真实总履约成本。
- 明确哪些地区或重量段风险更高。
- 输出能直接支持定价或门槛设置。
- 不用虚假精度掩盖估算。
- 未确认口径前不假装精确。

## 资源

参考 `references/output-template.md`。
