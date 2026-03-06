import { loadConfig } from '../config.js';
import { deployments } from '../commands/deployments.js';
import { healthCheck } from '../commands/health.js';
import { inference } from '../commands/inference.js';
import { ondemand } from '../commands/ondemand.js';
import { video } from '../commands/video.js';
import { resolveThetaInferenceAuth, resolveThetaOnDemandToken } from './secretResolver.js';
function coerceBool(value, fallback) {
    if (value === undefined)
        return fallback;
    const normalized = value.trim().toLowerCase();
    if (['1', 'true', 'yes', 'on'].includes(normalized))
        return true;
    if (['0', 'false', 'no', 'off'].includes(normalized))
        return false;
    return fallback;
}
function coerceInt(value, fallback, min, max) {
    if (!value)
        return fallback;
    const parsed = Number.parseInt(value, 10);
    if (!Number.isFinite(parsed))
        return fallback;
    return Math.min(Math.max(parsed, min), max);
}
async function buildRuntimeConfig(ctx) {
    const base = loadConfig();
    const env = ctx.env ?? {};
    const onDemandApiToken = await resolveThetaOnDemandToken(ctx, base.onDemandApiToken);
    const inferenceAuth = await resolveThetaInferenceAuth(ctx, base.inferenceAuth);
    return {
        ...base,
        dryRun: coerceBool(env.THETA_DRY_RUN, base.dryRun),
        edgecloudApiKey: env.THETA_EC_API_KEY ?? base.edgecloudApiKey,
        edgecloudProjectId: env.THETA_EC_PROJECT_ID ?? base.edgecloudProjectId,
        edgecloudOrgId: env.THETA_ORG_ID ?? base.edgecloudOrgId,
        videoSaId: env.THETA_VIDEO_SA_ID ?? base.videoSaId,
        videoSaSecret: env.THETA_VIDEO_SA_SECRET ?? base.videoSaSecret,
        inferenceEndpoint: env.THETA_INFERENCE_ENDPOINT ?? base.inferenceEndpoint,
        inferenceAuth,
        onDemandApiToken,
        httpTimeoutMs: coerceInt(env.THETA_HTTP_TIMEOUT_MS, base.httpTimeoutMs, 1000, 120000),
        httpMaxRetries: coerceInt(env.THETA_HTTP_MAX_RETRIES, base.httpMaxRetries, 0, 6),
        httpRetryBackoffMs: coerceInt(env.THETA_HTTP_RETRY_BACKOFF_MS, base.httpRetryBackoffMs, 25, 10000)
    };
}
function requireFields(args, fields) {
    for (const field of fields) {
        if (!(field in args) || args[field] === undefined || args[field] === null || args[field] === '') {
            throw new Error(`Missing required field: ${field}`);
        }
    }
}
function resolveProjectId(cfg, args) {
    const projectId = args?.projectId ?? cfg.edgecloudProjectId;
    if (!projectId)
        throw new Error('projectId missing. Set THETA_EC_PROJECT_ID or pass args.projectId. Find it in thetaedgecloud.com -> Account -> Projects (prj_...).');
    return projectId;
}
function summarizeError(error) {
    let message;
    if (error instanceof Error) {
        message = error.message;
    }
    else if (error && typeof error === 'object') {
        const asObj = error;
        message = asObj.message ? String(asObj.message) : JSON.stringify(asObj);
    }
    else {
        message = String(error);
    }
    return message.length > 220 ? `${message.slice(0, 220)}…` : message;
}
async function probeCapability(name, probe, required, notes = undefined) {
    try {
        const result = await probe();
        return { name, configured: true, verified: true, required, notes, sample: result ? { keys: Object.keys(result).slice(0, 8) } : undefined };
    }
    catch (error) {
        return { name, configured: true, verified: false, required, notes, error: summarizeError(error) };
    }
}
async function authCapabilities(cfg, args = {}) {
    const endpoint = args.endpoint;
    const overrideOrgId = args.orgId;
    const caps = [];
    const controllerConfigured = Boolean(cfg.edgecloudApiKey && cfg.edgecloudProjectId);
    if (!controllerConfigured) {
        caps.push({
            name: 'controller.project',
            configured: false,
            verified: false,
            required: ['THETA_EC_API_KEY', 'THETA_EC_PROJECT_ID'],
            notes: 'Project-scoped controller APIs (deployments/templates/cluster/storage/chatbot listings).'
        });
    }
    else {
        caps.push(await probeCapability('controller.project', () => deployments.listVm(cfg), ['THETA_EC_API_KEY', 'THETA_EC_PROJECT_ID'], 'Project-scoped controller APIs.'));
    }
    const balanceOrgId = overrideOrgId ?? cfg.edgecloudOrgId;
    if (!controllerConfigured || !balanceOrgId) {
        caps.push({
            name: 'billing.balance',
            configured: false,
            verified: false,
            required: ['THETA_EC_API_KEY', 'THETA_ORG_ID'],
            notes: 'Org credit balance lookup.'
        });
    }
    else {
        caps.push(await probeCapability('billing.balance', () => deployments.balance(cfg, balanceOrgId), ['THETA_EC_API_KEY', 'THETA_ORG_ID'], 'Org credit balance lookup.'));
    }
    caps.push(await probeCapability('ondemand.catalog', () => ondemand.listServices(), [], 'Public on-demand model catalog.'));
    if (!cfg.onDemandApiToken) {
        caps.push({
            name: 'ondemand.inference',
            configured: false,
            verified: false,
            required: ['THETA_ONDEMAND_API_TOKEN or THETA_ONDEMAND_API_KEY'],
            notes: 'On-demand infer/status/poll commands.'
        });
    }
    else {
        try {
            await ondemand.status(cfg, 'infr_rqst_capability_probe_invalid');
            caps.push({
                name: 'ondemand.inference',
                configured: true,
                verified: true,
                required: ['THETA_ONDEMAND_API_TOKEN or THETA_ONDEMAND_API_KEY'],
                notes: 'On-demand infer/status/poll commands.'
            });
        }
        catch (error) {
            const message = summarizeError(error).toLowerCase();
            const maybeAuthorizedNotFound = message.includes('not found') || message.includes('404') || message.includes('invalid request');
            caps.push({
                name: 'ondemand.inference',
                configured: true,
                verified: maybeAuthorizedNotFound,
                required: ['THETA_ONDEMAND_API_TOKEN or THETA_ONDEMAND_API_KEY'],
                notes: 'Auth probe uses invalid requestId; not-found responses indicate token accepted.',
                error: maybeAuthorizedNotFound ? undefined : summarizeError(error)
            });
        }
    }
    const infEndpoint = endpoint ?? cfg.inferenceEndpoint;
    if (!infEndpoint) {
        caps.push({
            name: 'inference.endpoint',
            configured: false,
            verified: false,
            required: ['THETA_INFERENCE_ENDPOINT', 'THETA_INFERENCE_AUTH_TOKEN or THETA_INFERENCE_AUTH_USER/PASS'],
            notes: 'Dedicated endpoint model/chat commands.'
        });
    }
    else {
        caps.push(await probeCapability('inference.endpoint', () => inference.models(cfg, infEndpoint), ['THETA_INFERENCE_ENDPOINT', 'THETA_INFERENCE_AUTH_TOKEN or THETA_INFERENCE_AUTH_USER/PASS'], 'Dedicated endpoint model/chat commands.'));
    }
    if (!cfg.videoSaId || !cfg.videoSaSecret) {
        caps.push({
            name: 'video.api',
            configured: false,
            verified: false,
            required: ['THETA_VIDEO_SA_ID', 'THETA_VIDEO_SA_SECRET'],
            notes: 'Video service commands.'
        });
    }
    else {
        caps.push(await probeCapability('video.api', () => video.videoList(cfg, cfg.videoSaId, 1, 1), ['THETA_VIDEO_SA_ID', 'THETA_VIDEO_SA_SECRET'], 'Video service commands.'));
    }
    return {
        mode: 'api-key-first',
        dryRun: cfg.dryRun,
        timestamp: new Date().toISOString(),
        capabilities: caps,
        summary: {
            configured: caps.filter((c) => c.configured).length,
            verified: caps.filter((c) => c.verified).length,
            total: caps.length
        }
    };
}
const commandRegistry = {
    'theta.health': {
        schema: { command: 'theta.health', description: 'EdgeCloud health check via controller VM listing', required: [] },
        handler: (cfg) => healthCheck(cfg)
    },
    'theta.auth.capabilities': {
        schema: { command: 'theta.auth.capabilities', description: 'Return command-family capabilities for current credential set', required: [] },
        handler: (cfg, args) => authCapabilities(cfg, args)
    },
    'theta.setup': {
        schema: { command: 'theta.setup', description: 'Show first-run setup checklist and where to create Theta API keys', required: [] },
        handler: () => ({
            mode: 'api-key-first',
            checklist: [
                'Log in at https://www.thetaedgecloud.com/',
                'Go to Account -> Projects and select your project.',
                'Click Create API Key and copy the project API key.',
                'Set THETA_EC_API_KEY and THETA_EC_PROJECT_ID in OpenClaw.',
                'Optional: for on-demand image/video infer, create On-demand API key/token and set THETA_ONDEMAND_API_KEY (or THETA_ONDEMAND_API_TOKEN).',
                'Run theta.auth.capabilities to verify configured command families.'
            ],
            env: {
                baselineRequired: ['THETA_EC_API_KEY', 'THETA_EC_PROJECT_ID'],
                optionalByFeature: {
                    billing: ['THETA_ORG_ID'],
                    ondemand: ['THETA_ONDEMAND_API_KEY or THETA_ONDEMAND_API_TOKEN'],
                    dedicatedInference: ['THETA_INFERENCE_ENDPOINT', 'THETA_INFERENCE_AUTH_TOKEN or THETA_INFERENCE_AUTH_USER/PASS'],
                    video: ['THETA_VIDEO_SA_ID', 'THETA_VIDEO_SA_SECRET']
                }
            },
            links: {
                thetaDashboard: 'https://www.thetaedgecloud.com/',
                apiKeyDoc: 'https://docs.thetatoken.org/docs/edgecloud-api-keys'
            }
        })
    },
    'theta.inference.models': {
        schema: { command: 'theta.inference.models', description: 'List models from dedicated inference endpoint', required: [] },
        handler: (cfg, args) => inference.models(cfg, args.endpoint)
    },
    'theta.inference.chat': {
        schema: { command: 'theta.inference.chat', description: 'Run chat completion on dedicated inference endpoint', required: ['body'] },
        handler: (cfg, args) => inference.chat(cfg, args.body, args.endpoint)
    },
    'theta.ondemand.listServices': {
        schema: { command: 'theta.ondemand.listServices', description: 'List supported on-demand services', required: [] },
        handler: () => ondemand.listServices()
    },
    'theta.ondemand.infer': {
        schema: { command: 'theta.ondemand.infer', description: 'Create on-demand infer request', required: ['service', 'payload'] },
        handler: (cfg, args) => ondemand.infer(cfg, args.service, args.payload)
    },
    'theta.ondemand.status': {
        schema: { command: 'theta.ondemand.status', description: 'Get on-demand infer request status', required: ['requestId'] },
        handler: (cfg, args) => ondemand.status(cfg, args.requestId)
    },
    'theta.ondemand.inputPresignedUrls': {
        schema: { command: 'theta.ondemand.inputPresignedUrls', description: 'Create presigned URLs for on-demand inputs', required: ['service'] },
        handler: (cfg, args) => ondemand.inputPresignedUrls(cfg, args.service)
    },
    'theta.ondemand.pollUntilDone': {
        schema: { command: 'theta.ondemand.pollUntilDone', description: 'Poll on-demand request until terminal state', required: ['requestId'] },
        handler: (cfg, args) => ondemand.pollUntilDone(cfg, args.requestId, args.options)
    },
    'theta.deployments.list': {
        schema: { command: 'theta.deployments.list', description: 'List deployments for project', required: [] },
        handler: (cfg, args) => deployments.list(cfg, resolveProjectId(cfg, args))
    },
    'theta.deployments.listVm': {
        schema: { command: 'theta.deployments.listVm', description: 'List EdgeCloud VM types', required: [] },
        handler: (cfg) => deployments.listVm(cfg)
    },
    'theta.billing.balance': {
        schema: { command: 'theta.billing.balance', description: 'Get org credit balance (API key scoped)', required: [] },
        handler: (cfg, args) => deployments.balance(cfg, args.orgId)
    },
    'theta.deployments.listStandard': {
        schema: { command: 'theta.deployments.listStandard', description: 'List standard deployment templates by category', required: ['category'] },
        handler: (cfg, args) => deployments.listStandard(cfg, args.category)
    },
    'theta.deployments.listCustom': {
        schema: { command: 'theta.deployments.listCustom', description: 'List custom templates for project', required: [] },
        handler: (cfg, args) => deployments.listCustom(cfg, resolveProjectId(cfg, args))
    },
    'theta.ai.dedicatedDeployments.list': {
        schema: { command: 'theta.ai.dedicatedDeployments.list', description: 'List dedicated deployments for project', required: [] },
        handler: (cfg, args) => deployments.listDedicated(cfg, resolveProjectId(cfg, args))
    },
    'theta.ai.jupyter.list': {
        schema: { command: 'theta.ai.jupyter.list', description: 'List Jupyter notebook deployments', required: [] },
        handler: (cfg, args) => deployments.listJupyter(cfg, resolveProjectId(cfg, args))
    },
    'theta.ai.gpuNode.list': {
        schema: { command: 'theta.ai.gpuNode.list', description: 'List GPU node deployments', required: [] },
        handler: (cfg, args) => deployments.listGpuNodes(cfg, resolveProjectId(cfg, args))
    },
    'theta.ai.gpuCluster.list': {
        schema: { command: 'theta.ai.gpuCluster.list', description: 'List GPU clusters', required: [] },
        handler: (cfg, args) => deployments.listClusters(cfg, resolveProjectId(cfg, args))
    },
    'theta.ai.storage.list': {
        schema: { command: 'theta.ai.storage.list', description: 'List persistent storage claims', required: [] },
        handler: (cfg, args) => deployments.listStorageClaims(cfg, resolveProjectId(cfg, args), args.page ?? 1, args.number ?? 20)
    },
    'theta.ai.agent.list': {
        schema: { command: 'theta.ai.agent.list', description: 'List AI agent (RAG chatbot) resources', required: [] },
        handler: (cfg, args) => deployments.listChatbots(cfg, resolveProjectId(cfg, args))
    },
    'theta.video.list': {
        schema: { command: 'theta.video.list', description: 'List videos for service account', required: ['serviceAccountId'] },
        handler: (cfg, args) => video.videoList(cfg, args.serviceAccountId, args.page ?? 1, args.number ?? 10)
    },
};
const onDemandTokenCommands = new Set([
    'theta.ondemand.infer',
    'theta.ondemand.status',
    'theta.ondemand.inputPresignedUrls',
    'theta.ondemand.pollUntilDone'
]);
export const thetaRuntimeCommandSchemas = Object.fromEntries(Object.entries(commandRegistry).map(([cmd, reg]) => [cmd, reg.schema]));
export function listThetaRuntimeCommands() {
    return Object.keys(commandRegistry).sort();
}
export async function executeThetaRuntimeCommand(args, ctx = {}) {
    const registration = commandRegistry[args.command];
    if (!registration) {
        throw new Error(`Unsupported theta runtime command: ${args.command}`);
    }
    requireFields(args, registration.schema.required);
    const cfg = await buildRuntimeConfig(ctx);
    if (onDemandTokenCommands.has(args.command) && !cfg.dryRun && !cfg.onDemandApiToken) {
        throw new Error('On-demand API key/token missing. Set THETA_ONDEMAND_API_KEY (or THETA_ONDEMAND_API_TOKEN). You can create it from Theta dashboard under On-demand Model APIs -> API Key.');
    }
    return registration.handler(cfg, args);
}
