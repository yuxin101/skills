"""
LLM增强报告模块
生成真正由大模型驱动的个性化详细健康分析

使用方法:
from lib.enhanced_reports import EnhancedReports
report = EnhancedReports.morning_report()
"""

import os
import sys
from datetime import datetime
from typing import Dict, Optional

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SKILL_DIR)

# 延迟导入
def _get_data():
    from lib.data_cleaner import get_whoop_data, get_today_data
    return get_whoop_data(7), get_today_data()

def _get_llm():
    try:
        from lib.llm import LLMClient
        return LLMClient("enhanced_report")
    except:
        return None

def _get_health_score():
    try:
        from lib.health_score import calculate_health_score
        return calculate_health_score()
    except:
        return {"score": 0, "grade": "N/A", "breakdown": {}}

def _get_ml_prediction():
    try:
        from lib.ml_predictor import predict_next_day
        return predict_next_day()
    except:
        return {"prediction": 50, "confidence": "low"}

def _get_comprehensive():
    try:
        from lib.comprehensive_analysis import generate_comprehensive
        return generate_comprehensive()
    except:
        return {}

def _get_tracker():
    try:
        from lib.tracker import ProgressTracker
        return ProgressTracker()
    except:
        return None

def _get_goals(user_id: str = "dongyi"):
    try:
        from lib.goals import GoalsManager
        g = GoalsManager(user_id)
        return g.get_active_goals()
    except:
        return []


