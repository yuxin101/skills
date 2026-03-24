#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from config import build_ssh_tunnel_command, build_web_url, get_runtime_summary, load_install_info
from runtime_state import build_page_state, parse_basic_auth

HOST = os.environ.get('OPENAI_AUTH_SWITCHER_HOST', '127.0.0.1')
PORT = int(os.environ.get('OPENAI_AUTH_SWITCHER_PORT', '9527'))


def is_authorized(handler: BaseHTTPRequestHandler) -> bool:
    install = load_install_info()
    expected_user = install.get('username', 'admin')
    expected_password = install.get('password', '')
    creds = parse_basic_auth(handler.headers.get('Authorization'))
    return bool(creds and creds[0] == expected_user and creds[1] == expected_password)


def require_auth(handler: BaseHTTPRequestHandler) -> bool:
    if is_authorized(handler):
        return True
    handler.send_response(401)
    handler.send_header('WWW-Authenticate', 'Basic realm="OpenAI Auth Switcher Public"')
    handler.end_headers()
    return False


def build_html() -> str:
    install = load_install_info()
    summary = get_runtime_summary()
    runtime = summary['runtime']
    mode = summary['mode']
    auth_ready = summary['auth_ready']
    username = install.get('username', 'admin')
    password = install.get('password', '<generated-at-install>')
    port = install.get('port', PORT)
    local_url = build_web_url('127.0.0.1', int(port))
    ssh_cmd = build_ssh_tunnel_command(int(port))
    headline = '首次接管模式' if not auth_ready else '已接管模式'
    lead = '当前未检测到 auth-profiles.json，请先导入已有配置或完成首次授权。' if not auth_ready else '当前已检测到 auth-profiles.json，可以继续进行切换、回滚与统计操作。'
    service = install.get('service') or {}
    service_mode = service.get('mode', 'unknown')
    service_ready = bool(install.get('ready') or service.get('ready') or service.get('ok'))
    mode_badge = '<span class="badge badge-warn">Onboarding</span>' if not auth_ready else '<span class="badge badge-ok">Managed</span>'
    service_badge = '<span class="badge badge-ok">Service Ready</span>' if service_ready else '<span class="badge badge-warn">Service Starting</span>'
    next_steps = '''
      <ol>
        <li>确认 OpenClaw 环境路径识别正确。</li>
        <li>如果你已有 auth 文件，可在下方直接导入。</li>
        <li>如果还没有 auth，请先完成 OpenAI OAuth 接入，再刷新页面。</li>
        <li>完成后即可正式接管该机器上的账号切换能力。</li>
      </ol>
    ''' if not auth_ready else '''
      <ol>
        <li>运行 doctor / inspect 确认环境状态。</li>
        <li>创建槽位并导入目标账号配置。</li>
        <li>先执行 dry-run，再进行正式切换。</li>
      </ol>
    '''
    onboarding_panel = f'''
    <section class="panel warn" id="onboarding-panel">
      <h2>首次接管</h2>
      <p>如果你已经有一份可用的 <code>auth-profiles.json</code>，可以直接在这里导入。</p>
      <form id="import-form">
        <label class="label">auth 文件路径</label>
        <input id="auth-source" type="text" placeholder="例如：/root/.openclaw/agents/main/agent/auth-profiles.json" />
        <button type="submit">导入并接管</button>
      </form>
      <div id="import-result" class="muted"></div>
      <div class="toolbar">
        <button type="button" id="refresh-state">重新检测环境</button>
      </div>
    </section>
    ''' if not auth_ready else ''
    managed_panel = '''
    <section class="panel">
      <h2>已接管提示</h2>
      <p>当前环境已具备 auth 配置，后续可继续接回切换、回滚与统计页面能力。</p>
    </section>
    ''' if auth_ready else ''
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>OpenAI Auth Switcher Public 0.2.0 Preview</title>
  <style>
    :root {{
      --bg: #f4f9ff;
      --card: rgba(255,255,255,.82);
      --card-strong: #ffffff;
      --line: rgba(148,184,255,.24);
      --text: #12304f;
      --muted: #5f7694;
      --primary: #2563eb;
      --primary-soft: #dbeafe;
      --warn-bg: #fff7ed;
      --warn-line: #fdba74;
      --ok-bg: #dcfce7;
      --ok-text: #166534;
      --shadow: 0 18px 42px rgba(59,130,246,.12);
    }}
    * {{ box-sizing:border-box; }}
    body {{
      font-family: Arial, sans-serif;
      margin:0;
      color:var(--text);
      background:
        radial-gradient(circle at top right, rgba(125,211,252,.22), transparent 26%),
        radial-gradient(circle at top left, rgba(191,219,254,.28), transparent 22%),
        linear-gradient(180deg,#f8fbff 0%,var(--bg) 100%);
    }}
    .wrap {{ max-width: 1120px; margin:0 auto; padding:20px; }}
    .hero, .panel {{
      background:var(--card);
      border:1px solid var(--line);
      box-shadow:var(--shadow);
      backdrop-filter: blur(16px);
    }}
    .hero {{ border-radius:22px; padding:22px; margin-bottom:16px; }}
    .hero h1 {{ margin:10px 0 8px; color:var(--text); }}
    .hero p {{ margin:0; color:var(--muted); line-height:1.7; }}
    .grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:16px; }}
    .panel {{ border-radius:18px; padding:18px; margin-bottom:16px; }}
    .warn {{ border:1px solid var(--warn-line); background:var(--warn-bg); }}
    pre {{ background:#eaf4ff; color:#16365d; padding:12px; border-radius:14px; overflow:auto; white-space:pre-wrap; border:1px solid rgba(147,197,253,.28); }}
    .kv {{ line-height:1.9; word-break:break-word; }}
    .pill {{ display:inline-block; padding:5px 10px; border-radius:999px; background:var(--primary-soft); color:var(--primary); font-size:12px; font-weight:700; }}
    .badge {{ display:inline-block; padding:5px 10px; border-radius:999px; font-size:12px; font-weight:700; }}
    .badge-ok {{ background:var(--ok-bg); color:var(--ok-text); }}
    .badge-warn {{ background:#fef3c7; color:#92400e; }}
    .status-row {{ display:flex; gap:10px; flex-wrap:wrap; margin-top:12px; }}
    .status-grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:12px; margin-top:16px; }}
    .status-card {{ background:rgba(255,255,255,.72); border:1px solid rgba(147,197,253,.26); border-radius:16px; padding:14px; }}
    .status-card .k {{ font-size:12px; color:var(--muted); margin-bottom:6px; font-weight:700; }}
    .status-card .v {{ font-size:16px; font-weight:800; word-break:break-word; color:var(--text); }}
    h2 {{ margin-top:0; }}
    .label {{ display:block; font-size:12px; font-weight:700; margin-bottom:6px; color:#475569; }}
    input {{ width:100%; padding:12px; border:1px solid #cbd5e1; border-radius:12px; box-sizing:border-box; margin-bottom:10px; background:#fff; }}
    .toolbar {{ display:flex; gap:10px; flex-wrap:wrap; margin-top:10px; }}
    button {{ padding:11px 15px; border:none; border-radius:12px; background:linear-gradient(135deg,#3b82f6 0%,#2563eb 100%); color:#fff; font-weight:700; cursor:pointer; box-shadow:0 10px 22px rgba(37,99,235,.16); }}
    button:hover {{ filter:brightness(.98); }}
    .muted {{ color:var(--muted); font-size:12px; margin-top:8px; }}
    .success {{ color:#166534; }}
    .error {{ color:#991b1b; }}
    @media (max-width: 900px) {{ .grid {{ grid-template-columns:1fr; }} .status-grid {{ grid-template-columns:1fr; }} }}
    @media (max-width: 640px) {{ .wrap {{ padding:14px; }} .hero, .panel {{ padding:16px; border-radius:16px; }} .status-row, .toolbar {{ flex-direction:column; align-items:stretch; }} button {{ width:100%; }} }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <span class="pill">0.2.0 Preview</span>
      <h1>OpenAI Auth Switcher Public</h1>
      <p>{headline}：{lead}</p>
      <div class="status-row">{mode_badge}{service_badge}<span class="pill">端口 {port}</span><span class="pill">服务模式 {service_mode}</span></div>
      <div class="status-grid">
        <div class="status-card"><div class="k">当前模式</div><div class="v">{mode}</div></div>
        <div class="status-card"><div class="k">服务状态</div><div class="v">{'ready' if service_ready else 'starting'}</div></div>
        <div class="status-card"><div class="k">下一步</div><div class="v">{'导入 auth / 首次授权' if not auth_ready else '检查状态后切换账号'}</div></div>
        <div class="status-card"><div class="k">本地地址</div><div class="v">{local_url}</div></div>
        <div class="status-card"><div class="k">用户名</div><div class="v">{username}</div></div>
        <div class="status-card"><div class="k">状态目录</div><div class="v">{summary['state_base_dir']}</div></div>
        <div class="status-card"><div class="k">Systemd ActiveState</div><div class="v">{service.get('status', {}).get('active_state', 'n/a')}</div></div>
        <div class="status-card"><div class="k">Systemd SubState</div><div class="v">{service.get('status', {}).get('sub_state', 'n/a')}</div></div>
        <div class="status-card"><div class="k">日志文件</div><div class="v">{service.get('log_path', 'n/a')}</div></div>
      </div>
    </div>

    <div class="grid">
      <section class="panel">
        <h2>安装信息</h2>
        <div class="kv">
          <div><strong>本地地址：</strong>{local_url}</div>
          <div><strong>默认用户名：</strong>{username}</div>
          <div><strong>默认密码：</strong>{password}</div>
          <div><strong>模式：</strong>{mode}</div>
          <div><strong>服务模式：</strong>{service_mode}</div>
          <div><strong>服务就绪：</strong>{'yes' if service_ready else 'no'}</div>
          <div><strong>ActiveState：</strong>{service.get('status', {}).get('active_state', 'n/a')}</div>
          <div><strong>SubState：</strong>{service.get('status', {}).get('sub_state', 'n/a')}</div>
          <div><strong>日志文件：</strong>{service.get('log_path', 'n/a')}</div>
          <div><strong>状态目录：</strong>{summary['state_base_dir']}</div>
        </div>
      </section>
      <section class="panel">
        <h2>SSH 隧道</h2>
        <pre>{ssh_cmd}</pre>
        <div>本地浏览器打开：<strong>{local_url}</strong></div>
      </section>
    </div>

    <section class="panel {'warn' if not auth_ready else ''}">
      <h2>下一步</h2>
      <div class="muted">建议动作：{'导入 auth 或完成首次授权' if not auth_ready else '检查运行状态后再切换账号'}</div>
      {next_steps}
    </section>

    {onboarding_panel}
    {managed_panel}

    <section class="panel">
      <h2>环境识别</h2>
      <pre id="runtime-json">{json.dumps(runtime, ensure_ascii=False, indent=2)}</pre>
    </section>
  </div>
  <script>
    async function reloadState() {{
      try {{
        const resp = await fetch('/api/state');
        const data = await resp.json();
        const runtimeEl = document.getElementById('runtime-json');
        if (runtimeEl) runtimeEl.textContent = JSON.stringify(data.runtime.runtime, null, 2);
        return data;
      }} catch (err) {{
        return null;
      }}
    }}
    const form = document.getElementById('import-form');
    if (form) {{
      form.addEventListener('submit', async (e) => {{
        e.preventDefault();
        const source = document.getElementById('auth-source').value.trim();
        const resultEl = document.getElementById('import-result');
        resultEl.textContent = '正在导入...';
        resultEl.className = 'muted';
        try {{
          const resp = await fetch('/api/import-auth', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{ source }})
          }});
          const data = await resp.json();
          if (data.ok) {{
            resultEl.textContent = '导入成功，正在重新检测环境...';
            resultEl.className = 'muted success';
            const state = await reloadState();
            if (state && state.auth_ready) {{
              resultEl.textContent = '导入成功，已检测到 auth，页面将在 1 秒后自动刷新进入已接管模式。';
              setTimeout(() => window.location.reload(), 1000);
            }} else {{
              resultEl.textContent = '导入成功，但当前仍未检测到 auth 生效，请检查目标路径后刷新页面。';
              resultEl.className = 'muted error';
            }}
          }} else {{
            resultEl.textContent = '导入失败：' + (data.error || '未知错误');
            resultEl.className = 'muted error';
          }}
        }} catch (err) {{
          resultEl.textContent = '导入失败：' + err;
          resultEl.className = 'muted error';
        }}
      }});
      const refreshBtn = document.getElementById('refresh-state');
      if (refreshBtn) {{
        refreshBtn.addEventListener('click', async () => {{
          const resultEl = document.getElementById('import-result');
          resultEl.textContent = '正在重新检测环境...';
          resultEl.className = 'muted';
          const state = await reloadState();
          if (state) {{
            resultEl.textContent = state.auth_ready ? '已检测到 auth，可刷新页面进入已接管模式。' : '当前仍未检测到 auth，请继续导入或完成首次授权。';
            resultEl.className = state.auth_ready ? 'muted success' : 'muted';
          }} else {{
            resultEl.textContent = '重新检测失败，请稍后重试。';
            resultEl.className = 'muted error';
          }}
        }});
      }}
    }}
  </script>
</body>
</html>'''


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if not require_auth(self):
            return
        if self.path in ('/', '/index.html'):
            body = build_html().encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == '/api/state':
            body = json.dumps(build_page_state(), ensure_ascii=False, indent=2).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == '/api/health':
            payload = {'ok': True, 'service': 'openai-auth-switcher-public-web-preview'}
            body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        if not require_auth(self):
            return
        if self.path == '/api/import-auth':
            length = int(self.headers.get('Content-Length', '0') or '0')
            raw = self.rfile.read(length) if length > 0 else b'{}'
            try:
                payload = json.loads(raw.decode('utf-8'))
            except Exception:
                payload = {}
            source = payload.get('source')
            if not source:
                body = json.dumps({'ok': False, 'error': 'missing source'}, ensure_ascii=False).encode('utf-8')
                self.send_response(400)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            cmd = ['python3', str((__file__ and os.path.join(os.path.dirname(__file__), '..', 'scripts', 'import_auth_file.py'))), '--source', source, '--json']
            proc = subprocess.run(cmd, capture_output=True, text=True)
            out = proc.stdout or proc.stderr or '{"ok": false, "error": "import failed"}'
            body = out.encode('utf-8', errors='ignore')
            self.send_response(200 if proc.returncode == 0 else 400)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        return


def main() -> int:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f'OpenAI Auth Switcher Public web preview listening on http://{HOST}:{PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
