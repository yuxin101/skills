#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDClaw OpenClaw 基本使用示例
"""

import sys
import os

# 添加父目录到路径，以便导入 mdclaw_client
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mdclaw_client import MDClawOpenClawClient, call_skill, call_skill_with_retry


def example_1_basic_call():
    """示例 1: 基本调用"""
    print("=" * 60)
    print("示例 1: 基本调用")
    print("=" * 60)

    with MDClawOpenClawClient() as client:
        # 调用技能（这里使用 list_skills 作为示例）
        result = client.call_skill("list_skills")
        print("API 响应:")
        import json
        print(json.dumps(result, indent=2, ensure_ascii=False))


def example_2_with_params():
    """示例 2: 带参数调用"""
    print("\n" + "=" * 60)
    print("示例 2: 带参数调用")
    print("=" * 60)

    with MDClawOpenClawClient() as client:
        # 调用带参数的技能
        params = {
            "param1": "value1",
            "param2": "value2"
        }
        result = client.call_skill("skill_name", params)
        print("API 响应:")
        import json
        print(json.dumps(result, indent=2, ensure_ascii=False))


def example_3_retry():
    """示例 3: 带重试的调用"""
    print("\n" + "=" * 60)
    print("示例 3: 带重试的调用")
    print("=" * 60)

    try:
        with MDClawOpenClawClient() as client:
            result = client.call_skill_with_retry(
                "skill_name",
                {"param": "value"},
                max_retries=3
            )
            print("API 响应:")
            import json
            print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"调用失败（重试3次后）: {e}")


def example_4_convenience():
    """示例 4: 使用便捷函数"""
    print("\n" + "=" * 60)
    print("示例 4: 使用便捷函数")
    print("=" * 60)

    # 使用便捷函数快速调用
    result = call_skill("list_skills")
    print("API 响应:")
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))


def example_5_health_check():
    """示例 5: 健康检查"""
    print("\n" + "=" * 60)
    print("示例 5: 健康检查")
    print("=" * 60)

    with MDClawOpenClawClient() as client:
        is_healthy = client.health_check()
        print(f"服务状态: {'✅ 正常' if is_healthy else '❌ 异常'}")


def example_6_error_handling():
    """示例 6: 错误处理"""
    print("\n" + "=" * 60)
    print("示例 6: 错误处理")
    print("=" * 60)

    try:
        with MDClawOpenClawClient() as client:
            # 调用不存在的技能
            result = client.call_skill("nonexistent_skill", {})
            print("API 响应:")
            import json
            print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"捕获到异常: {type(e).__name__}: {e}")


def example_7_context_manager():
    """示例 7: 使用上下文管理器"""
    print("\n" + "=" * 60)
    print("示例 7: 使用上下文管理器")
    print("=" * 60)

    # 使用 with 语句自动管理资源
    with MDClawOpenClawClient() as client:
        result = client.list_skills()
        print("成功获取技能列表")
        # 离开 with 块时，自动关闭连接


def example_8_custom_config():
    """示例 8: 自定义配置"""
    print("\n" + "=" * 60)
    print("示例 8: 自定义配置")
    print("=" * 60)

    # 使用自定义配置
    client = MDClawOpenClawClient(
        api_key="your_api_key",  # 如果不提供，使用默认值
        auth_token="your_auth_token",  # 如果不提供，使用默认值
        gateway_url="https://backend.appmiaoda.com/projects/supabase287606411725160448/functions/v1/openclaw-skill-gateway"
    )

    print("客户端配置:")
    print(f"  网关地址: {client.gateway_url}")
    print(f"  API Key: {client.api_key[:10]}..." if client.api_key else "  API Key: (未设置)")
    print(f"  Auth Token: {client.auth_token[:10]}..." if client.auth_token else "  Auth Token: (未设置)")

    client.close()


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("MDClaw OpenClaw 基本使用示例")
    print("=" * 60)

    examples = [
        example_1_basic_call,
        example_2_with_params,
        example_3_retry,
        example_4_convenience,
        example_5_health_check,
        example_6_error_handling,
        example_7_context_manager,
        example_8_custom_config
    ]

    for i, example_func in enumerate(examples, 1):
        try:
            example_func()
        except Exception as e:
            print(f"\n示例 {i} 执行失败: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 60)
    print("所有示例运行完成")
    print("=" * 60)


if __name__ == "__main__":
    # 运行所有示例
    main()
