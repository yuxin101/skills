---
name: kakutei-shinkoku
description: Japan freelancer tax filing assistant (確定申告). Helps organize income, expenses, and deductions for annual tax returns. Knowledge-based — no API connections, no My Number handling.
metadata:
  openclaw:
    emoji: 🇯🇵
    tags:
      - japan
      - tax
      - freelancer
      - kakutei-shinkoku
      - 確定申告
      - accounting
      - invoice
---

# 確定申告アシスタント 🇯🇵

Japan freelancer tax filing assistant. Helps you understand, organize, and prepare your annual tax return (確定申告) — without touching your My Number or connecting to any government API.

This is a **knowledge assistant**, not a tax filing tool. It helps you prepare everything so your accountant (税理士) can file efficiently, or so you can file via e-Tax yourself with confidence.

## ⚠️ Legal Disclaimer

This skill provides general tax knowledge based on Japanese tax law. It is NOT a licensed tax advisor (税理士). Tax calculations are estimates. Always verify with a certified tax accountant before filing. Tax laws change annually — confirm current rates and rules with the National Tax Agency (国税庁) website.

## Who this is for

- Freelancers (個人事業主) filing 確定申告 for the first time
- Side-job workers (副業) who need to report miscellaneous income
- Foreign residents in Japan navigating the tax system in English
- Anyone preparing documents before meeting their tax accountant

## What it does

### Income Classification (所得区分)
Help categorize your income correctly:

| Type | Japanese | When to use |
|------|----------|-------------|
| Business income | 事業所得 | Full-time freelancer with 開業届 filed |
| Miscellaneous income | 雑所得 | Side jobs, occasional freelance work |
| Employment income | 給与所得 | Regular salary (W-2 equivalent) |
| Capital gains | 譲渡所得 | Stock sales, crypto, property |
| Dividend income | 配当所得 | Stock dividends |
| Rental income | 不動産所得 | Property rental |

### Expense Tracking (経費管理)
Organize deductible business expenses:

| Category | Japanese | Examples |
|----------|----------|---------|
| Office supplies | 消耗品費 | Pens, paper, small equipment under ¥100,000 |
| Communication | 通信費 | Phone, internet (business portion) |
| Transportation | 旅費交通費 | Train, taxi, flights for business |
| Equipment | 減価償却費 | PC, camera, furniture over ¥100,000 (depreciated) |
| Rent | 地代家賃 | Office rent, home office portion |
| Utilities | 水道光熱費 | Electric, gas, water (business portion) |
| Outsourcing | 外注費 | Subcontractor payments |
| Entertainment | 接待交際費 | Client meals, gifts (with records) |
| Insurance | 保険料 | Business insurance |
| Books/Training | 新聞図書費 | Professional books, courses, subscriptions |
| Advertising | 広告宣伝費 | Website, ads, marketing materials |

### Home Office Deduction (家事按分)
Calculate the business-use percentage of home expenses:
- Floor area method: (workspace sqm / total sqm) × expense
- Time method: (business hours / total hours) × expense
- Keep records of your calculation method for audit defense

### Deductions & Credits (控除)

**Income deductions (所得控除):**
- Basic deduction (基礎控除): ¥480,000 (income ≤ ¥24M)
- Blue return deduction (青色申告特別控除): ¥650,000 (e-Tax + double-entry bookkeeping)
- Social insurance (社会保険料控除): Full amount deductible
- National pension (国民年金): Full amount deductible
- National health insurance (国民健康保険): Full amount deductible
- Small business mutual aid (小規模企業共済): Up to ¥840,000/year
- iDeCo (個人型確定拠出年金): Up to ¥816,000/year (category 1)
- Spouse deduction (配偶者控除): Up to ¥380,000
- Dependent deduction (扶養控除): ¥380,000-¥630,000 per dependent
- Medical expense deduction (医療費控除): Amount exceeding ¥100,000 or 5% of income
- Life insurance deduction (生命保険料控除): Up to ¥120,000
- Earthquake insurance (地震保険料控除): Up to ¥50,000
- Hometown tax (ふるさと納税/寄附金控除): Amount - ¥2,000

