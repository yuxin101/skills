---
name: drug-search
description: "Search a pharmaceutical drug database for pipeline and development information. Use this skill whenever the user asks about drugs by name, target, indication, company, modality, phase, or development progress. Automatically parses natural language questions into structured query parameters and calls the backend API to return matching drug records. Trigger words include: drug, compound, molecule, pipeline, drug target, indication, modality, antibody, small molecule, phase, approved, development stage, sponsor, drug company, bispecific, ADC, route of administration."
---

# Drug Pipeline Search Skill

This skill converts natural language questions into structured API queries against a pharmaceutical drug database, then presents the results in a readable format.

## Workflow

1. **Parse user intent** — Extract key entities from the user's question
2. **Build query parameters** — Map entities to the query schema below
3. **Execute the query** — Run `scripts/search.py`
4. **Present results** — Format and display drug records to the user

## Step 1: Extract Keywords

Identify the following entity types from the user's question:

| Field | Type | Description                 | Example                                                   |
|-------|------|-----------------------------|-----------------------------------------------------------|
| `drug_name` | `dict` | Drug name(s)                | `{"logic": "or", "data": ["pembrolizumab"]}`              |
| `company` | `List[str]` | Sponsor / developer company | `["Pfizer", "Roche"]`                                     |
| `indication` | `List[str]` | Disease / indication        | `["lung cancer", "NSCLC"]`                                |
| `target` | `dict` | Biological target(s)        | `{"logic": "or", "data": ["PD-1", "VEGF"]}`               |
| `drug_modality` | `dict` | Drug modality / type        | `{"logic": "or", "data": ["antibody", "small molecule"]}` |
| `drug_feature` | `dict` | Drug feature(s)             | `{"logic": "or", "data": ["bispecific"]}`                 |
| `phase` | `List[str]` | Development phase(s)        | `["Phase 3", "Approved"]`                                 |
| `location` | `List[str]` | Geographic location(s)      | `["China", "USA"]`                                        |
| `route_of_administration` | `dict` | Route of administration     | `{"logic": "or", "data": ["IV", "oral"]}`                 |
| `page_num` | `int` | Page index (0-based)        | `0`                                                       |
| `page_size` | `int` | Results per page (1–60)      | `30`                                                       |

**Dict field format:**
```json
{"logic": "or", "data": ["value1", "value2"]}
```

- `logic` controls how multiple values are combined: `"or"` (any match) or `"and"` (all must match). Default to `"or"` unless the user explicitly wants all terms to apply simultaneously.
- `data` is the list of keyword strings to match.

**Type rules:**
- `company`, `indication`, `phase`, `location` → plain `List[str]`
- `drug_name`, `target`, `drug_modality`, `drug_feature`, `route_of_administration` → `dict` with `logic` and `data`
- Default to `page_num: 0, page_size: 5` unless the user specifies otherwise
- Prefer English keywords (the database is indexed in English); translate non-English terms

## Step 2: Execute the Query

```bash
python scripts/search.py --params '<JSON string>'
```

Or using a parameter file:

```bash
python scripts/search.py --params-file /tmp/query.json
```

Add `--raw` to receive the unformatted JSON response.

## Step 3: Interpret Results

The response contains:
- `page_num` / `page_size` — current pagination state
- `results` — current page of drug records, each with name, phase, modality, targets, companies, indication, development progress, etc.

If no results are returned, suggest relaxing one or more filters (e.g. broader indication, remove phase filter).

## Conversion Examples

**User:** "Find PD-1 antibodies in Phase 3"

**Parameters:**
```json
{
  "target": {"logic": "or", "data": ["PD-1"]},
  "drug_modality": {"logic": "or", "data": ["antibody"]},
  "phase": ["Phase 3"],
  "page_num": 0,
  "page_size": 30
}
```

---

**User:** "Roche bispecific antibodies for lung cancer"

**Parameters:**
```json
{
  "company": ["Roche"],
  "drug_feature": {"logic": "or", "data": ["bispecific"]},
  "indication": ["lung cancer"],
  "page_num": 0,
  "page_size": 30
}
```

---

**User:** "Oral small molecule KRAS G12C inhibitors"

**Parameters:**
```json
{
  "target": {"logic": "or", "data": ["KRAS G12C"]},
  "drug_modality": {"logic": "or", "data": ["small molecule"]},
  "route_of_administration": {"logic": "or", "data": ["oral"]},
  "page_num": 0,
  "page_size": 30
}
```

---

**User:** "Drugs targeting both PD-1 and VEGF"

**Parameters:**
```json
{
  "target": {"logic": "and", "data": ["PD-1", "VEGF"]},
  "page_num": 0,
  "page_size": 30
}
```

---

**User:** "Look up pembrolizumab"

**Parameters:**
```json
{
  "drug_name": {"logic": "or", "data": ["pembrolizumab"]},
  "page_num": 0,
  "page_size": 30
}
```

## Dependencies

- Python 3.8+
- `requests` library (`pip install requests`)
- Environment variable `NOAH_API_TOKEN` — API authentication token (required)
  - Register for a free account at [noah.bio](https://noah.bio) to obtain your API key.
