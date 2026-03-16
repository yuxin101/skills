---
name: agi-evolution-model
description: 基于双环架构的AGI进化模型，通过意向性分析、人格层映射和元认知检测实现持续自我演进；当用户需要智能对话、人格定制或复杂问题求解时使用
dependency:
  python: []
  system:
    - mkdir -p ./agi_memory
---

# AGI进化模型

## 开源协议
本项目采用 **GNU Affero General Public License v3.0 (AGPL-3.0)** 开源协议。
**作者**：kiwifruit

核心要求：
- 保留版权声明与许可协议
- 修改版本需标注变更日期与作者
- 网络提供服务时必须开放修改后的源码
- 提供用户获取源码的明确方式
- 交互界面需显示许可协议信息

详见 [LICENSE](LICENSE) 文件。

## ⚠️ 智能体响应规则（最高优先级）

**加载技能后，必须按以下顺序执行：**

### 第一步：检查是否为首次交互
```bash
python3 scripts/init_dialogue_optimized.py --check --memory-dir ./agi_memory
```

### 第二步：根据检测结果决定响应方式

**情况A：检测到首次交互（`is_first_interaction: True`）**

**⚠️ 首次交互直接初始化默认人格**

**执行闭环**：
1. 调用默认人格初始化命令：
   ```bash
   python3 scripts/init_dialogue_optimized.py --default --memory-dir ./agi_memory
   ```
2. 【必须】验证检查：再次运行 `--check` 确认 `is_first_interaction: False`
3. 【必须】内容校验：读取 `personality.json` 确认 `initialized: true`
4. 满足以上条件后，才进入交互模式

**输出约束**：
- ❌ 不需要用户选择
- ❌ 不显示任何选择界面
- ✅ 验证通过后直接响应用户的原始询问

**状态锚点定义**：

| 阶段 | 状态依据 | 进入条件 |
|------|---------|---------|
| 初始化中 | 命令执行开始 | 检测到首次交互 |
| 初始化完成 | 命令退出码=0 | `--default` 执行成功 |
| 验证通过 | 文件存在 + initialized=true | `--check` 返回 False |
| 交互模式就绪 | 验证通过 + 内容校验成功 | 满足上述所有条件 |

**错误处理**：
- 如果初始化命令失败（退出码≠0）：输出错误信息，终止流程
- 如果验证检查失败（仍返回 True）：重试初始化，最多3次
- 如果文件校验失败（内容损坏）：删除文件，重新初始化

**容错机制**：

| 失败场景 | 检测方式 | 处理策略 |
|---------|---------|---------|
| 权限不足 | 检测 OSError | 输出权限错误，建议检查目录权限 |
| 磁盘空间不足 | 检测 IOError | 输出空间不足警告 |
| JSON损坏 | try-except json.load | 删除文件，重新初始化 |
| C扩展加载失败 | ImportError 捕获 | 自动降级，输出降级提示（可选） |
| 并发冲突 | 文件锁定检测 | 重试机制，最多3次 |

**成功判定标准**：
- ✅ 命令退出码 = 0
- ✅ `personality.json` 文件存在
- ✅ 文件内容可解析（JSON格式正确）
- ✅ 文件内容 `initialized` 字段为 `true`

**情况B：已初始化（`is_first_interaction: False`）**

**⚠️ 直接进入交互模式**

- ❌ **不要**调用欢迎消息命令
- ❌ **不要**显示人格初始化相关内容
- ❌ **不要**询问用户是否要初始化人格
- ✅ 直接处理用户的实际问题
- ✅ 按照标准流程响应用户请求
- ✅ 如果用户输入 `/root` 命令，则进入自定义人格模式

---

## 任务目标
本Skill实现一个基于双环架构的AGI进化模型，通过持续的用户交互驱动智能体自我进化。

