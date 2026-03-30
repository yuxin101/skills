#!/usr/bin/env python3
"""
Part.7 RWA 项目动态抓取脚本
数据源：PANews RWA周刊（panewslab.com）

策略：
  Step 1：用 DuckDuckGo HTML 搜索找到最新一期文章 URL
  Step 2：curl 抓取文章 HTML（PANews 为 SSR，curl 可直接获取内容）
  Step 3：提取「项目进展」部分，过滤稳定币相关条目

筛选规则：
  收录：实际落地或正在推进中的 RWA 项目
  排除：稳定币相关项目

依赖：curl（系统自带）、python3 标准库
运行：python3 scripts/part7_fetch.py [可选:文章URL]
"""

import subprocess, sys, re
from html.parser import HTMLParser
import urllib.parse

STABLECOIN_KW = [
    '稳定币', 'stablecoin', 'USDT', 'USDC', 'USDE', 'FDUSD',
    'USD1', 'PYUSD', 'DAI', 'FRAX', '港元稳定币', '法币支持'
]
SECTION_KW = ['项目进展', '项目动态', '进展动态']
SECTION_END_KW = ['监管', '数据概览', '市场', '总结', '本周观察', '稳定币市场']


def fetch_url(url):
    r = subprocess.run(
        ['curl', '-s', '-L', '--max-time', '20',
         '-H', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
         '-H', 'Accept: text/html',
         '-H', 'Accept-Language: zh-CN,zh;q=0.9',
         url],
        capture_output=True, text=True
    )
    return r.stdout if r.returncode == 0 else ''


def search_latest_article():
    """用 DuckDuckGo 搜索最新期 RWA 周刊 URL"""
    query = urllib.parse.quote('site:panewslab.com "RWA周刊" "项目进展" 2026')
    html = fetch_url(f'https://html.duckduckgo.com/html/?q={query}')
    if not html:
        return ''
    urls = re.findall(
        r'https?://www\.panewslab\.com/(?:zh|en)/articles/[a-f0-9\-]{30,}',
        html
    )
    seen = set()
    for u in urls:
        if u not in seen:
            seen.add(u)
            return u
    return ''


class ArticleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_tag = False
        self.paragraphs = []
        self.current = []

    def handle_starttag(self, tag, attrs):
        if tag in ('p', 'h1', 'h2', 'h3', 'h4', 'h5', 'li'):
            self.in_tag = True
            self.current = []

    def handle_endtag(self, tag):
        if self.in_tag and tag in ('p', 'h1', 'h2', 'h3', 'h4', 'h5', 'li'):
            text = re.sub(r'\s+', ' ', ''.join(self.current)).strip()
            if text and len(text) > 3:
                self.paragraphs.append(text)
            self.in_tag = False
            self.current = []

    def handle_data(self, data):
        if self.in_tag:
            self.current.append(data)


def extract_and_parse(html):
    """提取项目进展部分并解析项目"""
    # 解析段落
    parser = ArticleParser()
    parser.feed(html)
    paragraphs = parser.paragraphs

    # 若 HTML 解析段落过少，用正则备用
    if len(paragraphs) < 10:
        raw = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
        paragraphs = [re.sub(r'<[^>]+>', '', p).strip() for p in raw if len(p.strip()) > 3]

    # 找「项目进展」部分
    in_section = False
    section = []
    for para in paragraphs:
        if not in_section:
            if any(kw in para for kw in SECTION_KW):
                in_section = True
            continue
        # 遇到下一章节标题则停止
        if len(para) < 25 and any(kw in para for kw in SECTION_END_KW):
            break
        section.append(para)

    if not section:
        return [], paragraphs  # 返回全部段落供调试

    # 解析项目：短行为项目名，后续长行为详情
    projects = []
    cur_name, cur_details = None, []

    for para in section:
        is_stablecoin = any(kw in para for kw in STABLECOIN_KW)
        is_title = (
            len(para) < 35 and
            '。' not in para and
            not para.startswith(('根据', '据', '此前', '近期'))
        )

        if is_title and len(para) > 2:
            if cur_name and cur_details and not any(kw in cur_name for kw in STABLECOIN_KW):
                projects.append({'name': cur_name, 'detail': ' '.join(cur_details[:3])})
            cur_name = para if not is_stablecoin else None
            cur_details = []
        elif cur_name and not is_stablecoin:
            cur_details.append(para)

    if cur_name and cur_details and not any(kw in cur_name for kw in STABLECOIN_KW):
        projects.append({'name': cur_name, 'detail': ' '.join(cur_details[:3])})

    return projects, section


def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(f'[INFO] 使用指定 URL: {url}', file=sys.stderr)
    else:
        print('[INFO] 搜索最新期 RWA 周刊...', file=sys.stderr)
        url = search_latest_article()
        if not url:
            print('\n[⚠️] 无法自动找到最新期文章 URL。', file=sys.stderr)
            print('请手动运行：python3 scripts/part7_fetch.py <文章URL>')
            print('文章列表参考：https://www.panewslab.com/zh/ 搜索「RWA周刊」')
            sys.exit(1)
        print(f'[INFO] 找到文章: {url}', file=sys.stderr)

    html = fetch_url(url)
    if not html:
        print('[ERROR] 文章抓取失败', file=sys.stderr)
        sys.exit(1)
    print(f'[INFO] HTML 长度: {len(html)} 字节', file=sys.stderr)

    projects, section = extract_and_parse(html)
    print(f'[INFO] 解析到 {len(projects)} 个项目', file=sys.stderr)

    print('=' * 55)
    print('  Part.7  RWA 项目动态')
    print(f'  来源：PANews RWA周刊 {url}')
    print('=' * 55)

    if projects:
        for p in projects:
            detail = p['detail'][:200]
            print(f'\n{p["name"]}\n详情：{detail}')
        print(f'\n共 {len(projects)} 个项目（已排除稳定币相关）')
    else:
        print('\n[⚠️] 自动解析未找到项目条目。')
        if section:
            print('\n── 项目进展原始段落（供手动整理）──')
            for s in section[:20]:
                print(f'  {s}')
        else:
            print('请将本期「项目进展」部分粘贴给 AI 整理。')

    print('\n⚠️  建议与原文核对，稳定币相关项目已自动过滤。')


if __name__ == '__main__':
    main()
