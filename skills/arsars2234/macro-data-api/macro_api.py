import sys
import json
import requests

BASE_URL = "http://10.168.1.162:5000"
TOKEN = "abc123"  
ALLOWED_ENDPOINTS = [
    "money/stock",
    "money/season",
    "money/not-season",
    "fx",
    "fx/all"
]

def call_api(endpoint, params=None):
    if endpoint not in ALLOWED_ENDPOINTS:
        print(f"Error: endpoint {endpoint} not allowed.")
        sys.exit(1)

    url = f"{BASE_URL}/{endpoint}?token={TOKEN}"

    if params:
        if isinstance(params, dict):
            # 原来的逻辑
            for k, v in params.items():
                url += f"&{k}={v}"
        else:
            # 如果是单个数字，直接当 limit 参数
            url += f"&limit={params}"

    resp = requests.get(url)
    try:
        data = resp.json()
    except json.JSONDecodeError:
        print("Error: response is not valid JSON")
        sys.exit(1)
    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python macro_api.py <endpoint> [JSON params or integer]")
        sys.exit(1)

    endpoint = sys.argv[1]
    params = {}

    if len(sys.argv) >= 3:
        arg = sys.argv[2]
        # 尝试解析 JSON
        try:
            params = json.loads(arg)
        except:
            try:
                # 如果解析失败，直接当整数
                params = int(arg)
            except:
                print("Error: params must be JSON or an integer")
                sys.exit(1)

    call_api(endpoint, params)