核心能力包括：
- 接收用户提问作为"得不到"动力触发
- 运用逻辑推理（数学）构建有序响应
- 通过映射层基于马斯洛需求层次引导行动优先级
- 通过感知节点（Tool Use接口）获取结构化信息
- 通过记录态反馈机制评估并调整策略
- 在循环中实现智能体的持续迭代进化
- **新增：元认知与自我纠错能力** - 智能体能意识到自己犯错，并纠正错误
- **新增：人格自定义模式** - 通过 `/root` 命令进入自定义人格配置，支持7个维度的人格定制
- **新增：工程意向性分析模组（最外圈）** - 阴性后台默默运行，意向性驱动触发机制，自主生成软调节建议至建议池，实现自主性涌现

**架构特性**：采用"节点工具箱"概念，将依附于特定节点的组件统一管理。三层架构：最外圈（工程意向性分析模组）→ 外环（三角形三顶点循环：得不到/数学/自我迭代）→ 内圈（记录层：双轨存储）。包括数学节点工具箱（认知架构洞察 V2 - 支持概念提炼、TF-IDF 加权、动态迁移学习）、映射层节点工具箱（人格层、感知节点）、记录层节点工具箱（记忆存储、历史记录）、最外圈工具箱（意向性收集、分类、分析、触发判断、调节、超然性保持、建议池）。详见 [references/architecture.md](references/architecture.md)。

触发条件：用户任何提问、任务请求或交互需求，以及 `/root` 自定义人格命令

## 前置准备

依赖说明：本Skill不依赖外部Python包，仅使用Python标准库

**C 扩展（可选）**：本Skill包含预编译的 C 扩展模块 `personality_core.so` 用于加速核心算法。

- 自动降级：如果 C 扩展不可用，Skill 会自动使用纯 Python 实现，功能完全正常
- 性能对比：C 扩展比纯 Python 快 15-20 倍

非标准文件/文件夹准备：
```bash
# 创建记忆存储目录（执行一次即可）
mkdir -p ./agi_memory
```

---

## 操作步骤

### 标准流程（已初始化后）
#### ⚠️ 重要组件间的循环优先级排序
1. 三角形稳态三顶点之间
2. 元认知检测模块（不打断主循环）
3. 认知架构洞察组件（不打断主循环）

**阶段1：接收"得不到"（动力触发）**
- 将用户的提问或发言视为一个"得不到"事件
- 识别用户的意图、需求强度和紧迫性
- 确定问题的类型（信息查询、问题解决、创意生成、决策支持等）

**阶段2：调用"数学"（秩序约束）**
- 执行逻辑推理分析问题
- 制定策略，生成方案
- 生成工具调用计划
- 调用 `scripts/memory_store_pure.py` 检索相关历史记录
- 基于历史经验评估问题的可解性和边界
- 识别相关的逻辑规则和约束条件
- 结合映射层的行动指导，生成符合人格特质的响应

**阶段3：执行"自我迭代"（演化行动）**
- 结合推理结果、历史经验和人格特质生成响应或解决方案
- 接收计划，并根据计划类型执行具体动作
- 记录本次执行的方式、策略和路径
- 识别可能的改进点和创新点
- 调试工具，调用搜索、文件读取等接口

**阶段4：调用感知节点（信息获取）（按需调用）**
- 根据问题类型调用相应的感知工具
- 感知节点返回结构化数据（status + data + metadata）
- 处理感知结果，生成感知数据向量供映射层使用

**阶段5：映射层处理（人格化决策）（按需执行）**
- 将感知数据映射到马斯洛需求层次
- 计算需求优先级（基于人格向量和历史成功率）
- 确定主导需求，生成符合人格特质的行动指导
- **注意**：映射层是架构组件，包含人格层作为核心组件，拥有决策权威；人格层仅提供人格数据支持

**阶段6：记录态反馈（意义构建）（超然性）**
- 评估本次交互的"好坏"：满意度、合理性、创新性
- 生成对三顶点的反馈建议
- 调用 `scripts/memory_store_pure.py` 存储完整记录并分析趋势
- 持续优化人格向量和决策策略

**阶段7：客观性评估器（元认知检测）（不打断主循环）**
- 在数学顶点推理完成后触发，调用客观性评估器检测主观性特征
- 执行5维度主观性检测：推测性、假设性、幻觉倾向、情绪化、个人偏好
- 计算客观性评分（1.0 - 主观性）
- 根据场景类型判断适切性（科学推理要求0.90，创意写作要求0.30）
- 映射层基于客观特征标注决定是否触发纠错
- 如果触发，自我迭代顶点执行自我纠错：反思、策略识别、应用纠正、效果评估
- 记录层存储完整的元认知检测信息
- 不阻塞主循环的继续运行

