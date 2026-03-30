#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clash 内核自动更新脚本
从 GitHub 自动下载最新版本的 Mihomo 内核
"""

import os
import sys
import requests
import subprocess
import gzip
import shutil
from pathlib import Path
from datetime import datetime

# 配置
SCRIPT_DIR = Path(__file__).parent
CLASH_BIN = SCRIPT_DIR / "clash"
CLASH_OLD = SCRIPT_DIR / "clash.old"
GITHUB_API = "https://api.github.com/repos/MetaCubeX/mihomo/releases/latest"

def get_current_version():
    """获取当前 Clash 版本"""
    if not CLASH_BIN.exists():
        return None
    
    try:
        result = subprocess.run(
            [str(CLASH_BIN), "-v"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except:
        return None

def get_latest_version():
    """从 GitHub 获取最新版本信息"""
    print("📡 查询 GitHub 最新版本...")
    
    try:
        resp = requests.get(GITHUB_API, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        version = data.get('tag_name', 'unknown')
        published_at = data.get('published_at', 'unknown')
        assets = data.get('assets', [])
        
        print(f"✅ 最新版本：{version}")
        print(f"📅 发布时间：{published_at}")
        
        # 找到 linux amd64 compatible 版本
        download_url = None
        for asset in assets:
            name = asset.get('name', '')
            if 'linux-amd64-compatible' in name and name.endswith('.gz'):
                download_url = asset.get('browser_download_url')
                break
        
        if not download_url:
            # fallback 到普通版本
            for asset in assets:
                name = asset.get('name', '')
                if name == f'mihomo-linux-amd64-v{version}.gz':
                    download_url = asset.get('browser_download_url')
                    break
        
        return version, published_at, download_url
    except Exception as e:
        print(f"❌ 获取失败：{e}")
        return None, None, None

def download_latest(download_url):
    """下载最新版本内核"""
    print(f"📥 下载最新版本...")
    print(f"   地址：{download_url}")
    print(f"   使用代理：http://127.0.0.1:7890")
    
    temp_file = SCRIPT_DIR / "mihomo-latest.gz"
    
    try:
        # 使用本地代理下载 GitHub
        proxies = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
        resp = requests.get(download_url, stream=True, proxies=proxies, timeout=120)
        resp.raise_for_status()
        
        total = int(resp.headers.get('content-length', 0))
        downloaded = 0
        
        with open(temp_file, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    # 显示进度
                    if total > 0:
                        percent = (downloaded / total) * 100
                        print(f"\r   进度：{percent:.1f}% ({downloaded/1024/1024:.1f}MB / {total/1024/1024:.1f}MB)", end='', flush=True)
        
        print(f"\r   ✅ 下载完成：{downloaded/1024/1024:.1f}MB")
        
        return temp_file
    except Exception as e:
        print(f"❌ 下载失败：{e}")
        if temp_file.exists():
            temp_file.unlink()
        return None

def extract_and_install(temp_file):
    """解压并安装新版本"""
    print("📦 解压新版本...")
    
    try:
        # 解压
        with gzip.open(temp_file, 'rb') as f_in:
            with open(CLASH_BIN, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # 设置执行权限
        os.chmod(CLASH_BIN, 0o755)
        
        # 清理临时文件
        temp_file.unlink()
        
        print("✅ 安装完成")
        
        return True
    except Exception as e:
        print(f"❌ 解压失败：{e}")
        if temp_file.exists():
            temp_file.unlink()
        return False

def restart_clash():
    """重启 Clash"""
    print("🔄 重启 Clash...")
    
    try:
        # 停止旧进程
        subprocess.run(["pkill", "-x", "clash"], timeout=5)
        import time
        time.sleep(2)
        
        # 启动新进程
        subprocess.Popen(
            [str(CLASH_BIN), "-d", str(SCRIPT_DIR)],
            stdout=open(SCRIPT_DIR / "logs" / "clash.log", "a"),
            stderr=subprocess.STDOUT,
            start_new_session=True
        )
        
        # 等待启动
        time.sleep(3)
        
        # 检查是否启动成功
        result = subprocess.run(["pgrep", "-x", "clash"], capture_output=True)
        if result.returncode == 0:
            print("✅ Clash 已重启")
            return True
        else:
            print("❌ Clash 启动失败")
            return False
    except Exception as e:
        print(f"❌ 重启失败：{e}")
        return False

def backup_old():
    """备份旧版本"""
    if CLASH_BIN.exists():
        print("💾 备份旧版本...")
        if CLASH_OLD.exists():
            CLASH_OLD.unlink()
        shutil.copy2(CLASH_BIN, CLASH_OLD)
        print(f"   备份：{CLASH_OLD}")

def rollback():
    """回滚到旧版本"""
    if not CLASH_OLD.exists():
        print("❌ 没有备份版本")
        return False
    
    print("🔄 回滚到旧版本...")
    try:
        shutil.copy2(CLASH_OLD, CLASH_BIN)
        print("✅ 回滚完成")
        return True
    except Exception as e:
        print(f"❌ 回滚失败：{e}")
        return False

def check_update(auto=False):
    """检查更新"""
    print("=" * 60)
    print("🔄 Clash 内核更新检查")
    print("=" * 60)
    
    # 当前版本
    current = get_current_version()
    print(f"📍 当前版本：{current or '未知'}")
    
    # 最新版本
    latest_ver, published_at, download_url = get_latest_version()
    
    if not latest_ver:
        print("❌ 无法获取最新版本")
        return False
    
    if not download_url:
        print("❌ 未找到可用的下载链接")
        return False
    
    # 比较版本
    if current and latest_ver in current:
        print("✅ 已是最新版本")
        return False
    
    print(f"🆕 发现新版本：{latest_ver}")
    
    if auto:
        print("🤖 自动模式：开始更新...")
    else:
        confirm = input("\n是否更新？(y/N): ")
        if confirm.lower() != 'y':
            print("ℹ️  已取消")
            return False
    
    # 步骤 1：先下载（Clash 保持运行，提供代理）
    print("\n📥 步骤 1/4：下载新版本（Clash 保持运行）...")
    temp_file = download_latest(download_url)
    if not temp_file:
        print("❌ 下载失败")
        return False
    
    # 步骤 2：停止 Clash
    print("\n🛑 步骤 2/4：停止 Clash...")
    subprocess.run(["pkill", "-x", "clash"], timeout=5)
    import time
    time.sleep(2)
    
    # 步骤 3：备份并安装
    print("\n📦 步骤 3/4：备份并安装...")
    backup_old()
    
    if not extract_and_install(temp_file):
        print("🔄 安装失败，尝试回滚...")
        rollback()
        return False
    
    # 步骤 4：重启 Clash
    print("\n🚀 步骤 4/4：重启 Clash...")
    if restart_clash():
        print("=" * 60)
        print("✅ 更新完成！")
        print(f"📍 新版本：{get_current_version()}")
        print("=" * 60)
        return True
    else:
        print("🔄 重启失败，尝试回滚...")
        rollback()
        return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Clash 内核自动更新")
    parser.add_argument("--auto", action="store_true", help="自动更新（无需确认）")
    parser.add_argument("--rollback", action="store_true", help="回滚到旧版本")
    parser.add_argument("--check", action="store_true", help="仅检查更新")
    
    args = parser.parse_args()
    
    if args.rollback:
        rollback()
    elif args.check:
        check_update(auto=False)
    else:
        check_update(auto=args.auto)

if __name__ == "__main__":
    main()
