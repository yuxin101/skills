import { getJson, postJson } from './http.js';
import { fromConfigError } from '../errors.js';
const BASE = 'https://ondemand.thetaedgecloud.com';
function onDemandBearerHeaders(cfg) {
    if (!cfg.onDemandApiToken)
        throw fromConfigError('THETA_ONDEMAND_API_TOKEN missing', 'MISSING_THETA_ONDEMAND_API_TOKEN');
    return {
        Authorization: `Bearer ${cfg.onDemandApiToken}`
    };
}
function segment(value, field, code) {
    if (value === undefined || value === null)
        throw fromConfigError(`${field} is required`, code);
    const raw = String(value).trim();
    if (!raw)
        throw fromConfigError(`${field} is required`, code);
    return encodeURIComponent(raw);
}
function net(cfg) {
    return {
        headers: onDemandBearerHeaders(cfg),
        service: 'theta-ondemand-api',
        timeoutMs: cfg.httpTimeoutMs,
        maxRetries: cfg.httpMaxRetries,
        retryBackoffMs: cfg.httpRetryBackoffMs
    };
}
export const onDemandApiClient = {
    listServices: (cfg) => getJson(`${BASE}/service/list?expand=template_id`, {
        service: 'theta-ondemand-api',
        timeoutMs: cfg?.httpTimeoutMs ?? 20000,
        maxRetries: cfg?.httpMaxRetries ?? 2,
        retryBackoffMs: cfg?.httpRetryBackoffMs ?? 250
    }),
    createInferRequest: (cfg, service, payload) => {
        const body = payload && typeof payload === 'object' && Object.prototype.hasOwnProperty.call(payload, 'input')
            ? payload
            : { input: payload };
        if (body?.input && typeof body.input === 'object' && body.input !== null && !Object.prototype.hasOwnProperty.call(body.input, 'stream') && Array.isArray(body.input.messages)) {
            body.input = { ...body.input, stream: false };
        }
        return postJson(`${BASE}/infer_request/${segment(service, 'service', 'INVALID_ONDEMAND_SERVICE')}`, body, net(cfg));
    },
    getInferRequest: (cfg, requestId) => getJson(`${BASE}/infer_request/${segment(requestId, 'requestId', 'INVALID_ONDEMAND_REQUEST_ID')}`, net(cfg)),
    createInputPresignedUrls: (cfg, service) => postJson(`${BASE}/infer_request/${segment(service, 'service', 'INVALID_ONDEMAND_SERVICE')}/input_presigned_urls`, {}, net(cfg))
};