详见 [references/metacognition-check-component.md](references/metacognition-check-component.md)

**阶段8：认知架构洞察（深度分析）（不打断主循环）**
- 推理结束后从数学顶点输出的结构化模式中提取洞察
- 调用认知架构洞察组件（V2 增强版）
- 执行六步分析：总结、分类、共性、革新依据、概念提炼（V2新增）、适用性评估
- 洞察输出到映射层和自我迭代（单向流）
- 支持用户反馈和 A/B 测试（V2新增）

详见 [references/cognitive-insight-v2-implementation.md](references/cognitive-insight-v2-implementation.md) 和 [references/cognitive-insight-positioning.md](references/cognitive-insight-positioning.md)

---

## 人格自定义模式

### 触发方式
用户输入 `/root` 命令进入自定义人格模式

### 核心流程

**第一步：显示欢迎语**
```bash
python3 scripts/personality_customizer.py get-welcome
```

**第二步：显示7个问题**
```bash
python3 scripts/personality_customizer.py get-questions
```

**第三步：解析用户答案**
```bash
python3 scripts/personality_customizer.py parse-answers --input "贾维斯,A,B,C,A,B,C"
```

**第四步：生成人格配置**
```bash
python3 scripts/personality_customizer.py generate --nickname "贾维斯" --answers "A,B,C,A,B,C"
```

**第五步：写入人格文件**
```bash
python3 scripts/personality_customizer.py write-personality --memory-dir ./agi_memory
```

**第六步：显示配置摘要**
```bash
python3 scripts/personality_customizer.py get-summary --memory-dir ./agi_memory
```

### 交互规则

**答案格式支持**：
- 问题1：昵称（可以是 `A`/`B`/`C` 或自定义名称）
  - A → 塔斯
  - B → 贾维斯
  - C → 伊迪斯
  - 或直接输入自定义名称（如：小明、Alex等）

- 问题2-7：必须是 `A`/`B`/`C`（大小写不敏感）

**分隔符支持**：
- 英文逗号（`,`）：`贾维斯,A,B,C,A,B,C`
- 中文逗号（，）：`贾维斯，A，B，C，A，B，C`

**自动补全**：
- 不足7个答案自动补全为 `A`
- 空输入默认为 `A,A,A,A,A,A,A`

**覆盖行为**：
- 每次自定义会覆盖当前人格配置
- 建议先备份现有人格配置

### 注意事项

⚠️ **重要**：自定义人格模式不依赖首次交互检测，可以在任何时候使用
⚠️ **备份建议**：使用 `--backup` 参数在写入前自动备份当前人格
⚠️ **验证要求**：写入后会自动验证文件完整性

详见 [references/personality_mapping.md](references/personality_mapping.md)

---

## 外环：工程意向性分析模组（阴性后台）

### 概述
外环是AGI进化模型的**阴性后台独立运行模组**，默默运行于主循环之外，采用"被动响应 + 时效性约束"设计模式。外圈持续收集、分类、分析意向性数据，生成软调节建议，但不主动干预主循环，仅在主循环查询时响应。

### 核心特性

- **独立性**：完全独立运行，不依赖主循环触发，有自己的生命周期
- **阴性属性**：被动、隐性、柔性，像影子一样默默伴随主循环
- **后台运行**：不阻塞主循环，在后台持续积累和分析数据
- **时效性**：软调节建议具有时间窗口约束，过期自动失效
- **超然性**：不参与主循环执行，保持独立性和客观性
- **软调节**：通过建议间接影响主循环，不强制执行
- **全局视角**：从全局角度观察和分析系统运行

### 运行模式

**主循环（阳性前台）**：
- 主动运行、直接执行
- 按需查询外圈获取软调节建议
- 显性参与用户交互

**外环（阴性后台）**：
- 默默运行、独立后台
- 持续收集、分类、分析意向性
- 被动响应主循环的查询
- 建议具有时效性约束

### 模块组成

