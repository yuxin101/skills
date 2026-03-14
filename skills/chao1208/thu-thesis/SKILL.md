---
name: thu-thesis
description: 清华大学毕业论文 Word → PDF 一键格式规范化工具。输入任意 Word (.docx) 格式的清华毕业论文，自动转换为符合清华 thuthesis 官方 LaTeX 模板规范的高质量 PDF。适用于所有清华学位论文（MBA/学硕/专硕），一条命令搞定。功能：自动提取章节结构、中英文摘要、参考文献（自动生成 BibTeX）、图片（含 caption）、表格（含表头和标题）、致谢、个人简历；自动生成符号和缩略语说明（含孤儿缩略语检测与正文首次出现处自动补写）；自动生成插图清单和附表清单；输出完整 thuthesis LaTeX 项目并编译为 PDF，最终 PDF 复制到 Word 原文件同目录。运行时依赖：python-docx、jinja2、xelatex/bibtex（TeX Live）；setup.sh 会从 GitHub 克隆 thuthesis 到 /tmp/thuthesis-latest；脚本仅读写技能 workspace 及临时目录，不访问无关系统配置或网络端点（仅访问 thuthesis GitHub 仓库）；macOS 下自动用 open 打开生成的 PDF；外部命令：xelatex、bibtex、git。Use when: 用户需要把 Word 格式的清华毕业论文转为规范 PDF，或需要对毕业论文做格式规范化处理。
---

# 清华 MBA 论文 Word → PDF 一键转换

## ⚠️ 核心操作原则（不得违反）

> **只从 Word 中提取信息，不修改 thuthesis 模板格式。**
>
> - thuthesis 的封面、页眉、目录、参考文献、图表样式等，全部由 `thuthesis.cls` 自动生成
> - 脚本只负责把 Word 里的内容（标题、摘要、章节、图表、参考文献等）提取出来填入 `.tex` 文件
> - 若 Word 中某字段缺失，对应 LaTeX 字段留空，**不删除**、不跳过、不用占位符替代
> - 任何格式上的"改进"都必须以 `assets/databk/` 中的官方示例为准，不得自行发挥

## 格式参考：assets/databk/

`assets/databk/` 是从官方 thuthesis 项目备份的原始示例 data 文件，是本工具一切格式决策的**黄金标准**：

| 文件 | 参考内容 |
|------|----------|
| `chap01.tex` ~ `chap04.tex` | 正文章节、三线表、图片、公式格式 |
| `abstract.tex` | 中英文摘要格式 |
| `denotation.tex` | 缩略语/符号说明格式 |
| `acknowledgements.tex` | 致谢格式 |
| `resume.tex` | 个人简历格式 |
| `committee.tex` | 答辩委员会名单格式 |
| `comments.tex` | 导师评语格式 |
| `resolution.tex` | 答辩决议书格式 |

**遇到任何格式问题，先查 `databk/` 里的对应文件，再动代码。**

## 初次使用：拉取 thuthesis 格式参考

**首次使用前必须运行一次：**

```bash
SKILL_DIR="${WORKSPACE}/skills/thu-thesis"
bash "$SKILL_DIR/scripts/setup.sh" "$SKILL_DIR"
```

这会从 GitHub 拉取最新 thuthesis 源码，将 `data/` 目录复制到 `assets/databk/` 作为格式参考基准，并将 thuthesis.cls 等类文件缓存到 `/tmp/thuthesis-latest/`。`databk/` 不打包进 skill，每次按需拉取最新版。

## 依赖

```bash
pip3 install python-docx jinja2
# 需要已安装 TeX Live，xelatex 通常位于 /Library/TeX/texbin（macOS）或 /usr/bin（Linux）
```

## 一键转换

```bash
SKILL_DIR="${WORKSPACE}/skills/thu-thesis"
python3 "$SKILL_DIR/scripts/convert.py" <输入.docx> [输出目录]

# 示例：
python3 "$SKILL_DIR/scripts/convert.py" "论文.docx" /tmp/my-thesis
```

完成后自动打开 PDF。

## 三步流程

```
input.docx
  ↓ parse_docx.py   → output/parsed_*.json + output/figures/（图片）
  ↓ render.py       → <output_dir>/thesis.tex + data/*.tex + ref/refs.bib + figures/
  ↓ xelatex → bibtex → xelatex × 2~3  → <output_dir>/thesis.pdf ✅
```

### Step 1: parse_docx.py — 仅提取，不转换格式

```bash
SKILL_DIR="${WORKSPACE}/skills/thu-thesis"
python3 "$SKILL_DIR/scripts/parse_docx.py" <input.docx> [output_dir]
```

提取内容到 JSON：封面元数据、中英文摘要+关键词、章节结构（Heading1/2/3）、图片（提取到 `output/figures/`）、表格（表头+行数据+caption）、参考文献、致谢、个人简历。

**封面字段提取规则（表格格式封面）：**
- 合并单元格每行去重，只取第一次出现的值
- 字段名和值在同一单元格（"培养单位：经济管理学院"）或相邻列（"指导教师" | "肖勇波教授"）均支持
- 导师格式化为"姓名, 职称"（thuthesis 要求）
- 字段缺失时留空，不强制填充
- 中文日期支持：二○二五年、二〇二五年、2025年 等多种写法

