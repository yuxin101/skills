---
name: kam-qianlu-doc-standards
description: 千路=询价管理+出入库/WMS(开发中)。本包权威=询价侧 Excel 表头/文件名(REFERENCE §1–10)、报价对比§12。术语/流程=naming+process。触发：表头命名、单据核验、报价对比矩阵、两子系统边界、filebrowser、采购单回传作用。
---

# kam-qianlu-doc-standards（精简版，详表见 REFERENCE）

## 1. 产品边界（必答清）
- **询价管理系统**：询价/报价/回询/订货/采购/报价对比/可订等 — **本 SKILL + 同目录 [REFERENCE.md](REFERENCE.md) 管表头与文件名**。
- **出入库管理系统（WMS）**：**开发中**；实收核销、库内表头 **不在此包权威范围**，答用户时单列说明。
- **易混**：「订货单入库完整版」= 询价侧**导出**给仓库用的 Excel，**≠** WMS 产品本体。

## 2. 同目录文档（勿在对话里复述长表）
| 文件 | 内容 |
|------|------|
| [REFERENCE.md](REFERENCE.md) | **§1–10** 各单据表头/别名/文件名；**§11** 术语索引；**§12** 报价对比（基准单/品牌矩阵，仅有效报价单） |
| [naming-and-terminology.md](naming-and-terminology.md) | 术语、UI 用词 |
| [process-and-rules.md](process-and-rules.md) | 流程、校验（订货↔回询匹配等） |

## 3. 行为约定
- **查标准**：按用户单据类型打开 REFERENCE 对应节，**摘要**要点即可；完整列名/别名以 REFERENCE 为准。
- **核验 Excel**：确认类型 → **先问**是否核验表头与建议文件名 → 用 openpyxl 找表头行（含「品牌」或 brand 的首行，否则第 1 行）→ 对照 REFERENCE 别名 → 输出映射 + §1 文件名规则。
- **术语/流程**：REFERENCE §11 → 打开 naming 或 process。
- **上传**：若有 filebrowser-api / kam-filebrowser-operator 可代传；本 skill 只做表头/命名。

## 4. 单据类型 → REFERENCE 节号（速查）
二询价导入 · 三报价导入 · 四问价导出 · 五回询导出 · 六订货导入 · **七**订货导出（§7.1 校对版 9 列 / §7.2 入库版 11 列）· 八采购导出 · **九采购单回传导入** · 十可订导入 · **十二报价对比**

**采购单回传（业务一句）**：我方导出采购单 → 供应商填**无效/替换号/备注** → 文件 `校对-采购单-*.xlsx` 再导入 → 按品牌+零件号更新订货行，与线下一致。

## 5. ClawHub / 嵌入
正文刻意缩短以防 **8192 token** 上限；**任何「完整表头表」必须从 REFERENCE.md 读取**，不要凭记忆编造列名。
