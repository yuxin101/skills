#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDClaw OpenClaw 连接测试脚本

用于测试 API 连接和基本功能
"""

import sys
import os
import json

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mdclaw_client import MDClawOpenClawClient


def test_connection():
    """测试 API 连接"""
    print("=" * 60)
    print("测试 1: API 连接测试")
    print("=" * 60)

    try:
        client = MDClawOpenClawClient()
        print(f"✅ 客户端初始化成功")
        print(f"   网关地址: {client.gateway_url}")
        print(f"   API Key: {client.api_key[:10]}...")
        print(f"   Auth Token: {client.auth_token[:10]}...")
        client.close()
        return True
    except Exception as e:
        print(f"❌ 客户端初始化失败: {e}")
        return False


def test_list_skills():
    """测试获取技能列表"""
    print("\n" + "=" * 60)
    print("测试 2: 获取技能列表")
    print("=" * 60)

    try:
        with MDClawOpenClawClient() as client:
            print("正在获取技能列表...")
            result = client.call_skill("list_skills")
            print("✅ 成功获取技能列表")
            print("\n响应数据:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return True
    except Exception as e:
        print(f"❌ 获取技能列表失败: {e}")
        return False


def test_health_check():
    """测试健康检查"""
    print("\n" + "=" * 60)
    print("测试 3: 健康检查")
    print("=" * 60)

    try:
        with MDClawOpenClawClient() as client:
            is_healthy = client.health_check()
            print(f"✅ 健康检查完成")
            print(f"   状态: {'正常' if is_healthy else '异常'}")
            return is_healthy
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False


def test_skill_call():
    """测试技能调用"""
    print("\n" + "=" * 60)
    print("测试 4: 技能调用测试")
    print("=" * 60)

    try:
        with MDClawOpenClawClient() as client:
            print("正在调用技能...")
            # 这里使用 list_skills 作为测试
            result = client.call_skill("list_skills", {})
            print("✅ 技能调用成功")
            print("\n响应数据:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return True
    except Exception as e:
        print(f"❌ 技能调用失败: {e}")
        return False


def test_retry_mechanism():
    """测试重试机制"""
    print("\n" + "=" * 60)
    print("测试 5: 重试机制测试")
    print("=" * 60)

    try:
        with MDClawOpenClawClient() as client:
            print("正在测试重试机制（调用不存在的技能）...")
            # 故意调用不存在的技能来测试重试
            try:
                result = client.call_skill_with_retry(
                    "nonexistent_skill_test",
                    {},
                    max_retries=2,
                    backoff_factor=0.5
                )
                print("❌ 应该抛出异常但没有")
                return False
            except Exception as e:
                print(f"✅ 重试机制正常工作")
                print(f"   捕获到预期异常: {type(e).__name__}")
                return True
    except Exception as e:
        print(f"❌ 重试机制测试失败: {e}")
        return False


def test_error_handling():
    """测试错误处理"""
    print("\n" + "=" * 60)
    print("测试 6: 错误处理测试")
    print("=" * 60)

    try:
        with MDClawOpenClawClient() as client:
            # 测试空技能名称
            try:
                result = client.call_skill("", {})
                print("❌ 应该抛出 ValueError 但没有")
                return False
            except ValueError as e:
                print(f"✅ 正确捕获 ValueError: {e}")

            # 测试 None 技能名称
            try:
                result = client.call_skill(None, {})
                print("❌ 应该抛出 ValueError 但没有")
                return False
            except ValueError as e:
                print(f"✅ 正确捕获 ValueError: {e}")

            return True
    except Exception as e:
        print(f"❌ 错误处理测试失败: {e}")
        return False


def test_context_manager():
    """测试上下文管理器"""
    print("\n" + "=" * 60)
    print("测试 7: 上下文管理器测试")
    print("=" * 60)

    try:
        print("测试 with 语句...")
        with MDClawOpenClawClient() as client:
            print(f"✅ 进入上下文: {client}")
            result = client.list_skills()
            print("✅ 成功执行操作")
        print("✅ 自动退出上下文（连接已关闭）")
        return True
    except Exception as e:
        print(f"❌ 上下文管理器测试失败: {e}")
        return False


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("MDClaw OpenClaw 连接测试")
    print("=" * 60)
    print()

    tests = [
        ("API 连接", test_connection),
        ("获取技能列表", test_list_skills),
        ("健康检查", test_health_check),
        ("技能调用", test_skill_call),
        ("重试机制", test_retry_mechanism),
        ("错误处理", test_error_handling),
        ("上下文管理器", test_context_manager)
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ 测试 '{name}' 执行时发生异常: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # 打印测试总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)

    passed = 0
    failed = 0

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1

    print("\n" + "=" * 60)
    print(f"总计: {len(results)} 个测试")
    print(f"通过: {passed} 个")
    print(f"失败: {failed} 个")
    print(f"成功率: {passed/len(results)*100:.1f}%")
    print("=" * 60)

    # 返回退出码
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
