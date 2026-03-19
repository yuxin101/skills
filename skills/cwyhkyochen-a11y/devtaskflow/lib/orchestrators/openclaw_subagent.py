from orchestrators.base import BaseOrchestrator
from openclaw_bridge import build_openclaw_request


class OpenClawSubagentOrchestrator(BaseOrchestrator):
    """Round 3 adapter placeholder.

    已具备：
    - 统一 orchestrator 接口
    - OpenClaw 请求描述构建
    - 标准化未实现返回

    仍未具备：
    - 在 skill 内直接调用 OpenClaw sessions_spawn 的安全运行条件
    """

    def run(self, action: str, payload: dict) -> dict:
        request = build_openclaw_request(self.config, action, payload)
        return {
            'status': 'not_implemented',
            'action': action,
            'adapter': 'openclaw_subagent',
            'message': 'openclaw_subagent 已完成请求构建层，但当前 skill 内尚未直连 OpenClaw sessions_spawn。',
            'request': request,
        }
