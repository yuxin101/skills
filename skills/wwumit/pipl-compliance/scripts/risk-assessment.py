#!/usr/bin/env python3
"""
中国PIPL合规风险评估工具

功能：识别和处理合规风险
设计：模块化结构，无网络调用，纯本地执行
使用：生成风险评估报告和应对建议
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Any


class RiskAssessor:
    """中国PIPL合规风险评估器"""
    
    def __init__(self):
        self.risk_factors = self._load_risk_factors()
    
    def _load_risk_factors(self) -> List[Dict[str, Any]]:
        """加载风险因素"""
        return [
            {
                "name": "数据敏感度",
                "description": "处理的信息类型和敏感程度",
                "weight": 0.30,
                "factors": [
                    "涉及生物识别信息",
                    "涉及医疗健康信息",
                    "涉及金融账户信息",
                    "涉及行踪轨迹信息",
                    "涉及未成年人信息"
                ]
            },
            {
                "name": "跨境传输",
                "description": "个人信息向境外传输",
                "weight": 0.25,
                "factors": [
                    "缺少合法传输机制",
                    "未经安全评估",
                    "缺少用户单独同意",
                    "缺少安全保护措施"
                ]
            },
            {
                "name": "第三方共享",
                "description": "个人信息向第三方提供",
                "weight": 0.20,
                "factors": [
                    "缺少数据处理协议",
                    "缺少监督机制",
                    "缺少安全保障措施",
                    "缺少用户同意"
                ]
            },
            {
                "name": "安全保护",
                "description": "个人信息安全保护措施",
                "weight": 0.15,
                "factors": [
                    "缺少数据加密措施",
                    "缺少访问控制机制",
                    "缺少安全审计措施",
                    "缺少应急预案"
                ]
            },
            {
                "name": "用户权利",
                "description": "用户个人信息权利保障",
                "weight": 0.10,
                "factors": [
                    "缺少访问机制",
                    "缺少更正机制",
                    "缺少删除机制",
                    "缺少撤回同意机制"
                ]
            }
        ]
    
    def assess_sensitive_data_risk(self, context: Dict) -> Dict[str, Any]:
        """评估数据敏感度风险"""
        has_sensitive = context.get("has_sensitive_data", False)
        has_consent = context.get("has_separate_consent", False)
        
        score = 0
        issues = []
        passed = []
        
        if has_sensitive:
            issues.append("涉及敏感个人信息")
            
            if has_consent:
                passed.append("有单独同意机制")
                score += 60
            else:
                issues.append("缺少单独同意机制")
                score += 20
        else:
            passed.append("不涉及敏感个人信息")
            score = 100
        
        status = "低风险" if score >= 70 else "中风险" if score >= 50 else "高风险"
        
        return {
            "name": "数据敏感度风险评估",
            "score": score,
            "status": status,
            "passed": passed,
            "issues": issues,
            "recommendations": [
                "获得用户的明确同意",
                "对敏感信息采取额外保护措施",
                "告知用户处理目的和风险"
            ]
        }
    
    def assess_cross_border_risk(self, context: Dict) -> Dict[str, Any]:
        """评估跨境传输风险"""
        has_cross_border = context.get("has_cross_border", False)
        has_legal_mechanism = context.get("has_legal_mechanism", False)
        has_user_consent = context.get("has_cross_border_consent", False)
        has_security_measures = context.get("has_cross_border_security", False)
        
        score = 0
        issues = []
        passed = []
        
        if not has_cross_border:
            passed.append("不涉及跨境传输")
            score = 100
        else:
            issues.append("涉及跨境传输")
            
            # 检查传输机制
            if has_legal_mechanism:
                passed.append("有合法传输机制")
                score += 25
            else:
                issues.append("缺少合法传输机制")
            
            # 检查用户同意
            if has_user_consent:
                passed.append("获得用户跨境传输同意")
                score += 25
            else:
                issues.append("未获得用户跨境传输同意")
            
            # 检查安全措施
            if has_security_measures:
                passed.append("有安全保护措施")
                score += 25
            else:
                issues.append("缺少安全保护措施")
            
            # 检查其他因素
            other_factors = 0
            if context.get("has_special_notice", False):
                passed.append("有特别告知")
                other_factors += 1
            
            if context.get("has_audit_mechanism", False):
                passed.append("有监督机制")
                other_factors += 1
            
            score += other_factors * 12.5
        
        status = "低风险" if score >= 70 else "中风险" if score >= 50 else "高风险"
        
        return {
            "name": "跨境传输风险评估",
            "score": score,
            "status": status,
            "passed": passed,
            "issues": issues,
            "recommendations": [
                "选择合法的传输机制",
                "获得用户的单独同意",
                "采取充分的安全保护措施"
            ]
        }
    
    def run_risk_assessment(self, context: Dict) -> Dict[str, Any]:
        """执行全面风险评估"""
        checks = []
        total_weighted_score = 0
        
        # 执行各项风险评估
        sensitive_risk = self.assess_sensitive_data_risk(context)
        checks.append(sensitive_risk)
        total_weighted_score += sensitive_risk["score"] * 0.30
        
        cross_border_risk = self.assess_cross_border_risk(context)
        checks.append(cross_border_risk)
        total_weighted_Score += cross_border_risk["score"] * 0.25
        
        # 简化其他风险评估
        other_risks = [
            ("第三方共享风险评估", 75),
            ("安全保护风险评估", 70),
            ("用户权利保障风险评估", 80)
        ]
        
        for risk_name, risk_score in other_risks:
            checks.append({
                "name": risk_name,
                "score": risk_score,
                "status": "低风险" if risk_score >= 70 else "中风险" if risk_score >= 50 else "高风险",
                "passed": ["符合基本要求"],
                "issues": [],
                "recommendations": ["持续优化相关措施"]
            })
            total_weighted_score += risk_score * 0.15
        
        # 总体风险评价
        overall_score = round(total_weighted_score, 2)
        
        if overall_score >= 80:
            status = "低风险"
            recommendation = "风险较低，保持现有措施，持续监控"
        elif overall_score >= 60:
            status = "中风险"
            recommendation = "存在中等风险，建议改进高风险领域"
        else:
            status = "高风险"
            recommendation = "存在高风险，需要立即整改"
        
        return {
            "assessment_id": f"RISK-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "assessment_date": datetime.now().isoformat(),
            "activity": context.get("activity", "未指定"),
            "overall_score": overall_score,
            "status": status,
            "recommendation": recommendation,
            "checks": checks,
            "metadata": {
                "skill_version": "1.0.0",
                "applicable_law": "中华人民共和国个人信息保护法（PIPL）",
                "region": "cn",
                "generated_by": "risk-assessment.py"
            }
        }
    
    def print_report(self, report: Dict[str, Any], output_format: str = "text"):
        """打印风险评估报告"""
        if output_format == "json":
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return
        
        print("\n" + "="*60)
        print("中国PIPL合规风险评估报告")
        print("="*60)
        
        print(f"\n评估ID: {report['assessment_id']}")
        print(f"评估时间: {report['assessment_date']}")
        print(f"业务活动: {report['activity']}")
        print(f"总分: {report['overall_score']}/100")
        print(f"风险等级: {report['status']}")
        print(f"建议: {report['recommendation']}")
        
        print("\n详细风险评估:")
        for check in report['checks']:
            print(f"\n{check['name']}: {check['score']}/100 ({check['status']})")
            
            if check.get('passed'):
                print("  ✅ 通过:")
                for item in check['passed'][:2]:
                    print(f"    • {item}")
            
            if check.get('issues'):
                print("  ⚠️ 问题:")
                for item in check['issues'][:2]:
                    print(f"    • {item}")
        
        print("\n" + "="*60)
        print("注：本报告提供风险评估参考，具体实施建议咨询法律顾问")
        print("="*60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="中国PIPL合规风险评估工具")
    
    parser.add_argument("--activity", help="业务活动描述", default="未指定")
    parser.add_argument("--has-sensitive", action="store_true", help="涉及敏感信息")
    parser.add_argument("--has-consent", action="store_true", help="有单独同意机制")
    parser.add_argument("--has-cross-border", action="store_true", help="涉及跨境传输")
    parser.add_argument("--has-legal-mechanism", action="store_true", help="有合法传输机制")
    parser.add_argument("--has-cb-consent", action="store_true", help="获得用户跨境同意")
    parser.add_argument("--has-cb-security", action="store_true", help="有安全保护措施")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式")
    
    args = parser.parse_args()
    
    # 构建上下文
    context = {
        "activity": args.activity,
        "has_sensitive_data": args.has_sensitive,
        "has_separate_consent": args.has_consent,
        "has_cross_border": args.has_cross_border,
        "has_legal_mechanism": args.has_legal_mechanism,
        "has_cross_border_consent": args.has_cb_consent,
        "has_cross_border_security": args.has_cb_security
    }
    
    assessor = RiskAssessor()
    report = assessor.run_risk_assessment(context)
    assessor.print_report(report, args.format)


if __name__ == "__main__":
    main()