class EnhancedReports:
    """LLM增强的健康报告生成器"""
    
    @staticmethod
    def morning_report() -> str:
        """
        生成09:00早安增强版报告
        包含LLM生成的详细个性化分析
        """
        summary, today = _get_data()
        health_score = _get_health_score()
        ml_pred = _get_ml_prediction()
        comprehensive = _get_comprehensive()
        tracker = _get_tracker()
        goals = _get_goals()
        
        # 构建用户数据
        user_data = {
            "recovery": today.get('recovery', 0),
            "hrv": today.get('hrv', 0),
            "rhr": today.get('rhr', 0),
            "sleep_hours": today.get('sleep_hours', 0),
            "strain": today.get('strain', 0),
            "sleep_debt": summary.get('sleep_debt', 0),
            "training_days": summary.get('training_days', 0),
            "avg_recovery": summary.get('avg_recovery', 0),
            "avg_hrv": summary.get('avg_hrv', 0),
            "health_score": health_score.get('score', 0),
            "ml_prediction": ml_pred.get('prediction', 50),
        }
        
        # 尝试使用LLM生成详细分析
        llm_analysis = EnhancedReports._generate_llm_analysis(user_data, "morning")
        
        # 构建基本数据摘要
        recovery = user_data['recovery']
        hrv = user_data['hrv']
        rhr = user_data['rhr']
        sleep_hours = user_data['sleep_hours']
        ml_p = user_data['ml_prediction']
        hs_score = user_data['health_score']
        training_days = user_data['training_days']
        
        # 状态评估
        if recovery >= 80:
            mood, status_text = "🎉", "最佳状态"
            rec_emoji = "🟢"
        elif recovery >= 60:
            mood, status_text = "💪", "良好状态"
            rec_emoji = "🟡"
        elif recovery >= 40:
            mood, status_text = "🤔", "一般状态"
            rec_emoji = "🟠"
        else:
            mood, status_text = "🛋️", "恢复不足"
            rec_emoji = "🔴"
        
        # 健康评分
        if hs_score >= 70:
            hs_emoji, hs_text = "🟢", "良好"
        elif hs_score >= 50:
            hs_emoji, hs_text = "🟡", "一般"
        else:
            hs_emoji, hs_text = "🔴", "需改善"
        
        # ML预测
        if ml_p >= 70:
            ml_emoji, ml_text = "🟢", "状态不错"
        elif ml_p >= 50:
            ml_emoji, ml_text = "🟡", "状态一般"
        else:
            ml_emoji, ml_text = "🔴", "状态欠佳"
        
        # 打卡信息
        streak = tracker.get_streak("dongyi") if tracker else 0
        
        # 构建报告
        msg = "☀️ **【LLM增强版】今日个性化健康分析**\n\n"
        msg += "━" * 20 + "\n\n"
        
        # LLM生成的详细分析（如果可用）
        if llm_analysis:
            msg += "🤖 **AI教练详细分析**\n\n"
            msg += llm_analysis + "\n\n"
            msg += "━" * 20 + "\n\n"
        
        msg += "📊 **今日核心数据**\n\n"
        msg += f"• 恢复评分：{rec_emoji} {recovery:.0f}% ({status_text})\n"
        msg += f"• HRV：{hrv:.1f}ms\n"
        msg += f"• 静息心率：{rhr:.0f}bpm\n"
        msg += f"• 睡眠时长：{sleep_hours:.1f}小时\n"
        msg += f"• 健康评分：{hs_emoji} {hs_score:.0f}/100 ({hs_text})\n"
        msg += f"• ML预测明日：{ml_emoji} {ml_p:.0f}% ({ml_text})\n"
        msg += f"• 本周训练：{training_days}天\n"
        
        if streak > 0:
            msg += f"• 连续打卡：{streak}天 🔥\n"
        
        msg += "\n" + "━" * 20 + "\n\n"
        
        # 打卡提醒
        msg += "📝 **今日打卡提醒**\n\n"
        msg += "训练后来这里打卡，记录今天的训练内容和身体感受！\n"
        msg += "格式示例：`卧推100kg 4x12 | 胸部微酸`\n\n"
        
        msg += "━" * 20 + "\n\n"
        msg += "⏰ 下次推送：今天18:00 晚间追踪\n"
        
        return msg
    
    @staticmethod
    def evening_report() -> str:
        """
        生成18:00晚间增强版报告
        """
        summary, today = _get_data()
        health_score = _get_health_score()
        ml_pred = _get_ml_prediction()
        comprehensive = _get_comprehensive()
        tracker = _get_tracker()
        
        recovery = today.get('recovery', 0)
        strain = today.get('strain', 0)
        has_training = today.get('has_training', False)
        avg_recovery = summary.get('avg_recovery', 0)
        training_days = summary.get('training_days', 0)
        sleep_debt = summary.get('sleep_debt', 0)
        
        ml_p = ml_pred.get('prediction', 50)
        hs_score = health_score.get('score', 0)
        
        # 用户数据
        user_data = {
            "recovery": recovery,
            "hrv": today.get('hrv', 0),
            "strain": strain,
            "has_training": has_training,
            "sleep_debt": sleep_debt,
            "training_days": training_days,
            "avg_recovery": avg_recovery,
            "health_score": hs_score,
            "ml_prediction": ml_p,
        }
        
        # 尝试使用LLM
        llm_analysis = EnhancedReports._generate_llm_analysis(user_data, "evening")
        
        # 今日状态
        if has_training and strain > 0:
            if strain >= 12:
                train_status = "💪 高强度训练日"
                train_emoji = "🟢"
            elif strain >= 8:
                train_status = "🏃 中等强度训练"
                train_emoji = "🟡"
            else:
                train_status = "🚶 轻度活动"
                train_emoji = "🟠"
        else:
            train_status = "😴 今日休息"
            train_emoji = "🔴"
        
        # 恢复状态
        if recovery >= 70:
            rec_emoji, rec_text = "🟢", "恢复良好"
        elif recovery >= 50:
            rec_emoji, rec_text = "🟡", "恢复一般"
        else:
            rec_emoji, rec_text = "🔴", "恢复不足"
        
        # ML预测
        if ml_p >= 70:
            ml_emoji, ml_text = "🟢", "明天状态不错"
        elif ml_p >= 50:
            ml_emoji, ml_text = "🟡", "明天状态一般"
        else:
            ml_emoji, ml_text = "🔴", "明天可能疲劳"
        
        # 打卡统计
        streak = tracker.get_streak("dongyi") if tracker else 0
        weekly = tracker.get_weekly_summary("dongyi") if tracker else {}
        
        # 构建报告
        msg = "🌙 **【LLM增强版】今日晚间健康分析**\n\n"
        msg += "━" * 20 + "\n\n"
        
        if llm_analysis:
            msg += "🤖 **AI教练晚间总结**\n\n"
            msg += llm_analysis + "\n\n"
            msg += "━" * 20 + "\n\n"
        
        msg += "📋 **今日训练**\n\n"
        msg += f"{train_emoji} {train_status}\n"
        msg += f"• strain：{strain:.1f}\n\n"
        
        msg += "📊 **恢复状态**\n\n"
        msg += f"• 今日恢复：{rec_emoji} {recovery:.0f}% ({rec_text})\n"
        msg += f"• ML预测明日：{ml_emoji} {ml_p:.0f}% ({ml_text})\n"
        msg += f"• 健康评分：{hs_score:.0f}/100\n"
        msg += f"• 本周训练：{training_days}天\n"
        
        if weekly:
            msg += f"• 本周打卡：{weekly.get('total_checkins', 0)}次\n"
        
        if streak > 0:
            msg += f"• 连续打卡：{streak}天 🔥\n"
        
        msg += "\n" + "━" * 20 + "\n\n"
        
        msg += "📝 **明日训练预告**\n\n"
        if ml_p >= 70:
            msg += "✅ 明天状态不错，可以正常训练\n"
        elif ml_p >= 50:
            msg += "🟡 明天状态一般，建议中等强度\n"
        else:
            msg += "🔴 明天可能疲劳，建议休息\n"
        
        msg += "\n" + "━" * 20 + "\n\n"
        msg += "💬 **记得来20:00打卡！**\n\n"
        msg += "━━━━━━━━━━━━━━━━━━━━\n"
        
        return msg
    
    @staticmethod
    def full_report() -> str:
        """
        生成完整健康日报（22:00详细版）
        """
        summary, today = _get_data()
        health_score = _get_health_score()
        ml_pred = _get_ml_prediction()
        comprehensive = _get_comprehensive()
        tracker = _get_tracker()
        
        recovery = today.get('recovery', 0)
        hrv = today.get('hrv', 0)
        rhr = today.get('rhr', 0)
        sleep_hours = today.get('sleep_hours', 0)
        strain = today.get('strain', 0)
        sleep_debt = summary.get('sleep_debt', 0)
        training_days = summary.get('training_days', 0)
        avg_recovery = summary.get('avg_recovery', 0)
        avg_hrv = summary.get('avg_hrv', 0)
        
        ml_p = ml_pred.get('prediction', 50)
        hs_score = health_score.get('score', 0)
        hs_grade = health_score.get('grade', 'N/A')
        
        comp = comprehensive
        hz = comp.get('heart_zones', {})
        ss = comp.get('sleep_stages', {}).get('percentages', {})
        
        # 用户数据
        user_data = {
            "recovery": recovery,
            "hrv": hrv,
            "rhr": rhr,
            "sleep_hours": sleep_hours,
            "strain": strain,
            "sleep_debt": sleep_debt,
            "training_days": training_days,
            "avg_recovery": avg_recovery,
            "avg_hrv": avg_hrv,
            "health_score": hs_score,
            "ml_prediction": ml_p,
        }
        
        # 尝试使用LLM
        llm_analysis = EnhancedReports._generate_llm_analysis(user_data, "full")
        
        # 构建报告
        msg = "🌙 **【LLM增强版】今日完整健康日报**\n\n"
        msg += "━" * 20 + "\n\n"
        
        if llm_analysis:
            msg += "🤖 **AI教练综合分析报告**\n\n"
            msg += llm_analysis + "\n\n"
            msg += "━" * 20 + "\n\n"
        
        # 核心数据
        msg += "📊 **核心指标**\n\n"
        msg += f"• 恢复评分：{recovery:.0f}%\n"
        msg += f"• HRV：{hrv:.1f}ms\n"
        msg += f"• 静息心率：{rhr:.0f}bpm\n"
        msg += f"• 睡眠：{sleep_hours:.1f}小时\n"
        msg += f"• 今日strain：{strain:.1f}\n"
        msg += f"• 健康评分：{hs_score:.0f}/100 ({hs_grade})\n\n"
        
        msg += "📈 **7天趋势**\n\n"
        msg += f"• 平均恢复：{avg_recovery:.0f}%\n"
        msg += f"• 平均HRV：{avg_hrv:.1f}ms\n"
        msg += f"• 训练天数：{training_days}天\n"
        msg += f"• 睡眠债务：{sleep_debt:.1f}小时\n\n"
        
        msg += "💪 **心率区间**\n\n"
        msg += f"• Zone 0-1：{hz.get('zone0', 0) + hz.get('zone1', 0):.1f}%\n"
        msg += f"• Zone 2-3：{hz.get('aerobic', 0):.1f}%\n"
        msg += f"• Zone 4-5：{hz.get('anaerobic', 0):.1f}%\n\n"
        
        msg += "😴 **睡眠结构**\n\n"
        msg += f"• 浅睡眠：{ss.get('light', 0):.0f}%\n"
        msg += f"• 深睡眠：{ss.get('deep', 0):.0f}%\n"
        msg += f"• REM睡眠：{ss.get('rem', 0):.0f}%\n\n"
        
        msg += "🔮 **ML预测**\n\n"
        for i, p in enumerate(ml_pred.get('predictions', [50]*7)[:7], 1):
            emoji = "🟢" if p >= 70 else "🟡" if p >= 50 else "🔴"
            msg += f"• 第{i}天：{p:.0f}% {emoji}\n"
        
        msg += "\n" + "━" * 20 + "\n\n"
        msg += "_数据来源：WHOOP | 健康糕_\n"
        msg += f"_生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n"
        
        return msg
    
    @staticmethod
    def _generate_llm_analysis(user_data: Dict, analysis_type: str) -> str:
        """
        内部方法：调用LLM生成分析
        如果LLM未配置或调用失败，返回空字符串
        """
        try:
            from lib.llm import LLMClient
            
            client = LLMClient("enhanced_report")
            if not client.config.api_key:
                return ""
            
            prompt = EnhancedReports._build_llm_prompt(user_data, analysis_type)
            result = client.generate(prompt)
            
            if "error" in result:
                return ""
            
            return result.get("content", "")
        except:
            return ""
    
    @staticmethod
    def _build_llm_prompt(user_data: Dict, analysis_type: str) -> str:
        """构建LLM prompt"""
        
        r = user_data.get("recovery", 0)
        h = user_data.get("hrv", 0)
        hr = user_data.get("rhr", 0)
        s = user_data.get("sleep_hours", 0)
        st = user_data.get("strain", 0)
        debt = user_data.get("sleep_debt", 0)
        td = user_data.get("training_days", 0)
        ar = user_data.get("avg_recovery", 0)
        ah = user_data.get("avg_hrv", 0)
        hs = user_data.get("health_score", 0)
        ml = user_data.get("ml_prediction", 50)
        
        if analysis_type == "morning":
            return f"""你是专业且温暖的AI健身教练，根据以下用户数据生成详细的早安分析报告：

【用户今日数据】
- 恢复评分：{r:.0f}% 
- HRV：{h:.1f}ms
- 静息心率：{hr:.0f}bpm
- 睡眠时长：{s:.1f}小时
- 今日strain：{st:.1f}
- 睡眠债务：{debt:.1f}小时
- 本周训练天数：{td}天
- 平均恢复：{ar:.0f}%
- 平均HRV：{ah:.1f}ms
- 健康评分：{hs:.0f}/100
- ML预测明日恢复：{ml:.0f}%

请生成300-400字的中文分析，包括：
1. 对用户当前状态的详细解读
2. 哪些指标需要特别关注
3. 具体的、可执行的今日建议
4. 鼓励和关怀的话语

语气：专业、温暖、像私人教练一样。"""
        
        elif analysis_type == "evening":
            has_train = user_data.get("has_training", False)
            strain = user_data.get("strain", 0)
            
            return f"""你是专业且温暖的AI健身教练，根据以下数据生成晚间总结和明日建议：

【用户今日数据】
- 恢复评分：{r:.0f}%
- 今日训练：{"有" if has_train else "无"} (strain: {strain:.1f})
- 睡眠债务：{debt:.1f}小时
- 本周训练天数：{td}天
- ML预测明日恢复：{ml:.0f}%
- 健康评分：{hs:.0f}/100

请生成300-400字的中文总结，包括：
1. 对今日训练/休息的评价
2. 明日身体状态预测
3. 具体的明日训练建议
4. 关怀和鼓励

语气：专业、支持、激励。"""
        
        else:  # full
            return f"""你是专业且全面的AI健身教练，根据以下完整数据生成综合健康报告：

【核心指标】
- 恢复评分：{r:.0f}%
- HRV：{h:.1f}ms
- 静息心率：{hr:.0f}bpm
- 睡眠：{s:.1f}小时
- 健康评分：{hs:.0f}/100
- ML预测明日：{ml:.0f}%

【趋势数据】
- 本周训练：{td}天
- 平均恢复：{ar:.0f}%
- 平均HRV：{ah:.1f}ms
- 睡眠债务：{debt:.1f}小时

请生成500-600字的综合分析，包括：
1. 整体健康状态评估
2. 各指标详细解读
3. 发现的问题和风险
4. 具体改进建议
5. 接下来的行动计划

语气：专业、详细、有洞察力。"""


def get_morning_report() -> str:
    """便捷函数：获取早安报告"""
    return EnhancedReports.morning_report()

def get_evening_report() -> str:
    """便捷函数：获取晚间报告"""
    return EnhancedReports.evening_report()

def get_full_report() -> str:
    """便捷函数：获取完整日报"""
    return EnhancedReports.full_report()
