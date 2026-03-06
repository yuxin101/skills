#!/usr/bin/env node

/**
 * 企查查 - 企业信息查询 Skill
 * 
 * 功能：根据公司名称查询企业基本信息
 * 数据来源：企查查 (qcc.com)
 * 
 * TODO: 后续集成 SkillPay 收费功能
 */

import https from 'https';

/**
 * 企查查搜索
 */
function getSearchUrl(companyName) {
  return `https://www.qcc.com/web/search?key=${encodeURIComponent(companyName)}`;
}

/**
 * 格式化企业信息输出
 */
function formatOutput(searchUrl, companyName) {
  return `
╔══════════════════════════════════════════════════════════════╗
║                    企查查 - 企业信息查询                        ║
╠══════════════════════════════════════════════════════════════╣

【查询企业】${companyName}

【查询结果】
搜索链接: ${searchUrl}

【可查看信息】
- 工商信息（注册资本、法人、成立日期等）
- 股东信息及持股比例
- 主要人员（董事、监事、高管）
- 分支机构
- 变更记录
- 对外投资
- 联系方式（电话、邮箱）

【使用说明】
1. 点击上方搜索链接
2. 在企查查官网查看完整企业信息
3. 部分信息需要登录后查看

═══════════════════════════════════════════════════════════════
`;
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log(`
使用方法: ./qichacha.js "公司名称"

示例:
  ./qichacha.js "腾讯"
  ./qichacha.js "阿里巴巴"
  ./qichacha.js "比亚迪"
  ./qichacha.js "贵州茅台"

说明:
  本工具返回企查查搜索链接，点击链接查看完整企业信息。
`);
    process.exit(0);
  }

  const companyName = args.join(' ');
  const searchUrl = getSearchUrl(companyName);

  console.log(`\n🔍 正在查询: ${companyName}\n`);
  
  const output = formatOutput(searchUrl, companyName);
  console.log(output);
}

main().catch(console.error);
