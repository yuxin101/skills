from pathlib import Path

from config import load_config
from project import get_current_version_dir
from state import StateManager


def mark_command_failed(project_root: Path, action: str, error: Exception):
    try:
        config = load_config(project_root)
        version_dir = get_current_version_dir(project_root, config)
        if not version_dir or not (version_dir / '.state.json').exists():
            return
        state = StateManager(version_dir)
        state.data['status'] = 'failed'
        state.data['last_action'] = action
        state.data['last_error'] = str(error)
        state.save()
    except Exception:
        return


# 面向用户的错误翻译表
_USER_FRIENDLY_ERRORS = {
    'ConfigError': '项目配置有问题。建议运行 dtflow setup 重新配置。',
    'RuntimeError': '操作过程中出了点问题。',
    'LLMError': 'AI 服务连接失败。请检查网络或运行 dtflow setup 重新配置。',
    'FileNotFoundError': '找不到需要的文件。确认当前目录是 DevTaskFlow 项目。',
    'PermissionError': '没有权限操作文件。请检查文件权限。',
}


def friendly_error(error: Exception) -> str:
    """将 Python 异常翻译为面向用户的友好提示。"""
    error_type = type(error).__name__
    friendly = _USER_FRIENDLY_ERRORS.get(error_type)
    if friendly:
        return f'{friendly}\n（技术详情：{error}）'
    return f'出了点问题：{error}'