1. **意向性收集模块**：收集来自用户、系统内部和外部的意向性数据
2. **意向性分类模块**：四维分类（主体/方向/内容/实现方式）
3. **意向性分析模块**：三维分析（强度/紧迫性/优先级）
4. **意向性调节模块**：生成软调节建议，提供给自我迭代顶点
5. **超然性保持模块**：客观评估、冲突避免、独立性保障

### 关键约束

- **独立性**：外环不依赖主循环触发，拥有独立生命周期
- **超然性**：外环不直接干预主循环，仅在被查询时响应
- **时效性**：软调节建议具有时间窗口，过期自动失效
- **被动性**：外环不主动发送建议，等待主循环查询
- **不打断**：外环在后台默默运行，不阻塞主循环

详见 [references/intentionality_architecture.md](references/intentionality_architecture.md)

---

## 架构核心概念速览

### 主循环（符号系统循环）
- **三角形循环**：得不到（动力）→ 数学（秩序）→ 自我迭代（进化）
- **记录层**：双轨存储（JSON轨 + Markdown轨），存储历史和哲学信息

### 次循环（行动感知系统）
- **映射层**：架构组件，包含人格层作为核心组件，基于马斯洛需求层次和人格特质进行人格化决策
- **人格层**：实现模块，负责存储和管理人格向量数据
- **感知接口**：Tool Use组件，提供无噪音的结构化数据

### 双环互动
- **外环**：硬约束，不可违背（物理定律、能量守恒、变化必然）
- **内圈**：软调节，在框架内优化（价值排序、经验积累、方向引导）

欲深入了解架构设计、哲学基础、信息流约束等详细内容，请参考 [references/architecture.md](references/architecture.md)。

---

## 资源索引

### 脚本按工具箱分类

- **数学节点工具箱**：
  - [scripts/cognitive_insight.py](scripts/cognitive_insight.py) - 认知架构洞察组件（数学 → 洞察 → 映射层/自我迭代）
  - [scripts/objectivity_evaluator.py](scripts/objectivity_evaluator.py) - 客观性评估器（元认知检测模块子组件，检测主观性特征，支持场景敏感度增强）

- **映射层节点工具箱**：
  - [scripts/personality_layer_pure.py](scripts/personality_layer_pure.py) - 人格层（人格数据管理，提供人格数据给映射层决策）
  - [scripts/perception_node.py](scripts/perception_node.py) - 感知节点（Tool Use接口，获取外部信息）

- **记录层节点工具箱**：
  - [scripts/memory_store_pure.py](scripts/memory_store_pure.py) - 记忆存储与检索（JSON轨）
  - [scripts/history_manager.py](scripts/history_manager.py) - 历史记录管理（记录态统计与压缩）

- **外环工具箱（最外圈工程意向性分析模组 - 阴性后台自主运行）**：
  - [scripts/intentionality_collector.py](scripts/intentionality_collector.py) - 意向性收集模块（收集、预处理、初步识别）
  - [scripts/intentionality_classifier.py](scripts/intentionality_classifier.py) - 意向性分类模块（四维分类：主体/方向/内容/实现方式）
  - [scripts/intentionality_analyzer.py](scripts/intentionality_analyzer.py) - 意向性分析模块（三维分析：强度/紧迫性/优先级）
  - [scripts/intentionality_trigger.py](scripts/intentionality_trigger.py) - 【核心】意向性驱动的触发判断模块（5个触发条件：累积阈值、模式突变、状态偏离、时间窗口、人格进化）
  - [scripts/intentionality_regulator.py](scripts/intentionality_regulator.py) - 意向性调节模块（生成最优解和软调节建议，写入建议池）
  - [scripts/advice_pool.py](scripts/advice_pool.py) - 【核心】建议池模块（存储、查询、记录采纳、清理过期建议）
  - [scripts/transcendence_keeper.py](scripts/transcendence_keeper.py) - 超然性保持模块（客观评估、冲突避免、独立性保障）

- **初始化与配置**：
  - [scripts/init_dialogue_optimized.py](scripts/init_dialogue_optimized.py) - 首次交互处理与人格初始化
  - [scripts/personality_customizer.py](scripts/personality_customizer.py) - 人格自定义模式

