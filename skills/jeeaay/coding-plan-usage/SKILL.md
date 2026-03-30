---
name: "coding-plan-usage"
description: "Queries the remaining hours of Alibaba Cloud Coding Plan using a command-line tool. Invoke when user asks for Coding Plan usage."
---

# Coding Plan Usage Helper

用于查询阿里云 Coding Plan 余量的命令行工具。

## 何时使用

在以下场景主动调用：
- 用户希望“查询阿里云 Coding Plan余量”

## 执行流程

1. 先直接尝试运行 `coding-plan-usage`（或 `coding-plan-usage.exe`）
2. 若命令不存在：执行技能目录下的跨平台下载脚本，自动下载并解压后运行
3. 若运行时报 `agent-browser` 不存在：先判断是否沙盒环境；仅真实环境缺失时安装依赖，否则提示用户：沙盒中找不到依赖是正常现象
4. 输出并解释结果

> 注意运行时的路径，切换到包含二进制文件的目录或使用完整路径执行。

## 如何使用运行 `coding-plan-usage`

先尝试以下位置找到 `coding-plan-usage` 或 `coding-plan-usage.exe` 文件：
- 当前目录
- 记忆中
- 当前agent的技能目录 如~/.opencode/skills/coding-plan-usage/scripts/coding-plan-usage-darwin-**/coding-plan-usage
- 当前agent的项目的技能目录 如./.opencode/skills/coding-plan-usage/scripts/coding-plan-usage-darwin-**/coding-plan-usage
- 环境变量 `PATH` 中指定的目录

如果找到了，用完整路径替换下面的`path/to/`

macOS / Linux:

```bash
path/to/coding-plan-usage
```

Windows（PowerShell）:

```powershell
path\to\coding-plan-usage.exe
```

如果命令存在，直接进入“输出解释规则”。
如果提示 `command not found` / `不是内部或外部命令`，再执行“下载流程”。

## 输出解释规则

- **未登录**：会自动打开阿里云首页并进入登录页，保存截图到当前目录`aliyu-login.png`，终端提示你扫码；扫码后再次运行即可。如果频道允许发送图片 你可以直接发给用户，否则可以帮用户打开图片。

截图完成后脚本会停止运行，当用户回复已经完成扫码登陆后，再次运行即可。

示例输出：

```text
Already logged in: false
Entered login page: true
请使用阿里云 App 扫码完成登录后，再次执行此程序以查询用量。
Login screenshot: /opt/coding-plan-usage/aliyu-login.png
Scan completed: false
```

- **已登录**：会自动进入 Coding Plan 页面并输出余量 JSON。

示例输出：

```json
{
  "hours5": {
    "usage": "0%",
    "resetTime": "2026-03-14 18:27:45"
  },
  "week": {
    "usage": "27%",
    "resetTime": "2026-03-16 00:00:00"
  },
  "month": {
    "usage": "15%",
    "resetTime": "2026-04-09 00:00:00"
  }
}
```

成功读取到用量后，程序会自动关闭浏览器会话。

## 下载流程

优先使用技能目录下脚本完成下载与安装：

- macOS / Linux 脚本：`skills/coding-plan-usage/scripts/install.sh`
- Python 脚本适合有Python环境的系统：`skills/coding-plan-usage/scripts/install.py`

默认不传参数时，会下载到脚本同级目录（`skills/coding-plan-usage/scripts/`）。

macOS / Linux：

```bash
chmod +x skills/coding-plan-usage/scripts/install.sh
skills/coding-plan-usage/scripts/install.sh
```

指定下载目录（可选）：

```bash
skills/coding-plan-usage/scripts/install.sh /opt/coding-plan-usage
```

Windows（Python）：

```powershell
python .\skills\coding-plan-usage\scripts\install.py
```

指定下载目录（可选）：

```powershell
python .\skills\coding-plan-usage\scripts\install.py "C:\coding-plan-usage"
```

脚本会输出：
- `installed_bundle=...`
- `binary=...`

拿到 `binary` 路径后，保存到记忆中，后续直接用完整路径运行。
