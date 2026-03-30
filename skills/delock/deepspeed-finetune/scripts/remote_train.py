#!/usr/bin/env python3
"""
远程训练管理器：在远程 GPU 服务器上异步执行训练，通过日志文件监控进度。

设计原则：
1. 异步执行 — 启动训练后立即返回，不阻塞主进程
2. 实时日志 — 训练脚本使用 -u (unbuffered) + tee 写日志
3. 进度轮询 — 主进程通过读取日志文件获取最新进度
4. 状态追踪 — 通过状态文件记录训练状态（running/completed/failed）

使用方式（在本地机器上调用）：
    # 1. 启动远程训练（异步，立即返回）
    python3 scripts/remote_train.py launch \\
        --host user@your-server.com \\
        --port 22 \\
        --password YOUR_PASSWORD \\
        --script train_qwen25_0.5b.py \\
        --log train_log.txt

    # 2. 查询训练进度（随时调用）
    python3 scripts/remote_train.py status \\
        --host user@your-server.com \\
        --port 22 \\
        --password YOUR_PASSWORD \\
        --log train_log.txt

    # 3. 获取完整日志
    python3 scripts/remote_train.py logs \\
        --host user@your-server.com \\
        --port 22 \\
        --password YOUR_PASSWORD \\
        --log train_log.txt

    # 4. 终止训练
    python3 scripts/remote_train.py stop \\
        --host user@your-server.com \\
        --port 22 \\
        --password YOUR_PASSWORD \\
        --log train_log.txt
"""

import argparse
import subprocess
import re
import sys
import json
import os
import time