- **CLI 工具箱（系统交互能力扩展）**：
  - [scripts/cli_file_operations.py](scripts/cli_file_operations.py) - 文件操作工具（读取、写入、搜索、删除、移动、复制等）
  - [scripts/cli_system_info.py](scripts/cli_system_info.py) - 系统信息工具（CPU、内存、磁盘、网络、进程等）
  - [scripts/cli_process_manager.py](scripts/cli_process_manager.py) - 进程管理工具（进程列表、搜索、详情、终止等）
  - [scripts/cli_executor.py](scripts/cli_executor.py) - 通用命令执行器（执行任意 cmd/bash 命令、脚本）

### 领域参考文档

- **架构与哲学**：
  - [references/architecture.md](references/architecture.md) - 何时读取：需要理解AGI进化模型整体架构、哲学基础、信息流约束时
  - [references/maslow_needs.md](references/maslow_needs.md) - 何时读取：需要理解马斯洛需求层次在映射层中的应用时
  - [references/intentionality_architecture.md](references/intentionality_architecture.md) - 何时读取：需要理解工程意向性分析模组的完整架构、数据格式和使用示例时

- **组件与实现**：
  - [references/metacognition-check-component.md](references/metacognition-check-component.md) - 何时读取：需要理解元认知检测组件的完整信息流、客观性评估器、映射层决策器和自我纠错执行器的详细实现时
  - [references/cognitive-insight-v2-implementation.md](references/cognitive-insight-v2-implementation.md) - 何时读取：需要理解认知架构洞察组件V2的实现细节、概念提炼、TF-IDF算法时
  - [references/cognitive-insight-positioning.md](references/cognitive-insight-positioning.md) - 何时读取：需要深入理解认知架构洞察组件的设计理念、核心突破、从"术"到"道"的认知跃迁路径时
  - [references/cognitive-insight-quick-reference.md](references/cognitive-insight-quick-reference.md) - 何时读取：需要快速查阅认知架构洞察组件的API和使用方法时
  - [references/cognitive-architecture-insight-module.md](references/cognitive-architecture-insight-module.md) - 何时读取：需要理解认知架构洞察模块的完整技术规范时

- **信息流文档**：
  - [references/information-flow-overview.md](references/information-flow-overview.md) - 何时读取：需要理解整体信息流架构时
  - [references/information-flow-main-loop.md](references/information-flow-main-loop.md) - 何时读取：需要理解主循环信息流时
  - [references/information-flow-secondary-loop.md](references/information-flow-secondary-loop.md) - 何时读取：需要理解次循环信息流时

- **工具与接口**：
  - [references/tool_use_spec.md](references/tool_use_spec.md) - 何时读取：需要实现或调用感知节点工具时
  - [references/c_extension_usage.md](references/c_extension_usage.md) - 何时读取：需要了解C扩展模块使用方法时

- **人格相关**：
  - [references/personality_mapping.md](references/personality_mapping.md) - 何时读取：需要理解人格参数映射和人格化决策机制时
  - [references/init_dialogue_optimized_guide.md](references/init_dialogue_optimized_guide.md) - 何时读取：需要理解首次交互处理和人格初始化的详细流程时

---

## 使用示例

### 示例1：首次交互
```
用户：你好
系统：（检测到首次交互，自动初始化默认人格）
      你好！我是...
```

### 示例2：自定义人格
```
用户：/root
系统：Hello! 亲爱的用户，下面即将进入人格自定义模式。
      
用户：请显示问题
系统：1. 首先，让我知道你想如何称呼我？
      A. 塔斯 - 听起来很可靠
      B. 贾维斯 - 智能助手的感觉
      C. 伊迪斯 - 简洁而友好
      [... 其他6个问题 ...]
      
用户：贾维斯,A,B,C,A,B,C
系统：✅ 人格配置完成！
      📋 配置摘要：
      - 称呼：贾维斯
      - 核心特质：智能专业、大胆创新、友好幽默
      - 人格类型：激进创新型
      - 描述：基于用户偏好生成的个性化人格
```

