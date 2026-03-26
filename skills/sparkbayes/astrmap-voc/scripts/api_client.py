"""
CustomerInsights API Client
用于 AI Agent 调用评论采集和分析接口

Author: Zhang Di
Email: dizflyme@qq.com
Date: 2025-03-25
Description: 跨境电商客户洞察 API 客户端封装（零外部依赖版）
"""

import json
import os
import ssl

# 使用 requests 库以确保 macOS 证书兼容性
try:
    import requests
except ImportError:
    raise ImportError("请安装 requests 库: pip install requests")
from typing import Any, Dict

# 从环境变量读取配置，可在 ~/.zshrc 或 ~/.bashrc 中设置：
#   export CUSTOMER_INSIGHTS_API_KEY="your-api-key"
#   export CUSTOMER_INSIGHTS_BASE_URL="https://api.astrmap.com"  # 可选，默认已填入
_DEFAULT_API_KEY = os.environ.get("CUSTOMER_INSIGHTS_API_KEY", "")
_DEFAULT_BASE_URL = os.environ.get(
    "CUSTOMER_INSIGHTS_BASE_URL", "https://api.astrmap.com"
)

# 使用 requests 库以确保 macOS 证书兼容性
try:
    import requests
except ImportError:
    raise ImportError("请安装 requests 库: pip install requests")

# SSL 上下文（安全配置）
_SSL_CONTEXT = ssl.create_default_context()


