import { buildDefaultHeaders, cleanObject, getBaseUrl } from "./runtime.mjs";

function buildUrl(path, query = {}) {
  const url = new URL(path, getBaseUrl());
  const cleanQuery = cleanObject(query);
  for (const [key, value] of Object.entries(cleanQuery)) {
    url.searchParams.set(key, String(value));
  }
  return url;
}

function tryParseJson(text) {
  if (!text) {
    return null;
  }
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

export async function requestJson(method, path, { query = {}, headers = {}, body, timeoutMs = 30000 } = {}) {
  const url = buildUrl(path, query);
  const response = await fetch(url, {
    method,
    headers: buildDefaultHeaders({
      ...(body ? { "Content-Type": "application/json" } : {}),
      ...headers
    }),
    body: body ? JSON.stringify(body) : undefined,
    signal: AbortSignal.timeout(timeoutMs)
  });

  const text = await response.text();
  const parsed = tryParseJson(text);

  if (!response.ok) {
    const detail = typeof parsed === "string" ? parsed : JSON.stringify(parsed);
    throw new Error(`HTTP ${response.status} ${response.statusText} for ${url.pathname}: ${detail}`);
  }

  return parsed;
}

export async function getJson(path, query = {}, options = {}) {
  return requestJson("GET", path, { query, ...options });
}
