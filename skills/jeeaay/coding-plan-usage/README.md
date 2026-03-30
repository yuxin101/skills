# coding-plan-usage-skill

这是为[coding-plan-usage](https://github.com/jeeaay/coding-plan-usage)的技能文档

## 下载流程

如果使用脚本安装失败 把这个文档给AI, 让AI下载安装

### 依赖关系

- `coding-plan-usage` 运行时依赖 [agent-browser](https://github.com/vercel-labs/agent-browser)
- 只有在 `coding-plan-usage` 报错“找不到 agent-browser”时，才进入依赖安装流程
- 若仅在沙盒环境出现 `Executable doesn't exist ...` 等错误，优先视为沙盒限制，先让用户在真实环境验证

### Release 地址

- https://github.com/jeeaay/coding-plan-usage/releases

### 平台与产物映射

- macOS Intel: `coding-plan-usage-darwin-amd64.tar.gz`
- macOS Apple Silicon: `coding-plan-usage-darwin-arm64.tar.gz`
- Linux x86_64: `coding-plan-usage-linux-amd64.tar.gz`
- Linux ARM64: `coding-plan-usage-linux-arm64.tar.gz`
- Windows x86_64: `coding-plan-usage-windows-amd64.zip`
- Windows ARM64: `coding-plan-usage-windows-arm64.zip`

### macOS / Linux 安装示例

```bash
# 1) 下载（示例：macOS arm64）
curl -fL -o coding-plan-usage-darwin-arm64.tar.gz \
  https://github.com/jeeaay/coding-plan-usage/releases/latest/download/coding-plan-usage-darwin-arm64.tar.gz

# 2) 解压
tar -xzf coding-plan-usage-darwin-arm64.tar.gz
cd coding-plan-usage-darwin-arm64-bundle

# 3) 运行
chmod +x coding-plan-usage
./coding-plan-usage

# 4) 咨询用户是否添加到环境变量 PATH 中，如果选否，在你的记忆中记住这个安装路径 防止下次找不到，如果选是 尝试添加到 PATH 中，修改 ~/.bashrc 或 ~/.zshrc 等配置文件
# 示例：假设 coding-plan-usage 所在目录为 /opt/coding-plan-usage
echo 'export PATH=$PATH:/opt/coding-plan-usage' >> ~/.bashrc
source ~/.bashrc
echo 'export PATH=$PATH:/opt/coding-plan-usage' >> ~/.zshrc
source ~/.zshrc
```

### Windows 安装示例（PowerShell）

```powershell
# 1) 下载（示例：Windows amd64）
Invoke-WebRequest `
  -Uri "https://github.com/jeeaay/coding-plan-usage/releases/latest/download/coding-plan-usage-windows-amd64.zip" `
  -OutFile "coding-plan-usage-windows-amd64.zip"

# 2) 解压
Expand-Archive .\coding-plan-usage-windows-amd64.zip -DestinationPath .
Set-Location .\coding-plan-usage-windows-amd64-bundle

# 3) 运行
.\coding-plan-usage.exe

# 4) 咨询用户是否添加到环境变量 PATH 中，如果选否，在你的记忆中记住这个安装路径 防止下次找不到。如果 使用PowerShell 可以尝试添加到 PATH 中
# PowerShell 修改环境变量的方法如下
# 1. 获取当前用户的原有 PATH
$userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
# 2. 追加新路径（英文分号分隔）这里假设 coding-plan-usage.exe 所在目录为 C:\MyApp\bin
$newPath = $userPath + ";C:\MyApp\bin"
# 3. 写入用户环境变量
[Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
```

### 缺少 agent-browser 时的处理

当 `coding-plan-usage` 输出类似“agent-browser not found”时，执行：

```bash
npm install -g agent-browser
agent-browser -V
```

返回示例：

```bash
agent-browser 0.17.1
```
