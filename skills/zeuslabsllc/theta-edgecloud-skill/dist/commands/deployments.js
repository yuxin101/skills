import { edgecloudControllerClient } from '../clients/edgecloudController.js';
export const deployments = {
    listStandard: (cfg, category) => edgecloudControllerClient.listStandardTemplates(cfg, category),
    listCustom: (cfg, projectId) => edgecloudControllerClient.listCustomTemplates(cfg, projectId),
    listVm: (cfg) => edgecloudControllerClient.listVmTypes(cfg),
    balance: (cfg, orgId) => edgecloudControllerClient.getBalance(cfg, orgId ?? cfg.edgecloudOrgId),
    listJupyter: (cfg, projectId) => edgecloudControllerClient.listJupyterNotebooks(cfg, projectId),
    listGpuNodes: (cfg, projectId) => edgecloudControllerClient.listGpuNodes(cfg, projectId),
    listDedicated: (cfg, projectId) => edgecloudControllerClient.listDedicatedDeployments(cfg, projectId),
    listClusters: (cfg, projectId) => edgecloudControllerClient.listClusters(cfg, projectId),
    listStorageClaims: (cfg, projectId, page = 1, number = 20) => edgecloudControllerClient.listStorageClaims(cfg, projectId, page, number),
    listChatbots: (cfg, projectId) => edgecloudControllerClient.listChatbots(cfg, projectId),
    create: (cfg, payload) => cfg.dryRun ? { dryRun: true, payload } : edgecloudControllerClient.createDeployment(cfg, payload),
    list: (cfg, projectId) => edgecloudControllerClient.listDeployments(cfg, projectId),
    stop: (cfg, projectId, shard, suffix) => cfg.dryRun ? { dryRun: true } : edgecloudControllerClient.stopDeployment(cfg, projectId, shard, suffix),
    delete: (cfg, projectId, shard, suffix) => cfg.dryRun ? { dryRun: true } : edgecloudControllerClient.deleteDeployment(cfg, projectId, shard, suffix)
};
