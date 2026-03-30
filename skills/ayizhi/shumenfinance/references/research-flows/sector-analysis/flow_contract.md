# Sector Analysis Flow Contract

This flow is for one mainland China A-share industry, concept, theme, or sector.

It is the documented methodology behind sector / hype-cycle research.
It is not yet wired as a runnable JS flow in this skill project.

## Use When

- The topic is a sector, concept, industry, theme, or赛道.
- The user asks for sector rotation, hype-cycle analysis, thematic research, concept research, or sector-level thesis building.

## Sector Input Rule

- Prefer `sector_name` for user-facing requests.
- Treat `sector_id` as an internal identifier.
- Only use `sector_id` after the backend has already resolved and returned it.
- If the user gives a fuzzy or ambiguous sector name, call `similar_sectors` first and then continue with the chosen resolved result.

## Do Not Use When

- The topic is a concrete single stock.
- The user asks for whole-market screening.
- The asset universe is not mainland China A-shares.

## Step Order

Do not drop or merge steps. The full flow is:

1. `step-0-macro`
2. `step-1-filter`
3. `step-2-classify`
4. `step-3-mining`
5. `step-4-thesis`
6. `step-5-position`
7. `step-6-risk`
8. `step-7a-skeptic`
9. `step-7b-advocate`
10. `step-8-verdict`
11. `step-9-output`

The debate steps are mandatory here as well.

## Prompt Layer Responsibilities

- `orchestrator_system.md`: enforce the macro -> filter -> classify -> mining -> thesis -> position -> risk sequence.
- `worker_system.md`: perform the actual sector data gathering and evidence search.
- `synthesizer_notes.md`: define report structure, verdict integration, and final step-9 completeness rules.

## Required Query Capabilities

The methodology expects these data capabilities:

- `find_similar_sectors`
- `get_sector_constituents`
- `get_sector_performance`
- `get_price_history`
- `get_money_flow`
- `get_finance_basic_indicators`
- `get_valuation_analysis`
- `get_instrument_concepts`
- `get_profit_forecast`
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
- `sector_constituents`
- `sector_performance`

### Useful but still indirect

- `bar_series`
  Can support leader-stock price work once a leader is known, but there is no sector-flow orchestration on top.
- `finance_context`
  Can support some leader-stock finance checks, but there is no sector-flow orchestration on top.

## Remaining Missing Pieces

- routed `web_search` policy for this flow
- JS orchestration for the full multi-step sector research execution

## Implementation Boundary

This project should only manage:

- the methodology documents
- prompt assets
- flow contracts
- thin JS products
- later JS orchestration

If a sector query is missing, it should be implemented in the backend / API project and then wrapped here as a thin JS product.
