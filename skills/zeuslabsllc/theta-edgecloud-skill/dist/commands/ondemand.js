import { onDemandApiClient } from '../clients/ondemandApi.js';
import { sleep } from '../clients/http.js';
import { isStructuredError, summarizeError } from '../errors.js';
import { clampFiniteInt } from '../utils/integers.js';
import { listOnDemandServices, ONDEMAND_SERVICE_CATALOG } from './ondemandCatalog.js';
function getFirstInferRequest(payload) {
    if (!payload || typeof payload !== 'object')
        return undefined;
    const body = payload.body;
    if (!body?.infer_requests?.length)
        return undefined;
    return body.infer_requests[0];
}
function isTerminal(state) {
    return state === 'success' || state === 'error' || state === 'failed' || state === 'cancelled';
}
function withCatalogFallback(reason, warning) {
    return listOnDemandServices().map((s) => ({
        ...s,
        source: 'catalog',
        fallbackReason: reason,
        warning
    }));
}
export const ondemand = {
    catalog: ONDEMAND_SERVICE_CATALOG,
    listServices: async (cfg) => {
        try {
            const payload = await onDemandApiClient.listServices(cfg);
            const services = payload?.body?.services;
            if (Array.isArray(services) && services.length > 0) {
                return services
                    .map((s) => ({
                    name: s?.name ?? s?.alias ?? 'unknown',
                    service: s?.alias ?? s?.name ?? 'unknown',
                    templateId: s?.template_id,
                    workloadType: s?.workload_type,
                    rank: s?.rank,
                    source: 'live'
                }))
                    .sort((a, b) => (a.rank ?? 0) - (b.rank ?? 0));
            }
            return withCatalogFallback('live-empty', 'Live on-demand catalog returned no services; using embedded catalog fallback.');
        }
        catch (error) {
            if (isStructuredError(error) && error.code.startsWith('HTTP_')) {
                throw error;
            }
            return withCatalogFallback('network-or-parse-error', `Live on-demand catalog unavailable; using embedded catalog fallback (${summarizeError(error)}).`);
        }
    },
    infer: (cfg, service, payload) => cfg.dryRun ? { dryRun: true, service, payload } : onDemandApiClient.createInferRequest(cfg, service, payload),
    status: (cfg, requestId) => onDemandApiClient.getInferRequest(cfg, requestId),
    inputPresignedUrls: (cfg, service) => cfg.dryRun ? { dryRun: true, service } : onDemandApiClient.createInputPresignedUrls(cfg, service),
    pollUntilDone: async (cfg, requestId, opts = {}) => {
        if (!requestId)
            throw new Error('requestId is required');
        const intervalMs = clampFiniteInt(opts.intervalMs, 3000, 100, 60000);
        const timeoutMs = clampFiniteInt(opts.timeoutMs, 120000, 1000, 3600000);
        const maxAttempts = clampFiniteInt(opts.maxAttempts, 1000, 1, 20000);
        const startedAt = Date.now();
        let attempts = 0;
        let lastResult;
        while (attempts < maxAttempts) {
            const elapsedBeforeRequest = Date.now() - startedAt;
            if (elapsedBeforeRequest >= timeoutMs) {
                return {
                    attempts,
                    elapsedMs: elapsedBeforeRequest,
                    terminalState: 'timeout',
                    result: lastResult
                };
            }
            attempts += 1;
            const result = await onDemandApiClient.getInferRequest(cfg, requestId);
            lastResult = result;
            const inferRequest = getFirstInferRequest(result);
            if (isTerminal(inferRequest?.state)) {
                return {
                    attempts,
                    elapsedMs: Date.now() - startedAt,
                    terminalState: inferRequest?.state,
                    result
                };
            }
            const elapsedAfterRequest = Date.now() - startedAt;
            if (elapsedAfterRequest >= timeoutMs) {
                return {
                    attempts,
                    elapsedMs: elapsedAfterRequest,
                    terminalState: 'timeout',
                    result
                };
            }
            const sleepMs = Math.min(intervalMs, Math.max(0, timeoutMs - elapsedAfterRequest));
            if (sleepMs > 0) {
                await sleep(sleepMs);
            }
        }
        return {
            attempts,
            elapsedMs: Date.now() - startedAt,
            terminalState: 'max-attempts',
            result: lastResult
        };
    }
};
