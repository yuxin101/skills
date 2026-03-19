from pathlib import Path

from orchestrator import get_orchestrator
from project import scan_project_files, get_current_version_dir
from state import StateManager
from contracts_review import build_review_payload


def parse_review_passed(review_result: str):
    return '❌ 不通过' not in review_result


def run_review(project_root: Path, config: dict):
    version_dir = get_current_version_dir(project_root, config)
    if not version_dir:
        raise RuntimeError('没有找到当前版本目录')

    state = StateManager(version_dir)
    if state.data.get('status') != 'written':
        raise RuntimeError(f"当前状态不允许 review: {state.data.get('status')}")

    task_id = state.data.get('current_task')
    tasks = state.data.get('tasks', [])
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        raise RuntimeError('找不到当前任务')

    dev_plan_file = version_dir / 'docs' / 'DEV_PLAN.md'
    if not dev_plan_file.exists():
        raise RuntimeError('找不到 DEV_PLAN.md')
    dev_plan = dev_plan_file.read_text(encoding='utf-8')

    code_files = scan_project_files(project_root, limit=20)
    code = '\n\n'.join([
        f"=== 文件: {f['path']} ===\n```\n{f['content'][:4000]}\n```" for f in code_files[:10]
    ])

    state.data['status'] = 'reviewing'
    state.data['last_action'] = 'review'
    state.data['last_error'] = None
    state.save()

    orchestrator = get_orchestrator(config)
    result = orchestrator.run('review', build_review_payload(project_root, version_dir, task, dev_plan, code))

    if result.get('status') == 'not_implemented':
        raise RuntimeError(result.get('message', 'review 编排器未实现'))

    review_text = result.get('raw_text', '') or result.get('summary', '')
    if not review_text:
        raise RuntimeError('review 未返回 raw_text')

    review_file = version_dir / 'docs' / f'REVIEW_TASK_{task_id}.md'
    review_file.write_text(review_text, encoding='utf-8')

    passed = result.get('passed') if isinstance(result.get('passed'), bool) else parse_review_passed(review_text)
    state.data['status'] = 'review_passed' if passed else 'needs_fix'
    state.data['last_orchestration'] = config.get('adapters', {}).get('orchestration', 'local_llm') or 'local_llm'
    state.data['last_result_format'] = result.get('result_format', 'unknown')
    state.data['last_summary'] = result.get('summary', '')
    state.save()

    return {
        'task_id': task['id'],
        'task_name': task['name'],
        'review_file': str(review_file),
        'passed': passed,
        'orchestration': state.data['last_orchestration'],
        'result_format': state.data['last_result_format'],
        'summary': state.data['last_summary'],
    }
