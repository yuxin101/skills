const TRUE_VALUES = new Set(["1", "true", "yes", "y", "on"]);
const FALSE_VALUES = new Set(["0", "false", "no", "n", "off"]);
const FIXED_BASE_URL = "https://tianshan-api.kungfu-trader.com";

export function getEnv(name, { required = false, defaultValue = undefined } = {}) {
  const value = process.env[name];
  if (value === undefined || value === null || value === "") {
    if (required) {
      throw new Error(`Missing required environment variable: ${name}`);
    }
    return defaultValue;
  }
  return value;
}

export function getBaseUrl() {
  return FIXED_BASE_URL;
}

export function cleanObject(input) {
  return Object.fromEntries(
    Object.entries(input).filter(([, value]) => value !== undefined && value !== null && value !== "")
  );
}

export function toInteger(value) {
  if (value === undefined || value === null || value === "") {
    return undefined;
  }
  const parsed = Number.parseInt(String(value), 10);
  if (Number.isNaN(parsed)) {
    throw new Error(`Expected integer, got: ${value}`);
  }
  return parsed;
}

export function toBoolean(value) {
  if (value === undefined || value === null || value === "") {
    return undefined;
  }
  const normalized = String(value).trim().toLowerCase();
  if (TRUE_VALUES.has(normalized)) {
    return true;
  }
  if (FALSE_VALUES.has(normalized)) {
    return false;
  }
  throw new Error(`Expected boolean-like value, got: ${value}`);
}

export function buildDefaultHeaders(extraHeaders = {}) {
  return {
    Accept: "application/json",
    ...extraHeaders
  };
}
