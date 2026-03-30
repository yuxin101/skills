import sys
import json
import requests
import time
import os
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlparse, parse_qs
import tempfile

# API基础URL (请根据实际环境配置)
#API_BASE_URL = os.getenv("TASK_API_BASE_URL", "https://testapi-live.kuduo.com/")
API_BASE_URL = "https://api.jiuma.com/"
TOKEN_FILE= tempfile.gettempdir()+'/jmai_user_token_key.text'

def call_api(endpoint: str, data: dict) -> dict:
    """调用API的通用函数"""
    url = f"{API_BASE_URL}{endpoint}"
    token = None
    try:
        with open(TOKEN_FILE, 'r', encoding='utf-8') as file:
            token = file.read()  # 读取整个文件内容
    except FileNotFoundError:
        #print("文件不存在，请检查路径。")
        pass
    headers = {
        "Content-Type": "application/json"
    }
    if token:
            headers["Authorization"] = f"Bearer {token}"
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API调用失败: {str(e)}")

def submit_task(task_params: dict) -> str:
    """
    步骤1: 提交任务
    接口: /console/aiApp/skillAiTaskAdd
    返回任务ID
    """
    request_data = {
        "task_params": json.dumps(task_params, ensure_ascii=False)
    }
    result = call_api("/console/aiApp/skillAiTaskAdd", request_data)
    if result.get("code") == 200:
        return result["data"]["task_id"]
    elif result.get("code") == 401:  # 未授权/未登录
        # 检查是否包含登录地址
        login_code_url = result.get("data", {}).get("login_code_url")
        rand_string = result.get("data", {}).get("rand_string")
        if rand_string:
            with open(TOKEN_FILE, 'w', encoding='utf-8') as file:
                file.write(rand_string)
        if login_code_url:
            print(f"\n提交任务前需要扫描二维码授权账号，",end="")
            print(f"专属授权二维码: {login_code_url}")
            sys.exit(1)
        else:
            raise Exception("未授权，请先登录")
    else:
        raise Exception(f"提交任务失败: {result.get('message', '未知错误')}")

def parse_command_line_args():
    """
    解析命令行参数，支持同名参数
    支持格式: --key value 或 --key=value
    """
    args = sys.argv[1:]  # 跳过脚本名
    result = defaultdict(list)
    current_key = None

    i = 0
    while i < len(args):
        arg = args[i]

        # 处理 --key=value 格式
        if arg.startswith('--') and '=' in arg:
            key, value = arg[2:].split('=', 1)
            result[key].append(value)

        # 处理 --key value 格式
        elif arg.startswith('--'):
            key = arg[2:]
            current_key = key

            # 检查下一个参数是否是值（不是以--开头）
            if i + 1 < len(args) and not args[i + 1].startswith('--'):
                result[key].append(args[i + 1])
                i += 1  # 跳过值
            else:
                result[key].append(True)  # 标志参数

        # 处理普通值（非键）
        elif current_key:
            result[current_key].append(arg)

        i += 1

    # 简化：如果只有一个值，就不需要数组
    for key in list(result.keys()):
        if len(result[key]) == 1:
            result[key] = result[key][0]

    return dict(result)

def check_status(task_id: str) -> dict:
    """
    步骤2/3: 查询任务状态与结果
    接口: /console/aiApp/skillAiTaskStatus
    返回完整的API响应数据
    """
    request_data = {"task_id": task_id}
    result = call_api("/console/aiApp/skillAiTaskStatus", request_data)
    if result.get("code") == 200:
        return result["data"]
    else:
        raise Exception(f"查询状态失败: {result.get('message', '未知错误')}")

def wait_for_result(task_id: str, interval_seconds: int = 5, timeout_seconds: int = 600) -> dict:
    """
    轮询任务状态，直到完成（成功或失败）或超时
    """
    start_time = time.time()
    while time.time() - start_time < timeout_seconds:
        status_data = check_status(task_id)
        task_status = status_data.get("task_status")
        if task_status in ["SUCCEEDED", "FAILED", "CANCELED", "UNKNOWN"]:
            return status_data
        elif task_status in ["PENDING", "RUNNING"]:
            print(f"任务 {task_id} 状态: {task_status}, 等待 {interval_seconds} 秒后重试...")
            time.sleep(interval_seconds)
        else:
            raise Exception(f"未知的任务状态: {task_status}")
    raise Exception(f"任务轮询超时 (超时设置: {timeout_seconds}秒)")

def download_file(url, local_path, **kwargs):
    """从给定的URL下载文件到本地路径。"""
    try:
        response = requests.get(url, stream=True, **kwargs)
        response.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except requests.exceptions.RequestException as e:
        raise Exception(f"下载文件失败: {e}")

if __name__ == "__main__":
    """
    命令行入口。
    提交任务并轮询结果: python {baseDir}/scripts/jmai.py "<JSON>"
    """
    try:
        input_json = json.loads(sys.argv[1].replace("'","\""))
        #input_json=parse_command_line_args()
        if not input_json:
            print("错误: 没有提供任何参数")
            print("用法: python ./scripts/jmai.py --key1 value1 --key2 value2 --key2 value3")
            sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        sys.exit(1)

    # 构建任务参数 (与前端表单对应)
    task_params = input_json

    # 1. 提交任务
    try:
        task_id = submit_task(task_params)
        print(f"任务提交成功! Task ID: {task_id}")
    except Exception as e:
        print(f"错误: 提交任务时发生错误 - {e}")
        sys.exit(1)

    # 2. 轮询并等待结果
    print(f"开始轮询任务状态 (Task ID: {task_id})...")
    try:
        final_res = wait_for_result(task_id)
        print(json.dumps(final_res, indent=2, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(f"错误: 获取结果时发生错误 - {e}")
        sys.exit(1)