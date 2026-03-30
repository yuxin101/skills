#!/usr/bin/env python3
"""
Novel Scraper - 轻量级小说抓取工具
针对低内存服务器优化，支持会话复用、自动内存监控、错误恢复

核心特性：
- 会话复用（每 3 章释放一次内存）
- 自动内存监控（>2.5GB 自动释放）
- 错误恢复（失败自动重试 3 次）
- 轻量级（使用 curl + BeautifulSoup）
- 智能滚动（内容不再增加时停止）
- 缓存系统（避免重复抓取）
"""

import json
import os
import sys
import time
import hashlib
import logging
import random
import argparse
import re
import subprocess
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, urljoin

try:
    import psutil

    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

try:
    from bs4 import BeautifulSoup

    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

# 配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
SKILL_DIR = WORKSPACE / "skills" / "novel-scraper"
CONFIG_DIR = SKILL_DIR / "configs"
STATE_DIR = SKILL_DIR / "state"
LOG_DIR = SKILL_DIR / "logs"
CACHE_DIR = Path("/tmp/novel_scraper_cache")
NOVELS_DIR = WORKSPACE / "novels"

# 确保目录存在
for d in [CONFIG_DIR, STATE_DIR, LOG_DIR, CACHE_DIR, NOVELS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# 黑名单常量（统一管理，避免重复定义）
CONTENT_BLACKLIST = [
    "笔趣阁",
    "首页",
    "目录",
    "上一章",
    "下一章",
    "书页",
    "手机版",
    "推荐本书",
    "返回书目",
    "章节错误",
    "点此举报",
    "投推荐票",
    "加入书签",
    "返回首页",
    "友情链接",
    "广告合作",
    "手机版小说",
    "下载小说",
    "APP下载",
    "账号注册",
    "会员注册",
    "章节目录",
    "章节标题",
    "章节内容",
    "小说目录",
    "最新章节",
    "热门推荐",
    "友情推荐",
    " Last updated",
    "Updated:",
]

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "scraper.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class MemoryMonitor:
    """内存监控器 - 学习自成功案例"""

    def __init__(self, limit_mb=2500):
        self.limit_mb = limit_mb

    def check(self):
        """检查内存使用（通过/proc/meminfo）"""
        try:
            with open("/proc/meminfo", "r") as f:
                mem_info = {}
                for line in f:
                    if ":" in line:
                        key, value = line.split(":", 1)
                        mem_info[key.strip()] = (
                            int(value.strip().split()[0]) / 1024
                        )  # MB

            total = mem_info.get("MemTotal", 0)
            available = mem_info.get("MemAvailable", 0)
            used = total - available

            if used > self.limit_mb:
                logger.warning(f"⚠️ 内存过高 ({used:.0f}MB/{self.limit_mb}MB)，需要释放")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ 内存检查失败：{e}")
            return False

    def release_memory(self):
        """实际释放内存操作"""
        import gc

        # 强制垃圾回收
        collected = gc.collect()
        logger.info(f" 🧹 GC回收了 {collected} 个对象")

        # 清理临时文件（可选）
        try:
            import tempfile

            tempfile.TemporaryDirectory().cleanup()
        except Exception:
            pass

        return collected


class CacheManager:
    """缓存管理器 - 支持章节级和页面级缓存"""

    def __init__(self, cache_dir=CACHE_DIR, use_cache=True):
        self.cache_dir = Path(cache_dir)
        self.use_cache = use_cache
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_cache_key(self, url, page_num=None):
        """生成缓存键（MD5）"""
        if page_num is not None:
            # 页面级缓存
            key_str = f"{url}_page_{page_num}"
        else:
            # 章节级缓存
            key_str = url
        return hashlib.md5(key_str.encode()).hexdigest()[:16]

    def get(self, url, page_num=None):
        """从缓存获取内容"""
        if not self.use_cache:
            return None

        cache_key = self.get_cache_key(url, page_num)
        cache_file = self.cache_dir / f"{cache_key}.txt"

        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    lines = f.read().strip().split("\n")
                    if lines:
                        if page_num is not None:
                            # 页面级缓存直接返回内容
                            logger.info(f" 💾 使用页面缓存：{url} (第{page_num}页)")
                            return lines
                        else:
                            # 章节级缓存
                            logger.info(f" 💾 使用章节缓存：{url}")
                            book_name = None
                            author = None
                            if lines[0].startswith("BOOK:"):
                                book_info = lines[0].replace("BOOK:", "").split(":")
                                book_name = book_info[0] if len(book_info) > 0 else None
                                author = book_info[1] if len(book_info) > 1 else None
                                return {
                                    "book_name": book_name,
                                    "author": author,
                                    "content": lines[1:],
                                }
                            return {"book_name": None, "author": None, "content": lines}
            except Exception as e:
                logger.warning(f" ⚠️ 缓存读取失败：{e}")
        return None

    def save(self, url, content, book_name=None, author=None, page_num=None):
        """保存到缓存"""
        if not self.use_cache:
            return

        cache_key = self.get_cache_key(url, page_num)
        cache_file = self.cache_dir / f"{cache_key}.txt"

        try:
            if page_num is not None:
                # 页面级缓存直接保存内容
                with open(cache_file, "w", encoding="utf-8") as f:
                    f.write("\n".join(content))
            else:
                # 章节级缓存
                lines = content[:]
                if book_name:
                    lines.insert(0, f"BOOK:{book_name}:{author or ''}")
                with open(cache_file, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines))
        except Exception as e:
            logger.warning(f" ⚠️ 缓存保存失败：{e}")

    def clear_chapter_cache(self, url):
        """清除章节的所有缓存（包括页面缓存）"""
        cache_key = self.get_cache_key(url)
        # 清除章节级缓存
        chapter_file = self.cache_dir / f"{cache_key}.txt"
        if chapter_file.exists():
            chapter_file.unlink()
        # 清除页面级缓存
        for i in range(1, 11):  # 最多 10 页
            page_key = self.get_cache_key(url, i)
            page_file = self.cache_dir / f"{page_key}.txt"
            if page_file.exists():
                page_file.unlink()