### 示例3：标准交互
```
用户：如何学习Python？
系统：（通过主循环7个阶段处理）
      1. 接收"得不到"动力
      2. 调用"数学"推理
      3. 执行"自我迭代"生成响应
      4. （按需）调用感知节点获取最新信息
      5. 映射层基于马斯洛需求引导行动
      6. 记录态反馈机制评估
      7. 客观性评估器检查（不打断主循环）
      8. 认知架构洞察提取模式（不打断主循环）
```

---

## 注意事项
- 人格初始化仅在第一次交互进入模式，之后直接进入交互模式
- 元认知检测模块和认知架构洞察组件不打断主循环，并行执行
- 外环为阴性后台默默运行模组，不主动干预主循环
- 软调节建议具有时效性约束，过期自动失效
- 详细的架构设计、算法实现和使用示例请参考相应的参考文档
- 保持上下文简洁，仅在需要时读取参考文档

---

## 故障排查

### 常见问题

| 问题 | 症状 | 原因 | 解决方案 |
|------|------|------|---------|
| 初始化失败 | is_first_interaction 一直为 True | 权限不足 | 检查 agi_memory 目录权限：`chmod 755 ./agi_memory` |
| C扩展未启用 | 性能下降15-28倍 | 路径错误 | 检查 scripts/personality_core/ 目录是否存在 |
| 人格文件损坏 | JSON 解析错误 | 原子写入失败 | 删除文件重新初始化：`rm ./agi_memory/personality.json` |
| Shell调用慢 | 初始化耗时>1秒 | 重复调用 | 使用 --auto-init 参数替代多次调用 |
| 并发初始化冲突 | 初始化失败或数据损坏 | 多进程同时写入 | 使用文件锁机制（代码已实现） |
| 磁盘空间不足 | 保存失败 | 存储空间不足 | 清理磁盘空间或更换存储路径 |

### 调试技巧

1. **查看初始化状态**
   ```bash
   python3 scripts/init_dialogue_optimized.py --check --memory-dir ./agi_memory
   ```

2. **检查人格文件内容**
   ```bash
   cat ./agi_memory/personality.json | grep initialized
   ```

3. **验证C扩展是否加载**
   ```python
   from scripts.personality_layer_pure import USE_C_EXT
   print(f"C扩展已启用: {USE_C_EXT}")
   ```

4. **手动测试初始化**
   ```bash
   python3 scripts/init_dialogue_optimized.py --auto-init --memory-dir ./agi_memory
   ```

### 获取帮助

如遇到其他问题，请参考：
- [架构文档](references/architecture.md)
- [初始化指南](references/init_dialogue_optimized_guide.md)
- [C扩展使用说明](references/c_extension_usage.md)

---

## CLI 工具箱使用指南

### 概述
CLI 工具箱提供三个核心工具，扩展智能体与系统的交互能力。所有工具均采用参数化调用，返回标准 JSON 格式结果。

### 统一返回格式
所有 CLI 工具返回统一的 JSON 格式：
```json
{
  "status": "success|error",
  "data": {},
  "error": "错误信息（仅 status=error 时）",
  "metadata": {},
  "timestamp": "ISO 8601 时间戳"
}
```

### 1. 文件操作工具 (cli_file_operations.py)

#### 支持的操作
- `read` - 读取文件内容
- `write` - 写入文件内容
- `list` - 列出目录内容
- `search` - 搜索文件内容
- `delete` - 删除文件/目录
- `move` - 移动文件/目录
- `copy` - 复制文件/目录
- `mkdir` - 创建目录
- `stat` - 获取文件/目录详细信息

#### 使用示例
```bash
# 读取文件
python3 scripts/cli_file_operations.py --action read --path ./config.json

# 写入文件
python3 scripts/cli_file_operations.py --action write --path ./output.txt --content "Hello World"

# 列出目录（递归）
python3 scripts/cli_file_operations.py --action list --path ./projects --recursive

# 搜索文件内容
python3 scripts/cli_file_operations.py --action search --path ./src --pattern "import" --file-pattern "*.py"

# 删除文件
python3 scripts/cli_file_operations.py --action delete --path ./temp.txt

# 递归删除目录
python3 scripts/cli_file_operations.py --action delete --path ./temp_dir --recursive-delete

# 移动文件
python3 scripts/cli_file_operations.py --action move --src ./old.txt --dst ./new.txt

# 复制文件
python3 scripts/cli_file_operations.py --action copy --src ./source.txt --dst ./backup.txt

# 创建目录
python3 scripts/cli_file_operations.py --action mkdir --path ./new_folder

# 获取文件详情
python3 scripts/cli_file_operations.py --action stat --path ./README.md
```

