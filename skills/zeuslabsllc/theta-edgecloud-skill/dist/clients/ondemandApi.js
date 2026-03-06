import { getJson, postJson } from './http.js';
const BASE = 'https://ondemand.thetaedgecloud.com';
function h(cfg) {
    if (!cfg.onDemandApiToken)
        throw new Error('THETA_ONDEMAND_API_TOKEN missing');
    return {
        Authorization: `Bearer ${cfg.onDemandApiToken}`,
        'content-type': 'application/json'
    };
}
function net(cfg) {
    return {
        headers: h(cfg),
        service: 'theta-ondemand-api',
        timeoutMs: cfg.httpTimeoutMs,
        maxRetries: cfg.httpMaxRetries,
        retryBackoffMs: cfg.httpRetryBackoffMs
    };
}
export const onDemandApiClient = {
    listServices: () => getJson(`${BASE}/service/list?expand=template_id`, {
        service: 'theta-ondemand-api',
        timeoutMs: 20000,
        maxRetries: 2,
        retryBackoffMs: 250
    }),
    createInferRequest: (cfg, service, payload) => {
        const body = payload && typeof payload === 'object' && Object.prototype.hasOwnProperty.call(payload, 'input')
            ? payload
            : { input: payload };
        return postJson(`${BASE}/infer_request/${service}`, body, net(cfg));
    },
    getInferRequest: (cfg, requestId) => getJson(`${BASE}/infer_request/${requestId}`, net(cfg)),
    createInputPresignedUrls: (cfg, service) => postJson(`${BASE}/infer_request/${service}/input_presigned_urls`, {}, net(cfg))
};
