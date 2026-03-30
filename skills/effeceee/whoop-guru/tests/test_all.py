"""
WHOOP Guru 完整测试套件
运行: python3 -m pytest tests/ -v
或: python3 tests/test_all.py
"""

import sys
import os
import unittest
from datetime import datetime

# Setup path
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SKILL_DIR)
sys.path.insert(0, os.path.join(SKILL_DIR, 'lib'))


class TestDataCleaner(unittest.TestCase):
    """测试数据清理模块"""
    
    def test_get_today_data(self):
        from lib.data_cleaner import get_today_data
        data = get_today_data()
        self.assertIsInstance(data, dict)
        self.assertIn('recovery', data)
        self.assertIn('hrv', data)
        self.assertIn('rhr', data)
        self.assertIn('sleep_hours', data)
        print(f"✓ get_today_data: recovery={data.get('recovery')}")
    
    def test_get_whoop_data(self):
        from lib.data_cleaner import get_whoop_data
        data = get_whoop_data(7)
        self.assertIsInstance(data, dict)
        self.assertIn('avg_recovery', data)
        self.assertIn('training_days', data)
        self.assertIn('sleep_debt', data)
        print(f"✓ get_whoop_data: training_days={data.get('training_days')}")


class TestHealthScore(unittest.TestCase):
    """测试健康评分模块"""
    
    def test_calculate_health_score(self):
        from lib.health_score import calculate_health_score
        result = calculate_health_score()
        self.assertIsInstance(result, dict)
        self.assertIn('score', result)
        self.assertIn('grade', result)
        self.assertIn('breakdown', result)
        score = result['score']
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        print(f"✓ Health score: {score}/100 ({result['grade']})")


class TestMLPredictor(unittest.TestCase):
    """测试ML预测模块"""
    
    def test_predict_next_day(self):
        from lib.ml_predictor import predict_next_day
        result = predict_next_day()
        self.assertIsInstance(result, dict)
        self.assertIn('prediction', result)
        self.assertIn('confidence', result)
        pred = result['prediction']
        self.assertGreaterEqual(pred, 0)
        self.assertLessEqual(pred, 100)
        print(f"✓ ML prediction: {pred}% (confidence: {result['confidence']})")


class TestComprehensiveAnalysis(unittest.TestCase):
    """测试综合分析模块"""
    
    def test_generate_comprehensive(self):
        from lib.comprehensive_analysis import generate_comprehensive
        result = generate_comprehensive()
        self.assertIsInstance(result, dict)
        self.assertIn('heart_zones', result)
        self.assertIn('sleep_stages', result)
        self.assertIn('body_battery', result)
        self.assertIn('hrv_trend', result)
        print(f"✓ Comprehensive analysis keys: {list(result.keys())}")


class TestHealthAdvisor(unittest.TestCase):
    """测试健康顾问模块"""
    
    def test_generate_health_report(self):
        from lib.health_advisor import generate_health_report
        result = generate_health_report()
        self.assertIsInstance(result, dict)
        self.assertIn('overall_score', result)
        self.assertIn('state', result)
        self.assertIn('training_recommendation', result)
        print(f"✓ Health advisor: state={result['state']}")


class TestDynamicPlanner(unittest.TestCase):
    """测试动态规划模块"""
    
    def setUp(self):
        from lib.dynamic_planner import DynamicPlanner
        self.planner = DynamicPlanner()
    
    def test_get_current_status(self):
        status = self.planner.get_current_status()
        self.assertIsInstance(status, dict)
        self.assertIn('recovery', status)
        self.assertIn('hrv', status)
        print(f"✓ Dynamic planner status: recovery={status['recovery']}")
    
    def test_get_recommended_intensity(self):
        rec = self.planner.get_recommended_intensity()
        self.assertIsInstance(rec, dict)
        self.assertIn('intensity', rec)
        self.assertIn('description', rec)
        print(f"✓ Recommended intensity: {rec['intensity']} - {rec['description']}")


class TestGoals(unittest.TestCase):
    """测试目标管理模块"""
    
    def setUp(self):
        from lib.goals import GoalsManager
        self.manager = GoalsManager("test_user_" + str(datetime.now().timestamp()))
    
    def test_get_active_goals(self):
        goals = self.manager.get_active_goals()
        self.assertIsInstance(goals, list)
        print(f"✓ Active goals: {len(goals)}")
    
    def test_create_and_delete_goal(self):
        # Create
        goal = self.manager.create_goal("增肌", 80, 60, "kg", "2026-06-01")
        self.assertIsNotNone(goal)
        goals = self.manager.get_active_goals()
        self.assertEqual(len(goals), 1)
        # Delete
        self.manager.delete_goal(goal.goal_id)
        goals = self.manager.get_active_goals()
        self.assertEqual(len(goals), 0)
        print(f"✓ Create/delete goal: OK")
    
    def test_mark_completed(self):
        goal = self.manager.create_goal("减脂", 15, 20, "%", "2026-07-01")
        self.manager.mark_completed(goal.goal_id)
        completed = self.manager.get_completed_goals()
        self.assertEqual(len(completed), 1)
        print(f"✓ Mark completed: {completed[0].goal_type}")


