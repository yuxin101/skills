#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clash 流量统计脚本
"""

import requests
import argparse
from datetime import datetime

API_URL = "http://127.0.0.1:9090"

def format_bytes(bytes_num):
    """格式化字节显示"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(bytes_num) < 1024.0:
            return f"{bytes_num:.2f} {unit}"
        bytes_num /= 1024.0
    return f"{bytes_num:.2f} PB"

def get_traffic():
    """获取总流量"""
    try:
        resp = requests.get(f"{API_URL}/traffic", timeout=5)
        data = resp.json()
        
        upload = data.get('up', 0)
        download = data.get('down', 0)
        total = upload + download
        
        print("=" * 50)
        print("📊 Clash 流量统计")
        print("=" * 50)
        print(f"📤 上传：   {format_bytes(upload)}")
        print(f"📥 下载：   {format_bytes(download)}")
        print(f"📊 总计：   {format_bytes(total)}")
        print("=" * 50)
        
        return data
    except Exception as e:
        print(f"❌ 获取失败：{e}")
        return None

def get_connections():
    """获取连接信息"""
    try:
        resp = requests.get(f"{API_URL}/connections", timeout=5)
        data = resp.json()
        
        connections = data.get('connections', [])
        
        print("=" * 50)
        print(f"🔗 当前连接：{len(connections)} 个")
        print("=" * 50)
        
        if connections:
            print(f"{'ID':<10} {'主机':<30} {'上传':<12} {'下载':<12} {'时间'}")
            print("-" * 80)
            
            for i, conn in enumerate(connections[:10], 1):  # 只显示前 10 个
                metadata = conn.get('metadata', {})
                host = metadata.get('host', metadata.get('destinationIP', 'Unknown'))
                upload = conn.get('upload', 0)
                download = conn.get('download', 0)
                start = conn.get('start', '')
                
                print(f"{i:<10} {host:<30} {format_bytes(upload):<12} {format_bytes(download):<12} {start}")
            
            if len(connections) > 10:
                print(f"... 还有 {len(connections) - 10} 个连接")
        else:
            print("ℹ️  当前无活动连接")
        
        print("=" * 50)
        
        return data
    except Exception as e:
        print(f"❌ 获取失败：{e}")
        return None

def get_proxies_traffic():
    """获取各节点流量"""
    try:
        resp = requests.get(f"{API_URL}/proxies", timeout=5)
        data = resp.json()
        
        proxies = data.get('proxies', {})
        
        print("=" * 50)
        print("📍 节点流量统计")
        print("=" * 50)
        
        # 统计每个节点的流量
        node_stats = []
        for name, info in proxies.items():
            if info.get('type') in ['ss', 'vmess', 'trojan', 'hysteria']:
                upload = info.get('history', {}).get('up', 0) if isinstance(info.get('history'), dict) else 0
                download = info.get('history', {}).get('down', 0) if isinstance(info.get('history'), dict) else 0
                total = upload + download
                if total > 0:
                    node_stats.append((name, upload, download, total))
        
        # 按总流量排序
        node_stats.sort(key=lambda x: x[3], reverse=True)
        
        if node_stats:
            print(f"{'节点':<30} {'上传':<12} {'下载':<12} {'总计'}")
            print("-" * 70)
            
            for name, upload, download, total in node_stats[:15]:  # 显示前 15 个
                print(f"{name:<30} {format_bytes(upload):<12} {format_bytes(download):<12} {format_bytes(total)}")
        else:
            print("ℹ️  暂无节点流量数据")
        
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ 获取失败：{e}")

def reset_traffic():
    """重置流量统计"""
    try:
        resp = requests.delete(f"{API_URL}/traffic", timeout=5)
        if resp.status_code == 204:
            print("✅ 流量统计已重置")
        else:
            print(f"❌ 重置失败：{resp.status_code}")
    except Exception as e:
        print(f"❌ 重置失败：{e}")

def watch_traffic(interval=5):
    """实时监控流量"""
    print(f"📊 实时监控流量（每 {interval} 秒更新，Ctrl+C 退出）")
    print("=" * 50)
    
    try:
        last_up = 0
        last_down = 0
        
        while True:
            import time
            resp = requests.get(f"{API_URL}/traffic", timeout=5)
            data = resp.json()
            
            upload = data.get('up', 0)
            download = data.get('down', 0)
            
            # 计算速率
            up_speed = (upload - last_up) / interval if last_up > 0 else 0
            down_speed = (download - last_down) / interval if last_down > 0 else 0
            
            print(f"\r📤 ↑ {format_bytes(up_speed)}/s  |  📥 ↓ {format_bytes(down_speed)}/s  |  总计：{format_bytes(upload + download)}    ", end='', flush=True)
            
            last_up = upload
            last_down = download
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n✅ 监控已停止")

def main():
    parser = argparse.ArgumentParser(description="Clash 流量统计")
    parser.add_argument("action", choices=["total", "connections", "proxies", "reset", "watch"],
                       help="操作类型")
    parser.add_argument("--interval", type=int, default=5, help="监控间隔（秒）")
    
    args = parser.parse_args()
    
    if args.action == "total":
        get_traffic()
    
    elif args.action == "connections":
        get_connections()
    
    elif args.action == "proxies":
        get_proxies_traffic()
    
    elif args.action == "reset":
        confirm = input("⚠️  确定要重置流量统计吗？(y/N): ")
        if confirm.lower() == 'y':
            reset_traffic()
    
    elif args.action == "watch":
        watch_traffic(args.interval)


if __name__ == "__main__":
    main()