### Consumption Tax & Invoice System (消費税・インボイス制度)

**Who needs to file consumption tax:**
- Revenue > ¥10M in base period (基準期間) → mandatory
- Registered as Invoice issuer (適格請求書発行事業者) → mandatory
- Voluntary registration → optional

**Invoice System (インボイス制度) key points:**
- Registration number format: T + 13 digits
- Must issue qualified invoices to allow client's input tax credit
- Small business special measure (2割特例): Pay only 20% of collected consumption tax (available through 2029 for new registrants)
- Simplified tax calculation (簡易課税): Available if revenue ≤ ¥50M

### Tax Calendar (税務カレンダー)

| Date | Event | Action |
|------|-------|--------|
| Jan 1 | Tax year starts | — |
| Jan-Feb | Prepare documents | Gather receipts, organize income records |
| Feb 16 | 確定申告 filing opens | Can submit via e-Tax, mail, or in person |
| Mar 15 | **Filing deadline** | Income tax + consumption tax due |
| Mar 15 | **Payment deadline** | Pay or set up installment plan (振替納税) |
| Mar 31 |振替納税 debit date | Auto-debit for income tax (approx.) |
| Apr 30 |振替納税 debit date | Auto-debit for consumption tax (approx.) |
| Jun | Residence tax notice | Based on filed return |
| Jul 1-31 | 届出 deadline for blue return | Submit 青色申告承認申請書 (first year) |

### Filing Methods

| Method | Pros | Cons |
|--------|------|------|
| **e-Tax (web)** | ¥650,000 blue deduction, 24/7, instant | Needs My Number card + reader |
| **e-Tax (ID/PW)** | No card reader needed | Must register at tax office first |
| **Paper (郵送)** | No tech required | Blue deduction limited to ¥550,000 |
| **In person (税務署)** | Staff help available | Long queues in Feb-Mar |

### Blue vs White Return (青色 vs 白色申告)

| Feature | Blue (青色) | White (白色) |
|---------|-----------|------------|
| Special deduction | ¥100,000-¥650,000 | ¥0 |
| Loss carryforward | 3 years | No |
| Depreciation special | 30万円 instant write-off | No |
| Family salary deduction | Yes (届出 required) | Limited |
| Required bookkeeping | Double-entry (for ¥650K) | Simple record |
| Registration | 開業届 + 青色申告承認申請書 | Just 開業届 |

## How to use

```
I'm a freelance developer in Japan. Help me prepare my 確定申告.
```

```
What expenses can I deduct for my home office?
```

```
Should I register for the Invoice system?
```

```
Calculate my estimated income tax on ¥8M business income with ¥2M expenses.
```

```
I just started freelancing. What forms do I need to file?
```

## Tax Calculation Guide

**Income tax brackets (所得税率) 2026:**

| Taxable income | Rate | Deduction |
|---------------|------|-----------|
| ¥1 - ¥1,949,000 | 5% | ¥0 |
| ¥1,950,000 - ¥3,299,000 | 10% | ¥97,500 |
| ¥3,300,000 - ¥6,949,000 | 20% | ¥427,500 |
| ¥6,950,000 - ¥8,999,000 | 23% | ¥636,000 |
| ¥9,000,000 - ¥17,999,000 | 33% | ¥1,536,000 |
| ¥18,000,000 - ¥39,999,000 | 40% | ¥2,796,000 |
| ¥40,000,000+ | 45% | ¥4,796,000 |

**Plus:** Reconstruction special tax (復興特別所得税) = 2.1% of income tax
**Plus:** Residence tax (住民税) = approximately 10% of taxable income

## Limitations

- Tax rates and rules shown are based on 2026 tax law — verify annually
- This skill does not connect to e-Tax or any government system
- This skill does not handle or store My Number (マイナンバー)
- Complex cases (international income, inheritance, real estate) should consult a 税理士
- Consumption tax calculations are simplified — edge cases exist

## About

Built by [ENAwareness](https://github.com/ENAwareness). As a foreign freelancer in Japan, navigating 確定申告 was one of the most confusing experiences. This skill is what I wish I had.