class TestTracker(unittest.TestCase):
    """测试进度追踪模块"""
    
    def setUp(self):
        from lib.tracker import ProgressTracker
        self.tracker = ProgressTracker()
        self.user_id = "test_user_" + str(datetime.now().timestamp())
    
    def test_add_and_get_checkin(self):
        self.tracker.add_checkin(self.user_id, "卧推", "完成", "良好")
        checkins = self.tracker.get_checkins(self.user_id)
        self.assertIsInstance(checkins, list)
        self.assertGreaterEqual(len(checkins), 1)
        print(f"✓ Checkins: {len(checkins)}")
    
    def test_get_streak(self):
        streak = self.tracker.get_streak(self.user_id)
        self.assertIsInstance(streak, int)
        self.assertGreaterEqual(streak, 0)
        print(f"✓ Streak: {streak} days")
    
    def test_weekly_summary(self):
        summary = self.tracker.get_weekly_summary(self.user_id)
        self.assertIsInstance(summary, dict)
        self.assertIn('total_checkins', summary)
        print(f"✓ Weekly summary: {summary}")


class TestLLM(unittest.TestCase):
    """测试LLM模块"""
    
    def test_llm_client_init(self):
        from lib.llm import LLMClient
        client = LLMClient("test_user")
        self.assertIsNotNone(client)
        info = client.get_info()
        self.assertIn('provider', info)
        self.assertIn('model', info)
        print(f"✓ LLM Client: provider={info['provider']}, model={info['model']}")


class TestPlanGenerator(unittest.TestCase):
    """测试计划生成模块"""
    
    def test_plan_generator_init(self):
        from lib.plan_generator import TrainingPlanGenerator
        pg = TrainingPlanGenerator()
        self.assertIsNotNone(pg)
        print(f"✓ TrainingPlanGenerator initialized")


class TestEnhancedReports(unittest.TestCase):
    """测试增强报告模块"""
    
    def test_morning_report(self):
        from lib.enhanced_reports import EnhancedReports
        report = EnhancedReports.morning_report()
        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 100)
        print(f"✓ Morning report length: {len(report)}")
    
    def test_evening_report(self):
        from lib.enhanced_reports import EnhancedReports
        report = EnhancedReports.evening_report()
        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 100)
        print(f"✓ Evening report length: {len(report)}")
    
    def test_full_report(self):
        from lib.enhanced_reports import EnhancedReports
        report = EnhancedReports.full_report()
        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 100)
        print(f"✓ Full report length: {len(report)}")


class TestPusher(unittest.TestCase):
    """测试推送模块"""
    
    def test_morning_push(self):
        from lib.pusher import CoachPushMessage
        msg = CoachPushMessage.morning()
        self.assertIsInstance(msg, str)
        self.assertIn('早安', msg)
        self.assertIn('教练', msg)
        self.assertIn('训练', msg)
        print(f"✓ Morning push length: {len(msg)}")
    
    def test_evening_push(self):
        from lib.pusher import CoachPushMessage
        msg = CoachPushMessage.evening()
        self.assertIsInstance(msg, str)
        self.assertIn('晚间', msg)
        self.assertIn('教练', msg)
        print(f"✓ Evening push length: {len(msg)}")
    
    def test_checkin_reminder(self):
        from lib.pusher import CoachPushMessage
        msg = CoachPushMessage.checkin_reminder()
        self.assertIsInstance(msg, str)
        self.assertIn('打卡', msg)
        print(f"✓ Checkin reminder length: {len(msg)}")
    
    def test_scheduler(self):
        from lib.pusher import CoachScheduler
        times = CoachScheduler.PUSH_TIMES
        self.assertIn('morning', times)
        self.assertIn('evening', times)
        self.assertIn('checkin', times)
        print(f"✓ Scheduler times: {list(times.keys())}")


class TestCLI(unittest.TestCase):
    """测试CLI模块"""
    
    def test_cli_import(self):
        from lib import cli
        self.assertIsNotNone(cli)
        print(f"✓ CLI module imported")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("WHOOP GURU - 完整测试套件")
    print("=" * 60)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestDataCleaner,
        TestHealthScore,
        TestMLPredictor,
        TestComprehensiveAnalysis,
        TestHealthAdvisor,
        TestDynamicPlanner,
        TestGoals,
        TestTracker,
        TestLLM,
        TestPlanGenerator,
        TestEnhancedReports,
        TestPusher,
        TestCLI,
    ]
    
    for tc in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(tc))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print()
    print("=" * 60)
    print("测试结果摘要")
    print("=" * 60)
    print(f"测试数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ 所有测试通过!")
        return 0
    else:
        print("\n❌ 有测试失败")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
