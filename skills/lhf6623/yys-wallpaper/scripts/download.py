#!/usr/bin/env python3
"""
阴阳师原画壁纸下载脚本
- 自动抓取页面所有图片 URL
- 按分辨率筛选/下载
- 跳过已存在的文件
"""

import os
import re
import sys
import random
import time
import urllib.request
import urllib.error
from urllib.parse import urljoin

BASE_URL = "https://yys.163.com/media/picture.html"
DEFAULT_RESOLUTION = "1920x1080"
SAVE_DIR = os.path.expanduser("~/Pictures")
TIMEOUT = 10
SKIP_EXISTING = True
MIN_DELAY = 0.2
MAX_DELAY = 0.8


def fetch_page(url):
    """获取网页内容"""
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read().decode('utf-8', errors='ignore')


def extract_image_urls(html, resolution):
    """从页面 HTML 中提取所有图片 URL"""
    pattern = r'(https://yys\.res\.netease\.com/pc/zt/\d+/data/picture/\d+/\d+/' + re.escape(resolution) + r'\.(?:jpg|png))'
    urls = re.findall(pattern, html)
    return list(set(urls))


def url_to_filename(url, resolution):
    """将 URL 转换为文件名"""
    match = re.search(r'(picture/\d+/\d+/' + re.escape(resolution) + r'\.(?:jpg|png))', url)
    if match:
        path = match.group(1)
        return path.replace('picture/', '').replace('/', '_')
    return None


def get_save_path(url, resolution):
    """获取完整保存路径"""
    filename = url_to_filename(url, resolution)
    if not filename:
        return None
    return os.path.join(SAVE_DIR, resolution, filename)


def download_file(url, save_path, retries=3):
    """下载单个文件，失败自动重试"""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                data = resp.read()
                with open(save_path, 'wb') as f:
                    f.write(data)
            if os.path.getsize(save_path) == 0:
                raise ValueError("文件大小为0，重试")
            return True
        except Exception as e:
            if attempt < retries - 1:
                continue
            raise
    return False


def main():
    resolution = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_RESOLUTION

    print(f"📥 开始下载阴阳师壁纸 | 分辨率: {resolution}")
    print(f"📁 保存目录: {SAVE_DIR}/{resolution}/")
    print("-" * 50)

    # 创建保存目录
    target_dir = os.path.join(SAVE_DIR, resolution)
    os.makedirs(target_dir, exist_ok=True)

    # 获取页面
    print("🌐 获取页面...")
    try:
        html = fetch_page(BASE_URL)
    except Exception as e:
        print(f"❌ 获取页面失败: {e}")
        sys.exit(1)

    # 提取 URL
    urls = extract_image_urls(html, resolution)
    print(f"🔍 找到 {len(urls)} 张图片")

    if not urls:
        print("⚠️ 未找到图片，可能页面结构已变或该分辨率不存在")
        sys.exit(1)

    # 下载
    downloaded = skipped = failed = 0
    total = len(urls)

    for i, url in enumerate(sorted(urls), 1):
        save_path = get_save_path(url, resolution)

        if SKIP_EXISTING and os.path.exists(save_path):
            time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
            print(f"⏭️  [{i}/{total}] 跳过 (已存在): {os.path.basename(save_path)}")
            skipped += 1
            continue

        time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
        print(f"⬇️  [{i}/{total}] 下载: {os.path.basename(save_path)}", end=" ... ", flush=True)

        try:
            download_file(url, save_path)
            size = os.path.getsize(save_path) / 1024
            print(f"✅ {size:.1f} KB")
            downloaded += 1
        except Exception as e:
            print(f"❌ {e}")
            failed += 1

    print("-" * 50)
    print(f"✅ 完成！共 {total} 张 | 下载: {downloaded} | 跳过: {skipped} | 失败: {failed}")


if __name__ == "__main__":
    main()
