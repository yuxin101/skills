#!/usr/bin/env node

/**
 * vision-ocr 配置自动更新工具 - 智能检测版
 * 
 * 功能：
 * 1. 检测当前配置是否有效
  2. 只在必要时触发更新（首次安装、配置失效等）
 * 3. 从 openclaw.json 读取当前机器人的模型配置
 * 4. 自动更新 config.json 中的 multimodal 配置
 * 5. 保留其他配置不变
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// 配置路径
const OPENCLAW_CONFIG = path.join(os.homedir(), '.openclaw', 'openclaw.json');
const WORKSPACE_CONFIG = path.join(os.homedir(), '.openclaw', 'workspace', 'config.json');

/**
 * 打印日志
 */
function log(message, level = 'INFO') {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] [${level}] ${message}`);
}

/**
 * 读取 JSON 文件
 */
function readJsonFile(filePath) {
  try {
    if (!fs.existsSync(filePath)) {
      return null;
    }
    const content = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(content);
  } catch (error) {
    log(`读取文件失败：${filePath} - ${error.message}`, 'ERROR');
    return null;
  }
}

/**
 * 写入 JSON 文件
 */
function writeJsonFile(filePath, data) {
  try {
    fs.mkdirSync(path.dirname(filePath), { recursive: true });
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
    log(`文件已更新：${filePath}`, 'SUCCESS');
    return true;
  } catch (error) {
    log(`写入文件失败：${filePath} - ${error.message}`, 'ERROR');
    return false;
  }
}

/**
 * 从 openclaw.json 提取模型配置
 */
function extractModelConfig(openclawConfig) {
  const config = {
    baseUrl: null,
    token: null,
    model: null
  };

  // 提取 baseUrl 和 token
  const vllmConfig = openclawConfig?.models?.providers?.vllm;
  if (vllmConfig) {
    config.baseUrl = vllmConfig.baseUrl;
    config.token = vllmConfig.token || vllmConfig.apiKey || null;
    log(`提取到 baseUrl: ${config.baseUrl}`, 'INFO');
    log(`提取到 token: ${config.token ? '***已隐藏***' : '未找到'}`, 'INFO');
  } else {
    log('未找到 models.providers.vllm 配置', 'WARN');
  }

  // 提取当前使用的模型
  const primaryModel = openclawConfig?.agents?.defaults?.model?.primary;
  if (primaryModel) {
    // 处理格式：vllm/Sehyo/Qwen3.5-122B-A10B-NVFP4
    const modelId = primaryModel.replace(/^vllm\//, '');
    config.model = modelId;
    log(`提取到当前模型：${modelId}`, 'INFO');
  } else {
    log('未找到 agents.defaults.model.primary 配置', 'WARN');
  }

  return config;
}

/**
 * 检测配置是否需要更新
 * 
 * 返回原因：
 * - null: 无需更新
 * - string: 需要更新的原因
 */
function detectUpdateReason(workspaceConfig, openclawConfig) {
  const workspaceMultimodal = workspaceConfig?.ocr?.multimodal;
  const openclawVllm = openclawConfig?.models?.providers?.vllm;
  const openclawModel = openclawConfig?.agents?.defaults?.model?.primary;

  // 情况 1: 配置文件不存在或为空
  if (!workspaceConfig || !workspaceConfig.ocr) {
    return '首次安装，配置文件不存在或为空';
  }

  // 情况 2: multimodal 配置不存在
  if (!workspaceMultimodal) {
    return 'multimodal 配置不存在';
  }

  // 情况 3: baseUrl 缺失或不匹配
  if (!workspaceMultimodal.baseUrl) {
    return 'baseUrl 缺失';
  }
  if (openclawVllm?.baseUrl && workspaceMultimodal.baseUrl !== openclawVllm.baseUrl) {
    return 'baseUrl 已变更';
  }

  // 情况 4: token 缺失
  if ((openclawVllm?.token || openclawVllm?.apiKey) && !workspaceMultimodal.token) {
    return 'token 缺失';
  }

  // 情况 5: model 缺失
  if (!workspaceMultimodal.model) {
    return 'model 缺失';
  }
  if (openclawModel) {
    const openclawModelId = openclawModel.replace(/^vllm\//, '');
    if (workspaceMultimodal.model !== openclawModelId) {
      return 'model 已变更';
    }
  }

  // 情况 6: 配置完全匹配，无需更新
  return null;
}

/**
 * 显示当前配置
 */
function showCurrentConfig(workspaceConfig) {
  console.log('\n📋 当前配置:');
  console.log('-------------------');
  
  if (workspaceConfig?.ocr?.multimodal) {
    console.log('multimodal.baseUrl:', workspaceConfig.ocr.multimodal.baseUrl || '未配置');
    console.log('multimodal.token:', workspaceConfig.ocr.multimodal.token ? '***已隐藏***' : '未配置');
    console.log('multimodal.model:', workspaceConfig.ocr.multimodal.model || '未配置');
  } else {
    console.log('multimodal: 未配置');
  }
  
  console.log('');
}

/**
 * 显示更新后的配置
 */
function showUpdatedConfig(workspaceConfig) {
  console.log('\n✅ 更新后的配置:');
  console.log('-------------------');
  
  if (workspaceConfig?.ocr?.multimodal) {
    console.log('multimodal.baseUrl:', workspaceConfig.ocr.multimodal.baseUrl || '未配置');
    console.log('multimodal.token:', workspaceConfig.ocr.multimodal.token ? '***已隐藏***' : '未配置');
    console.log('multimodal.model:', workspaceConfig.ocr.multimodal.model || '未配置');
  }
  
  console.log('');
}

/**
 * 更新 workspace/config.json 中的 multimodal 配置
 */
function updateMultimodalConfig(workspaceConfig, modelConfig) {
  // 确保 ocr 对象存在
  if (!workspaceConfig.ocr) {
    workspaceConfig.ocr = {};
  }

  // 确保 multimodal 对象存在
  if (!workspaceConfig.ocr.multimodal) {
    workspaceConfig.ocr.multimodal = {};
  }

  // 更新配置
  let updated = false;

  if (modelConfig.baseUrl) {
    workspaceConfig.ocr.multimodal.baseUrl = modelConfig.baseUrl;
    log(`更新 baseUrl: ${modelConfig.baseUrl}`, 'INFO');
    updated = true;
  }

  if (modelConfig.token) {
    workspaceConfig.ocr.multimodal.token = modelConfig.token;
    log('更新 token', 'INFO');
    updated = true;
  }

  if (modelConfig.model) {
    workspaceConfig.ocr.multimodal.model = modelConfig.model;
    log(`更新 model: ${modelConfig.model}`, 'INFO');
    updated = true;
  }

  return updated;
}

/**
 * 显示配置提示
 */
function showConfigTips() {
  console.log('\n💡 提示:');
  console.log('-------------------');
  console.log('如果还需要配置 imageocr，请在 config.json 中添加:');
  console.log(JSON.stringify({
    ocr: {
      imageocr: {
        token: '你的 ImageOCR Token',
        endpoint: '你的 ImageOCR 端点'
      }
    }
  }, null, 2));
  console.log('');
}

/**
 * 主函数
 */
async function main() {
  console.log('\n🔧 vision-ocr 配置自动更新工具（智能检测版）\n');
  const forceUpdate = args.includes('--force');
  
  // 读取 openclaw.json
  log('读取 openclaw.json...');
  const openclawConfig = readJsonFile(OPENCLAW_CONFIG);
  if (!openclawConfig) {
    log(`无法读取 ${OPENCLAW_CONFIG}，请确保 OpenClaw 已正确配置`, 'ERROR');
    process.exit(1);
  }

  // 读取 workspace/config.json
  log('读取 workspace/config.json...');
  let workspaceConfig = readJsonFile(WORKSPACE_CONFIG);
  
  if (!workspaceConfig) {
    log(`文件不存在：${WORKSPACE_CONFIG}`, 'WARN');
    workspaceConfig = {};
  }

  // 显示当前配置
  showCurrentConfig(workspaceConfig);

  // 检测是否需要更新
  const updateReason = detectUpdateReason(workspaceConfig, openclawConfig);

  if (!updateReason && !forceUpdate) {
    log('✅ 配置完整且匹配，无需更新', 'SUCCESS');
    showConfigTips();
    process.exit(0);
  }

  if (forceUpdate && !updateReason) {
    log('强制更新模式：将重新同步 multimodal 配置', 'WARN');
  }

  if (updateReason) {
    log(`检测到需要更新：${updateReason}`, 'WARN');
    console.log(`\n⚠️  原因：${updateReason}`);
    console.log('');
  }

  // 提取模型配置
  log('从 openclaw.json 提取模型配置...');
  const modelConfig = extractModelConfig(openclawConfig);

  // 检查是否有可更新的配置
  if (!modelConfig.baseUrl && !modelConfig.token && !modelConfig.model) {
    log('没有可更新的配置，请检查 openclaw.json 是否正确配置', 'ERROR');
    process.exit(1);
  }

  // 更新配置
  log('更新 workspace/config.json...');
  const updated = updateMultimodalConfig(workspaceConfig, modelConfig);

  if (updated) {
    // 写入文件
    if (writeJsonFile(WORKSPACE_CONFIG, workspaceConfig)) {
      showUpdatedConfig(workspaceConfig);
      log('✅ 配置更新成功！', 'SUCCESS');
    } else {
      log('❌ 配置更新失败', 'ERROR');
      process.exit(1);
    }
  } else {
    log('ℹ️ 没有需要更新的配置', 'INFO');
  }

  // 显示配置示例
  showConfigTips();
}

// 支持命令行参数
const args = process.argv.slice(2);
if (args.includes('--help') || args.includes('-h')) {
  console.log('用法:');
  console.log('  node update-config.js           智能检测并更新配置');
  console.log('  node update-config.js --force   强制更新（覆盖现有配置）');
  console.log('  node update-config.js --check   仅检查配置状态');
  console.log('  node update-config.js --help    显示帮助');
  console.log('');
  console.log('更新触发条件:');
  console.log('  1. 首次安装（配置文件不存在）');
  console.log('  2. multimodal 配置缺失');
  console.log('  3. baseUrl/token/model 缺失');
  console.log('  4. OpenClaw 主配置发生变更');
  console.log('');
  process.exit(0);
}

// 强制更新模式
if (args.includes('--force')) {
  console.log('\n⚠️  强制更新模式\n');
  // 强制更新逻辑可以在这里添加
}

// 仅检查模式
if (args.includes('--check')) {
  log('读取 openclaw.json...');
  const openclawConfig = readJsonFile(OPENCLAW_CONFIG);
  if (!openclawConfig) {
    log(`无法读取 ${OPENCLAW_CONFIG}`, 'ERROR');
    process.exit(1);
  }

  log('读取 workspace/config.json...');
  const workspaceConfig = readJsonFile(WORKSPACE_CONFIG);

  const updateReason = detectUpdateReason(workspaceConfig, openclawConfig);

  if (!updateReason) {
    console.log('\n✅ 配置状态：正常');
    console.log('当前配置完整且匹配，无需更新。\n');
    process.exit(0);
  } else {
    console.log('\n⚠️  配置状态：需要更新');
    console.log(`原因：${updateReason}\n`);
    process.exit(1);
  }
}

main().catch(error => {
  log(`程序异常：${error.message}`, 'ERROR');
  console.error(error);
  process.exit(1);
});