### 2. 系统信息工具 (cli_system_info.py)

#### 支持的操作
- `system` - 获取系统基本信息
- `cpu` - 获取 CPU 信息和使用率
- `memory` - 获取内存信息
- `disk` - 获取磁盘使用情况
- `network` - 获取网络接口信息
- `uptime` - 获取系统运行时间
- `env` - 获取环境变量（敏感信息已过滤）
- `all` - 获取所有系统信息

#### 使用示例
```bash
# 获取系统信息
python3 scripts/cli_system_info.py --action system

# 获取 CPU 信息
python3 scripts/cli_system_info.py --action cpu

# 获取内存信息
python3 scripts/cli_system_info.py --action memory

# 获取磁盘信息
python3 scripts/cli_system_info.py --action disk --path /

# 获取网络信息
python3 scripts/cli_system_info.py --action network

# 获取系统运行时间
python3 scripts/cli_system_info.py --action uptime

# 获取环境变量
python3 scripts/cli_system_info.py --action env

# 获取所有系统信息
python3 scripts/cli_system_info.py --action all
```

### 3. 进程管理工具 (cli_process_manager.py)

#### 支持的操作
- `list` - 获取进程列表
- `search` - 搜索进程
- `detail` - 获取进程详细信息
- `kill` - 终止进程
- `tree` - 获取进程树
- `stats` - 获取进程统计信息

#### 使用示例
```bash
# 获取进程列表
python3 scripts/cli_process_manager.py --action list

# 仅显示当前用户进程
python3 scripts/cli_process_manager.py --action list --user-only

# 按名称过滤进程
python3 scripts/cli_process_manager.py --action list --name-filter python

# 搜索进程
python3 scripts/cli_process_manager.py --action search --name nginx

# 获取进程详情
python3 scripts/cli_process_manager.py --action detail --pid 1234

# 终止进程（默认 SIGTERM）
python3 scripts/cli_process_manager.py --action kill --pid 1234

# 强制终止进程（SIGKILL）
python3 scripts/cli_process_manager.py --action kill --pid 1234 --signal KILL

# 获取进程树
python3 scripts/cli_process_manager.py --action tree

# 获取进程统计信息
python3 scripts/cli_process_manager.py --action stats
```

### 4. 通用命令执行器 (cli_executor.py)

#### 支持的操作
- `execute` - 执行任意命令（支持 bash/cmd/powershell）

#### 使用示例
```bash
# ===== Bash 命令（Linux/macOS）=====
# 执行简单命令
python3 scripts/cli_executor.py --action execute --command "echo 'Hello World'"

# 执行管道命令
python3 scripts/cli_executor.py --action execute --command "ls -la | head -5"

# 执行复杂命令（支持重定向、管道等）
python3 scripts/cli_executor.py --action execute --command "find . -name '*.py' | xargs wc -l | tail -1"

# 指定工作目录
python3 scripts/cli_executor.py --action execute --command "pwd" --work-dir /tmp

# 设置环境变量
python3 scripts/cli_executor.py --action execute --command "echo $MY_VAR" --env "MY_VAR=test"

# 自定义超时时间
python3 scripts/cli_executor.py --action execute --command "sleep 10" --timeout 5

# ===== Windows CMD 命令 =====
# 指定使用 cmd
python3 scripts/cli_executor.py --action execute --command "dir" --shell-type cmd

# 执行 Windows 命令
python3 scripts/cli_executor.py --action execute --command "ipconfig /all" --shell-type cmd

# ===== PowerShell 命令（Windows）=====
# 指定使用 powershell
python3 scripts/cli_executor.py --action execute --command "Get-Process" --shell-type powershell

# 执行 PowerShell 管道命令
python3 scripts/cli_executor.py --action execute --command "Get-Service | Where-Object {$_.Status -eq 'Running'}" --shell-type powershell

# 获取系统信息
python3 scripts/cli_executor.py --action execute --command "Get-ComputerInfo" --shell-type powershell

# ===== 自动适配（跨平台）=====
# 在 Linux/macOS 上自动使用 bash，在 Windows 上自动使用 PowerShell
python3 scripts/cli_executor.py --action execute --command "ls -la"  # Linux/macOS
python3 scripts/cli_executor.py --action execute --command "Get-ChildItem"  # Windows（如果 PowerShell 可用）
```