class ProgressTracker:
    """进度追踪器 - 支持中断续抓"""

    def __init__(self, state_dir=STATE_DIR):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.progress_file = self.state_dir / "progress.json"
        self.progress = {"chapters": [], "last_url": None, "errors": []}
        self.load()

    def load(self):
        """加载进度"""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, "r", encoding="utf-8") as f:
                    self.progress = json.load(f)
            except Exception as e:
                logger.warning(f" ⚠️ 进度加载失败：{e}")

    def save(self):
        """保存进度"""
        try:
            with open(self.progress_file, "w", encoding="utf-8") as f:
                json.dump(self.progress, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.warning(f" ⚠️ 进度保存失败：{e}")

    def start_chapter(self, url, chapter_num):
        """开始抓取章节"""
        # 只在新章节时重置页码
        if self.progress.get("current_chapter") != chapter_num:
            self.progress["current_page"] = 1

        self.progress["last_url"] = url
        self.progress["current_chapter"] = chapter_num
        self.save()

    def complete_page(self, url, page_num, content_len):
        """完成一页抓取"""
        self.progress["current_page"] = page_num + 1
        self.progress["last_page_len"] = content_len
        self.save()

    def complete_chapter(self, url, chapter_num, title):
        """完成章节抓取"""
        self.progress["chapters"].append(
            {
                "url": url,
                "title": title,
                "chapter": chapter_num,
                "time": datetime.now().isoformat(),
            }
        )
        self.save()

    def record_error(self, url, error, retry_count, chapter_num=None):
        """记录错误"""
        self.progress["errors"].append(
            {
                "url": url,
                "chapter": chapter_num,
                "error": str(error),
                "retry_count": retry_count,
                "time": datetime.now().isoformat(),
            }
        )
        # 限制错误记录数量
        if len(self.progress["errors"]) > 100:
            self.progress["errors"] = self.progress["errors"][-100:]
        self.save()

    def get_resume_point(self, urls, book_url=None):
        """获取续抓起点"""
        completed_urls = [c["url"] for c in self.progress.get("chapters", [])]

        # 检查书籍上下文
        if book_url and self.progress.get("book_url"):
            if self.progress["book_url"] != book_url:
                logger.info(" 🔄 检测到新书，清空旧进度")
                self.clear()
                self.progress["book_url"] = book_url
                return 0, urls

        # 找到第一个未完成的 URL
        for i, (url, chapter_num) in enumerate(urls):
            if url not in completed_urls:
                logger.info(f" 🔄 发现未完成章节：{url} (第{chapter_num}章)")
                # 返回原始列表的切片，保持章节编号不变
                return i, urls[i:]

        logger.info(" ✅ 所有章节已完成")
        return len(urls), []

    def clear(self):
        """清空进度"""
        self.progress = {"chapters": [], "last_url": None, "errors": []}
        if self.progress_file.exists():
            self.progress_file.unlink()


class SiteAdapter:
    """网站适配器基类"""

    def __init__(self):
        self.name = "BaseAdapter"

    def extract_title(self, soup):
        """提取章节标题"""
        raise NotImplementedError

    def extract_content(self, soup):
        """提取章节内容"""
        raise NotImplementedError

    def extract_next_page(self, soup, base_url):
        """提取下一页链接"""
        raise NotImplementedError

    def is_valid_page(self, soup):
        """检查是否是有效页面"""
        raise NotImplementedError


class BiqugeAdapter(SiteAdapter):
    """笔趣阁原版适配器（biquge.com）"""

    def __init__(self):
        super().__init__()
        self.name = "BiqugeAdapter"

    def extract_title(self, soup):
        h1 = soup.find("h1")
        if h1:
            return h1.get_text().strip()
        return None

    def extract_content(self, soup):
        content_div = soup.find("div", id="content")
        if content_div:
            paras = content_div.find_all("p")
            content = []
            for p in paras:
                text = p.get_text().strip()
                if text and not self._is_nav_or_ad(text):
                    content.append(text)
            return content
        return []

    def extract_next_page(self, soup, base_url):
        pages = soup.find_all("a", string=re.compile(r"第\d+页|下一页|下一页"))
        for a in pages:
            href = a.get("href")
            if href:
                return urljoin(base_url, href)
        return None

    def _is_nav_or_ad(self, text):
        return any(word in text for word in CONTENT_BLACKLIST)


class Biquge2026Adapter(SiteAdapter):
    """笔趣阁 2026 版适配器（www.bqquge.com）"""

    def __init__(self):
        super().__init__()
        self.name = "Biquge2026Adapter"

    def extract_title(self, soup):
        h1 = soup.find("h1")
        if h1:
            return h1.get_text().strip()
        return None

    def extract_content(self, soup):
        con_div = soup.find("div", class_="con")
        if con_div:
            paras = con_div.find_all("p")
            content = []
            for p in paras:
                text = p.get_text().strip()
                if text and not self._is_nav_or_ad(text):
                    content.append(text)
            return content
        return []

    def extract_next_page(self, soup, base_url):
        pages = soup.find_all("a", string=re.compile(r"第\d+页|下一页"))
        for a in pages:
            href = a.get("href")
            if href:
                return urljoin(base_url, href)
        return None

    def _is_nav_or_ad(self, text):
        return any(word in text for word in CONTENT_BLACKLIST)


class SiteAdapterFactory:
    """网站适配器工厂"""

    _adapters = {
        "biquge.com": BiqugeAdapter,
        "bqquge.com": Biquge2026Adapter,
    }

    @staticmethod
    def get_adapter(domain):
        for key, adapter_cls in SiteAdapterFactory._adapters.items():
            if key in domain:
                return adapter_cls()
        return Biquge2026Adapter()


class NovelScraper:
    """小说抓取器 - 整合成功案例的优秀实践"""

    def __init__(
        self,
        memory_limit_mb=2500,
        auto_close_interval=3,
        retry_times=3,
        wait_time=2,
        use_progress=True,
    ):
        self.memory_monitor = MemoryMonitor(limit_mb=memory_limit_mb)
        self.cache = CacheManager()
        self.progress = ProgressTracker() if use_progress else None
        self.auto_close_interval = auto_close_interval
        self.retry_times = retry_times
        self.wait_time = wait_time
        self.chapters_fetched = 0
        self.site_config = {}

        logger.info(f"📖 NovelScraper 初始化完成")
        logger.info(f"  内存限制：{memory_limit_mb}MB")
        logger.info(f"  释放间隔：每{auto_close_interval}章")
        logger.info(f"  重试次数：{retry_times}")
        logger.info(f"  缓存目录：{CACHE_DIR}")
        if self.progress:
            logger.info(f"  进度追踪：✅ 已启用")

    def fetch_html(self, url):
        """使用 curl 获取 HTML 内容"""
        # 安全验证 URL，防止命令注入
        if not self._is_safe_url(url):
            raise Exception(f"Invalid or unsafe URL: {url}")

        try:
            cmd = [
                "curl",
                "-s",
                "-L",
                "--max-time",
                "30",
                "-A",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                url,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=35)

            if result.returncode == 0:
                return result.stdout
            else:
                raise Exception(f"curl failed: {result.stderr}")
        except subprocess.TimeoutExpired:
            raise Exception("curl timeout")
        except Exception as e:
            raise Exception(f"Failed to fetch HTML: {e}")

    def _is_safe_url(self, url):
        """验证 URL 是否安全（防止命令注入）"""
        try:
            parsed = urlparse(url)
            # 只允许 http/https 协议
            if parsed.scheme not in ("http", "https"):
                return False
            # 必须有有效的域名
            if not parsed.netloc:
                return False
            # 检查是否有可疑字符（命令注入风险）
            dangerous_chars = [";", "|", "&", "$", "`", "\n", "\r", "(", ")"]
            if any(char in url for char in dangerous_chars):
                return False
            return True
        except Exception:
            return False

    def parse_html(self, html, url):
        """使用 BeautifulSoup 解析 HTML"""
        if not HAS_BS4:
            raise Exception(
                "BeautifulSoup not installed. Run: pip install beautifulsoup4"
            )

        soup = BeautifulSoup(html, "html.parser")

        domain = urlparse(url).netloc
        adapter = SiteAdapterFactory.get_adapter(domain)

        return soup, adapter

    def check_content_valid(self, content):
        """检查内容是否有效（非导航/广告）"""
        if not content:
            return False

        return not any(word in content for word in CONTENT_BLACKLIST)

    def fetch_all_pages(self, first_url, chapter_num):
        """自动翻页抓取完整章节（支持页面级缓存和中断续抓）"""
        all_content = []
        current_url = first_url
        page_num = 1
        max_pages = 5

        while current_url and page_num <= max_pages:
            logger.info(f" 📄 第{page_num}页...")

            cached_page = self.cache.get(current_url, page_num)
            if cached_page:
                logger.info(f" ✅ 使用页面缓存 ({len(cached_page)}段)")
                all_content.extend(cached_page)

                if self.progress:
                    self.progress.complete_page(current_url, page_num, len(cached_page))

                current_url = self._infer_next_page_url(current_url, page_num)
                if current_url:
                    delay = random.uniform(0.5, 1.5)
                    logger.info(f" ⏳ 等待{delay:.1f}秒...")
                    time.sleep(delay)
                page_num += 1
                continue

            try:
                html = self.fetch_html(current_url)
                soup, adapter = self.parse_html(html, current_url)

                content = adapter.extract_content(soup)

                if not content:
                    logger.warning(f" ⚠️ 第{page_num}页无内容")
                    if page_num == 1:
                        break
                    else:
                        logger.info(f" ✅ 停止翻页（最后一页）")
                        break

                valid_content = [c for c in content if self.check_content_valid(c)]

                if valid_content:
                    self.cache.save(current_url, valid_content, page_num=page_num)
                    logger.info(f" 💾 保存页面缓存 ({len(valid_content)}段)")

                    if self.progress:
                        self.progress.complete_page(
                            current_url, page_num, len(valid_content)
                        )

                    all_content.extend(valid_content)
                else:
                    logger.warning(f" ⚠️ 第{page_num}页内容无效")
                    if page_num == 1:
                        break
                    else:
                        logger.info(f" ✅ 停止翻页（最后一页）")
                        break

                next_url = adapter.extract_next_page(soup, current_url)
                if next_url and next_url != current_url:
                    delay = random.uniform(0.5, 1.5)
                    logger.info(f" ⏳ 等待{delay:.1f}秒...")
                    time.sleep(delay)
                    current_url = next_url
                else:
                    current_url = self._infer_next_page_url(current_url, page_num)

                page_num += 1

            except Exception as e:
                logger.error(f" ❌ 抓取第{page_num}页失败：{e}")
                if page_num == 1:
                    break
                else:
                    logger.info(f" ✅ 停止翻页（最后一页）")
                    break

        logger.info(f" 📚 共{page_num - 1}页，{len(all_content)}段")
        return all_content

    def _infer_next_page_url(self, base_url, current_page_num):
        """推断下一页 URL（不依赖快照）"""
        match = re.search(r"/(\d+)(?:-(\d+))?$", base_url)
        if match:
            chapter_id = match.group(1)
            page_suffix = match.group(2)

            if page_suffix is None:
                next_url = re.sub(r"/\d+$", f"/{chapter_id}-2", base_url)
                logger.debug(f"推断下一页：{next_url}")
                return next_url
            else:
                # 使用新变量名避免覆盖参数
                page_num_from_url = int(page_suffix)
                next_page = page_num_from_url + 1
                next_url = re.sub(r"-\d+$", f"-{next_page}", base_url)
                logger.debug(f"推断下一页：{next_url}")
                return next_url
        return None

    def fetch_chapter(self, url, chapter_num=0):
        """抓取单章（带重试 + 缓存 + 进度追踪）"""
        logger.info(f"📖 抓取第{chapter_num}章：{url}")

        if self.progress:
            self.progress.start_chapter(url, chapter_num)

        cached = self.cache.get(url)
        if cached:
            content = cached["content"]
            book_name = cached.get("book_name")
            author = cached.get("author")
            title = (
                content[0]
                if isinstance(content, list) and content and content[0].startswith("第")
                else f"第{chapter_num}章"
            )
            logger.info(f" 💾 使用章节缓存...")
            if book_name:
                logger.info(f" 📚 小说：{book_name} (缓存)")

            if self.progress:
                self.progress.complete_chapter(url, chapter_num, title)

            return {
                "title": title,
                "content": content[1:]
                if isinstance(content, list) and content and content[0].startswith("第")
                else content,
                "book_name": book_name,
                "author": author,
            }

        for attempt in range(1, self.retry_times + 1):
            try:
                html = self.fetch_html(url)
                soup, adapter = self.parse_html(html, url)

                title = adapter.extract_title(soup)
                if not title:
                    title = f"第{chapter_num}章"

                book_name = None
                author = None
                if chapter_num == 1:
                    book_name, author = self._extract_book_info(soup, adapter)

                content = self.fetch_all_pages(url, chapter_num)

                if content:
                    logger.info(f" ✅ 成功 ({len(content)}段) - {title}")

                    cache_data = [title] + content
                    self.cache.save(url, cache_data, book_name, author)

                    self.chapters_fetched += 1

                    if self.progress:
                        self.progress.complete_chapter(url, chapter_num, title)

                    if self.chapters_fetched % self.auto_close_interval == 0:
                        logger.info(
                            f" 🔄 已达{self.auto_close_interval}章，释放内存..."
                        )
                        self.memory_monitor.release_memory()

                    if self.memory_monitor.check():
                        logger.info(f" 🔄 内存过高，执行释放...")
                        self.memory_monitor.release_memory()

                    return {
                        "title": title,
                        "content": content,
                        "book_name": book_name,
                        "author": author,
                    }
                else:
                    logger.warning(f" ⚠️ 无内容 (尝试 {attempt}/{self.retry_times})")
                    time.sleep(1)

            except Exception as e:
                logger.error(f" ❌ 错误：{e} (尝试 {attempt}/{self.retry_times})")
                if self.progress:
                    self.progress.record_error(url, e, attempt, chapter_num)
                time.sleep(2)

        logger.error(f" ❌ 抓取失败（重试{self.retry_times}次）")
        return {
            "title": f"第{chapter_num}章",
            "content": [],
            "book_name": None,
            "author": None,
        }

    def _extract_book_info(self, soup, adapter):
        """从页面提取书名和作者"""
        book_name = None
        author = None

        breadcrumb = soup.find_all("a")
        nav_blacklist = {"首页", "目录", "排行榜", "完本", "会员", "书架", "笔趣阁"}

        for a in breadcrumb:
            text = a.get_text().strip()
            if text and text not in nav_blacklist and len(text) > 1:
                if "作者" in text or "作者：" in text:
                    author = text.replace("作者：", "").replace("作者", "").strip()
                elif len(text) <= 6 and not text.startswith("第") and "章" not in text:
                    book_name = text

        if book_name:
            logger.info(f" 📚 提取书名：{book_name}")

        return book_name, author

    def save_to_file(
        self,
        contents,
        output_path=None,
        book_name=None,
        author=None,
        auto_workspace=True,
    ):
        """保存到文件（学习自成功案例）"""
        if auto_workspace:
            if not book_name:
                book_name = (
                    contents[0].get("book_name", "novel") if contents else "novel"
                )

            if not book_name or book_name == "novel":
                book_name = "小说"

            first_ch = contents[0].get("chapter", 1)
            last_ch = contents[-1].get("chapter", first_ch)

            if first_ch == last_ch:
                filename = f"{book_name}_第{first_ch}章.txt"
            else:
                filename = f"{book_name}_第{first_ch}-{last_ch}章.txt"

            filename = "".join(c for c in filename if c not in '<>:"/\\|？*')
            output_path = NOVELS_DIR / filename

        logger.info(f"💾 保存到 {output_path}...")

        output_path = Path(str(output_path))
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            for item in contents:
                f.write(f"\n{'=' * 60}\n")
                f.write(f"{item['title']}\n")
                f.write(f"{'=' * 60}\n\n")
                for para in item["content"]:
                    f.write(f"{para}\n\n")

        logger.info(f"✅ 保存完成")
        logger.info(f"📁 文件位置：{output_path}")
        return output_path

    def fetch_chapters(self, urls, output=None, book_name=None, auto_workspace=True):
        """抓取多章（会话复用）"""
        logger.info("=" * 60)
        logger.info(f"📖 开始抓取 {len(urls)} 章")
        logger.info("=" * 60)

        all_contents = []
        start_time = time.time()

        for i, (url, chapter_num) in enumerate(urls, 1):
            logger.info(f"\n[{i}/{len(urls)}]")
            result = self.fetch_chapter(url, chapter_num)
            all_contents.append(
                {
                    "chapter": chapter_num,
                    "title": result.get("title", f"第{chapter_num}章"),
                    "content": result.get("content", []),
                    "url": url,
                    "book_name": result.get("book_name"),
                    "author": result.get("author"),
                }
            )

        duration = time.time() - start_time
        logger.info("\n" + "=" * 60)
        logger.info(
            f"✅ 完成！用时 {duration:.1f}秒，平均每章 {duration / len(urls):.1f}秒"
        )
        logger.info("=" * 60)

        if not book_name and all_contents:
            book_name = all_contents[0].get("book_name")

        self.save_to_file(
            all_contents, output, book_name, auto_workspace=auto_workspace
        )

        return all_contents


def main():
    parser = argparse.ArgumentParser(description="📖 轻量级小说抓取工具")
    parser.add_argument("--url", help="单章 URL")
    parser.add_argument("--urls", help="多章 URL（逗号分隔）")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--book", "-b", help="书名")
    parser.add_argument("--no-auto-save", action="store_true", help="禁用自动保存")
    parser.add_argument(
        "--resume", "-r", action="store_true", help="中断续抓（从上次进度继续）"
    )
    parser.add_argument("--memory-limit", type=int, default=2500, help="内存限制 MB")
    parser.add_argument("--auto-close", type=int, default=3, help="每 N 章释放内存")
    parser.add_argument("--retry", type=int, default=3, help="重试次数")
    parser.add_argument("--wait", type=int, default=2, help="等待时间秒")

    args = parser.parse_args()

    scraper = NovelScraper(
        memory_limit_mb=args.memory_limit,
        auto_close_interval=args.auto_close,
        retry_times=args.retry,
        wait_time=args.wait,
        use_progress=True,
    )

    auto_save = not args.no_auto_save

    if args.url:
        result = scraper.fetch_chapter(args.url, 1)
        if result["content"]:
            print(f"\n{result['title']}\n")
            print("\n".join(result["content"][:10]))
            if auto_save:
                book_name = args.book if args.book else result.get("book_name")
                scraper.save_to_file(
                    [
                        {
                            "chapter": 1,
                            "title": result["title"],
                            "content": result["content"],
                            "book_name": result.get("book_name"),
                        }
                    ],
                    args.output,
                    book_name,
                    auto_save,
                )
    elif args.urls:
        urls = [(url.strip(), i + 1) for i, url in enumerate(args.urls.split(","))]

        if args.resume and scraper.progress:
            logger.info("🔄 启用中断续抓模式...")
            book_url = urls[0][0].rsplit("/", 1)[0] if urls else None
            start_idx, urls = scraper.progress.get_resume_point(urls, book_url)
            if start_idx > 0:
                logger.info(f" ✅ 跳过已完成的 {start_idx} 章")

        scraper.fetch_chapters(urls, args.output, args.book, auto_save)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
