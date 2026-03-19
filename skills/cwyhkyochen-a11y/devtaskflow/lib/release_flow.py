from pathlib import Path
import shutil

from project import get_current_version_dir
from state import StateManager
from deploy_adapter import run_deploy_adapter


def ensure_deployment_guide(project_root: Path, version_dir: Path):
    deploy_guide = version_dir / 'docs' / 'DEPLOYMENT.md'
    if deploy_guide.exists():
        return deploy_guide

    content = f"""# DEPLOYMENT

## 项目路径
- project_root: {project_root}
- version: {version_dir.name}

## 部署方式
- 当前为手动部署占位说明
- 请补充：服务器地址、部署目录、启动命令、重启命令、回滚方式

## 建议模板
- 服务器：
- 部署目录：
- 环境变量：
- 构建命令：
- 启动命令：
- 重启命令：
- 回滚方法：
"""
    deploy_guide.write_text(content, encoding='utf-8')
    return deploy_guide


def archive_docs(version_dir: Path):
    docs_dir = version_dir / 'docs'
    docs_archive = version_dir / 'archive' / 'docs'
    docs_archive.mkdir(parents=True, exist_ok=True)
    copied = []
    for file in docs_dir.iterdir():
        if file.is_file():
            shutil.copy2(file, docs_archive / file.name)
            copied.append(file.name)
    return docs_archive, copied


def archive_source(project_root: Path, version_dir: Path):
    src_dir = version_dir / 'archive' / 'src'
    src_dir.mkdir(parents=True, exist_ok=True)

    exclude = {'versions', '.dtflow', '.git', 'node_modules', '__pycache__', 'PROJECTS.md', 'dtflow-dashboard.html'}
    copied = 0
    for item in project_root.iterdir():
        if item.name in exclude:
            continue
        dest = src_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
            copied += 1
        elif item.is_file():
            shutil.copy2(item, dest)
            copied += 1

    (src_dir / '.version').write_text(version_dir.name, encoding='utf-8')
    return src_dir, copied


def run_deploy(project_root: Path, config: dict):
    version_dir = get_current_version_dir(project_root, config)
    if not version_dir:
        raise RuntimeError('没有找到当前版本目录')

    state = StateManager(version_dir)
    allowed = {'review_passed', 'all_done', 'deployed'}
    if state.data.get('status') not in allowed:
        raise RuntimeError(f"当前状态不允许 deploy: {state.data.get('status')}")

    adapter_result = run_deploy_adapter(project_root, config)
    state.data['status'] = 'deployed'
    state.data['deploy'] = adapter_result
    state.save()

    return {
        'version': version_dir.name,
        'mode': config.get('adapters', {}).get('deploy', 'shell'),
        'adapter': adapter_result,
        'message': 'deploy 已切到 adapter 模式，当前仍为骨架实现。',
    }


def run_seal(project_root: Path, config: dict):
    version_dir = get_current_version_dir(project_root, config)
    if not version_dir:
        raise RuntimeError('没有找到当前版本目录')

    state = StateManager(version_dir)
    if state.data.get('status') not in {'deployed', 'review_passed', 'all_done'}:
        raise RuntimeError(f"当前状态不允许 seal: {state.data.get('status')}")

    deployment_file = ensure_deployment_guide(project_root, version_dir)
    docs_archive, docs_files = archive_docs(version_dir)
    src_dir, src_count = archive_source(project_root, version_dir)

    state.data['status'] = 'sealed'
    state.data['archive'] = {
        'docs_dir': str(docs_archive),
        'src_dir': str(src_dir),
        'deployment_file': str(deployment_file),
        'docs_files': docs_files,
        'src_items': src_count,
    }
    state.save()

    return {
        'version': version_dir.name,
        'docs_dir': str(docs_archive),
        'src_dir': str(src_dir),
        'deployment_file': str(deployment_file),
        'docs_files': docs_files,
        'src_items': src_count,
    }