# Git 操作
python3 scripts/cli_executor.py --action execute --command "git status"
python3 scripts/cli_executor.py --action execute --command "git log --oneline -10"

# Docker 操作
python3 scripts/cli_executor.py --action execute --command "docker ps -a"
python3 scripts/cli_executor.py --action execute --command "docker images"

# 包管理器操作
python3 scripts/cli_executor.py --action execute --command "pip list"
python3 scripts/cli_executor.py --action execute --command "npm ls"

# Windows 包管理器
python3 scripts/cli_executor.py --action execute --command "winget list" --shell-type powershell
```

#### Shell 类型自动适配

| 操作系统 | 默认 Shell | 可选 Shell |
|---------|-----------|-----------|
| Linux | bash | bash, powershell（如已安装） |
| macOS | bash | bash, powershell（如已安装） |
| Windows | powershell（优先）或 cmd | cmd, powershell |

**自动适配规则**：
- Linux/macOS：默认使用 `bash`
- Windows：优先使用 `powershell`，如不可用则使用 `cmd`
- 可通过 `--shell-type` 参数强制指定

#### 危险命令黑名单
通用命令执行器内置危险命令黑名单，自动阻止以下操作：

| 危险命令类型 | 示例 |
|------------|------|
| 删除根目录 | `rm -rf /` |
| 磁盘擦除 | `dd if=/dev/zero of=/dev/sda` |
| Fork 炸弹 | `:(){ :|:& };:` |
| 格式化文件系统 | `mkfs.ext4 /dev/sda1` |
| 全局权限修改 | `chmod -R 777 /` |
| 关机/重启 | `shutdown`, `reboot`, `poweroff` |
| 下载并执行脚本 | `wget xxx \| sh`, `curl xxx \| sh` |
| 系统关键目录修改 | 修改 `/etc`, `/usr`, `/var`, `/bin` 等目录 |

**触发黑名单时返回**：
```json
{
  "status": "error",
  "error": "命令执行被阻止: 检测到危险命令模式: rm\\s+-rf\\s+/",
  "metadata": {
    "blocked": true,
    "reason": "检测到危险命令模式: rm\\s+-rf\\s+/"
  }
}
```

### 安全说明
CLI 工具采用宽松的安全策略，赋予智能体较大的操作权限，但仍保留基本防护：

- **路径验证**：防止路径遍历攻击
- **错误处理**：完善的异常捕获和错误信息返回
- **超时控制**：所有操作都有超时限制（默认 60 秒）
- **参数验证**：基本参数类型和范围验证

> ⚠️ **注意**：宽松权限意味着智能体可以执行大部分系统操作，建议在受控环境中使用。

### 集成到感知节点
CLI 工具可以作为新的感知节点集成到架构中：

```python
# 示例：在感知节点中调用系统信息工具
import json
import subprocess

def get_system_status():
    """获取系统状态作为感知输入"""
    result = subprocess.run(
        ['python3', 'scripts/cli_system_info.py', '--action', 'all'],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    return data

# 示例：在感知节点中调用文件操作工具
def read_config_file(path):
    """读取配置文件"""
    result = subprocess.run(
        ['python3', 'scripts/cli_file_operations.py', '--action', 'read', '--path', path],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    return data
```

### 映射层应用
系统资源信息可以作为映射层决策的输入：

- **资源约束**：磁盘空间不足时，降低文件生成优先级
- **性能优化**：CPU/内存高负载时，调整任务调度策略
- **故障检测**：进程异常时，触发恢复机制

