#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clash Proxy Manager - Clash 代理管理脚本
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CLASH_BIN = SCRIPT_DIR / "clash"
CONFIG_FILE = SCRIPT_DIR / "config.yaml"
LOG_DIR = SCRIPT_DIR / "logs"
LOG_FILE = LOG_DIR / "clash.log"


def check_clash_running() -> bool:
    """检查 Clash 是否运行中"""
    result = subprocess.run(
        ["pgrep", "-x", "clash"],
        capture_output=True
    )
    return result.returncode == 0


def check_proxy_available() -> bool:
    """检查代理是否可用"""
    try:
        import requests
        proxies = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
        resp = requests.get("https://www.google.com", proxies=proxies, timeout=5)
        return resp.status_code == 200
    except:
        return False


def start_clash() -> bool:
    """启动 Clash"""
    if check_clash_running():
        print("✅ Clash 已在运行")
        return True
    
    # 确保日志目录存在
    LOG_DIR.mkdir(exist_ok=True)
    
    # 启动 Clash
    print("🚀 启动 Clash...")
    subprocess.Popen(
        [str(CLASH_BIN), "-d", str(SCRIPT_DIR)],
        stdout=open(LOG_FILE, "a"),
        stderr=subprocess.STDOUT,
        start_new_session=True
    )
    
    # 等待启动
    import time
    for i in range(10):
        time.sleep(1)
        if check_clash_running():
            print("✅ Clash 已启动")
            return True
    
    print("❌ Clash 启动失败")
    return False


def stop_clash() -> bool:
    """停止 Clash"""
    if not check_clash_running():
        print("ℹ️  Clash 未运行")
        return True
    
    print("🛑 停止 Clash...")
    subprocess.run(["pkill", "-x", "clash"])
    
    import time
    for i in range(5):
        time.sleep(1)
        if not check_clash_running():
            print("✅ Clash 已停止")
            return True
    
    print("⚠️  Clash 可能未完全停止")
    return False


def restart_clash() -> bool:
    """重启 Clash"""
    stop_clash()
    import time
    time.sleep(2)
    return start_clash()


def show_status():
    """显示状态"""
    print("=" * 50)
    print("🌐 Clash Proxy 状态")
    print("=" * 50)
    
    # 进程状态
    if check_clash_running():
        print("✅ 进程状态：运行中")
    else:
        print("❌ 进程状态：未运行")
    
    # 代理状态
    if check_proxy_available():
        print("✅ 代理状态：可用")
    else:
        print("❌ 代理状态：不可用")
    
    # 配置状态
    if CONFIG_FILE.exists():
        print(f"✅ 配置文件：{CONFIG_FILE}")
    else:
        print(f"❌ 配置文件：{CONFIG_FILE} (不存在)")
    
    # 二进制状态
    if CLASH_BIN.exists():
        print(f"✅ 二进制文件：{CLASH_BIN}")
    else:
        print(f"❌ 二进制文件：{CLASH_BIN} (不存在)")
    
    print("=" * 50)


def test_proxy():
    """测试代理"""
    print("🧪 测试代理连通性...")
    
    try:
        import requests
        proxies = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
        
        # 测试 Google
        print("  → 测试 Google...")
        resp = requests.get("https://www.google.com", proxies=proxies, timeout=10)
        print(f"     ✅ Google: {resp.status_code}")
        
        # 测试 Garmin
        print("  → 测试 Garmin...")
        resp = requests.get("https://sso.garmin.com", proxies=proxies, timeout=10)
        print(f"     ✅ Garmin: {resp.status_code}")
        
        print("\n✅ 代理测试通过")
        return True
        
    except Exception as e:
        print(f"\n❌ 代理测试失败：{e}")
        return False


def show_logs(lines=50):
    """查看日志"""
    if not LOG_FILE.exists():
        print("ℹ️  暂无日志")
        return
    
    print(f"📝 最近 {lines} 行日志:")
    print("=" * 50)
    
    with open(LOG_FILE, "r") as f:
        all_lines = f.readlines()
        for line in all_lines[-lines:]:
            print(line, end="")
    
    print("=" * 50)


def update_config(subscription_url: str = None):
    """更新配置"""
    if subscription_url:
        print(f"📥 更新订阅：{subscription_url}")
        # TODO: 实现订阅更新
        print("⚠️  订阅更新功能待实现")
    else:
        print("ℹ️  使用本地配置")


def main():
    parser = argparse.ArgumentParser(description="Clash Proxy Manager")
    parser.add_argument("action", choices=["start", "stop", "restart", "status", "test", "logs", "update"],
                       help="操作类型")
    parser.add_argument("--lines", type=int, default=50, help="日志行数")
    parser.add_argument("--subscription", type=str, help="订阅 URL")
    
    args = parser.parse_args()
    
    if args.action == "start":
        success = start_clash()
        sys.exit(0 if success else 1)
    
    elif args.action == "stop":
        success = stop_clash()
        sys.exit(0 if success else 1)
    
    elif args.action == "restart":
        success = restart_clash()
        sys.exit(0 if success else 1)
    
    elif args.action == "status":
        show_status()
    
    elif args.action == "test":
        test_proxy()
    
    elif args.action == "logs":
        show_logs(args.lines)
    
    elif args.action == "update":
        update_config(args.subscription)


if __name__ == "__main__":
    main()
