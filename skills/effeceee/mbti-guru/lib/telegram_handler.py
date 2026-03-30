#!/usr/bin/env python3
"""
MBTI Guru - Telegram Bot Handler
支持进度保存、恢复、历史记录、实时反馈、进度条
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import Optional, Dict, List, Tuple

# 添加 lib 到路径
sys.path.insert(0, os.path.dirname(__file__))

from lib.session import save_session, load_session, get_incomplete_session, delete_session, list_user_sessions
from lib.history import save_test_result, get_test_history, get_test_detail
from lib.question_pool import sample_questions
from lib.scorer import calculate_type, calculate_clarity
from lib.pdf_combined import create_pdf_report

# ==================== 常量 ====================
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
VERSIONS = {
    "1": {"name": "快速版", "questions": 70, "minutes": 10},
    "2": {"name": "标准版", "questions": 93, "minutes": 15},
    "3": {"name": "扩展版", "questions": 144, "minutes": 25},
    "4": {"name": "专业版", "questions": 200, "minutes": 35},
}

# ==================== 用户状态 ====================
class UserState:
    """用户测试状态"""
    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.state = "idle"  # idle, selecting_version, testing, completed
        self.version: Optional[int] = None
        self.questions: List[Dict] = []
        self.current_index: int = 0
        self.answers: List[Tuple[str, str]] = []
        self.session_id: Optional[str] = None
        self.start_time: Optional[float] = None
    
    def to_dict(self) -> Dict:
        return {
            "chat_id": self.chat_id,
            "state": self.state,
            "version": self.version,
            "current_index": self.current_index,
            "answers_count": len(self.answers),
            "session_id": self.session_id
        }

# 内存中的用户状态 (实际应该用Redis等持久化)
_user_states: Dict[int, UserState] = {}

def get_user_state(chat_id: int) -> UserState:
    """获取或创建用户状态"""
    if chat_id not in _user_states:
        _user_states[chat_id] = UserState(chat_id)
    return _user_states[chat_id]

def clear_user_state(chat_id: int):
    """清除用户状态"""
    if chat_id in _user_states:
        del _user_states[chat_id]

# ==================== 进度保存 ====================
def save_progress(chat_id: int, state: UserState) -> str:
    """保存测试进度"""
    if state.version and state.questions:
        return save_session(
            chat_id=chat_id,
            version=state.version,
            current_index=state.current_index,
            answers=state.answers,
            questions_total=len(state.questions)
        )
    return ""

def save_result(chat_id: int, type_code: str, scores: Dict, clarity: Dict, version: int, answers_count: int):
    """保存测试结果到历史"""
    save_test_result(chat_id, type_code, scores, clarity, version, answers_count)

# ==================== 消息生成 ====================
def get_version_selection_message() -> str:
    """版本选择消息"""
    msg = "📊 **MBTI 人格测试**\n\n"
    msg += "请选择测试版本：\n\n"
    for key, info in VERSIONS.items():
        msg += f"`{key}`. {info['name']} ({info['questions']}题) ~{info['minutes']}分钟\n"
    msg += "\n发送数字 `1-4` 选择版本"
    return msg

def get_version_selection_inline() -> List[List[dict]]:
    """版本选择内联按钮"""
    buttons = []
    for key, info in VERSIONS.items():
        buttons.append({
            "text": f"{info['name']} ({info['questions']}题)",
            "callback_data": f"version_{key}"
        })
    # 2x2布局
    return [buttons[:2], buttons[2:4]] if len(buttons) > 2 else [buttons]

def get_resume_inline(has_session: bool) -> List[List[dict]]:
    """恢复测试内联按钮"""
    if has_session:
        return [[{"text": "▶️ 继续上次测试", "callback_data": "resume"}]]
    return []

def get_progress_bar(current: int, total: int, width: int = 10) -> str:
    """生成进度条"""
    filled = int(current * width / total)
    empty = width - filled
    pct = int(current * 100 / total)
    return f"[{'█' * filled}{'░' * empty}] {pct}% ({current}/{total})"

def get_question_message(state: UserState) -> Tuple[str, str]:
    """获取当前题目消息"""
    q = state.questions[state.current_index]
    q_num = state.current_index + 1
    total = len(state.questions)
    
    # 进度条
    progress = get_progress_bar(q_num, total)
    
    header = f"📝 **问题 {q_num}/{total}**\n{progress}\n\n"
    
    # 选项
    option_a = q.get("option_a", "")
    option_b = q.get("option_b", "")
    
    body = f"{q.get('question_cn', '')}\n\n"
    body += f"🅰️ {option_a}\n\n"
    body += f"🅱️ {option_b}"
    
    return header + body, f"q_{state.current_index}"

def get_completion_message(type_code: str, scores: Dict, clarity: Dict) -> str:
    """完成消息"""
    type_names = {
        "ISTJ": "物流师", "ISFJ": "守卫者", "INFJ": "提倡者", "INTJ": "建筑师",
        "ISTP": "鉴赏家", "ISFP": "探险家", "INFP": "调停者", "INTP": "逻辑学家",
        "ESTP": "企业家", "ESFP": "表演者", "ENFP": "竞选者", "ENTP": "辩论家",
        "ESTJ": "经理", "ESFJ": "执政官", "ENFJ": "主人公", "ENTJ": "指挥官",
    }
    
    name_en = type_names.get(type_code, type_code)
    
    msg = f"🎉 **测试完成！**\n\n"
    msg += f"你的MBTI类型：**{type_code}** ({name_en})\n\n"
    msg += "**维度得分：**\n"
    
    dim_names = {"EI": "能量倾向", "SN": "信息获取", "TF": "决策方式", "JP": "生活态度"}
    for dim, (score, pref) in clarity.items():
        dim_name = dim_names.get(dim, dim)
        bar = "▓" * int(score // 10) + "░" * (10 - int(score // 10))
        msg += f"{dim} {dim_name}: {bar} {score}%\n"
    
    msg += "\n正在生成PDF报告..."
    return msg

def get_history_message(history: List[Dict]) -> str:
    """历史记录消息"""
    if not history:
        return "📭 暂无测试历史\n\n开始新测试：/start"
    
    msg = "📜 **测试历史**\n\n"
    for i, test in enumerate(history[:5], 1):
        date = test.get("date", "")[:10]
        mtype = test.get("type_code", "")
        version = test.get("version", "")
        clarity_val = test.get("clarity", {})
        
        # 计算综合清晰度
        if clarity_val:
            vals = [v.get("value", 0) for v in clarity_val.values() if isinstance(v, dict)]
            avg = sum(vals) / len(vals) if vals else 0
            clarity_str = f"{avg:.0f}%"
        else:
            clarity_str = "N/A"
        
        msg += f"`{i}`. **{mtype}** | 清晰度: {clarity_str} | {date} | v{version}题\n"
    
    if len(history) > 5:
        msg += f"\n_显示最近5条，共{len(history)}条历史_"
    
    return msg

def get_feedback_message(type_code: str, dim: str, score: int, total: int) -> str:
    """实时反馈消息"""
    msg = f"📊 **维度分析：** `{dim}`\n"
    msg += f"进度：{score}/{total}题 ({int(score*100/total)}%)\n"
    
    if score >= total * 0.5:
        trend = "你倾向于"
        if dim == "EI":
            trend += "外向" if score > total * 0.5 else "内向"
        elif dim == "SN":
            trend += "直觉" if score > total * 0.5 else "感觉"
        elif dim == "TF":
            trend += "思考" if score > total * 0.5 else "情感"
        elif dim == "JP":
            trend += "判断" if score > total * 0.5 else "知觉"
        msg += f"\n🔮 {trend}"
    
    return msg

# ==================== 命令处理 ====================
def handle_start(chat_id: int) -> Dict:
    """处理 /start 命令"""
    state = get_user_state(chat_id)
    
    # 检查是否有未完成的测试
    incomplete = get_incomplete_session(chat_id)
    buttons = []
    
    if incomplete:
        buttons = get_resume_inline(True)
    
    return {
        "action": "send",
        "message": get_version_selection_message(),
        "buttons": buttons,
        "state": "selecting_version"
    }

def handle_version_select(chat_id: int, version_key: str) -> Dict:
    """处理版本选择"""
    if version_key not in VERSIONS:
        return {"action": "send", "message": "请发送数字 1-4 选择版本"}
    
    version_info = VERSIONS[version_key]
    version_num = version_info["questions"]
    
    state = get_user_state(chat_id)
    state.state = "testing"
    state.version = version_num
    state.questions = sample_questions(version_num)
    state.current_index = 0
    state.answers = []
    state.start_time = time.time()
    
    question_msg, ref = get_question_message(state)
    
    return {
        "action": "send",
        "message": question_msg,
        "ref": ref,
        "state": "testing"
    }

def handle_answer(chat_id: int, answer: str) -> Dict:
    """处理用户回答"""
    state = get_user_state(chat_id)
    
    if state.state != "testing":
        return {"action": "send", "message": "请先开始测试：/start"}
    
    if answer.upper() not in ["A", "B"]:
        return {"action": "send", "message": "请回复 A 或 B"}
    
    # 保存答案
    q = state.questions[state.current_index]
    state.answers.append((q["id"], answer.upper()))
    
    # 下一题
    state.current_index += 1
    
    # 每10题保存一次进度（在递增后）
    if (state.current_index) % 10 == 0:
        session_id = save_progress(chat_id, state)
        state.session_id = session_id
    
    # 检查是否完成
    if state.current_index >= len(state.questions):
        # 计算结果
        type_code, scores = calculate_type(state.answers)
        clarity = {dim: calculate_clarity(score) for dim, score in scores.items()}
        
        # 保存结果到历史
        save_result(chat_id, type_code, scores, clarity, state.version, len(state.answers))
        
        # 生成PDF
        filename = f"MBTI-{type_code}-{datetime.now().strftime('%Y-%m-%d')}.pdf"
        pdf_path = create_pdf_report(type_code, scores, clarity, filename)
        
        # 清理状态
        if state.session_id:
            delete_session(state.session_id)
        clear_user_state(chat_id)
        
        return {
            "action": "complete",
            "message": get_completion_message(type_code, scores, clarity),
            "pdf": pdf_path,
            "type_code": type_code
        }
    
    # 返回下一题
    question_msg, ref = get_question_message(state)
    
    # 每20题发送一次维度反馈
    feedback = None
    if (state.current_index) % 20 == 0 and state.current_index < len(state.questions):
        # 计算当前类型（临时）
        temp_type, _ = calculate_type(state.answers)
        
        # 计算当前维度
        current_dim_idx = (state.current_index // (len(state.questions) // 4))
        dim_keys = ["EI", "SN", "TF", "JP"]
        dim = dim_keys[min(current_dim_idx, 3)]
        
        # 统计该维度已回答的选项
        dim_questions = state.questions[:state.current_index]
        dim_answers = state.answers[:state.current_index]
        
        # 简单计算当前维度的得分
        dim_score = len([a for a in dim_answers if a[1] == 'A'])
        feedback = get_feedback_message(temp_type, dim, dim_score, state.current_index)
    
    return {
        "action": "send",
        "message": question_msg,
        "ref": ref,
        "feedback": feedback,
        "state": "testing"
    }

def handle_resume(chat_id: int) -> Dict:
    """处理恢复测试"""
    incomplete = get_incomplete_session(chat_id)
    
    if not incomplete:
        return handle_start(chat_id)
    
    state = get_user_state(chat_id)
    state.state = "testing"
    state.version = incomplete["version"]
    state.questions = sample_questions(incomplete["questions_total"])
    state.current_index = incomplete["current_index"]
    state.answers = incomplete["answers"]
    state.start_time = time.time()
    state.session_id = incomplete["session_id"]
    
    question_msg, ref = get_question_message(state)
    
    return {
        "action": "send",
        "message": f"✅ 已恢复上次进度\n\n{question_msg}",
        "ref": ref,
        "state": "testing"
    }

def handle_history(chat_id: int) -> Dict:
    """处理历史记录"""
    history = get_test_history(chat_id)
    return {
        "action": "send",
        "message": get_history_message(history)
    }

def handle_status(chat_id: int) -> Dict:
    """处理状态查询"""
    state = get_user_state(chat_id)
    incomplete = get_incomplete_session(chat_id)
    
    if state.state == "testing" and state.questions:
        progress = get_progress_bar(state.current_index, len(state.questions))
        msg = f"📍 **测试进行中**\n\n"
        msg += f"版本：{state.version}题\n"
        msg += f"进度：{progress}\n"
        msg += f"已答：{len(state.answers)}题"
        return {"action": "send", "message": msg}
    
    if incomplete:
        progress = get_progress_bar(incomplete["current_index"], incomplete["questions_total"])
        msg = f"📍 **有未完成的测试**\n\n"
        msg += f"版本：{incomplete['version']}题\n"
        msg += f"进度：{progress}\n"
        msg += f"发送 /resume 继续"
        return {"action": "send", "message": msg}
    
    msg = "📍 **当前状态：** 空闲\n\n发送 /start 开始新测试"
    return {"action": "send", "message": msg}

def handle_cancel(chat_id: int) -> Dict:
    """处理取消测试"""
    state = get_user_state(chat_id)
    
    if state.session_id:
        delete_session(state.session_id)
    
    clear_user_state(chat_id)
    
    return {
        "action": "send",
        "message": "❌ 测试已取消\n\n发送 /start 开始新测试"
    }

# ==================== 消息路由 ====================
def handle_message(chat_id: int, text: str) -> Dict:
    """处理收到的消息"""
    text = text.strip()
    
    # 命令
    if text == "/start":
        return handle_start(chat_id)
    elif text == "/help":
        msg = "📖 **MBTI Guru 使用指南**\n\n"
        msg += "`/start` - 开始新测试\n"
        msg += "`/resume` - 继续未完成的测试\n"
        msg += "`/history` - 查看测试历史\n"
        msg += "`/status` - 查看当前状态\n"
        msg += "`/cancel` - 取消当前测试\n"
        msg += "\n直接回复 A 或 B 回答问题"
        return {"action": "send", "message": msg}
    elif text == "/resume":
        return handle_resume(chat_id)
    elif text == "/history":
        return handle_history(chat_id)
    elif text == "/status":
        return handle_status(chat_id)
    elif text == "/cancel":
        return handle_cancel(chat_id)
    
    # 版本选择
    if text in ["1", "2", "3", "4"]:
        return handle_version_select(chat_id, text)
    
    # 答题
    state = get_user_state(chat_id)
    if state.state == "testing":
        if text.upper() in ["A", "B"]:
            return handle_answer(chat_id, text.upper())
        elif text.upper() in ["Q", "问题", "题目"]:
            return {
                "action": "send",
                "message": get_question_message(state)[0]
            }
        elif text == "/progress":
            progress = get_progress_bar(state.current_index, len(state.questions))
            return {"action": "send", "message": f"📍 {progress}"}
    
    # 默认
    if state.state == "idle" or state.state == "completed":
        return handle_start(chat_id)
    
    return {"action": "send", "message": "请回复 A 或 B 回答问题"}

# ==================== 回调处理 ====================
def handle_callback(chat_id: int, data: str) -> Dict:
    """处理回调数据"""
    if data == "resume":
        return handle_resume(chat_id)
    elif data.startswith("version_"):
        version_key = data.split("_")[1]
        return handle_version_select(chat_id, version_key)
    elif data == "history":
        return handle_history(chat_id)
    
    return {"action": "send", "message": "未知操作"}
