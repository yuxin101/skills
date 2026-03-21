---
name: curl
version: "1.0.0"
description: "Send HTTP requests and test API endpoints using Python urllib. Use when you need to debug, test, or interact with web services."
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags: [http, api, testing, requests, web, curl, rest]
---

# Curl — HTTP Request Testing Tool

Curl is a command-line HTTP request tool built with Python's `urllib` module. It supports all major HTTP methods, file upload/download, custom headers, and maintains a history of all requests for debugging and replay.

Request history is stored in `~/.curl/data.jsonl` as JSONL records.

## Prerequisites

- Python 3.8+ with standard library
- `bash` shell

## Commands

### `get`
Send an HTTP GET request.

**Environment Variables:**
- `URL` (required) — Target URL
- `HEADERS` — JSON object of custom headers (e.g., '{"Authorization": "Bearer token"}')
- `PARAMS` — Query parameters as JSON object
- `TIMEOUT` — Request timeout in seconds (default: 30)
- `FOLLOW` — Follow redirects: `true`/`false` (default: true)

**Example:**
```bash
URL="https://api.example.com/users" HEADERS='{"Accept":"application/json"}' bash scripts/script.sh get
```

### `post`
Send an HTTP POST request.

**Environment Variables:**
- `URL` (required) — Target URL
- `BODY` — Request body (JSON string or plain text)
- `HEADERS` — JSON object of custom headers
- `CONTENT_TYPE` — Content-Type header (default: application/json)
- `TIMEOUT` — Request timeout in seconds (default: 30)

**Example:**
```bash
URL="https://api.example.com/users" BODY='{"name":"John"}' bash scripts/script.sh post
```

### `put`
Send an HTTP PUT request.

**Environment Variables:**
- `URL` (required) — Target URL
- `BODY` — Request body
- `HEADERS` — JSON object of custom headers
- `CONTENT_TYPE` — Content-Type (default: application/json)

### `delete`
Send an HTTP DELETE request.

**Environment Variables:**
- `URL` (required) — Target URL
- `HEADERS` — JSON object of custom headers

### `head`
Send an HTTP HEAD request (returns headers only).

**Environment Variables:**
- `URL` (required) — Target URL
- `HEADERS` — JSON object of custom headers

### `options`
Send an HTTP OPTIONS request to check allowed methods.

**Environment Variables:**
- `URL` (required) — Target URL

### `upload`
Upload a file via HTTP POST multipart/form-data.

**Environment Variables:**
- `URL` (required) — Upload endpoint URL
- `FILE` (required) — Path to file to upload
- `FIELD` — Form field name (default: file)
- `HEADERS` — JSON object of custom headers

### `download`
Download a file from a URL.

**Environment Variables:**
- `URL` (required) — File URL to download
- `OUTPUT` (required) — Local path to save file
- `HEADERS` — JSON object of custom headers

### `headers`
Display response headers from a request.

**Environment Variables:**
- `URL` (required) — Target URL
- `METHOD` — HTTP method (default: GET)

### `config`
View or update configuration settings.

**Environment Variables:**
- `KEY` — Configuration key
- `VALUE` — Configuration value

### `history`
View past request history.

**Environment Variables:**
- `LIMIT` — Maximum entries to show (default: 20)
- `METHOD` — Filter by HTTP method
- `STATUS` — Filter by status code
- `SEARCH` — Search in URLs

### `help`
Display usage information and available commands.

### `version`
Display the current version of the curl tool.

## Data Storage

Request history stored in `~/.curl/data.jsonl`. Each record contains:
- `id` — Unique request identifier
- `timestamp` — ISO 8601 time
- `method` — HTTP method
- `url` — Request URL
- `status` — Response status code
- `headers_sent` — Request headers
- `headers_received` — Response headers
- `body_sent` — Request body (truncated)
- `body_received` — Response body (truncated to 1KB)
- `duration_ms` — Request duration in milliseconds
- `error` — Error message if request failed

## Configuration

Config stored in `~/.curl/config.json`:
- `default_timeout` — Default timeout seconds (default: 30)
- `follow_redirects` — Follow redirects by default (default: true)
- `max_body_log` — Max response body chars to log (default: 1024)
- `default_headers` — Default headers for all requests
- `save_history` — Whether to save request history (default: true)

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