def ssh_exec(host, port, password, cmd, timeout=15):
    """在远程服务器上执行命令并返回输出。"""
    ssh_cmd = [
        "sshpass", "-p", password,
        "ssh", "-o", "StrictHostKeyChecking=no",
        "-o", "ServerAliveInterval=30",
        "-o", "ConnectTimeout=10",
        "-p", str(port), host,
        cmd
    ]
    try:
        result = subprocess.run(
            ssh_cmd, capture_output=True, text=True, timeout=timeout
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "SSH timeout", 1


def scp_upload(host, port, password, local_path, remote_path):
    """上传文件到远程服务器。"""
    scp_cmd = [
        "sshpass", "-p", password,
        "scp", "-o", "StrictHostKeyChecking=no",
        "-P", str(port), local_path, f"{host}:{remote_path}"
    ]
    result = subprocess.run(scp_cmd, capture_output=True, text=True, timeout=60)
    return result.returncode == 0


def launch(args):
    """在远程服务器上启动训练任务（异步）。"""

    # 1. 上传训练脚本
    print(f"📤 上传训练脚本 {args.script} → {args.remote_dir}/{args.script}")
    success = scp_upload(args.host, args.port, args.password, args.script, f"{args.remote_dir}/{args.script}")
    if not success:
        print("❌ 上传失败")
        return

    # 2. Build remote launch command
    # Use -u for unbuffered Python output
    log_path = f"{args.remote_dir}/{args.log}"
    remote_cmd = (
        f"cd {args.remote_dir} && "
        f"nohup {args.remote_python} -u {args.script} > {log_path} 2>&1 & echo $!; exit"
    )

    # 3. 启动远程训练
    print(f"🚀 在 {args.host} 上启动训练...")
    stdout, stderr, code = ssh_exec(args.host, args.port, args.password, remote_cmd, timeout=30)

    if code != 0:
        print(f"❌ 启动失败: {stderr}")
        return

    pid = stdout.strip().split('\n')[-1]
    print(f"✅ 训练已启动，远程 PID: {pid}")
    print(f"📋 日志文件: {args.host}:{log_path}")
    print(f"💡 使用 'status' 命令查看进度")

    # 保存连接信息到本地
    session_file = f".remote_train_session.json"
    session = {
        "host": args.host,
        "port": args.port,
        "password": args.password,
        "pid": pid,
        "log": log_path,
        "remote_dir": args.remote_dir,
        "script": args.script,
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    with open(session_file, "w") as f:
        json.dump(session, f, indent=2)
    print(f"💾 会话信息已保存到 {session_file}")


def get_status(args):
    """查询远程训练状态和进度。"""

    # 尝试读取本地会话文件
    session_file = ".remote_train_session.json"
    if os.path.exists(session_file):
        with open(session_file) as f:
            session = json.load(f)
        host = session.get("host", args.host)
        port = session.get("port", args.port)
        password = session.get("password", args.password)
        log_path = session.get("log", f"{args.remote_dir}/{args.log}")
        pid = session.get("pid")
    else:
        host = args.host
        port = args.port
        password = args.password
        log_path = f"{args.remote_dir}/{args.log}"
        pid = None

    # 检查进程是否还在运行
    if pid:
        check_cmd = f"ps -p {pid} -o pid,pcpu,pmem,etime,args --no-headers 2>/dev/null"
        stdout, _, code = ssh_exec(host, port, password, check_cmd)
        if code == 0 and stdout.strip():
            print(f"🟢 训练进程运行中:")
            print(f"   {stdout.strip()}")
        else:
            print(f"🔴 训练进程已结束 (PID {pid})")

    # 检查 GPU 使用情况
    gpu_cmd = "nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader 2>/dev/null"
    stdout, _, _ = ssh_exec(host, port, password, gpu_cmd)
    if stdout.strip():
        parts = stdout.strip().split(", ")
        if len(parts) >= 4:
            print(f"🎮 GPU: {parts[0]} / {parts[1]}, 利用率: {parts[2]}, 温度: {parts[3]}")

    # 读取日志最后 N 行
    log_cmd = f"tail -{args.tail_lines} {log_path} 2>/dev/null"
    stdout, _, _ = ssh_exec(host, port, password, log_cmd)
    if stdout.strip():
        print(f"\n📋 最新日志 ({log_path}):")
        print("-" * 60)

        # 提取关键训练指标
        lines = stdout.strip().split('\n')
        progress_info = []
        for line in lines:
            # 解析训练 loss 行
            loss_match = re.search(r"'loss':\s*'?([\d.]+)'?", line)
            eval_match = re.search(r"'eval_loss':\s*'?([\d.]+)'?", line)
            lr_match = re.search(r"'learning_rate':\s*'?([\d.e+-]+)'?", line)
            epoch_match = re.search(r"'epoch':\s*'?([\d.]+)'?", line)
            step_match = re.search(r"(\d+)%\|", line)

            if loss_match:
                progress_info.append(f"  📉 Train Loss: {loss_match.group(1)}")
                if lr_match:
                    progress_info.append(f"  📈 LR: {lr_match.group(1)}")
                if epoch_match:
                    progress_info.append(f"  🔄 Epoch: {epoch_match.group(1)}")

            if eval_match:
                progress_info.append(f"  🧪 Eval Loss: {eval_match.group(1)}")

        # 输出日志
        for line in lines:
            print(line)

        # 输出关键指标摘要
        if progress_info:
            print("\n📊 训练指标摘要:")
            for info in progress_info:
                print(info)
    else:
        print("⚠️ 日志文件为空或不存在")

    # 检查日志文件大小（判断是否有新输出）
    size_cmd = f"stat --format=%s {log_path} 2>/dev/null"
    stdout, _, _ = ssh_exec(host, port, password, size_cmd)
    if stdout.strip():
        size_kb = int(stdout.strip()) / 1024
        print(f"\n📄 日志大小: {size_kb:.1f} KB")


def get_logs(args):
    """获取完整或尾部日志。"""
    session_file = ".remote_train_session.json"
    if os.path.exists(session_file):
        with open(session_file) as f:
            session = json.load(f)
        log_path = session.get("log", f"{args.remote_dir}/{args.log}")
    else:
        log_path = f"{args.remote_dir}/{args.log}"

    lines = args.tail_lines if args.tail_lines else 100
    log_cmd = f"tail -{lines} {log_path} 2>/dev/null"
    stdout, _, _ = ssh_exec(args.host, args.port, args.password, log_cmd, timeout=30)
    print(stdout if stdout.strip() else "⚠️ 无日志输出")


def stop(args):
    """终止远程训练进程。"""
    session_file = ".remote_train_session.json"
    if os.path.exists(session_file):
        with open(session_file) as f:
            session = json.load(f)
        pid = session.get("pid")
    else:
        print("❌ 未找到会话文件")
        return

    if not pid:
        print("❌ 未找到 PID")
        return

    kill_cmd = f"kill {pid} 2>/dev/null; sleep 1; ps -p {pid} 2>/dev/null || echo 'Process terminated'"
    stdout, _, _ = ssh_exec(args.host, args.port, args.password, kill_cmd)
    print(f"🛑 终止进程 PID {pid}")
    print(stdout.strip())


def main():
    parser = argparse.ArgumentParser(description="远程训练管理器")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # launch 命令
    launch_parser = subparsers.add_parser("launch", help="在远程服务器上启动训练")
    launch_parser.add_argument("--host", required=True, help="SSH 地址 (user@host)")
    launch_parser.add_argument("--port", type=int, default=22, help="SSH 端口")
    launch_parser.add_argument("--password", required=True, help="SSH 密码")
    launch_parser.add_argument("--script", required=True, help="训练脚本文件名（本地路径）")
    launch_parser.add_argument("--log", default="train_log.txt", help="远程日志文件名")
    launch_parser.add_argument("--remote-dir", default="/root", help="Remote working directory")
    launch_parser.add_argument("--remote-python", default="python3", help="Python executable on remote host")

    # status 命令
    status_parser = subparsers.add_parser("status", help="查询训练状态")
    status_parser.add_argument("--host", help="SSH 地址")
    status_parser.add_argument("--port", type=int, default=22, help="SSH 端口")
    status_parser.add_argument("--password", help="SSH 密码")
    status_parser.add_argument("--log", default="train_log.txt", help="日志文件名")
    status_parser.add_argument("--remote-dir", default="/root", help="远程工作目录")
    status_parser.add_argument("--tail-lines", type=int, default=30, help="显示最后N行日志")

    # logs 命令
    logs_parser = subparsers.add_parser("logs", help="获取日志")
    logs_parser.add_argument("--host", required=True, help="SSH 地址")
    logs_parser.add_argument("--port", type=int, default=22, help="SSH 端口")
    logs_parser.add_argument("--password", required=True, help="SSH 密码")
    logs_parser.add_argument("--log", default="train_log.txt", help="日志文件名")
    logs_parser.add_argument("--remote-dir", default="/root", help="远程工作目录")
    logs_parser.add_argument("--tail-lines", type=int, default=100, help="显示最后N行日志")

    # stop 命令
    stop_parser = subparsers.add_parser("stop", help="终止训练")
    stop_parser.add_argument("--host", help="SSH 地址")
    stop_parser.add_argument("--port", type=int, default=22, help="SSH 端口")
    stop_parser.add_argument("--password", help="SSH 密码")

    args = parser.parse_args()

    if args.command == "launch":
        launch(args)
    elif args.command == "status":
        get_status(args)
    elif args.command == "logs":
        get_logs(args)
    elif args.command == "stop":
        stop(args)


if __name__ == "__main__":
    main()
