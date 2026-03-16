#!/usr/bin/env python3
"""
上海落户公示查询工具
功能：抓取上海国际人才网的落户公示信息并使用浏览器打开
"""

import subprocess
import sys
import re
import argparse
from urllib.request import urlopen, Request
from datetime import datetime
import html

# 公示列表页 URL
LIST_URL = "https://www.sh-italent.com/News/NewsList.aspx?TagID=5696"
BASE_URL = "https://www.sh-italent.com"

# User-Agent
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def fetch_url(url):
    """获取网页内容"""
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"错误：无法获取 {url}: {e}")
        return None

def extract_links(html_content):
    """从列表页面提取公示链接"""
    # 匹配公示文章链接
    pattern = r'href="(https://www\.sh-italent\.com/Article/\d+/\d+\.shtml)"'
    links = re.findall(pattern, html_content)
    return links

def extract_article_info(html_content):
    """提取公示文章信息"""
    # 提取标题
    title_match = re.search(r'<title>([^<]+)</title>', html_content)
    title = title_match.group(1).replace('_上海国际人才网', '').strip() if title_match else "未知标题"
    
    # 提取公示时间
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', html_content)
    date = date_match.group(1) if date_match else "未知日期"
    
    # 提取公示人数（通过表格行数）
    tr_count = len(re.findall(r'<tr', html_content, re.IGNORECASE))
    # 估算人数（减去表头）
    count = max(0, tr_count - 3) if tr_count > 5 else "未知"
    
    return {
        'title': title,
        'date': date,
        'count': count
    }

def get_default_browser():
    """检测 macOS 默认浏览器"""
    try:
        result = subprocess.run(
            ['osascript', '-e', 'tell application "System Events" to get name of first login item'],
            capture_output=True, text=True
        )
        # 通过默认浏览器配置文件检测
        result = subprocess.run(
            ['osascript', '-e', 
             'do shell script "defaults read com.apple.LaunchServices/com.apple.launchservices.secure LSHandlers | grep -A1 \\"LSHandlerRoleAll\\\\" | tail -1 | cut -d\'\\"\' -f2"'],
            capture_output=True, text=True
        )
        bundle_id = result.stdout.strip()
        
        # 映射 bundle ID 到浏览器名称
        browser_map = {
            'com.apple.Safari': 'Safari',
            'com.google.Chrome': 'Chrome',
            'org.mozilla.firefox': 'Firefox',
            'com.microsoft.edgemac': 'Edge',
            'com.brave.Browser': 'Brave',
            'com.operasoftware.Opera': 'Opera',
        }
        return browser_map.get(bundle_id, 'Safari')
    except:
        return 'Safari'

