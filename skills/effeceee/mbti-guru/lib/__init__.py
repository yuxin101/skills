#!/usr/bin/env python3
"""
MBTI Guru - OpenClaw Skill Interface
提供与OpenClaw集成的接口
"""

from lib.telegram_handler import (
    handle_message,
    handle_callback,
    handle_start,
    handle_resume,
    handle_history,
    handle_status,
    handle_cancel,
    get_version_selection_message,
    get_version_selection_inline,
    get_progress_bar,
    get_history_message,
    VERSIONS
)

__all__ = [
    'handle_message',
    'handle_callback', 
    'handle_start',
    'handle_resume',
    'handle_history',
    'handle_status',
    'handle_cancel',
    'get_version_selection_message',
    'get_version_selection_inline',
    'get_progress_bar',
    'get_history_message',
    'VERSIONS'
]
