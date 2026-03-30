#!/usr/bin/env python3
"""
中国PIPL合规文档生成工具

功能：生成隐私政策、同意书、数据处理协议等合规文档
设计：本地模板生成，无网络调用
使用：根据输入参数生成相应文档
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, Any


class DocumentGenerator:
    """中国PIPL合规文档生成器"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Dict[str, Any]]:
        """加载文档模板"""
        return {
            "privacy-policy": {
                "name": "隐私政策模板",
                "description": "符合中国PIPL要求的隐私政策",
                "schema": {
                    "company_name": "string",
                    "effective_date": "datetime",
                    "contact_email": "string",
                    "version": "string"
                }
            },
            "consent-form": {
                "name": "用户同意书模板", 
                "description": "告知同意和单独同意书模板",
                "schema": {
                    "company_name": "string",
                    "user_name": "string",
                    "data_types": "list",
                    "purposes": "list"
                }
            },
            "data-processing-agreement": {
                "name": "数据处理协议模板",
                "description": "委托处理和共同处理协议模板",
                "schema": {
                    "party_a": "string",
                    "party_b": "string",
                    "processing_scope": "object",
                    "security_measures": "list",
                    "validity_period": "object"
                }
            }
        }
    
    def generate_privacy_policy(self, context: Dict) -> Dict[str, Any]:
        """生成隐私政策文档"""
        company_name = context.get("company_name", "[公司名称]")
        contact_email = context.get("contact_email", "[联系邮箱]")
        effective_date = context.get("effective_date", datetime.now().strftime("%Y年%m月%d日"))
        
        content = f"""# {company_name} 隐私政策

**生效日期**：{effective_date}

## 1. 个人信息保护声明

{company_name}（以下简称"我们"）严格遵守《中华人民共和国个人信息保护法》（PIPL）等相关法律法规，制定本隐私政策，说明我们如何收集、使用、存储、处理和保护您的个人信息。

## 2. 个人信息处理



### 2.1 收集的信息类型



根据业务需要，我们可能收集以下类型的个人信息：

1. **身份识别信息**：姓名、身份证号码等
2. **联系信息**：手机号码、电子邮箱、通信地址等
3. **账户信息**：用户名、密码、账户设置等
4. **交易信息**：订单记录、支付信息等
5. **设备信息**：设备型号、操作系统、唯一标识符等
6. **日志信息**：IP地址、访问时间、浏览记录等



### 2.2 个人信息处理目的



我们收集和处理您的个人信息的主要目的包括：

- 提供和改善我们的产品和服务
- 处理您的订单和交易
- 提供客户支持和售后服务
- 履行法律义务和合规要求
- 进行服务和产品改进



## 3. 个人信息保护



我们采取以下措施保护您的个人信息安全：



1. **技术措施**：数据加密存储和传输、访问控制、安全审计
2. **管理措施**：权限管理、员工安全培训、内部安全制度
3. **物理措施**：数据中心安全、设备保护



## 4. 用户权利保障



根据《个人信息保护法》，您享有以下权利：



### 4.1 基本权利

- **知情权**：了解个人信息处理情况
- **访问权**：访问您的个人信息
- **更正权**：更正不准确的个人信息
- **删除权**：删除个人信息（被遗忘权）

### 4.2 特殊权利

- **撤回同意权**：随时撤回对本隐私政策的同意
- **限制处理权**：限制个人信息处理
- **可携权**：获取个人信息的副本



## 5. 联系我们



如果您对本隐私政策有任何疑问、意见或建议，请通过以下方式联系我们：

- **电子邮件**：{contact_email}

---

**最后更新**：{effective_date}
**版本**：1.0
**适用法律**：中华人民共和国个人信息保护法
"""
        
        return {
            "document_type": "privacy-policy",
            "generated_at": datetime.now().isoformat(),
            "company_name": company_name,
            "contact_email": contact_email,
            "effective_date": effective_date,
            "content": content,
            "file_name": f"privacy-policy-{datetime.now().strftime('%Y%m%d')}.md",
            "version": "1.0",
            "applicable_law": "中华人民共和国个人信息保护法（PIPL）"
        }
    
    def generate_consent_form(self, context: Dict) -> Dict[str, Any]:
        """生成用户同意书"""
        company_name = context.get("company_name", "[公司名称]")
        user_name = context.get("user_name", "[用户姓名]")
        data_types = context.get("data_types", ["基本信息", "联系信息"])
        purposes = context.get("purposes", ["提供服务", "改善体验"])
        
        content = f"""# {company_name} 个人信息处理同意书

**同意日期**：{datetime.now().strftime("%Y年%m月%d日")}

## 同意声明



本人（{user_name}）已阅读并理解《{company_name}隐私政策》，明确以下事项：



## 1. 同意内容



### 1.1 个人信息处理



本人同意 {company_name} 按照隐私政策中所述的方式处理本人的个人信息。



### 1.2 信息类型

- **处理信息**：{', '.join(data_types)}
- **处理目的**：{', '.join(purposes)}
- **处理方式**：详见隐私政策说明



## 2. 用户权利说明



根据《个人信息保护法》，本人知晓并享有以下权利：



### 2.1 基本权利

- **知情权**：了解个人信息处理情况
- **访问权**：访问本人个人信息的权利
- **更正权**：更正不准确个人信息的权利
- **删除权**：删除个人信息的权利



### 2.2 特殊权利

- **撤回同意权**：随时撤回对本同意书的同意
- **限制处理权**：限制个人信息处理的权利
- **可携权**：获取个人信息副本的权利



## 3. 撤回同意说明



本人知晓可以随时撤回本同意。撤回同意不影响撤回前基于本人同意的个人信息处理活动。



## 4. 签字确认



**用户声明**：

本人已阅读、理解并同意本同意书的全部内容。



**用户签名**：____________________
**签署日期**：____________________



**公司确认**：



**公司盖章**：____________________
**确认日期**：____________________
"""
        
        return {
            "document_type": "consent-form",
            "generated_at": datetime.now().isoformat(),
            "company_name": company_name,
            "user_name": user_name,
            "data_types": data_types,
            "purposes": purposes,
            "content": content,
            "file_name": f"consent-form-{datetime.now().strftime('%Y%m%d')}.md",
            "version": "1.0"
        }
    
    def generate_document(self, doc_type: str, context: Dict) -> Dict[str, Any]:
        """生成指定类型的文档"""
        try:
            if doc_type == "privacy-policy":
                result = self.generate_privacy_policy(context)
            elif doc_type == "consent-form":
                result = self.generate_consent_form(context)
            elif doc_type == "data-processing-agreement":
                result = {
                    "document_type": doc_type,
                    "generated_at": datetime.now().isoformat(),
                    "company_name": context.get("company_name", "[公司名称]"),
                    "content": "简化版数据处理协议模板",
                    "file_name": f"{doc_type}-{datetime.now().strftime('%Y%m%d')}.md",
                    "version": "1.0"
                }
            else:
                raise ValueError(f"不支持的文档类型: {doc_type}")
            
            # 添加成功状态和元数据
            result["success"] = True
            result["metadata"] = {
                "generated_by": "document-generator.py",
                "skill_version": "1.0.0",
                "applicable_law": "中华人民共和国个人信息保护法（PIPL）",
                "region": "cn",
                "timestamp": datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "document_type": doc_type,
                "generated_at": datetime.now().isoformat()
            }
    
    def print_result(self, result: Dict[str, Any], output_format: str = "text"):
        """打印生成结果"""
        if output_format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return
        
        if not result.get("success", False):
            print(f"❌ 生成失败：{result.get('error', '未知错误')}")
            return
        
        print("\n" + "="*60)
        print(f"✅ 文档生成成功")
        print("="*60)
        
        print(f"\n📄 文档类型：{result.get('document_type', '未知')}")
        print(f"📅 生成时间：{result.get('generated_at', '未知')}")
        print(f"📎 文件名称：{result.get('file_name', '未知')}")
        
        content = result.get("content", "")
        if content:
            print("\n📝 内容预览（前500字符）：")
            print("="*60)
            print(content[:500] + "..." if len(content) > 500 else content)
            print("="*60)
        
        print(f"\n💾 保存信息：")
        print(f"   文件：{result.get('file_name', '未知')}")
        print(f"   大小：{len(content)}字符")
        print(f"   版本：{result.get('version', '未知')}")
        
        print("\n" + "="*60)
        print("注：请根据实际情况调整和使用生成的文档")
        print("="*60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="中国PIPL合规文档生成工具")
    
    parser.add_argument("--type",
                      choices=["privacy-policy", "consent-form", "data-processing-agreement"],
                      required=True,
                      help="文档类型")
    
    parser.add_argument("--company-name",
                      default="[公司名称]",
                      help="公司名称")
    
    parser.add_argument("--contact-email",
                      default="[联系邮箱]",
                      help="联系邮箱")
    
    parser.add_argument("--user-name",
                      default="[用户姓名]",
                      help="用户姓名（用于同意书）")
    
    parser.add_argument("--data-types",
                      default="基本信息,联系信息,设备信息",
                      help="数据类型列表，用逗号分隔")
    
    parser.add_argument("--purposes",
                      default="提供服务,改善体验,合规要求",
                      help="处理目的列表，用逗号分隔")
    
    parser.add_argument("--format",
                      choices=["text", "json"],
                      default="text",
                      help="输出格式")
    
    args = parser.parse_args()
    
    # 构建上下文
    context = {
        "company_name": args.company_name,
        "contact_email": args.contact_email,
        "user_name": args.user_name,
        "data_types": [x.strip() for x in args.data_types.split(",")],
        "purposes": [x.strip() for x in args.purposes.split(",")]
    }
    
    generator = DocumentGenerator()
    result = generator.generate_document(args.type, context)
    generator.print_result(result, args.format)


if __name__ == "__main__":
    main()