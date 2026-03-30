# Stock Analysis Flow Contract

This flow is for one mainland China A-share stock.

It is the documented methodology behind deep single-stock research.
It is not yet wired as a runnable JS flow in this skill project.

## Use When

- The topic is a concrete single stock.
- The user asks for deep research, institutional stock research, investment thesis building, valuation review, or catalyst analysis.

## Do Not Use When

- The topic is an industry / concept / theme instead of one stock.
- The user asks for whole-market screening.
- The asset is not a mainland China A-share stock.

## Step Order

Do not drop or merge steps. The full flow is:

1. `step-0-macro-sector`
2. `step-1-company-profile`
3. `step-1b-forward-advantage`
4. `step-2-financials`
5. `step-3-valuation`
6. `step-4-price-action`
7. `step-5-thesis`
8. `step-6-catalyst`
9. `step-7a-skeptic`
10. `step-7b-advocate`
11. `step-8-verdict`
12. `step-9-output`

The debate steps are mandatory.
They are not optional polish.

## Prompt Layer Responsibilities

- `orchestrator_system.md`: route the research round-by-round, assign the main step, and enforce the SOP.
- `worker_system.md`: perform the concrete data gathering and evidence building for each assigned step.
- `synthesizer_notes.md`: define final report structure, verdict integration, output constraints, and step-9 completeness rules.

## Required Query Capabilities

The methodology expects these data capabilities:

- `get_finance_basic_indicators`
- `get_valuation_analysis`
- `get_mainbiz_analysis`
- `get_industry_rank`
- `get_price_history`
- `get_money_flow`
- `get_latest_price`
- `get_instrument_concepts`
- `get_profit_forecast`
- `find_similar_sectors`
- `web_search`

## Current Project Readiness

### Already available in `shumen_finance`

- `instrument_profile`
- `price_snapshot`
- `bar_series`
- `finance_context`
- `finance_analysis_context`
- `finance_report_status`
- `finance_basic_indicators`
- `finance_valuation_detail`
- `finance_profit_forecast`
- `finance_industry_rank`
- `holder_context`
- `chip_distribution`
- `price_levels`
- `instrument_concepts`
- `money_flow`
- `important_news`
- `high_frequency_news`
- `unusual_movement_context`
- `similar_sectors`

### Partially covered by current products

- `get_mainbiz_analysis`
  Covered in part by `finance_context`, but not yet as a dedicated stock-research wrapper.

## Remaining Missing Pieces

- routed `web_search` policy for this flow
- JS orchestration for the full multi-step stock research execution

## Implementation Boundary

This project should only manage:

- the methodology documents
- prompt assets
- flow contracts
- thin JS products
- later JS orchestration

If a required query is missing, it should be added in the backend / API project and then wrapped here as a thin JS product.