class CustomerInsightsClient:
    """CustomerInsights API 客户端（同步，零外部依赖）"""

    def __init__(self, api_key: str, base_url: str = _DEFAULT_BASE_URL):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def _post(self, path: str, data: dict = None) -> dict:
        """POST 请求"""
        url = f"{self.base_url}{path}"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            response = requests.post(url, json=data or {}, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            if result.get("code") != 0:
                raise Exception(f"API Error: {result.get('msg')}")
            return result.get("data", {})
        except requests.exceptions.HTTPError as e:
            raise Exception(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request Error: {e}")

    # ==================== 设备管理 ====================

    def check_device_online(self) -> Dict[str, Any]:
        """检查设备是否在线

        返回:
            online: bool - 是否在线
            device_id: str - 设备ID
            status: str - 设备状态 (idle/busy)
        """
        return self._post("/api/v1/external/device/status", {})

    # ==================== 任务管理 ====================

    def create_task(
        self, submit_content: str, site: str = "US", platform: str = "amazon"
    ) -> str:
        """创建采集任务

        支持的输入格式：
        1. Amazon URL (产品页): https://www.amazon.com/dp/B09V3KXJPB
        2. Amazon URL (评论页): https://www.amazon.com/product-reviews/B08P752RXQ
        3. 纯 ASIN: B09V3KXJPB

        参数:
            submit_content: 提交内容，支持 URL 或 ASIN
            site: 站点 (US/CA/DE/FR/UK/JP/IT/ES)
            platform: 平台 (默认 amazon)

        返回:
            task_id: 任务ID
        """
        data = {"platform": platform, "site": site, "submit_content": submit_content}
        result = self._post("/api/v1/external/task/create", data)
        return result["task_id"]

    def get_task_detail(self, task_id: str) -> Dict[str, Any]:
        """查询任务详情

        参数:
            task_id: 任务ID

        返回:
            任务详情对象，包含 status, create_time 等字段
        """
        return self._post("/api/v1/external/task/detail", {"task_id": task_id})

    def get_task_list(
        self,
        page: int = 1,
        page_size: int = 20,
        search_keyword: str = "",
        filter_monitoring: bool = False,
    ) -> Dict[str, Any]:
        """获取任务列表

        参数:
            page: 页码
            page_size: 每页数量
            search_keyword: 搜索关键词
            filter_monitoring: 是否过滤监控任务
        """
        return self._post(
            "/api/v1/external/task/list",
            {
                "page": page,
                "page_size": page_size,
                "search_keyword": search_keyword,
                "filter_monitoring": filter_monitoring,
            },
        )

    def create_incremental(self, task_id: str) -> Dict[str, Any]:
        """为终态任务创建增量采集

        增量采集只获取自上次采集后的新增评论，适用于：
        - 已完成的任务需要更新最新评论
        - 获取自上次采集后的新增差评

        参数:
            task_id: 任务ID（必须是终态任务：SUCCESS/FAILED/CANCELLED）

        返回:
            task_id: 任务ID
            job_id: Job ID
        """
        return self._post("/api/v1/external/task/incremental", {"task_id": task_id})

    # ==================== 分析结果 ====================

    def get_ai_insights(self, task_id: str) -> Dict[str, Any]:
        """获取 AI 洞察

        参数:
            task_id: 任务ID

        返回:
            executive_summary: 执行摘要
            key_problems: 关键问题
            improvement_recommendations: 改进建议
            priority_ranking: 优先级排名
        """
        return self._post("/api/v1/external/analysis/insights", {"task_id": task_id})

    def get_tag_categories(self, task_id: str) -> Dict[str, Any]:
        """获取标签分布

        参数:
            task_id: 任务ID

        返回:
            tag_categories: 标签分类列表
        """
        return self._post("/api/v1/external/analysis/tags", {"task_id": task_id})

    def get_issue_statistics(self, task_id: str) -> Dict[str, Any]:
        """获取问题维度统计

        参数:
            task_id: 任务ID

        返回:
            product_count, product_rate: 产品维度统计
            service_count, service_rate: 服务维度统计
            experience_count, experience_rate: 体验维度统计
        """
        return self._post(
            "/api/v1/external/analysis/issue-statistics", {"task_id": task_id}
        )

    def get_top_issues(self, task_id: str) -> Dict[str, Any]:
        """获取要点问题分布

        参数:
            task_id: 任务ID

        返回:
            top_issue_distribution: 各维度 TopN 问题
        """
        return self._post("/api/v1/external/analysis/top-issues", {"task_id": task_id})

    def get_basic_statistics(self, task_id: str) -> Dict[str, Any]:
        """获取基础统计

        参数:
            task_id: 任务ID

        返回:
            total_comments: 总评论数
            negative_comments: 差评数
            negative_rate: 差评率
            等统计信息
        """
        return self._post("/api/v1/external/analysis/statistics", {"task_id": task_id})

    def get_negative_reviews(
        self, task_id: str, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """获取差评列表

        参数:
            task_id: 任务ID
            page: 页码
            page_size: 每页数量

        返回:
            items: 差评列表
            total: 总数
        """
        return self._post(
            "/api/v1/external/analysis/negative-reviews",
            {"task_id": task_id, "page": page, "page_size": page_size},
        )

    def get_trend(
        self, task_id: str, filter_data: str = "30", filter_product: str = "all"
    ) -> Dict[str, Any]:
        """获取评论趋势

        参数:
            task_id: 任务ID
            filter_data: 数据范围 (30/60/all)
            filter_product: 商品筛选
        """
        return self._post(
            "/api/v1/external/analysis/trend",
            {
                "task_id": task_id,
                "filter_data": filter_data,
                "filter_product": filter_product,
            },
        )

    def get_comments(
        self,
        task_id: str,
        page: int = 1,
        page_size: int = 20,
        filter_star: str = "all",
        filter_verified: str = "all",
    ) -> Dict[str, Any]:
        """获取原始评论

        参数:
            task_id: 任务ID
            page: 页码
            page_size: 每页数量
            filter_star: 评分筛选 (1-5/all)
            filter_verified: 筛选已认证评论
        """
        return self._post(
            "/api/v1/external/analysis/comments",
            {
                "task_id": task_id,
                "page": page,
                "page_size": page_size,
                "filter_star": filter_star,
                "filter_verified": filter_verified,
            },
        )

    def get_comments_overview(self, task_id: str) -> Dict[str, Any]:
        """获取评论概览

        参数:
            task_id: 任务ID

        返回:
            total_reviews: 总评论数
            avg_rating: 平均评分
            verified_count: 认证评论数
            image_count: 带图评论数
            video_count: 带视频评论数
        """
        return self._post(
            "/api/v1/external/analysis/comments-overview", {"task_id": task_id}
        )

    # ==================== 账户管理 ====================

    def get_points(self) -> int:
        """获取积分余额

        返回:
            available_points: 可用积分
        """
        result = self._post("/api/v1/external/account/points", {})
        return result.get("available_points", 0)


# ==================== 便捷函数 ====================


def check_device_online(
    api_key: str = _DEFAULT_API_KEY, base_url: str = _DEFAULT_BASE_URL
) -> Dict[str, Any]:
    """便捷函数：检查设备是否在线"""
    client = CustomerInsightsClient(api_key, base_url)
    return client.check_device_online()


def create_task(
    submit_content: str,
    site: str = "US",
    platform: str = "amazon",
    api_key: str = _DEFAULT_API_KEY,
    base_url: str = _DEFAULT_BASE_URL,
) -> str:
    """便捷函数：创建采集任务"""
    client = CustomerInsightsClient(api_key, base_url)
    return client.create_task(submit_content, site, platform)


def get_ai_insights(
    task_id: str, api_key: str = _DEFAULT_API_KEY, base_url: str = _DEFAULT_BASE_URL
) -> Dict[str, Any]:
    """便捷函数：获取 AI 洞察"""
    client = CustomerInsightsClient(api_key, base_url)
    return client.get_ai_insights(task_id)


def get_points(
    api_key: str = _DEFAULT_API_KEY, base_url: str = _DEFAULT_BASE_URL
) -> int:
    """便捷函数：获取积分余额"""
    client = CustomerInsightsClient(api_key, base_url)
    return client.get_points()


def get_task_list(
    page: int = 1,
    page_size: int = 20,
    api_key: str = _DEFAULT_API_KEY,
    base_url: str = _DEFAULT_BASE_URL,
) -> Dict[str, Any]:
    """便捷函数：获取任务列表"""
    client = CustomerInsightsClient(api_key, base_url)
    return client.get_task_list(page, page_size)


def get_task_detail(
    task_id: str, api_key: str = _DEFAULT_API_KEY, base_url: str = _DEFAULT_BASE_URL
) -> Dict[str, Any]:
    """便捷函数：获取任务详情"""
    client = CustomerInsightsClient(api_key, base_url)
    return client.get_task_detail(task_id)


def create_incremental(
    task_id: str, api_key: str = _DEFAULT_API_KEY, base_url: str = _DEFAULT_BASE_URL
) -> Dict[str, Any]:
    """便捷函数：为终态任务创建增量采集"""
    client = CustomerInsightsClient(api_key, base_url)
    return client.create_incremental(task_id)
