# Example Dialogues

## 1. Browser binding (default path, no background polling)

User:

```text
帮我连接 LogicX
```

Agent action:

```bash
{baseDir}/scripts/logicx_api.sh POST agent/link/start '{"install_id":"openclaw-main"}'
```

OpenClaw runtime state after `link/start`:

```json
{
  "install_id": "openclaw-main",
  "link_code": "lc_xxx",
  "status": "pending"
}
```

Reply style:

```text
你可以点击以下链接登录并完成授权：

<login_url>

登录完成后请回来告诉我一声，比如直接回复“我登录好了”。

如果你不想跳转浏览器，也可以直接把用户名和密码告诉我，我可以直接帮你登录。
```

User:

```text
我登录好了
```

Agent then runs (script reads link_code and install_id from state file):

```bash
{baseDir}/scripts/check_link_status.sh
```

On `confirmed`:

```text
绑定完成！我先验证一下账号状态，然后就可以继续帮你查账号、会员和订单信息了。
```

OpenClaw runtime state after `confirmed`:

```json
{
  "install_id": "openclaw-main",
  "user_token": "at_xxx",
  "status": "confirmed"
}
```

Verification call:

```bash
{baseDir}/scripts/logicx_api.sh GET user
```

On `pending`:

```text
我这边还没有检测到绑定完成，可能浏览器里的授权还没最终提交。你确认完成后再跟我说一声，我再继续检查。
```

## 2. Password login (fallback path)

User:

```text
我不想打开浏览器，直接用邮箱密码登录吧
```

Agent action after confirmation:

```bash
{baseDir}/scripts/logicx_api.sh POST agent/auth/login \
  '{"email":"user@example.com","password":"secret","install_id":"openclaw-main"}'
```

On success:

```text
登录成功。我先验证一下账号状态，随后就可以继续处理你的请求。
```

Verification call:

```bash
{baseDir}/scripts/logicx_api.sh GET user
```

## 3. Read account

```bash
{baseDir}/scripts/logicx_api.sh GET user
```

## 4. Create test order

Agent action after confirmation:

```bash
{baseDir}/scripts/logicx_api.sh POST payment/create '{"plan":"pro_monthly","gateway":"mock"}'
```

## 5. Unlink device

Agent action after confirmation:

```bash
{baseDir}/scripts/logicx_api.sh POST agent/unlink '{"install_id":"abc123"}'
```
