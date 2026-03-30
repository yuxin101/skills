#!/usr/bin/env python3
"""
Part.5 上市公司 DAT 动态抓取脚本
数据源：CoinGecko 公开免费 API（无需 API Key）
端点：/api/v3/companies/public_treasury/{coin_id}

字段说明：
  name                     公司名称
  symbol                   股票代号（含交易所后缀，如 MSTR.US）
  country                  国家代码
  total_holdings           当前持仓数量
  total_current_value_usd  当前市值（美元）
  total_entry_value_usd    历史总成本（0 表示未披露）
  percentage_of_total_supply  占总供应量百分比

⚠️  局限：此 API 仅返回当前持仓快照，不含本周增减变化量。
    脚本输出持仓列表骨架，变动部分留空，由用户补充后 AI 生成点评。

依赖：curl（系统自带）、python3 标准库
运行：python3 scripts/part5_fetch.py
"""

import subprocess, sys, json

# 股票代号后缀 → 交易所全名
EXCHANGE_MAP = {
    'US': 'Nasdaq/NYSE', 'HK': 'HKEX',  'JP': 'TSE',
    'SW': 'SIX',         'AU': 'ASX',   'CA': 'TSX',
    'DE': 'Frankfurt',   'GB': 'LSE',   'KR': 'KRX',
    'SG': 'SGX',         'TW': 'TWSE',  'PA': 'Euronext Paris',
}

# 国家代码 → 中文名
COUNTRY_MAP = {
    'US': '美国',   'JP': '日本',   'HK': '香港',   'CN': '中国',
    'SG': '新加坡', 'AU': '澳大利亚', 'CA': '加拿大', 'GB': '英国',
    'DE': '德国',   'KR': '韩国',   'TW': '台湾',   'CH': '瑞士',
    'FR': '法国',   'IN': '印度',
}


def fetch_treasury(coin_id: str) -> dict | None:
    """调用 CoinGecko 免费 API 获取企业持仓列表"""
    url = f'https://api.coingecko.com/api/v3/companies/public_treasury/{coin_id}'
    r = subprocess.run(
        ['curl', '-s', '-L', '--max-time', '15',
         '-H', 'Accept: application/json',
         '-H', 'User-Agent: Mozilla/5.0',
         url],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        print(f'[ERROR] curl 失败: {r.stderr}', file=sys.stderr)
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError as e:
        print(f'[ERROR] JSON 解析失败 ({coin_id}): {e}', file=sys.stderr)
        return None


def fmt_usd(n: float) -> str:
    """将美元数值格式化为易读字符串"""
    if not n:
        return '未披露'
    if n >= 1e9:
        return f'约 {n/1e9:.2f} 亿美元'
    if n >= 1e6:
        return f'约 {n/1e6:.1f}M 美元'
    return f'约 ${n:,.0f}'


def fmt_qty(n: float) -> str:
    """格式化持仓数量"""
    if not n:
        return '0'
    return f'{n:,.0f}'


def parse_symbol(symbol: str) -> tuple[str, str]:
    """
    'MSTR.US'  → ('MSTR',  'Nasdaq/NYSE')
    'SBET.US'  → ('SBET',  'Nasdaq/NYSE')
    '3350.JP'  → ('3350',  'TSE')
    """
    if '.' in symbol:
        code, suffix = symbol.rsplit('.', 1)
        exchange = EXCHANGE_MAP.get(suffix, suffix)
        return code, exchange
    return symbol, '未知'


def print_entry(c: dict, asset: str) -> None:
    """按周报格式输出单个公司条目骨架"""
    code, exchange = parse_symbol(c.get('symbol', '--'))
    country = COUNTRY_MAP.get(c.get('country', ''), c.get('country', ''))
    holdings = fmt_qty(c.get('total_holdings', 0))
    cur_val = c.get('total_current_value_usd', 0)
    entry_val = c.get('total_entry_value_usd', 0)

    # 计算未实现盈亏（仅当成本有效时）
    pnl_note = ''
    if entry_val and entry_val > 0 and cur_val:
        pnl = cur_val - entry_val
        pct = pnl / entry_val * 100
        sign = '+' if pnl >= 0 else ''
        pnl_note = f'  未实现盈亏：{sign}{fmt_usd(abs(pnl))}（{sign}{pct:.1f}%）'

    print(f"""
{c['name']}（{country}）
股票代号：{code}（{exchange}）
动作：【⚠️ 待补充：本周买入/卖出数量及约价格】
总持仓：{holdings} {asset}（当前市值 {fmt_usd(cur_val)}）{pnl_note}
点评：（AI 根据公司特征与本周动作自动生成）""")


def main():
    print('=' * 58)
    print('  Part.5  上市公司 DAT 动态')
    print('  数据来源：CoinGecko 公开 API（当前持仓快照）')
    print('=' * 58)

    for coin_id, asset in [('bitcoin', 'BTC'), ('ethereum', 'ETH')]:
        data = fetch_treasury(coin_id)
        if not data:
            print(f'\n[WARN] {asset} 数据获取失败，跳过', file=sys.stderr)
            continue

        companies   = data.get('companies', [])
        ttl_qty     = fmt_qty(data.get('total_holdings', 0))
        ttl_val     = fmt_usd(data.get('total_value_usd', 0))

        print(f'\n{"─"*58}')
        print(f'  {asset} — 共 {len(companies)} 家机构，'
              f'合计持仓 {ttl_qty} {asset}（{ttl_val}）')
        print(f'{"─"*58}')

        # 只展示前 20 大持仓（按持仓量降序，API 已排好序）
        for c in companies[:20]:
            print_entry(c, asset)

        if len(companies) > 20:
            print(f'\n  … 另有 {len(companies) - 20} 家机构持仓较小，未展示')

    # 手动补充提示
    print('\n' + '=' * 58)
    print('  ⚠️  手动补充说明')
    print('=' * 58)
    print("""
以上为当前持仓快照。CoinGecko 免费 API 不含周度变化量。

补充本周各公司变动的方式：
  1. 访问 CoinGecko 公司详情页查看近期购买记录
     BTC: https://www.coingecko.com/en/treasuries/bitcoin
     ETH: https://www.coingecko.com/en/treasuries/ethereum
  2. 查阅公司官方公告 / SEC 8-K 文件
  3. 将变动信息以如下格式提供给 AI：
       公司名 | 买入/卖出 | 数量（枚）| 约价格/总金额

AI 收到后将自动填入"动作"字段并生成"点评"。
""")


if __name__ == '__main__':
    main()
