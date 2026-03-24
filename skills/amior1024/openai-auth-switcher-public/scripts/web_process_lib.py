from __future__ import annotations

import json
import socket
import subprocess
import time
from pathlib import Path


def port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    s = socket.socket()
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        return True
    except Exception:
        return False
    finally:
        s.close()


def wait_for_port(host: str, port: int, timeout_seconds: float = 8.0, interval_seconds: float = 0.2) -> bool:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        if port_open(host, port):
            return True
        time.sleep(interval_seconds)
    return False


def systemd_user_available() -> bool:
    probe = subprocess.run(['systemctl', '--user', 'is-enabled', 'default.target'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return probe.returncode in (0, 1)


def write_unit_file(template_path: Path, unit_path: Path, *, workspace: Path, host: str, port: int) -> None:
    text = template_path.read_text(encoding='utf-8')
    text = text.replace('__WORKSPACE__', str(workspace))
    text = text.replace('OPENAI_AUTH_SWITCHER_PORT=8765', f'OPENAI_AUTH_SWITCHER_PORT={port}')
    text = text.replace('OPENAI_AUTH_SWITCHER_HOST=127.0.0.1', f'OPENAI_AUTH_SWITCHER_HOST={host}')
    unit_path.parent.mkdir(parents=True, exist_ok=True)
    unit_path.write_text(text, encoding='utf-8')


def systemd_unit_exists(unit_name: str) -> bool:
    show = subprocess.run(
        ['systemctl', '--user', 'show', unit_name, '--property=LoadState,FragmentPath'],
        capture_output=True,
        text=True,
    )
    if show.returncode != 0:
        return False
    props = {}
    for line in (show.stdout or '').splitlines():
        if '=' in line:
            k, v = line.split('=', 1)
            props[k] = v
    return props.get('LoadState') == 'loaded' or bool(props.get('FragmentPath'))



def systemd_unit_status(unit_name: str) -> dict:
    active = subprocess.run(['systemctl', '--user', 'is-active', unit_name], capture_output=True, text=True)
    enabled = subprocess.run(['systemctl', '--user', 'is-enabled', unit_name], capture_output=True, text=True)
    show = subprocess.run(
        ['systemctl', '--user', 'show', unit_name, '--property=SubState,ActiveState,Result,ExecMainPID,FragmentPath'],
        capture_output=True,
        text=True,
    )
    props = {}
    if show.returncode == 0:
        for line in (show.stdout or '').splitlines():
            if '=' in line:
                k, v = line.split('=', 1)
                props[k] = v
    return {
        'unit_name': unit_name,
        'is_active': active.returncode == 0,
        'active_state': (active.stdout or '').strip() or props.get('ActiveState', ''),
        'is_enabled': enabled.returncode == 0,
        'enabled_state': (enabled.stdout or '').strip(),
        'sub_state': props.get('SubState', ''),
        'result': props.get('Result', ''),
        'exec_main_pid': props.get('ExecMainPID', ''),
        'fragment_path': props.get('FragmentPath', ''),
        'ok': show.returncode == 0,
    }



def read_unit_env(unit_name: str) -> dict:
    show = subprocess.run(['systemctl', '--user', 'show', unit_name, '--property=Environment'], capture_output=True, text=True)
    raw = ''
    if show.returncode == 0:
        for line in (show.stdout or '').splitlines():
            if line.startswith('Environment='):
                raw = line.split('=', 1)[1]
                break
    env = {}
    for part in raw.split(' '):
        if '=' in part:
            k, v = part.split('=', 1)
            env[k] = v
    return env