def open_browser_with_applescript(urls, browser=None):
    """使用 AppleScript 打开浏览器"""
    if browser is None:
        browser = get_default_browser()
    
    # 浏览器 AppleScript 名称映射
    browser_names = {
        'Safari': 'Safari',
        'Chrome': 'Google Chrome',
        'Firefox': 'Firefox',
        'Edge': 'Microsoft Edge',
        'Brave': 'Brave',
        'Opera': 'Opera',
    }
    
    app_name = browser_names.get(browser, 'Safari')
    
    print(f"正在使用 {browser} 浏览器打开...")
    
    # 根据不同浏览器生成 AppleScript
    if browser == 'Safari':
        applescript = f'''
tell application "Safari"
    activate
'''
        for i, url in enumerate(urls):
            if i == 0:
                applescript += f'''
    open location "{url}"
    delay 1
'''
            else:
                applescript += f'''
    tell application "System Events" to keystroke "t" using {{command down}}
    delay 0.5
    set URL of document 1 to "{url}"
    delay 0.5
'''
        applescript += '''
end tell
'''
    elif browser == 'Chrome':
        applescript = f'''
tell application "Google Chrome"
    activate
'''
        for i, url in enumerate(urls):
            applescript += f'''
    if (count of windows) = 0 then
        make new window
    end if
    open location "{url}"
    delay 0.5
'''
        applescript += '''
end tell
'''
    elif browser == 'Firefox':
        applescript = f'''
tell application "Firefox"
    activate
'''
        for url in urls:
            applescript += f'''
    open location "{url}"
    delay 1
'''
        applescript += '''
end tell
'''
    elif browser == 'Edge':
        applescript = f'''
tell application "Microsoft Edge"
    activate
'''
        for url in urls:
            applescript += f'''
    open location "{url}"
    delay 0.5
'''
        applescript += '''
end tell
'''
    elif browser == 'Brave':
        applescript = f'''
tell application "Brave"
    activate
'''
        for url in urls:
            applescript += f'''
    open location "{url}"
    delay 0.5
'''
        applescript += '''
end tell
'''
    elif browser == 'Opera':
        applescript = f'''
tell application "Opera"
    activate
'''
        for url in urls:
            applescript += f'''
    open location "{url}"
    delay 0.5
'''
        applescript += '''
end tell
'''
    else:
        # 默认使用 Safari
        applescript = f'''
tell application "Safari"
    activate
    open location "{urls[0]}"
end tell
'''
    
    try:
        subprocess.run(['osascript', '-e', applescript], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"警告：无法打开 {browser}，尝试使用默认浏览器...")
        # 回退到使用 macOS 默认打开方式
        try:
            for url in urls:
                subprocess.run(['open', url], check=True)
            return True
        except Exception as e2:
            print(f"打开浏览器失败: {e2}")
            return False

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='上海落户公示信息查询工具')
    parser.add_argument('-b', '--browser', 
                        choices=['Safari', 'Chrome', 'Firefox', 'Edge', 'Brave', 'Opera'],
                        help='指定使用的浏览器 (Safari/Chrome/Firefox/Edge/Brave/Opera)')
    parser.add_argument('-n', '--no-browser', action='store_true',
                        help='不打开浏览器，仅输出查询结果')
    args = parser.parse_args()
    
    print("=" * 50)
    print("    上海落户公示信息查询")
    print("=" * 50)
    print()
    
    # 1. 获取公示列表页面
    print("[1/4] 获取公示列表页面...")
    list_html = fetch_url(LIST_URL)
    if not list_html:
        print("错误：无法获取公示列表页面")
        sys.exit(1)
    print("✓ 列表页面获取成功")
    print()
    
    # 2. 提取公示链接
    print("[2/4] 解析公示链接...")
    links = extract_links(list_html)
    
    if not links:
        print("错误：未找到公示链接")
        sys.exit(1)
    
    # 区分人才引进和居转户公示
    talent_url = None
    juzhuan_url = None
    
    for link in links[:5]:  # 只检查前5个链接
        if '引进人才' in link or talent_url is None:
            html_content = fetch_url(link)
            if html_content:
                if '引进人才' in html_content and talent_url is None:
                    talent_url = link
                elif '居住证' in html_content and juzhuan_url is None:
                    juzhuan_url = link
    
    # 如果上面没找到，就用列表顺序
    if not talent_url and len(links) > 0:
        talent_url = links[0]
    if not juzhuan_url and len(links) > 1:
        juzhuan_url = links[1]
    
    print(f"✓ 人才引进公示: {talent_url}")
    print(f"✓ 居转户公示: {juzhuan_url}")
    print()
    
    # 3. 获取公示详情
    print("[3/4] 获取公示详情...")
    
    talent_info = None
    juzhuan_info = None
    
    if talent_url:
        talent_html = fetch_url(talent_url)
        if talent_html:
            talent_info = extract_article_info(talent_html)
            print(f"  人才引进: {talent_info['title']}")
            print(f"  公示日期: {talent_info['date']}")
    
    if juzhuan_url:
        juzhuan_html = fetch_url(juzhuan_url)
        if juzhuan_html:
            juzhuan_info = extract_article_info(juzhuan_html)
            print(f"  居转户: {juzhuan_info['title']}")
            print(f"  公示日期: {juzhuan_info['date']}")
    
    print()
    
    # 4. 输出汇总
    print("[4/4] 查询结果汇总")
    print("=" * 50)
    print()
    
    print("【一】人才引进公示")
    if talent_info and talent_url:
        print(f"  公示标题: {talent_info['title']}")
        print(f"  公示日期: {talent_info['date']}")
        print(f"  公示链接: {talent_url}")
    else:
        print("  未找到公示信息")
    print()
    
    print("【二】居转户公示")
    if juzhuan_info and juzhuan_url:
        print(f"  公示标题: {juzhuan_info['title']}")
        print(f"  公示日期: {juzhuan_info['date']}")
        print(f"  公示链接: {juzhuan_url}")
    else:
        print("  未找到公示信息")
    print()
    
    print("=" * 50)
    print(f"查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    print()
    
    # 5. 打开浏览器
    if args.no_browser:
        print("提示：跳过浏览器打开（使用了 --no-browser 参数）")
    else:
        print("正在打开浏览器查看公示页面...")
        
        urls_to_open = [LIST_URL]
        if talent_url:
            urls_to_open.append(talent_url)
        if juzhuan_url:
            urls_to_open.append(juzhuan_url)
        
        if open_browser_with_applescript(urls_to_open, args.browser):
            print("✓ 浏览器已打开")
        else:
            print("提示：请手动访问以下链接查看公示：")
            for url in urls_to_open:
                print(f"  {url}")
    
    print()
    print("提示：公示期通常为 5 天，每月两次公示（月中和月底）")

if __name__ == "__main__":
    main()
