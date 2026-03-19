"""交互式 setup 流程 — 帮非技术用户配置 LLM 依赖。"""
from __future__ import annotations

import os
import sys
from pathlib import Path


PRESETS = {
    '1': {
        'name': 'Claude Opus 4.6（推荐）',
        'base_url': '',
        'model_hint': 'claude-opus-4-6',
        'note': '综合能力最强，推荐用于复杂开发任务',
    },
    '2': {
        'name': 'GPT 5.4 Pro',
        'base_url': '',
        'model_hint': 'gpt-5.4-pro',
        'note': 'OpenAI 旗舰模型，大型项目首选',
    },
    '3': {
        'name': 'GPT 5.4',
        'base_url': '',
        'model_hint': 'gpt-5.4',
        'note': '性价比高，适合中小型项目',
    },
    '4': {
        'name': '小米 Mimo V2 Pro',
        'base_url': '',
        'model_hint': 'mimo-v2-pro',
        'note': '国产模型，中文表现好',
    },
    '5': {
        'name': '其他模型（手动填写）',
        'base_url': '',
        'model_hint': '',
        'note': '⚠️ 其他模型可能无法完成完整开发任务，建议从以上 4 个中选择',
    },
}


def _prompt(msg: str, default: str = '') -> str:
    """显示提示并读取用户输入。"""
    suffix = f' [{default}]' if default else ''
    try:
        val = input(f'{msg}{suffix}: ').strip()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)
    return val or default


def _test_connection(base_url: str, api_key: str, model: str) -> tuple[bool, str]:
    """尝试发送一个最简请求，验证连通性。"""
    try:
        import requests
        resp = requests.post(
            f'{base_url.rstrip("/")}/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            },
            json={
                'model': model,
                'messages': [{'role': 'user', 'content': 'hi'}],
                'max_tokens': 5,
            },
            timeout=15,
        )
        if resp.status_code == 200:
            return True, '连接成功！'
        return False, f'连接失败：HTTP {resp.status_code} — {resp.text[:200]}'
    except ImportError:
        return True, '跳过测试（未安装 requests 库，但配置已保存）'
    except Exception as e:
        return False, f'连接失败：{e}'


def _write_env_file(base_url: str, api_key: str, model: str, env_path: Path) -> None:
    """写入 .env 文件。"""
    content = (
        f'DTFLOW_LLM_BASE_URL={base_url}\n'
        f'DTFLOW_LLM_API_KEY={api_key}\n'
        f'DTFLOW_LLM_MODEL={model}\n'
    )
    env_path.write_text(content, encoding='utf-8')
    # 同时设置到当前进程环境，方便后续命令直接使用
    os.environ['DTFLOW_LLM_BASE_URL'] = base_url
    os.environ['DTFLOW_LLM_API_KEY'] = api_key
    os.environ['DTFLOW_LLM_MODEL'] = model


def run_setup(project_root: Path | None = None) -> int:
    """
    交互式 setup 主流程。

    1. 让用户选 AI 服务
    2. 填写 API key
    3. 验证连通性
    4. 写入 .env
    5. 跑 doctor 检查
    """
    print()
    print('🔧 DevTaskFlow 环境配置')
    print('=' * 40)
    print()
    print('DevTaskFlow 需要一个 AI 服务来帮你分析需求、生成代码。')
    print('请选择你使用的 AI 服务：')
    print()

    for k, v in PRESETS.items():
        note = f'  — {v["note"]}' if v.get('note') else ''
        print(f'  {k}. {v["name"]}{note}')

    print()
    choice = _prompt('请选择（输入数字）', '1')
    preset = PRESETS.get(choice, PRESETS['5'])

    print()

    # Base URL
    base_url = _prompt('请输入 AI 服务地址（API Endpoint）')
    if not base_url:
        print('❌ 服务地址不能为空')
        return 1

    # API Key
    print()
    api_key = _prompt('请输入你的 API Key')
    if not api_key:
        print('❌ API Key 不能为空')
        return 1

    # Model
    print()
    if preset['model_hint']:
        print(f'推荐模型：{preset["model_hint"]}')
        model = _prompt('直接回车使用推荐模型，否则输入你想用的模型名', preset['model_hint'])
    else:
        model = _prompt('请输入模型名称')
        if not model:
            print('❌ 模型名称不能为空')
            return 1

    # 测试连接
    print()
    print('⏳ 正在测试连接...')
    ok, msg = _test_connection(base_url, api_key, model)
    if ok:
        print(f'✅ {msg}')
    else:
        print(f'⚠️ {msg}')
        retry = _prompt('连接失败，是否仍然保存配置？(y/n)', 'n')
        if retry.lower() != 'y':
            print('已取消，配置未保存。')
            return 1

    # 写入 .env
    target_dir = project_root or Path.cwd()
    env_path = target_dir / '.env'
    _write_env_file(base_url, api_key, model, env_path)
    print(f'✅ 配置已保存到 {env_path}')

    # 运行 doctor
    print()
    print('⏳ 检查环境...')
    try:
        from doctor import run_doctor
        checks = run_doctor()
        all_ok = True
        for name, passed, detail in checks:
            mark = '✅' if passed else '❌'
            print(f'  {mark} {name}: {detail}')
            if not passed:
                all_ok = False
    except Exception as e:
        print(f'⚠️ doctor 检查出错：{e}，但配置已保存。')

    # 部署方式引导
    print()
    print('📦 部署方式（可以之后再配，先选一个方向）：')
    print('  1. 本地预览 — 写完代码先在本地看效果（推荐新手）')
    print('  2. Docker 容器 — 打包成镜像，方便分享和部署')
    print('  3. 远程服务器 — 通过 SSH 上传到服务器（需要有服务器）')
    print('  4. 先跳过 — 之后再说')
    deploy_choice = _prompt('请选择', '1')

    deploy_hint = {
        '1': '好的，代码生成后可以本地预览。运行 dtflow start --run 即可。',
        '2': '好的，会在项目中自动生成 Dockerfile。需要本地安装了 Docker。',
        '3': '好的，创建项目后需要在 .dtflow/config.json 中填写服务器信息（host、user、path）。',
        '4': '没问题，随时可以通过修改配置来设置。',
    }
    print(f'  {deploy_hint.get(deploy_choice, deploy_hint["4"])}')

    if all_ok:
        print()
        print('🎉 环境配置完成！你现在可以开始使用了。')
        print('   跟我说你想做什么，我来帮你搭建。')
    else:
        print()
        print('⚠️ 部分检查未通过，但基本环境已就绪，可以尝试使用。')

    return 0
