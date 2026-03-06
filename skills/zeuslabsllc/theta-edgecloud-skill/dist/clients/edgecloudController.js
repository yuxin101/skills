import { deleteEmpty, getJson, postJson, putEmpty } from './http.js';
const BASE_CTRL = 'https://controller.thetaedgecloud.com';
const BASE_API = 'https://api.thetaedgecloud.com';
function k(cfg) {
    if (!cfg.edgecloudApiKey)
        throw new Error('THETA_EC_API_KEY missing. In thetaedgecloud.com go to Account -> Projects -> select project -> Create API Key.');
    return { 'x-api-key': cfg.edgecloudApiKey };
}
function net(cfg, service, headers) {
    return {
        service,
        headers,
        timeoutMs: cfg.httpTimeoutMs,
        maxRetries: cfg.httpMaxRetries,
        retryBackoffMs: cfg.httpRetryBackoffMs
    };
}
export const edgecloudControllerClient = {
    listStandardTemplates: (cfg, category) => getJson(`${BASE_CTRL}/deployment_template/list_standard_templates?category=${category}`, net(cfg, 'edgecloud-controller', k(cfg))),
    listCustomTemplates: (cfg, projectId) => getJson(`${BASE_CTRL}/deployment_template/list_custom_templates?project_id=${projectId}`, net(cfg, 'edgecloud-controller', k(cfg))),
    listVmTypes: (cfg) => getJson(`${BASE_API}/resource/vm/list`, net(cfg, 'edgecloud-controller')),
    getBalance: (cfg, orgId) => {
        if (!orgId)
            throw new Error('orgId is required (set THETA_ORG_ID or pass args.orgId)');
        return getJson(`${BASE_API}/balance?orgID=${orgId}`, net(cfg, 'edgecloud-controller', k(cfg)));
    },
    createDeployment: (cfg, payload) => postJson(`${BASE_CTRL}/deployment`, payload, net(cfg, 'edgecloud-controller', k(cfg))),
    listDeployments: (cfg, projectId) => getJson(`${BASE_CTRL}/deployment/list?project_id=${projectId}`, net(cfg, 'edgecloud-controller', k(cfg))),
    listJupyterNotebooks: (cfg, projectId) => getJson(`${BASE_CTRL}/deployment/list?project_id=${projectId}&template_name=Jupyter%20Notebook`, net(cfg, 'edgecloud-controller', k(cfg))),
    listGpuNodes: (cfg, projectId) => getJson(`${BASE_CTRL}/deployment/list?project_id=${projectId}&template_name=GPU%20Node`, net(cfg, 'edgecloud-controller', k(cfg))),
    listDedicatedDeployments: (cfg, projectId) => getJson(`${BASE_CTRL}/deployment/list?project_id=${projectId}&not_template_name=Jupyter%20Notebook&not_template_name=GPU%20Node`, net(cfg, 'edgecloud-controller', k(cfg))),
    listClusters: (cfg, projectId) => getJson(`${BASE_CTRL}/cluster/list?project_id=${projectId}`, net(cfg, 'edgecloud-controller', k(cfg))),
    listStorageClaims: (cfg, projectId, page = 1, number = 20) => getJson(`${BASE_CTRL}/volume/claim?projectId=${projectId}&page=${page}&number=${number}`, net(cfg, 'edgecloud-controller', k(cfg))),
    listChatbots: (cfg, projectId) => getJson(`${BASE_CTRL}/chatbot/list?project_id=${projectId}&number=100`, net(cfg, 'edgecloud-controller', k(cfg))),
    stopDeployment: (cfg, projectId, shard, suffix) => putEmpty(`${BASE_CTRL}/deployment/${shard}/${suffix}/stop?project_id=${projectId}`, net(cfg, 'edgecloud-controller', k(cfg))),
    deleteDeployment: (cfg, projectId, shard, suffix) => deleteEmpty(`${BASE_CTRL}/deployment/${shard}/${suffix}?project_id=${projectId}`, net(cfg, 'edgecloud-controller', k(cfg)))
};
