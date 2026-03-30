import { parseArgs } from "node:util";
import { pathToFileURL } from "node:url";
import { cleanObject, toInteger } from "./runtime.mjs";

export const commonOptions = {
  product: { type: "string" },
  "instrument-id": { type: "string" },
  "exchange-id": { type: "string" },
  "instrument-name": { type: "string" },
  "sector-id": { type: "string" },
  "sector-name": { type: "string" },
  query: { type: "string" },
  "target-date": { type: "string" },
  "target-time": { type: "string" },
  "visual-days-len": { type: "string" }
};

export function parseCommonArgs({ allowPositionals = false, options = {} } = {}) {
  return parseArgs({
    allowPositionals,
    options: {
      ...commonOptions,
      ...options
    },
    strict: true
  });
}

// Public model-facing stock identifier modes:
// 1. instrument-name
// 2. instrument-id + exchange-id
export function buildInstrumentQuery(values) {
  return cleanObject({
    instrument_id: values["instrument-id"],
    exchange_id: values["exchange-id"],
    instrument_name: values["instrument-name"]
  });
}

// Public model-facing sector inputs:
// 1. sector-name / sector-id for detail products
// 2. query for resolver products
export function buildSectorQuery(values) {
  return cleanObject({
    sector_id: values["sector-id"],
    sector_name: values["sector-name"],
    query: values.query
  });
}

// Keep the public date surface narrow.
// We always expose target_date (+ optional visual_days_len) and hide
// start_date/end_date/is_realtime from the model side.
export function buildWindowQuery(values) {
  const targetDate = values["target-date"];
  const visualDaysLen = toInteger(values["visual-days-len"]);
  return cleanObject({
    target_date: targetDate,
    visual_days_len: visualDaysLen,
    is_realtime: true
  });
}

export function buildCommonRequest(values) {
  return {
    ...buildInstrumentQuery(values),
    ...buildSectorQuery(values),
    ...buildWindowQuery(values),
    target_time: values["target-time"]
  };
}

function hasValue(value) {
  return value !== undefined && value !== null && value !== "";
}

function hasAny(query, keys) {
  return keys.some((key) => hasValue(query[key]));
}

export function assertNoFields(query, keys, message) {
  if (hasAny(query, keys)) {
    throw new Error(message);
  }
}

export function assertTargetDate(query, product) {
  if (!query.target_date) {
    throw new Error(`${product} requires --target-date.`);
  }
}

export function assertSingleInstrumentInput(query) {
  const hasName = Boolean(query.instrument_name);
  const hasPair = Boolean(query.instrument_id && query.exchange_id);
  const hasPartialPair = Boolean(query.instrument_id || query.exchange_id);

  if (hasName && hasPair) {
    throw new Error("Use either --instrument-name, or both --instrument-id and --exchange-id. Do not mix both input modes. If the code is unknown, prefer --instrument-name.");
  }

  if (hasPartialPair && !hasPair) {
    throw new Error("When using instrument code mode, provide both --instrument-id and --exchange-id. If the code is unknown, prefer --instrument-name.");
  }

  if (!hasName && !hasPair) {
    throw new Error("Provide either --instrument-name, or both --instrument-id and --exchange-id. If the code is unknown, prefer --instrument-name.");
  }

  if (query.exchange_id && !["SSE", "SZE"].includes(query.exchange_id)) {
    throw new Error("When using instrument code mode, --exchange-id must be SSE or SZE.");
  }
}

export function assertSingleSectorInput(query) {
  const hasName = Boolean(query.sector_name);
  const hasId = Boolean(query.sector_id);

  if (hasName && hasId) {
    throw new Error("Use either --sector-name or --sector-id. Do not mix both input modes. Prefer --sector-name unless a resolved --sector-id was already returned by the backend.");
  }

  if (!hasName && !hasId) {
    throw new Error("Provide either --sector-name or --sector-id. Prefer --sector-name unless a resolved --sector-id was already returned by the backend.");
  }
}

export function printJson(data) {
  process.stdout.write(`${JSON.stringify(data, null, 2)}\n`);
}

export function isMain(importMeta) {
  if (!process.argv[1]) {
    return false;
  }
  return importMeta.url === pathToFileURL(process.argv[1]).href;
}
