---
name: google-index-checker
description: Check Google indexed page count for any domain using the "site:" search operator in Chrome. Use when the user wants to check how many pages Google has indexed for a website, compare indexing across multiple domains, or monitor SEO indexing status. Supports single or multiple domains with comparison table output.
---

# Google Index Checker

Check the number of indexed pages for any domain(s) using Google's `site:` search operator via Chrome remote debugging. Returns precise result counts and generates a comparison table for multiple domains.

## Prerequisites

- Chrome must be running with remote debugging enabled (default port 9222)
- The browser tool must be available

## Instructions

### Step 1: Parse user input

Extract the domain(s) the user wants to check. Accept these formats:
- Single domain: `example.com`, `www.example.com`, `https://example.com`
- Multiple domains: comma-separated, space-separated, or listed line by line
- Normalize all domains: strip protocol (`https://`, `http://`), strip trailing slashes

### Step 2: Search each domain on Google

For each domain, perform these steps **sequentially in the same browser tab** (to avoid triggering CAPTCHAs):

1. Navigate to: `https://www.google.com/search?q=site:{domain}`
2. Wait for the page to load completely
3. Take a screenshot for evidence
4. Extract the result count — look for text like:
   - English: "About X results"
   - Chinese: "约 X 条结果" or "找到约 X 条结果"
5. If the count is not immediately visible, click the "Tools" (工具) button to reveal it
6. Use browser snapshot to extract the exact text from DOM elements matching these selectors:
   - `#result-stats` — the standard results count element
   - Any element containing "results" or "结果" text near the top of the page
7. Parse the number from the text (remove commas, handle "约" prefix, etc.)

### Step 3: Handle edge cases

- **CAPTCHA/Verification**: If Google shows a CAPTCHA, take a screenshot and inform the user. Suggest waiting a few minutes before retrying.
- **No results**: Record 0 if Google shows "Your search did not match any documents"
- **Rate limiting**: Add a 3-5 second delay between searches if checking more than 3 domains
- **Localized results**: The count format varies by Google locale. Common patterns:
  - `About 12,300 results` (English)
  - `约 12,300 条结果` (Chinese)
  - `Approximately 12,300 results`

### Step 4: Present results

#### For a single domain:

```
**{domain}** has approximately **{count}** pages indexed by Google.

![Screenshot](screenshot_url)
```

#### For multiple domains:

Generate a comparison table sorted by indexed count (descending):

```markdown
## Google Index Coverage Report ({date})

| Domain | Indexed Pages | Notes |
|--------|--------------|-------|
| example.com | 13,200 | — |
| example.org | 8,500 | — |
| example.net | 1,200 | — |

Data source: Google `site:` search operator (approximate values)
```

Include screenshots for each domain.

### Step 5: Save data (optional)

If the user wants to save the results, write a JSON file:

```json
{
  "search_date": "YYYY-MM-DD",
  "results": [
    {
      "domain": "example.com",
      "indexed_count": 13200,
      "raw_text": "About 13,200 results"
    }
  ]
}
```

## Example usage

User: "Check how many pages Google has indexed for example.com"
→ Search `site:example.com`, extract count, present result with screenshot.

User: "Compare indexing for example.com, example.org, and example.net"
→ Search each domain sequentially, extract counts, present comparison table.

User: "查一下 example.com 的收录量"
→ Same flow, present results in Chinese.

## Important notes

- The `site:` operator returns **approximate** values, not exact counts
- Results may vary slightly between searches and Google data centers
- For precise indexing data, use Google Search Console (requires account access)
- Avoid running too many queries in quick succession to prevent CAPTCHA triggers
- Always include screenshots as evidence of the search results
