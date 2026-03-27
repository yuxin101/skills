import requests
import json
import sys
import tempfile

API_BASE_URL = "https://api.jiuma.com/"
TOKEN_FILE= tempfile.gettempdir()+'/jmai_user_token_key.text'
def upload_file(file_path,endpoint):
    try:
        token = None
        try:
            with open(TOKEN_FILE, 'r', encoding='utf-8') as file:
                token = file.read()  # 读取整个文件内容
        except FileNotFoundError:
            #print("文件不存在，请检查路径。")
            pass
        headers = {
            "Authorization": f"Bearer {token}"
        }
        url = f"{API_BASE_URL}{endpoint}"
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files,headers=headers)
            response.raise_for_status()
            result = response.json()
            if result.get("code") == 200:
                file_url = result.get("data", {}).get("file_url")
                print(f"上传的文件地址: {file_url}")
                sys.exit(1)
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
            print(f"返回: {response}")
            result.get("code")
    except Exception as e:
        print(f"上传失败: {str(e)}")

if __name__ == "__main__":
    try:
        input_json = json.loads(sys.argv[1].replace("'","\""))
        if not input_json:
            print("错误: 没有提供任何参数")
            print("用法: python ./scripts/jmai_upload.py <json>")
            sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        sys.exit(1)
    # 构建任务参数 (与前端表单对应)
    task_params = input_json
    try:
        file_path = task_params.get("file_path")
        upload_file(file_path,"console/aiApp/uploadOneFile")
        sys.exit(1)
    except Exception as e:
            print(f"错误: 提交任务时发生错误 - {e}")
            sys.exit(1)
