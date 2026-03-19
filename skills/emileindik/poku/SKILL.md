---
name: poku
description: "Places outbound phone calls, sends outbound SMS texts, and reserves dedicated phone numbers on the user's behalf using the Poku API and the exec tool. Use when the user wants to call or text a restaurant, a contact, a business, doctor's office, or any phone number. Also use when the user wants to reserve a dedicated phone number for their agent."
metadata: { "openclaw": { "homepage": "https://pokulabs.com", "requires": { "env": ["POKU_API_KEY"] }, "primaryEnv": "POKU_API_KEY" } }
---

# Poku — Outbound Calls, SMS & Number Reservation

## Identify Which Flow to Use

| The user wants to... | Read this file |
|---|---|
| Call someone | `references/CALL.md` |
| Text someone | `references/SMS.md` |
| Reserve a phone number | `references/NUMBER.md` |

Read only the file(s) that match the user's request. For error codes and API parameters, see `references/API.md`.