**图片 caption 提取规则（优先级）：**
1. 段落自身文本以"图"开头（图文在同一段落）
2. 后面紧跟 Caption1 样式段落
3. 后面2段内有 Normal/"图"开头的段落
4. 前面4段内有 Caption1 或 Normal/"图"开头的段落

**表格 caption 提取规则：**
- 先向前查3个 body element，找 Normal/"表"开头或 Caption1
- 再向后查3个 body element（表格后才有 caption 的情况）

**正文样式兼容列表：** `Body Text`、`Normal`、`List Paragraph`、`段落`（不同 Word 模板会用不同样式名）

### Step 2: render.py — 按模板填充，不改格式

```bash
SKILL_DIR="${WORKSPACE}/skills/thu-thesis"
python3 "$SKILL_DIR/scripts/render.py" <parsed.json> <output_dir>
```

**渲染顺序（严格按此顺序，不能乱）：**
1. 复制 thuthesis.cls 等类文件 + 图片
2. thusetup.tex（封面元数据）
3. abstract.tex
4. **`fix_orphan_abbrevs(data)`**：孤儿缩略语补写（必须在章节渲染前！）
5. **`generate_bibtex(refs, output_dir)`**：Word 参考文献列表 → `ref/refs.bib`（BibTeX 格式）
6. 各章节 chap0N.tex（正文中 `[N]` / `[N,M]` / `[N-M]` 自动转换为 `\cite{key}`）
7. acknowledgements.tex、resume.tex
8. denotation.tex（缩略语表）
9. 占位文件：committee.tex、comments.tex、resolution.tex

**表格格式（严格遵循 databk/chap02.tex 的三线表标准）：**
```latex
\begin{table}[htbp]
  \centering
  \caption{表题}
  \begin{tabularx}{\textwidth}{*{N}{X}}
    \toprule
    表头1 & 表头2 \\
    \midrule
    内容1 & 内容2 \\
    \bottomrule
  \end{tabularx}
\end{table}
```
- 无竖线，三线（toprule/midrule/bottomrule）
- `tabularx` + `*{N}{X}` 自动分配列宽，防止超出页面
- caption 在表格上方

### Step 3: 编译 PDF（xelatex → bibtex → xelatex × 2）

convert.py 自动运行完整 BibTeX 编译流程：
1. `xelatex`（生成 .aux，含 \citation 记录）
2. `bibtex`（根据 .aux 从 refs.bib 生成 .bbl）
3. `xelatex`（把参考文献 .bbl 写入 PDF）
4. `xelatex`（稳定目录/交叉引用）
5. 若 toc 仍变化，自动补第5次

## 参考文献处理

**Word 原文格式 → BibTeX 自动转换：**
- `render.py` 内置规则 based 解析器，自动识别 `@article` / `@book` / `@misc`
- BibTeX key 格式：`作者姓拼音 + 年份 + 关键词`（全 ASCII，无中文）
- 正文中 `[10]` → `\cite{venkatraman1994venkatraman}`，支持 `[1,2,3]` 和 `[1-3]` 范围
- 输出文件：`<output_dir>/ref/refs.bib`，包含编号→key 映射注释表

**已知限制：**
- 网络资源（`[EB/OL]`）title/author 字段依赖原文是否规范
- 原文引用编号超出参考文献总数时（如 [44] 但只有 43 条），bibtex 会警告 undefined

## 缩略语处理

**已知缩略语提取**（三种正则，词典优先覆盖）：
1. `XXX（中文解释）`
2. `中文名称（XXX）`
3. `Full English Name (XXX)`（校验首字母匹配）

内置 MBA 词典 40+ 词条，词典结果**覆盖**正则结果。

**孤儿缩略语**（出现≥2次但无解释）：
- 正文第一次出现处插入 `XXX（待补充全称）`
- denotation.tex 中标注 `% ← 请人工填写完整解释`

## 已知限制

- SVG 图片跳过（xelatex 不原生支持）
- committee.tex / comments.tex / resolution.tex 为占位，需手工填写
- `.doc` 格式需先用 `textutil -convert docx` 转换（macOS 自带），但转换后段落样式会丢失，标题层级靠字体大小推断（实验性）

## 文件说明

| 路径 | 说明 |
|------|------|
| `scripts/convert.py` | 一键入口 |
| `scripts/parse_docx.py` | Word 解析 → JSON（只提取，不格式化） |
| `scripts/render.py` | JSON → LaTeX 项目（填充模板，生成 BibTeX） |
| `assets/templates/*.j2` | Jinja2 模板（6个） |
| `assets/databk/` | **thuthesis 官方格式示例，格式决策唯一参考** |

## thuthesis 配置（MBA 专业硕士）

```latex
\thusetup{
  degree = {master},
  degree-type = {professional},
  degree-category = {工商管理硕士},
  degree-category* = {Master of Business Administration},
  department = {经济管理学院},
}
```
