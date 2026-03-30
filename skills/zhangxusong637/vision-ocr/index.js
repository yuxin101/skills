#!/usr/bin/env node

/**
 * 混合多模态 OCR 技能
 * 
 * 当前主流程：
 * 1. 图片默认按文档识别，先执行 OCR
 * 2. OCR 有效时，将 OCR Markdown 和原图一起交给多模态模型输出最终 Markdown
 * 3. OCR 无效时，切换为图片描述模式
 * 4. 结果默认发送到飞书，也可手动关闭
 * 
 * 配置：~/.openclaw/workspace/config.json
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const readline = require('readline/promises');
const { execFileSync } = require('child_process');

const DEBUG_ENABLED = /^(1|true)$/i.test(process.env.DEBUG || '');
const MAX_BASE64_CACHE_BYTES = 5 * 1024 * 1024;
const MAX_BASE64_CACHE_ENTRIES = 20;
const MAX_RESULT_CACHE_ENTRIES = 50;

// 性能统计
const performanceStats = {
  startTime: Date.now(),
  steps: []
};

// Base64 缓存（避免重复编码）
const base64Cache = new Map();

// 文件结果缓存（基于文件 hash）
const resultCache = new Map();

const multimodalModelCache = new Map();
const handwritingDetectionCache = new Map();

let preserveTempArtifacts = false;

function setLimitedCacheEntry(cache, key, value, maxEntries) {
  if (cache.has(key)) {
    cache.delete(key);
  }

  cache.set(key, value);

  if (cache.size > maxEntries) {
    const oldestKey = cache.keys().next().value;
    if (oldestKey !== undefined) {
      cache.delete(oldestKey);
    }
  }
}

function readBooleanEnv(name) {
  if (!(name in process.env)) {
    return undefined;
  }

  return /^(1|true|yes)$/i.test(process.env[name]);
}

function normalizeRecipientType(type) {
  const normalized = String(type || '').trim().toLowerCase();

  if (['chat', 'chat_id', 'group'].includes(normalized)) {
    return 'chat_id';
  }

  return 'open_id';
}

function buildFeishuTarget(type, id) {
  const normalizedType = normalizeRecipientType(type);
  const prefix = normalizedType === 'chat_id' ? 'chat' : 'open_id';
  return `${prefix}:${id}`;
}

function getRuntimeSessionRecipient() {
  const explicitId = process.env.VISION_SESSION_RECIPIENT_ID;
  const explicitType = process.env.VISION_SESSION_RECIPIENT_TYPE;

  if (explicitId) {
    return {
      id: explicitId,
      type: normalizeRecipientType(explicitType)
    };
  }

  if (process.env.VISION_SESSION_CHAT_ID) {
    return {
      id: process.env.VISION_SESSION_CHAT_ID,
      type: 'chat_id'
    };
  }

  if (process.env.VISION_SESSION_OPEN_ID) {
    return {
      id: process.env.VISION_SESSION_OPEN_ID,
      type: 'open_id'
    };
  }

  // 从 OpenClaw 运行时环境获取会话上下文
  if (process.env.OPENCLAW_CHAT_ID) {
    const chatId = process.env.OPENCLAW_CHAT_ID;
    // 判断是群聊还是私聊
    const isGroup = chatId.startsWith('chat:') || chatId.startsWith('oc_');
    const isPrivate = chatId.startsWith('user:') || chatId.startsWith('ou_');
    
    if (isPrivate) {
      // 提取 ID，保留原始格式
      let id = chatId;
      if (id.startsWith('user:')) {
        id = id.slice(5); // 去掉 user: 前缀
      }
      return {
        id: id,
        type: 'open_id'
      };
    } else if (isGroup) {
      return {
        id: chatId,
        type: 'chat_id'
      };
    }
  }

  if (process.env.OPENCLAW_SENDER_ID) {
    return {
      id: process.env.OPENCLAW_SENDER_ID,
      type: 'open_id'
    };
  }

  // 尝试从 OpenClaw 运行时获取当前会话信息（通过读取运行时文件）
  try {
    const runtimeInfoPath = path.join(os.homedir(), '.openclaw', 'runtime.json');
    if (fs.existsSync(runtimeInfoPath)) {
      const runtimeInfo = JSON.parse(fs.readFileSync(runtimeInfoPath, 'utf8'));
      if (runtimeInfo.senderId) {
        return {
          id: runtimeInfo.senderId,
          type: 'open_id'
        };
      }
      if (runtimeInfo.chatId) {
        const chatId = runtimeInfo.chatId;
        const isGroup = chatId.startsWith('chat:') || chatId.startsWith('oc_');
        const isPrivate = chatId.startsWith('user:') || chatId.startsWith('ou_');
        
        if (isPrivate) {
          let id = chatId;
          if (id.startsWith('user:')) {
            id = id.slice(5);
          }
          return {
            id: id,
            type: 'open_id'
          };
        } else if (isGroup) {
          return {
            id: chatId,
            type: 'chat_id'
          };
        }
      }
    }
  } catch (e) {
    log(`读取运行时信息失败：${e.message}`, 'DEBUG');
  }

  return null;
}

/**
 * 解析 --to 参数
 * 格式：--to "open_id:ou_xxx" 或 --to "chat:oc_xxx"
 */
function parseToArg() {
  const args = process.argv.slice(2);
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--to' && args[i + 1]) {
      const value = args[i + 1];
      return parseFeishuTarget(value);
    }
    if (args[i].startsWith('--to=')) {
      const value = args[i].split('=')[1];
      return parseFeishuTarget(value);
    }
  }
  return null;
}

/**
 * 解析飞书目标格式
 * 格式：open_id:ou_xxx 或 chat:oc_xxx
 */
function parseFeishuTarget(target) {
  if (!target) return null;
  
  if (target.startsWith('open_id:')) {
    return {
      id: target.slice(8),
      type: 'open_id'
    };
  }
  if (target.startsWith('chat:')) {
    return {
      id: target.slice(5),
      type: 'chat_id'
    };
  }
  // 默认当作 open_id
  return {
    id: target,
    type: 'open_id'
  };
}

/**
 * 计算文件 hash
 */
function calculateFileHash(filePath) {
  const crypto = require('crypto');
  const fileBuffer = fs.readFileSync(filePath);
  const hash = crypto.createHash('md5').update(fileBuffer).digest('hex');
  return hash;
}

/**
 * 从缓存获取结果
 */
function getCachedResult(filePath) {
  const hash = calculateFileHash(filePath);
  if (resultCache.has(hash)) {
    const cached = resultCache.get(hash);
    log(`使用缓存结果：${filePath} (hash: ${hash.substring(0, 8)}...)`, 'INFO');
    return cached;
  }
  return null;
}

/**
 * 保存结果到缓存
 */
function saveToCache(filePath, result) {
  const hash = calculateFileHash(filePath);
  setLimitedCacheEntry(resultCache, hash, result, MAX_RESULT_CACHE_ENTRIES);
  log(`结果已缓存：${filePath} (hash: ${hash.substring(0, 8)}...)`, 'DEBUG');
}

function calculateTextHash(content) {
  const crypto = require('crypto');
  return crypto.createHash('md5').update(String(content || '')).digest('hex');
}

/**
 * 根据文件扩展名判断类型（快速，无需 API 调用）
 */
function detectImageTypeByExtension(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const docExts = ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx'];
  const basename = path.basename(filePath).toLowerCase();
  
  if (docExts.includes(ext)) {
    return 'document';
  }

  if (/(screenshot|scan|invoice|receipt|contract|document|ocr|截图|扫描|发票|合同|文档)/.test(basename)) {
    return 'document';
  }

  return 'photo';
}

/**
 * 判断图片类型（可选，使用多模态 API）
 */
async function detectImageType(imageBase64, config) {
  log('正在判断图片类型...', 'INFO');
  
  const result = await callQwen(config.multimodal?.token, imageBase64, IMAGE_TYPE_PROMPT, false, null);
  
  if (result?.choices?.[0]?.message?.content) {
    const content = result.choices[0].message.content.toLowerCase();
    
    if (content.includes('类型 1') || content.includes('文档')) {
      log('判断结果：文档类（适合 OCR）', 'INFO');
      return 'document';
    } else if (content.includes('类型 2') || content.includes('照片') || content.includes('图片')) {
      log('判断结果：照片/图片类（适合多模态描述）', 'INFO');
      return 'photo';
    }
  }
  
  // 默认按文档处理
  log('判断失败，默认按文档类处理', 'WARN');
  return 'document';
}

/**
 * 打印日志
 */
function log(message, level = 'INFO') {
  if (level === 'DEBUG' && !DEBUG_ENABLED) {
    return;
  }

  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] [${level}] ${message}`);
}

/**
 * 读取文件并转换为 base64（带缓存）
 */
function readFileAsBase64(filePath) {
  try {
    // 检查缓存
    if (base64Cache.has(filePath)) {
      log(`使用 Base64 缓存：${filePath}`, 'DEBUG');
      return base64Cache.get(filePath);
    }
    
    // 读取并编码
    const fileStats = fs.statSync(filePath);
    const fileBuffer = fs.readFileSync(filePath);
    const base64 = fileBuffer.toString('base64');
    
    if (fileStats.size <= MAX_BASE64_CACHE_BYTES) {
      setLimitedCacheEntry(base64Cache, filePath, base64, MAX_BASE64_CACHE_ENTRIES);
      log(`Base64 编码完成（已缓存）: ${filePath}`, 'DEBUG');
    } else {
      log(`文件较大，跳过 Base64 缓存：${path.basename(filePath)}`, 'DEBUG');
    }
    
    return base64;
  } catch (error) {
    log(`读取文件失败：${error.message}`, 'ERROR');
    return null;
  }
}

/**
 * 结果质量验证
 */
function validateResult(content) {
  if (!content) return { valid: false, reason: '内容为空' };
  
  const normalized = content.trim();
  const lowered = normalized.toLowerCase();
  
  const checks = {
    minLength: normalized.length >= 20,
    hasText: /[\u4e00-\u9fffA-Za-z0-9]/.test(normalized),
    noError: !lowered.includes('error') && !normalized.includes('失败'),
    reasonableLength: normalized.length < 100000 // 防止异常长文本
  };
  
  const valid = Object.values(checks).every(v => v);
  
  if (!valid) {
    const failedChecks = Object.entries(checks)
      .filter(([_, v]) => !v)
      .map(([k]) => k);
    return { valid: false, reason: `验证失败：${failedChecks.join(', ')}` };
  }
  
  return { valid: true };
}

function sanitizeModelOutput(content) {
  if (typeof content !== 'string') {
    return content;
  }

  const normalized = content
    .replace(/^(?:\s*<image>\s*)+/i, '')
    .replace(/^(?:\s*<\|grounding\|>\s*)+/i, '')
    .trim();

  const fencedMatch = normalized.match(/^```(?:markdown|md)?\s*\n([\s\S]*?)\n```$/i);
  if (fencedMatch) {
    return fencedMatch[1].trim();
  }

  return normalized;
}

function hasUsableRecognitionContent(content, minLength = 5) {
  if (typeof content !== 'string') {
    return false;
  }

  const normalized = sanitizeModelOutput(content).trim();
  if (normalized.length < minLength) {
    return false;
  }

  if (!/[\u4e00-\u9fffA-Za-z0-9]/.test(normalized)) {
    return false;
  }

  const lowered = normalized.toLowerCase();
  return !lowered.includes('error') && !normalized.includes('失败');
}

function wrapContentAsResult(content) {
  return {
    choices: [
      {
        message: {
          content: sanitizeModelOutput(content || '')
        }
      }
    ]
  };
}

function debugPreview(label, content) {
  if (!DEBUG_ENABLED || !content) {
    return;
  }

  const preview = sanitizeModelOutput(content)
    .replace(/\s+/g, ' ')
    .slice(0, 240);
  log(`${label}：${preview}`, 'DEBUG');
}

/**
 * 打印性能统计
 */
function printPerformanceStats() {
  const totalDuration = Date.now() - performanceStats.startTime;
  console.log('\n📊 性能统计：');
  console.log(`总耗时：${totalDuration}ms (${(totalDuration / 1000).toFixed(2)}秒)`);
  console.log(`各步骤耗时:`);
  for (const s of performanceStats.steps) {
    console.log(`  ${s.step}: ${s.duration}ms`);
  }
}

// ==================== 配置 ====================

const CONFIG_FILE = path.join(os.homedir(), '.openclaw', 'workspace', 'config.json');
const OPENCLAW_CONFIG = path.join(os.homedir(), '.openclaw', 'openclaw.json');
const TEMP_DIR = path.join(os.tmpdir(), 'vision-ocr-' + process.pid);

function cleanupTempDir(force = false) {
  try {
    if (preserveTempArtifacts && !force) {
      return;
    }

    if (fs.existsSync(TEMP_DIR)) {
      fs.rmSync(TEMP_DIR, { recursive: true, force: true });
      log('临时文件已清理', 'INFO');
    }
  } catch (error) {
    log(`清理临时文件失败：${error.message}`, 'WARN');
  }
}

/**
 * 读取配置文件（多层优先级）
 * 
 * 优先级（从高到低）：
 * 1. 环境变量（最高）
 * 2. 技能目录本地配置（~/.openclaw/workspace/skills/vision-ocr/config.json）
 * 3. workspace 全局配置（~/.openclaw/workspace/config.json）
 * 4. openclaw 主配置（~/.openclaw/openclaw.json）
 */
function readConfig() {
  try {
    // 1. 尝试读取技能目录本地配置
    const localConfigPath = path.join(__dirname, 'config.json');
    let localConfig = {};
    if (fs.existsSync(localConfigPath)) {
      try {
        localConfig = JSON.parse(fs.readFileSync(localConfigPath, 'utf8'));
        log(`使用技能目录配置：${localConfigPath}`, 'INFO');
      } catch (e) {
        log(`读取技能目录配置失败：${e.message}`, 'WARN');
      }
    }
    
    // 2. 尝试读取 workspace 全局配置
    let workspaceConfig = {};
    if (fs.existsSync(CONFIG_FILE)) {
      try {
        workspaceConfig = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
        log(`使用 workspace 配置：${CONFIG_FILE}`, 'DEBUG');
      } catch (e) {
        log(`读取 workspace 配置失败：${e.message}`, 'WARN');
      }
    }
    
    // 3. 尝试读取 openclaw 主配置
    let mainConfig = {};
    if (fs.existsSync(OPENCLAW_CONFIG)) {
      try {
        mainConfig = JSON.parse(fs.readFileSync(OPENCLAW_CONFIG, 'utf8'));
        log(`使用 openclaw 配置：${OPENCLAW_CONFIG}`, 'DEBUG');
      } catch (e) {
        log(`读取 openclaw 配置失败：${e.message}`, 'WARN');
      }
    }
    
    // 4. 读取配置（优先级：本地 > workspace > openclaw）
    const localOcrConfig = localConfig?.ocr;
    const workspaceOcrConfig = workspaceConfig?.ocr;
    let autoSendToFeishu = localConfig?.autoSendToFeishu ?? workspaceConfig?.autoSendToFeishu ?? true;
    
    // 合并配置（本地配置优先，缺失字段回退到 openclaw 主配置）
    const ocrConfig = {
      imageocr: {
        ...workspaceOcrConfig?.imageocr,
        ...localOcrConfig?.imageocr
      },
      multimodal: {
        ...mainConfig?.models?.providers?.vllm,
        ...workspaceOcrConfig?.multimodal,
        ...localOcrConfig?.multimodal
      }
    };
    
    // 5. 环境变量覆盖（最高优先级）
    if (process.env.VISION_IMAGEOCR_TOKEN) {
      ocrConfig.imageocr.token = process.env.VISION_IMAGEOCR_TOKEN;
      log('使用环境变量 VISION_IMAGEOCR_TOKEN', 'INFO');
    }
    if (process.env.VISION_IMAGEOCR_ENDPOINT) {
      ocrConfig.imageocr.endpoint = process.env.VISION_IMAGEOCR_ENDPOINT;
      log('使用环境变量 VISION_IMAGEOCR_ENDPOINT', 'INFO');
    }
    if (process.env.VISION_BASE_URL) {
      ocrConfig.multimodal.baseUrl = process.env.VISION_BASE_URL;
      log('使用环境变量 VISION_BASE_URL', 'INFO');
    }
    if (process.env.VISION_MULTIMODAL_TOKEN) {
      ocrConfig.multimodal.token = process.env.VISION_MULTIMODAL_TOKEN;
      log('使用环境变量 VISION_MULTIMODAL_TOKEN', 'INFO');
    }
    if (process.env.VISION_MODEL) {
      ocrConfig.multimodal.model = process.env.VISION_MODEL;
      log('使用环境变量 VISION_MODEL', 'INFO');
    }

    const envAutoSendToFeishu = readBooleanEnv('VISION_AUTO_SEND_TO_FEISHU');
    if (envAutoSendToFeishu !== undefined) {
      autoSendToFeishu = envAutoSendToFeishu;
      log('使用环境变量 VISION_AUTO_SEND_TO_FEISHU', 'INFO');
    }
    
    // 6. 验证必需配置
    if (!ocrConfig.imageocr?.token || !ocrConfig.imageocr?.endpoint) {
      log('未找到 imageocr 配置', 'ERROR');
      console.log('\n请在以下位置之一配置（按优先级排序）：');
      console.log('1. 技能目录：~/.openclaw/workspace/skills/vision-ocr/config.json');
      console.log('2. Workspace: ~/.openclaw/workspace/config.json');
      console.log('3. 环境变量：VISION_IMAGEOCR_TOKEN, VISION_IMAGEOCR_ENDPOINT');
      console.log('\n配置示例:');
      console.log(JSON.stringify({
        ocr: {
          imageocr: {
            token: '你的 ImageOCR Token',
            endpoint: '你的 ImageOCR 端点'
          }
        }
      }, null, 2));
      return null;
    }
    
    // 7. 读取模型配置
    let qwenModel = ocrConfig.multimodal?.model || mainConfig?.agents?.defaults?.model?.primary;
    if (qwenModel) {
      qwenModel = qwenModel.replace(/^vllm\//, '');
    }

    if (!qwenModel) {
      log('未找到模型配置', 'ERROR');
      console.log('\n请在以下位置之一配置模型：');
      console.log('1. 技能目录：~/.openclaw/workspace/skills/vision-ocr/config.json');
      console.log('2. Workspace: ~/.openclaw/workspace/config.json');
      console.log('3. 环境变量：VISION_MODEL');
      console.log('\n配置示例:');
      console.log(JSON.stringify({
        ocr: {
          multimodal: {
            model: 'Sehyo/Qwen3.5-122B-A10B-NVFP4'
          }
        }
      }, null, 2));
      return null;
    }
    
    // 8. 读取 API 地址配置
    const modelsConfig = ocrConfig.multimodal;
    if (!modelsConfig?.baseUrl) {
      log('未找到多模态 API 地址配置', 'ERROR');
      console.log('\n请在以下位置之一配置 API 地址：');
      console.log('1. 技能目录：~/.openclaw/workspace/skills/vision-ocr/config.json');
      console.log('2. Workspace: ~/.openclaw/workspace/config.json');
      console.log('3. 环境变量：VISION_BASE_URL');
      console.log('\n配置示例:');
      console.log(JSON.stringify({
        ocr: {
          multimodal: {
            baseUrl: '你的多模态 API 地址'
          }
        }
      }, null, 2));
      return null;
    }
    
    const baseUrl = modelsConfig.baseUrl;
    const multimodalToken = modelsConfig.token;
    
    if (!multimodalToken) {
      log('未找到多模态 Token 配置', 'ERROR');
      console.log('\n请在以下位置之一配置多模态 Token：');
      console.log('1. 技能目录：~/.openclaw/workspace/skills/vision-ocr/config.json');
      console.log('2. Workspace: ~/.openclaw/workspace/config.json');
      console.log('3. 环境变量：VISION_MULTIMODAL_TOKEN');
      return null;
    }
    
    log(`当前模型：${qwenModel}`, 'INFO');
    log(`ImageOCR API 地址：${ocrConfig.imageocr.endpoint}`, 'INFO');
    log(`多模态 API 地址：${baseUrl}`, 'INFO');
    
    return {
      imageocr: ocrConfig.imageocr,
      multimodal: modelsConfig,
      qwenModel,
      baseUrl,
      autoSendToFeishu
    };
  } catch (error) {
    log(`读取配置失败：${error.message}`, 'ERROR');
    return null;
  }
}

// DeepSeek-OCR 2 优化 Prompt 模板
const DEEPSEEK_PROMPTS = {
  default: '<image>\n<|grounding|>Convert the document to markdown.',
  table: '专注于提取文档中的表格内容，将其转换为标准的 Markdown 表格格式。确保表头、行列对齐正确，忽略表格外的其他文本内容。',
  plain: 'Free OCR. 只提取文字内容，不需要格式',
  handwriting: '识别文档中的手写内容、手写便条、手写批注、签名和局部手写体。以图片中的手写内容为优先依据，必要时用多模态理解修正 OCR 误识别。输出清晰、完整的 Markdown，尽量区分打印体与手写补充内容。',
  tech: '识别技术文档，保留代码块（用 ``` 包裹）、标题层级（H1-H4）、表格格式。特别注意保护代码缩进和特殊符号。',
  finance: '专注处理财务报表表格：保持数字格式（包括千分位分隔符、货币符号），正确处理合并单元格，确保数值对齐。忽略表格外的文字说明。',
  invoice: '提取关键信息：发票号码、开票日期、销售方名称、购买方名称、金额合计。以键值对形式输出，忽略其他无关内容。',
  math: '识别数学题目和公式，使用 LaTeX 格式输出数学符号，保留题目结构和证明过程。'
};

// PDF 处理选项
const PDF_OPTIONS = {
  ocr_full: '📝 OCR 识别全部文字（逐页识别）',
  ocr_table: '📊 OCR 识别表格内容（逐页识别）',
  ocr_plain: '📄 OCR 纯文字提取（逐页识别）',
  save_images: '💾 保存 PDF 为图片（每页一张）',
  info: 'ℹ️ 查看 PDF 信息（页数、大小等）'
};

// 图片类型判断 Prompt（保留，但默认不使用）
const IMAGE_TYPE_PROMPT = `请判断这张图片属于以下哪种类型：

类型 1：【文档类】
- 特征：文字为主、表格、图表、扫描件、截图、PPT、PDF 转图等
- 适合：OCR 识别 + 多模态整合
- 输出：Markdown 格式

类型 2：【照片/图片类】
- 特征：风景、人物、物体、场景、生活照片等
- 适合：多模态描述分析
- 输出：自然语言描述

请回答：类型 1 或 类型 2，并简要说明理由。`;

const IMAGE_DESCRIPTION_PROMPT = '请详细描述这张图片的内容，包括场景、物体、人物、颜色、文字线索以及画面中值得注意的细节。';
const HANDWRITING_KEYWORD_REGEX = /(手写|手写体|手写文档|手写便条|批注|签名|签字|笔记|便签|便条)/i;
const HANDWRITING_DETECTION_PROMPT = `请判断这张文档图片中是否存在需要优先依赖视觉理解的明显手写内容。

手写内容包括：手写便条、手写批注、手写签名、手写勾画修改、手写箭头说明、局部手写补充。

判断规则：
1. 只要存在清晰可见的手写内容，就回答 HANDWRITING。
2. 如果整张图都是打印体、电子文本或规则印刷内容，没有明显手写部分，就回答 PRINTED。
3. 不要解释，不要输出其他内容，只能回答 HANDWRITING 或 PRINTED。`;

/**
 * 智能 Prompt 选择（基于内容特征）
 */
function classifyDocument(content) {
  if (!content) return 'default';
  
  const features = {
    hasTables: content.includes('|') && content.includes('\n'),
    hasCode: content.includes('```'),
    hasMath: content.includes('$') || content.includes('\\frac') || content.includes('^'),
    hasInvoice: /发票 | 订单 | 金额 | 收款 | 付款/.test(content),
    hasFinance: /报表 | 财务 | 预算 | 利润 | 收入 | 支出/.test(content),
    hasTech: /代码 | 函数 | 接口 | API|class|def/.test(content),
    hasMathProblem: /题|求证 | 已知 | 计算/.test(content)
  };
  
  // 规则分类
  if (features.hasTables && features.hasFinance) return 'finance';
  if (features.hasCode) return 'tech';
  if (features.hasMath || features.hasMathProblem) return 'math';
  if (features.hasInvoice) return 'invoice';
  if (features.hasTables) return 'table';
  
  return 'default';
}

/**
 * 智能 Prompt 选择（基于用户输入）
 */
function optimizePrompt(userPrompt) {
  if (!userPrompt) return DEEPSEEK_PROMPTS.default;
  
  // 简单关键词匹配
  if (/(手写|手写体|手写文档|便条|批注|签名|签字|笔记)/i.test(userPrompt)) return DEEPSEEK_PROMPTS.handwriting;
  if (/(表格|数据表|excel)/i.test(userPrompt)) return DEEPSEEK_PROMPTS.table;
  if (/(纯文字|文字|提取)/i.test(userPrompt)) return DEEPSEEK_PROMPTS.plain;
  if (/(技术|代码|编程)/i.test(userPrompt)) return DEEPSEEK_PROMPTS.tech;
  if (/(财务|报表|金额)/i.test(userPrompt)) return DEEPSEEK_PROMPTS.finance;
  if (/(发票|订单)/i.test(userPrompt)) return DEEPSEEK_PROMPTS.invoice;
  if (/(数学|公式|题目)/i.test(userPrompt)) return DEEPSEEK_PROMPTS.math;
  
  return DEEPSEEK_PROMPTS.default;
}

function isHandwritingPrompt(promptText) {
  if (!promptText || typeof promptText !== 'string') {
    return false;
  }

  return promptText === DEEPSEEK_PROMPTS.handwriting || HANDWRITING_KEYWORD_REGEX.test(promptText);
}

function stripMarkdownSyntax(line) {
  return line
    .replace(/^\s{0,3}(?:[-*+] |\d+\.\s+)/, '')
    .replace(/^#{1,6}\s*/, '')
    .replace(/[|`>*_~]/g, '')
    .trim();
}

function classifyHandwritingLikelihoodFromOCR(content) {
  if (!hasUsableRecognitionContent(content, 2)) {
    return 'uncertain';
  }

  const normalized = sanitizeModelOutput(content);
  const cleanedLines = normalized
    .split('\n')
    .map(stripMarkdownSyntax)
    .filter(Boolean);

  if (cleanedLines.length === 0) {
    return 'uncertain';
  }

  const suspiciousOcrNoise =
    /table\[\[/i.test(normalized) ||
    /<\/?table>/i.test(normalized) ||
    /\[(?:\d+\s*,\s*){3}\d+\]/.test(normalized);

  if (suspiciousOcrNoise && cleanedLines.length <= 3) {
    return 'handwriting';
  }

  const structuredSignals = [
    /```/.test(normalized),
    /\|.+\|/.test(normalized),
    /^#{1,6}\s/m.test(normalized) && cleanedLines.length >= 3,
    cleanedLines.some(line => line.length >= 40)
  ].filter(Boolean).length;

  if (structuredSignals >= 2) {
    return 'printed';
  }

  const avgLineLength = cleanedLines.reduce((sum, line) => sum + line.length, 0) / cleanedLines.length;
  const shortLineCount = cleanedLines.filter(line => line.length <= 6).length;
  const shortLineRatio = shortLineCount / cleanedLines.length;
  const fragmentedChars = /(?:[\u4e00-\u9fffA-Za-z0-9]\s+){4,}[\u4e00-\u9fffA-Za-z0-9]/.test(normalized);
  const replacementNoise = /�|[?？]{3,}/.test(normalized);

  if (fragmentedChars || replacementNoise) {
    return 'handwriting';
  }

  if (cleanedLines.length >= 4 && shortLineRatio >= 0.85 && avgLineLength <= 6) {
    return 'handwriting';
  }

  return 'uncertain';
}

function analyzeRecognitionLayout(content) {
  const normalized = sanitizeModelOutput(content || '');
  const cleanedLines = normalized
    .split('\n')
    .map(stripMarkdownSyntax)
    .filter(Boolean);

  const totalLength = cleanedLines.reduce((sum, line) => sum + line.length, 0);
  const avgLineLength = cleanedLines.length > 0 ? totalLength / cleanedLines.length : 0;
  const hasMarkdownStructure =
    /```/.test(normalized) ||
    /^#{1,6}\s/m.test(normalized) ||
    /\|.+\|/.test(normalized) ||
    /^\s*(?:[-*+] |\d+\.\s+)/m.test(normalized);
  const hasOcrArtifacts =
    /(?:text|table)\[\[/i.test(normalized) ||
    /<\/?table>/i.test(normalized) ||
    /\[(?:\d+\s*,\s*){3}\d+\]/.test(normalized);

  return {
    normalized,
    cleanedLines,
    lineCount: cleanedLines.length,
    totalLength,
    avgLineLength,
    hasMarkdownStructure,
    hasOcrArtifacts
  };
}

function isLikelyShortHandwrittenNote(content) {
  if (!hasUsableRecognitionContent(content, 3)) {
    return false;
  }

  const layout = analyzeRecognitionLayout(content);
  return !layout.hasMarkdownStructure && layout.lineCount >= 1 && layout.lineCount <= 4 && layout.totalLength <= 80 && layout.avgLineLength <= 20;
}

function isLikelyHandwritingDominantDocument(multimodalContent, ocrContent = '') {
  if (!hasUsableRecognitionContent(multimodalContent, 3)) {
    return false;
  }

  const multimodalLayout = analyzeRecognitionLayout(multimodalContent);
  const ocrLayout = analyzeRecognitionLayout(ocrContent);
  const ocrClassification = classifyHandwritingLikelihoodFromOCR(ocrContent);

  const multimodalLooksLikeMediumShortDoc =
    !multimodalLayout.hasMarkdownStructure &&
    multimodalLayout.lineCount >= 2 &&
    multimodalLayout.lineCount <= 8 &&
    multimodalLayout.totalLength <= 220 &&
    multimodalLayout.avgLineLength <= 30;

  const ocrLooksUnreliable =
    ocrLayout.hasOcrArtifacts ||
    ocrClassification === 'handwriting' ||
    (ocrLayout.lineCount <= 4 && ocrLayout.totalLength <= 120 && !ocrLayout.hasMarkdownStructure);

  return multimodalLooksLikeMediumShortDoc && ocrLooksUnreliable;
}

function parseHandwritingDetectionResponse(content) {
  const normalized = sanitizeModelOutput(content || '').trim().toLowerCase();

  if (!normalized) {
    return null;
  }

  if (normalized.includes('handwriting') || normalized.includes('手写')) {
    return true;
  }

  if (normalized.includes('printed') || normalized.includes('纯打印') || normalized.includes('无手写')) {
    return false;
  }

  return null;
}

async function detectHandwritingFromImage(imageBase64, token) {
  const cacheKey = calculateTextHash(imageBase64);
  if (handwritingDetectionCache.has(cacheKey)) {
    return handwritingDetectionCache.get(cacheKey);
  }

  log('正在自动判断图片中是否存在明显手写内容...', 'INFO');
  const result = await callQwen(token, imageBase64, HANDWRITING_DETECTION_PROMPT, false, null);
  const parsed = parseHandwritingDetectionResponse(result?.choices?.[0]?.message?.content || '');

  if (parsed !== null) {
    setLimitedCacheEntry(handwritingDetectionCache, cacheKey, parsed, MAX_RESULT_CACHE_ENTRIES);
  }

  return parsed;
}

async function shouldUseHandwritingMode(imageBase64, ocrContent, documentPrompt, token) {
  if (isHandwritingPrompt(documentPrompt)) {
    return { enabled: true, reason: 'prompt' };
  }

  const ocrClassification = classifyHandwritingLikelihoodFromOCR(ocrContent);
  if (ocrClassification === 'handwriting') {
    return { enabled: true, reason: 'ocr' };
  }

  if (ocrClassification === 'printed') {
    return { enabled: false, reason: 'ocr' };
  }

  const imageClassification = await detectHandwritingFromImage(imageBase64, token);
  if (imageClassification === true) {
    return { enabled: true, reason: 'image' };
  }

  if (imageClassification === false) {
    return { enabled: false, reason: 'image' };
  }

  return { enabled: false, reason: 'fallback' };
}

function buildDocumentIntegrationPrompt(ocrContent, documentPrompt) {
  const normalizedPrompt = documentPrompt || DEEPSEEK_PROMPTS.default;

  return `你将收到一张原始图片，以及该图片经过 OCR 提取后的 Markdown 文本。

请严格按照下面的文档识别指令，输出最终 Markdown：

【文档识别指令】
${normalizedPrompt}

【OCR Markdown】
${ocrContent}

【输出要求】
1. 以 OCR Markdown 为主，尽量保留标题、列表、表格、代码块等结构。
2. 结合图片内容修正 OCR 错字、缺漏、顺序问题。
3. 如果图片中包含手写便条、手写批注、签名或局部手写体，手写部分优先参考图片本身的多模态识别结果，不要机械照搬 OCR 结果。
4. 如果 OCR 与图片中的手写内容冲突，以你对原图中手写内容的判断为准，并在最终 Markdown 中直接给出修正后的结果。
5. 如果 OCR 中有结构问题，请整理成更清晰的 Markdown。
6. 不要输出分析过程，不要解释，只输出最终 Markdown。
7. 如果图片中存在 OCR 未识别到的关键文档内容，可以补入最终 Markdown。`;
}

function buildHandwritingVisionPrompt(documentPrompt) {
  const normalizedPrompt = documentPrompt || DEEPSEEK_PROMPTS.handwriting;

  return `你将收到一张可能包含打印体、手写便条、手写批注、签名、箭头标记、勾画或局部涂改的文档图片。

请直接基于原图做一次完整识别，并输出最终 Markdown。

【识别指令】
${normalizedPrompt}

【输出要求】
1. 手写内容、批注、签名、便条、箭头关联说明优先依据图片本身，不要依赖 OCR 文本。
2. 打印体正文、表格、标题、列表也要一起识别，尽量保持清晰的 Markdown 结构。
3. 如果手写内容是对打印体的补充、修正或备注，请直接在最终 Markdown 中体现修正后的结果。
4. 不要输出分析过程，不要解释，只输出最终 Markdown。`;
}

function buildHandwritingIntegrationPrompt(ocrContent, multimodalContent, documentPrompt) {
  const normalizedPrompt = documentPrompt || DEEPSEEK_PROMPTS.handwriting;

  return `你将收到同一张文档图片的两份识别结果：
1. OCR Markdown：结构通常更稳定，但手写内容可能有误。
2. 多模态直读结果：更适合识别手写便条、批注、签名、箭头说明和局部修改。

请综合两份结果，输出最终 Markdown。

【文档识别指令】
${normalizedPrompt}

【OCR Markdown】
${ocrContent}

【多模态直读结果】
${multimodalContent}

【融合要求】
1. 正文结构、标题层级、表格框架可优先参考 OCR。
2. 所有手写内容、批注、签名、勾画修正、箭头关联说明，优先参考多模态直读结果。
3. 如果 OCR 与多模态在手写内容上冲突，以多模态结果为准。
4. 如果多模态补充了 OCR 漏掉的手写信息，请补入最终 Markdown。
5. 如果 OCR 结构更清晰，但手写词句更准确，请保留 OCR 结构并替换为更准确的手写内容。
6. 不要输出分析过程，不要解释，只输出最终 Markdown。`;
}

async function recognizeHandwritingDocument(imageBase64, ocrContent, token, documentPrompt) {
  log('第二步：手写优先，多模态直接识别原图...', 'INFO');
  const rawResult = await callQwen(token, imageBase64, buildHandwritingVisionPrompt(documentPrompt), false, null);
  const rawContent = sanitizeModelOutput(rawResult?.choices?.[0]?.message?.content || '');
  const usableOcr = hasUsableRecognitionContent(ocrContent, 3);
  const usableRaw = hasUsableRecognitionContent(rawContent, 3);
  const ocrLayout = analyzeRecognitionLayout(ocrContent);

  debugPreview('手写模式 OCR 预览', ocrContent);
  debugPreview('手写模式多模态直读预览', rawContent);

  if (!usableOcr && !usableRaw) {
    return null;
  }

  if (!usableOcr && usableRaw) {
    log('OCR 对手写内容不稳定，直接采用多模态直读结果', 'INFO');
    return wrapContentAsResult(rawContent);
  }

  if (!usableRaw && usableOcr) {
    log('手写多模态直读失败，回退到 OCR 结果', 'WARN');
    return wrapContentAsResult(ocrContent);
  }

  if (isLikelyShortHandwrittenNote(rawContent)) {
    log('检测到短手写便条，直接采用多模态直读结果', 'INFO');
    return wrapContentAsResult(rawContent);
  }

  if (isLikelyHandwritingDominantDocument(rawContent, ocrContent)) {
    log('检测到手写主导的中短文档，直接采用多模态直读结果', 'INFO');
    return wrapContentAsResult(rawContent);
  }

  if (ocrLayout.hasOcrArtifacts && usableRaw) {
    log('OCR 输出包含明显噪声标记，直接采用多模态直读结果', 'INFO');
    return wrapContentAsResult(rawContent);
  }

  log('第三步：融合 OCR 结构和多模态手写识别结果...', 'INFO');
  const mergedResult = await callQwen(
    token,
    null,
    buildHandwritingIntegrationPrompt(ocrContent, rawContent, documentPrompt),
    true,
    null
  );

  const mergedContent = sanitizeModelOutput(mergedResult?.choices?.[0]?.message?.content || '');
  debugPreview('手写模式融合结果预览', mergedContent);

  if (hasUsableRecognitionContent(mergedContent, 3)) {
    return wrapContentAsResult(mergedContent);
  }

  log('手写融合失败，回退到多模态直读结果', 'WARN');
  return wrapContentAsResult(rawContent);
}

/**
 * 智能 Prompt 选择（基于 OCR 初步结果）
 */
function optimizePromptWithOCR(ocrContent, originalPrompt) {
  if (!ocrContent) return originalPrompt;
  
  const type = classifyDocument(ocrContent);
  const optimizedPrompt = DEEPSEEK_PROMPTS[type] || originalPrompt;
  
  if (type !== 'default') {
    log(`智能选择 Prompt 模板：${type}`, 'INFO');
  }
  
  return optimizedPrompt;
}

// 自然语言到 Prompt 模板的映射
const PROMPT_KEYWORDS = {
  handwriting: ['手写', '手写体', '手写文档', '手写便条', '批注', '签名', '签字', '笔记'],
  table: ['表格', '数据表', 'excel', 'sheet', '行列', '表头'],
  plain: ['纯文字', '文字', '内容', '提取', '识别', '转文字', 'ocr'],
  tech: ['技术', '代码', '编程', '程序', '文档', 'api', '接口'],
  finance: ['财务', '报表', '金额', '数字', '会计', '账目', '预算'],
  invoice: ['发票', '合同', '订单', '票据', '收据', '凭证'],
  math: ['数学', '公式', '题目', '证明', '几何', '代数', '方程'],
  default: ['文档', '文章', '文字', '内容', '识别', '转 markdown']
};

// ==================== PDF 处理函数 ====================

/**
 * PDF 转图片 - 流式处理（不保存文件）
 */
function pdfToImages(pdfPath, outputDir) {
  try {
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
    
    const script = `
import fitz
import sys

pdf_path = "${pdfPath.replace(/\\/g, '/').replace(/"/g, '\\"')}"
output_dir = "${outputDir.replace(/\\/g, '/').replace(/"/g, '\\"')}"

doc = fitz.open(pdf_path)
page_count = len(doc)

for page_num in range(page_count):
    page = doc[page_num]
    mat = fitz.Matrix(2.0, 2.0)  # 2x 缩放，提高清晰度
    pix = page.get_pixmap(matrix=mat)
    output_path = f"{output_dir}/page_{page_num + 1:03d}.png"
    pix.save(output_path)
    print(f"Saved: {output_path}")

doc.close()
print(f"Total pages: {page_count}")
`;
    
    const tempScript = path.join(outputDir, 'pdf_to_images.py');
    fs.writeFileSync(tempScript, script);
    
    execFileSync('python3', [tempScript], { stdio: 'pipe' });
    
    fs.unlinkSync(tempScript);
    
    const images = fs.readdirSync(outputDir)
      .filter(f => f.endsWith('.png'))
      .sort()
      .map(f => path.join(outputDir, f));
    
    return images;
  } catch (error) {
    log(`PDF 转图片失败：${error.message}`, 'ERROR');
    return null;
  }
}

/**
 * 获取 PDF 信息
 */
function getPDFInfo(pdfPath) {
  try {
    const scriptPath = path.join(TEMP_DIR, 'get_pdf_info.py');
    const script = `
import fitz
import sys

pdf_path = "${pdfPath.replace(/\\/g, '/').replace(/"/g, '\\"')}"
doc = fitz.open(pdf_path)
page_count = len(doc)
mediabox = doc[0].rect
print(f"pages:{page_count}")
print(f"width:{mediabox.width}")
print(f"height:{mediabox.height}")
doc.close()
`;
    
    fs.writeFileSync(scriptPath, script);
    const output = execFileSync('python3', [scriptPath], { encoding: 'utf8' });
    fs.unlinkSync(scriptPath);
    
    const lines = output.trim().split('\n');
    
    const info = {};
    for (const line of lines) {
      const [key, value] = line.split(':');
      if (key && value) info[key] = value;
    }
    
    return info;
  } catch (error) {
    log(`获取 PDF 信息失败：${error.message}`, 'ERROR');
    return null;
  }
}

/**
 * 显示 PDF 处理选项
 */
function showPDFOptions(pdfPath) {
  console.log('\n📄 检测到 PDF 文件：' + path.basename(pdfPath));
  console.log('\n请选择处理方式：');
  console.log('');
  
  let index = 1;
  for (const [key, label] of Object.entries(PDF_OPTIONS)) {
    console.log(`  ${index}. ${label}`);
    index++;
  }
  
  console.log('');
  console.log('请输入选项编号（1-5）：');
}

function isInteractiveCli() {
  return Boolean(process.stdin.isTTY && process.stdout.isTTY);
}

function parseImageModeChoice(input) {
  const normalized = (input || '').trim().toLowerCase();

  if (!normalized) return null;
  if (['1', 'document', 'doc', 'ocr', '文档', '识别文档', '文档识别'].includes(normalized)) return 'document';
  if (['2', 'photo', 'image', 'describe', 'description', '图片', '照片', '描述', '图片描述', '描述图片'].includes(normalized)) return 'photo';
  if (['3', 'exit', 'quit', 'q', '退出'].includes(normalized)) return 'exit';
  return null;
}

function parsePdfOptionChoice(input) {
  const normalized = (input || '').trim().toLowerCase();
  const optionMap = {
    '1': 'ocr_full',
    '2': 'ocr_table',
    '3': 'ocr_plain',
    '4': 'save_images',
    '5': 'info',
    ocr_full: 'ocr_full',
    ocr_table: 'ocr_table',
    ocr_plain: 'ocr_plain',
    save_images: 'save_images',
    info: 'info'
  };

  if (!normalized) return null;
  if (normalized in optionMap) return optionMap[normalized];
  if (['全部文字', '全文', '全部', 'ocr'].includes(normalized)) return 'ocr_full';
  if (['表格', 'table'].includes(normalized)) return 'ocr_table';
  if (['纯文字', '文字', 'plain'].includes(normalized)) return 'ocr_plain';
  if (['保存图片', '图片', 'save'].includes(normalized)) return 'save_images';
  if (['信息', '查看信息'].includes(normalized)) return 'info';
  if (['exit', 'quit', 'q', '退出'].includes(normalized)) return 'exit';
  return null;
}

function extractInputFilePath(input) {
  const text = String(input || '').trim();
  const candidates = [];
  const workspacePath = path.join(os.homedir(), '.openclaw', 'workspace');

  const absMatches = text.match(/(\/[^\s"']+)/g) || [];
  candidates.push(...absMatches);

  const fileMatches = text.match(/([^\s"']+\.(?:png|jpe?g|webp|gif|pdf))/gi) || [];
  for (const match of fileMatches) {
    candidates.push(match);
    candidates.push(path.join(process.cwd(), match));
    candidates.push(path.join(workspacePath, match));
  }

  for (const candidate of candidates) {
    if (candidate && fs.existsSync(candidate)) {
      return candidate;
    }
  }

  return null;
}

function inferPdfOptionFromText(input) {
  const text = String(input || '').trim();
  return parsePdfOptionChoice(text) || 'ocr_full';
}

function inferImageModeFromText(input) {
  const text = String(input || '').trim().toLowerCase();

  if (/(描述|图片描述|照片描述|describe|photo)/i.test(text)) {
    return 'photo';
  }

  return 'document';
}

function shouldDisableFeishuDelivery(input) {
  return /(不发飞书|不要发飞书|无需发飞书|关闭飞书|no-send-to-feishu)/i.test(String(input || ''));
}

function resolveSessionRecipientFromContext(session) {
  if (!session || typeof session !== 'object') {
    return null;
  }

  // 优先检查 senderId（OpenClaw SDK 传递的）
  if (session.senderId) {
    return { id: session.senderId, type: 'open_id' };
  }

  if (session.isGroup && session.chatId) {
    return { id: session.chatId, type: 'chat_id' };
  }

  if (session.openId) {
    return { id: session.openId, type: 'open_id' };
  }

  return null;
}

function extractResultContentFromOutput(output) {
  const match = String(output || '').match(/--- [^\n]+ ---\n([\s\S]*?)\n\n📄 Markdown 文件已保存/u);
  return match ? match[1].trim() : '';
}

function buildRobotReply(output, sessionRecipient) {
  const content = extractResultContentFromOutput(output);
  const lines = [];

  if (/✅ 已成功发送到飞书/.test(output)) {
    lines.push(`识别完成，结果已发送到当前${sessionRecipient?.type === 'chat_id' ? '群聊' : '会话'}。`);
  } else if (/🔒 已按当前设置关闭自动发送到飞书/.test(output)) {
    lines.push('识别完成，已按当前设置关闭自动发送到飞书。');
  } else {
    lines.push('识别完成。');
  }

  if (content) {
    const preview = content.split('\n').slice(0, 12).join('\n').trim();
    lines.push('');
    lines.push(preview);
  }

  return lines.join('\n');
}

function parseRecipientOverrideFromText(input) {
  const text = String(input || '');
  const match = text.match(/(?:发给|发送给|转发给|to)\s*(chat|chat_id|group|open_id)\s*:\s*([A-Za-z0-9_\-]+)/i);

  if (!match) {
    return null;
  }

  return {
    type: normalizeRecipientType(match[1]),
    id: match[2]
  };
}

async function promptForImageMode(imagePath) {
  if (!isInteractiveCli()) {
    return null;
  }

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  try {
    console.log('\n📋 检测到文件：' + path.basename(imagePath));
    console.log('\n请选择处理方式：');
    console.log('  1. 识别文档（OCR + 多模态整合，输出 Markdown）');
    console.log('  2. 描述图片（多模态分析，输出自然语言描述）');
    console.log('  3. 退出');

    while (true) {
      const answer = await rl.question('\n请输入选项（1-3）：');
      const choice = parseImageModeChoice(answer);
      if (choice) {
        return choice;
      }
      console.log('⚠️  输入无效，请输入 1、2 或 3。');
    }
  } finally {
    rl.close();
  }
}

async function promptForPdfOption(pdfPath) {
  if (!isInteractiveCli()) {
    return null;
  }

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  try {
    console.log('\n📄 检测到 PDF 文件：' + path.basename(pdfPath));
    console.log('\n请选择处理方式：');
    console.log('  1. 📝 OCR 识别全部文字（逐页识别）');
    console.log('  2. 📊 OCR 识别表格内容（逐页识别）');
    console.log('  3. 📄 OCR 纯文字提取（逐页识别）');
    console.log('  4. 💾 保存 PDF 为图片（每页一张）');
    console.log('  5. ℹ️ 查看 PDF 信息（页数、大小等）');
    console.log('  exit. 退出');

    while (true) {
      const answer = await rl.question('\n请输入选项编号（1-5）：');
      const choice = parsePdfOptionChoice(answer);
      if (choice) {
        return choice;
      }
      console.log('⚠️  输入无效，请输入 1-5、选项名或 exit。');
    }
  } finally {
    rl.close();
  }
}

// ==================== API 调用函数 ====================

/**
 * 调用 ImageOCR 接口（图片识别）
 */
async function callImageOCR(token, endpoint, imageBase64, prompt = '<image>\n<|grounding|>Convert the document to markdown.', maxRetries = 2) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          messages: [
            {
              role: 'user',
              content: [
                { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${imageBase64}` } },
                { type: 'text', text: prompt }
              ]
            }
          ]
        })
      });

      if (!response.ok) {
        const error = await response.text();
        log(`ImageOCR 调用失败 (尝试 ${attempt}/${maxRetries}): ${response.status}`, 'WARN');
        if (attempt < maxRetries) {
          await new Promise(resolve => setTimeout(resolve, 1000));
          continue;
        }
        return null;
      }

      const data = await response.json();
      const content = data.choices?.[0]?.message?.content;
      
      if (!content || content.trim() === '') {
        log(`ImageOCR 返回为空 (尝试 ${attempt}/${maxRetries})`, 'WARN');
        if (attempt < maxRetries) {
          await new Promise(resolve => setTimeout(resolve, 1000));
          continue;
        }
        return null;
      }
      
      log(`ImageOCR 识别成功 (尝试 ${attempt}/${maxRetries})`, 'INFO');
      return data;
    } catch (error) {
      log(`ImageOCR 调用异常 (尝试 ${attempt}/${maxRetries}): ${error.message}`, 'WARN');
      if (attempt < maxRetries) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        continue;
      }
      return null;
    }
  }
  return null;
}

/**
 * 从 API 获取可用模型列表
 */
async function getAvailableModels(token, baseUrl) {
  const cacheKey = `${baseUrl}::${token || ''}`;

  if (multimodalModelCache.has(cacheKey)) {
    return multimodalModelCache.get(cacheKey);
  }

  try {
    const apiToken = token;
    const response = await fetch(`${baseUrl}/models`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${apiToken}`
      }
    });

    if (!response.ok) {
      log(`获取模型列表失败：${response.status}`, 'WARN');
      return null;
    }

    const data = await response.json();
    multimodalModelCache.set(cacheKey, data);
    return data;
  } catch (error) {
    log(`获取模型列表异常：${error.message}`, 'ERROR');
    return null;
  }
}

/**
 * 查找多模态模型
 */
function findVisionModel(modelsData) {
  if (!modelsData || !modelsData.data) return null;
  
  const visionModels = modelsData.data.filter(m => 
    m.id.toLowerCase().includes('vision') || 
    m.id.toLowerCase().includes('multimodal') ||
    m.id.toLowerCase().includes('qwen') ||
    m.id.toLowerCase().includes('vl')
  );
  
  return visionModels.length > 0 ? visionModels[0].id : null;
}

/**
 * 调用 Qwen 3.5 多模态接口（带 enable_thinking 参数）
 */
async function callQwen(token, imageBase64, prompt, isTextOnly = false, modelsData = null) {
  try {
    const config = readConfig();
    const baseUrl = config?.baseUrl;
    if (!baseUrl) {
      log('未找到多模态 API 地址配置，请在 config.json 中配置 ocr.multimodal.baseUrl', 'ERROR');
      return null;
    }
    const apiToken = config?.multimodal?.token || token;
    
    let model = config?.qwenModel;

    if (!model) {
      let models = modelsData;
      if (!models) {
        log('正在获取可用模型列表...', 'INFO');
        models = await getAvailableModels(apiToken, baseUrl);
      }

      model = findVisionModel(models);
      if (!model) {
        log('未找到模型配置，请在 config.json 中配置 ocr.multimodal.model', 'ERROR');
        return null;
      }

      log(`自动选择多模态模型：${model}`, 'INFO');
    } else {
      log(`使用配置模型：${model}`, 'INFO');
    }
    
    let messages;
    if (isTextOnly) {
      messages = [{ role: 'user', content: prompt }];
    } else {
      messages = [{
        role: 'user',
        content: [
          { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${imageBase64}` } },
          { type: 'text', text: prompt }
        ]
      }];
    }
    
    const response = await fetch(`${baseUrl}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiToken}`
      },
      body: JSON.stringify({
        model: model,
        messages: messages,
        chat_template_kwargs: { enable_thinking: false }
      })
    });

    if (!response.ok) {
      const error = await response.text();
      log(`Qwen 多模态调用失败：${response.status} - ${error}`, 'ERROR');
      return null;
    }

    return await response.json();
  } catch (error) {
    log(`Qwen 多模态调用异常：${error.message}`, 'ERROR');
    return null;
  }
}

/**
 * 单页图片识别流程（带超时控制和重试，总超时 180 秒）
 */
async function processSinglePageWithRetry(imagePath, prompt, config, token, maxRetries = 3) {
  const startTime = Date.now();
  const totalTimeout = 180000; // 总超时 180 秒
  
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    // 检查总超时
    if (Date.now() - startTime > totalTimeout) {
      log(`总超时（${totalTimeout}ms），停止重试`, 'ERROR');
      return null;
    }
    
    try {
      const result = await processSinglePage(imagePath, prompt, config, token);
      if (result) return result;
      
      log(`重试 ${attempt}/${maxRetries}...`, 'WARN');
      if (attempt < maxRetries) {
        await new Promise(resolve => setTimeout(resolve, 2000));
        continue;
      }
    } catch (error) {
      log(`重试 ${attempt}/${maxRetries}: ${error.message}`, 'WARN');
      if (attempt < maxRetries) {
        await new Promise(resolve => setTimeout(resolve, 2000));
        continue;
      }
    }
  }
  return null;
}

/**
 * 单页文档识别流程（带超时控制）
 */
async function processSinglePage(imagePath, prompt, config, token) {
  // 设置总超时 180 秒
  const totalTimeoutMs = 180000;
  
  const totalTimeoutPromise = new Promise((_, reject) => {
    setTimeout(() => reject(new Error('总处理超时（180 秒）')), totalTimeoutMs);
  });
  
  try {
    const result = await Promise.race([
      (async () => {
        log('第一步：ImageOCR 识别（输出 Markdown）...', 'INFO');
        const imageBase64 = readFileAsBase64(imagePath);
        if (!imageBase64) return null;

        const promptRequestedHandwriting = isHandwritingPrompt(prompt);
        const ocrPrompt = promptRequestedHandwriting ? DEEPSEEK_PROMPTS.handwriting : prompt;
        const ocrResult = await callImageOCR(config.imageocr.token, config.imageocr.endpoint, imageBase64, ocrPrompt);
        const ocrContent = ocrResult?.choices?.[0]?.message?.content || '';

        const handwritingDecision = await shouldUseHandwritingMode(imageBase64, ocrContent, prompt, token);
        const handwritingMode = handwritingDecision.enabled;
        log(`手写自动判定：${handwritingMode ? '启用' : '关闭'}（依据：${handwritingDecision.reason}）`, 'INFO');

        if (handwritingMode) {
          const handwritingResult = await recognizeHandwritingDocument(imageBase64, ocrContent, token, prompt);
          if (handwritingResult?.choices?.[0]?.message?.content) {
            log('整合完成', 'INFO');
            return handwritingResult;
          }
        }

        if (!ocrContent || ocrContent.trim() === '') {
          log('OCR 识别失败', 'ERROR');
          return null;
        }

        log('第二步：大模型整合（OCR 文字 + 原图）...', 'INFO');

        const integrationPrompt = buildDocumentIntegrationPrompt(ocrContent, prompt);
        
        // 设置 LLM 整合超时 60 秒
        const llmTimeoutMs = 60000;
        const llmTimeoutPromise = new Promise((_, reject) => {
          setTimeout(() => reject(new Error('LLM 整合超时（60 秒）')), llmTimeoutMs);
        });
        
        const integrationResult = await Promise.race([
          callQwen(token, imageBase64, integrationPrompt, false, null),
          llmTimeoutPromise
        ]);
        
        if (integrationResult?.choices?.[0]?.message?.content) {
          log('整合完成', 'INFO');
          return integrationResult;
        }
        
        // LLM 失败，使用 OCR 结果
        log('整合失败，使用 OCR 结果', 'WARN');
        return { choices: [{ message: { content: ocrContent } }] };
      })(),
      totalTimeoutPromise
    ]);
    
    return result;
  } catch (error) {
    log(`单页处理失败：${error.message}`, 'ERROR');
    return null;
  }
}


async function sendMarkdownToFeishu(markdownPath, config, recipient) {
  try {
    const sendFilesPath = path.join(os.homedir(), '.openclaw', 'workspace', 'skills', 'feishu-send-files', 'index.js');
    
    const resolvedConfig = config || readConfig();
    // 优先使用 --to 参数，然后是 recipient 参数，最后是环境变量
    const toArgRecipient = parseToArg();
    const sessionRecipient = recipient || toArgRecipient || getRuntimeSessionRecipient();
    const finalRecipientId = sessionRecipient?.id;
    const finalRecipientType = normalizeRecipientType(sessionRecipient?.type || 'open_id');
    
    if (!finalRecipientId) {
      log('未找到当前会话接收者，跳过自动发送', 'WARN');
      console.log(`\n⚠️  文件已保存：${markdownPath}`);
      console.log('当前运行环境未提供会话接收者，未自动发送到飞书。');
      console.log('如果这是 OpenClaw 集成场景，请改为机器人模式调用 vision-ocr.run(context)，而不是仅执行命令行。');
      console.log('如需发送给其他对象，请在对话中明确指定，例如：发给 open_id:ou_xxx 或使用 --to 参数');
      return false;
    }
    
    // 检查 feishu-send-files 技能是否存在
    if (!fs.existsSync(sendFilesPath)) {
      log('feishu-send-files 技能不存在，无法自动发送', 'WARN');
      console.log(`\n📄 文件已保存：${markdownPath}`);
      console.log(`💡 请手动发送到飞书：${buildFeishuTarget(finalRecipientType, finalRecipientId)}`);
      console.log(`💡 或安装 feishu-send-files 技能以自动发送`);
      return false;
    }
    
    // 调用 feishu-send-files 技能
    const result = execFileSync('node', [sendFilesPath, '--file', markdownPath, '--to', buildFeishuTarget(finalRecipientType, finalRecipientId)], {
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe']
    });
    
    log(`文件发送成功：${result}`, 'INFO');
    return true;
  } catch (error) {
    log(`文件发送失败：${error.message}`, 'ERROR');
    return false;
  }
}

async function handleMarkdownDelivery(markdownPath, config, sendToFeishuOverride, recipient) {
  // 优先使用 --to 参数，然后是 recipient 参数，最后是环境变量
  const toArgRecipient = parseToArg();
  const runtimeRecipient = recipient || toArgRecipient || getRuntimeSessionRecipient();
  const shouldSendToFeishu = sendToFeishuOverride ?? config?.autoSendToFeishu ?? true;

  if (!shouldSendToFeishu) {
    preserveTempArtifacts = true;
    console.log('\n🔒 已按当前设置关闭自动发送到飞书。');
    console.log(`📄 结果文件保留在：${markdownPath}`);
    console.log('如需重新开启，请移除 --no-send-to-feishu，或在 config.json 中设置 "autoSendToFeishu": true');
    return false;
  }

  console.log('\n📤 正在发送到飞书...');
  const sent = await sendMarkdownToFeishu(markdownPath, config, runtimeRecipient);

  if (sent) {
    console.log('\n✅ 已成功发送到飞书');
    return true;
  }

  preserveTempArtifacts = true;
  console.log(`\n⚠️  自动发送未完成，结果文件保留在：${markdownPath}`);
  return false;
}

/**
 * 生成 Markdown 文档内容
 */
function generateMarkdownResult(filename, results, successCount, failCount) {
  let markdown = `# ${filename}\n\n`;
  markdown += `**识别时间**: ${new Date().toLocaleString('zh-CN')}\n\n`;
  markdown += `**统计**: 成功 ${successCount} 页，失败 ${failCount} 页\n\n`;
  markdown += `---\n\n`;
  
  for (const result of results) {
    if (result.success && result.content) {
      markdown += `## 第 ${result.page} 页\n\n`;
      markdown += `${result.content}\n\n`;
      markdown += `---\n\n`;
    }
  }
  
  return markdown;
}

function resolvePrompt(promptType, prompt) {
  if (promptType && DEEPSEEK_PROMPTS[promptType]) {
    log(`使用 Prompt 模板：${promptType}`, 'INFO');
    return DEEPSEEK_PROMPTS[promptType];
  }

  if (prompt && !promptType) {
    return optimizePrompt(prompt);
  }

  return DEEPSEEK_PROMPTS.default;
}

function resetPerformanceStats() {
  performanceStats.startTime = Date.now();
  performanceStats.steps = [];
}

function buildRobotReplyFromResult(result, sessionRecipient) {
  const lines = [];

  if (result?.sentToFeishu) {
    lines.push(`识别完成，结果已发送到当前${sessionRecipient?.type === 'chat_id' ? '群聊' : '会话'}。`);
  } else if (result?.sendAttempted) {
    lines.push('识别完成，但未自动发送到飞书，结果文件已保留。');
  } else {
    lines.push('识别完成。');
  }

  if (result?.content) {
    const preview = String(result.content).split('\n').slice(0, 12).join('\n').trim();
    if (preview) {
      lines.push('');
      lines.push(preview);
    }
  }

  return lines.join('\n');
}

async function executeRecognitionRequest(options) {
  const {
    imagePath,
    prompt: promptInput = null,
    promptType = null,
    pdfOption: pdfOptionInput = null,
    confirm: initialConfirm = false,
    useApiTypeDetection = false,
    showProgress = false,
    sendToFeishu = null,
    imageMode = null,
    interactive = true,
    sessionRecipient = null
  } = options;

  let prompt = promptInput;
  let pdfOption = pdfOptionInput;
  let confirm = initialConfirm;
  let selectedImageMode = imageMode;

  resetPerformanceStats();

  if (!imagePath) {
    throw new Error('未提供待识别的文件路径');
  }

  if (!fs.existsSync(imagePath)) {
    throw new Error(`文件不存在：${imagePath}`);
  }

  const isPdf = imagePath.toLowerCase().endsWith('.pdf');

  if (isPdf && !pdfOption) {
    if (interactive) {
      const interactivePdfOption = await promptForPdfOption(imagePath);

      if (interactivePdfOption === 'exit') {
        return { cancelled: true };
      }

      if (interactivePdfOption) {
        pdfOption = interactivePdfOption;
      } else {
        throw new Error('当前环境不支持交互输入，请在 OpenClaw 对话中明确指定 PDF 处理方式');
      }
    } else {
      pdfOption = 'ocr_full';
    }
  }

  if (!isPdf && !confirm) {
    if (interactive) {
      const interactiveImageMode = await promptForImageMode(imagePath);

      if (interactiveImageMode === 'exit') {
        return { cancelled: true };
      }

      if (interactiveImageMode) {
        selectedImageMode = interactiveImageMode;
        confirm = true;
      } else {
        throw new Error('当前环境不支持交互输入，请添加 --confirm 或在 OpenClaw 对话中确认处理方式');
      }
    } else {
      selectedImageMode = selectedImageMode || 'document';
      confirm = true;
    }
  }

  if (!isPdf && imageMode) {
    selectedImageMode = imageMode;
    confirm = true;
  }

  let runtimeConfig = null;
  function ensureRuntimeConfig() {
    if (runtimeConfig) {
      return runtimeConfig;
    }

    runtimeConfig = readConfig();
    if (!runtimeConfig || !runtimeConfig.imageocr) {
      throw new Error('未找到 OCR Token 配置');
    }

    const qwenModel = runtimeConfig.qwenModel || 'Sehyo/Qwen3.5-122B-A10B-NVFP4';
    log(`当前使用模型：${qwenModel}`, 'INFO');
    return runtimeConfig;
  }

  prompt = resolvePrompt(promptType, prompt);

  if (isPdf) {
    log('检测到 PDF 文件', 'INFO');
    const option = PDF_OPTIONS[pdfOption] ? pdfOption : null;

    if (!option) {
      throw new Error(`无效的 PDF 选项：${pdfOption}`);
    }

    if (!fs.existsSync(TEMP_DIR)) {
      fs.mkdirSync(TEMP_DIR, { recursive: true });
    }

    if (pdfOption === 'info') {
      const info = getPDFInfo(imagePath);
      if (!info) {
        throw new Error('获取 PDF 信息失败');
      }
      console.log('\n📄 PDF 信息：');
      console.log(`  页数：${info.pages}`);
      console.log(`  尺寸：${info.width} x ${info.height}`);
      return { success: true, type: 'pdf-info', info };
    }

    if (pdfOption === 'save_images') {
      log('正在将 PDF 转换为图片...', 'INFO');
      const images = pdfToImages(imagePath, TEMP_DIR);
      if (!images || images.length === 0) {
        throw new Error('PDF 转换失败');
      }
      console.log(`\n✅ 转换完成！共 ${images.length} 页：`);
      for (const img of images) {
        console.log(`  ${img}`);
      }
      return { success: true, type: 'pdf-images', images };
    }

    const config = ensureRuntimeConfig();
    const token = config.imageocr.token;
    let ocrPrompt = prompt;
    if (pdfOption === 'ocr_table') {
      ocrPrompt = DEEPSEEK_PROMPTS.table;
    } else if (pdfOption === 'ocr_plain') {
      ocrPrompt = DEEPSEEK_PROMPTS.plain;
    }

    log('正在将 PDF 转换为图片...', 'INFO');
    const images = pdfToImages(imagePath, TEMP_DIR);
    if (!images || images.length === 0) {
      throw new Error('PDF 转换失败');
    }

    log(`PDF 共 ${images.length} 页，开始逐页识别...`, 'INFO');
    const results = [];
    const avgPageTime = 15000;

    for (let i = 0; i < images.length; i++) {
      const pageImage = images[i];
      const pageNum = i + 1;
      const remainingPages = images.length - pageNum;
      const estimatedRemainingTime = remainingPages * avgPageTime;

      if (showProgress) {
        console.log(`\n[${'='.repeat(50)}]`);
        console.log(`📄 第 ${pageNum} 页 / 共 ${images.length} 页 (${((pageNum/images.length)*100).toFixed(0)}%)`);
        console.log(`⏱️  预计剩余：${(estimatedRemainingTime / 1000).toFixed(1)}秒`);
        console.log(`${'='.repeat(50)}\n`);
      } else {
        console.log(`\n${'='.repeat(60)}`);
        console.log(`📄 第 ${pageNum} 页 / 共 ${images.length} 页`);
        console.log(`⏱️  预计剩余：${(estimatedRemainingTime / 1000).toFixed(1)}秒`);
        console.log(`${'='.repeat(60)}\n`);
      }

      const cachedResult = getCachedResult(pageImage);
      if (cachedResult) {
        console.log('使用缓存结果');
        console.log(cachedResult.choices[0].message.content);
        results.push({ page: pageNum, success: true, content: cachedResult.choices[0].message.content });
        console.log('\n');
        continue;
      }

      const pageStart = Date.now();
      const result = await processSinglePageWithRetry(pageImage, ocrPrompt, config, token);
      const pageDuration = Date.now() - pageStart;

      if (showProgress) {
        console.log(`⏱️  本页耗时：${pageDuration}ms\n`);
      }

      if (result && result.choices?.[0]?.message?.content) {
        result.choices[0].message.content = sanitizeModelOutput(result.choices[0].message.content);
        const validation = validateResult(result.choices[0].message.content);
        if (!validation.valid) {
          log(`结果验证失败：${validation.reason}`, 'WARN');
        }
        console.log(result.choices[0].message.content);
        results.push({ page: pageNum, success: true, content: result.choices[0].message.content });
        saveToCache(pageImage, result);
      } else {
        console.log('⚠️ 识别失败或超时，跳过此页');
        results.push({ page: pageNum, success: false, content: null });
      }

      console.log('\n');
      try {
        if (fs.existsSync(pageImage)) {
          fs.unlinkSync(pageImage);
          log(`已清理临时文件：${path.basename(pageImage)}`, 'DEBUG');
        }
      } catch (e) {}

      if (i < images.length - 1) {
        console.log('⏳ 等待 2 秒后处理下一页...');
        await new Promise(resolve => setTimeout(resolve, 2000));
      }
    }

    if (showProgress) {
      printPerformanceStats();
    }

    console.log(`${'='.repeat(60)}`);
    console.log('✅ 全部页面识别完成！');
    console.log(`${'='.repeat(60)}`);

    const successCount = results.filter(r => r.success).length;
    const failCount = results.filter(r => !r.success).length;
    console.log(`\n📊 识别统计：成功 ${successCount} 页，失败 ${failCount} 页`);
    if (failCount > 0) {
      console.log(`失败页面：${results.filter(r => !r.success).map(r => r.page).join(', ')}`);
    }

    const markdown = generateMarkdownResult(path.basename(imagePath), results, successCount, failCount);
    const markdownPath = path.join(TEMP_DIR, 'result.md');
    fs.writeFileSync(markdownPath, markdown);
    console.log(`\n📄 Markdown 文件已保存：${markdownPath}`);

    const sentToFeishu = await handleMarkdownDelivery(markdownPath, config, sendToFeishu, sessionRecipient);
    return {
      success: true,
      type: 'pdf',
      content: markdown,
      markdownPath,
      sentToFeishu,
      sendAttempted: sendToFeishu ?? config?.autoSendToFeishu ?? true
    };
  }

  const config = ensureRuntimeConfig();
  const token = config.imageocr.token;

  log('正在识别图片：' + imagePath, 'INFO');
  const imageBase64 = readFileAsBase64(imagePath);
  if (!imageBase64) {
    throw new Error('读取图片失败');
  }

  const imageStart = Date.now();
  const imageType = selectedImageMode || (useApiTypeDetection ? await detectImageType(imageBase64, config) : 'document');
  log(`图片类型：${imageType === 'document' ? '文档类' : '照片/图片类'}`, 'INFO');

  if (imageType === 'document') {
    const promptRequestedHandwriting = isHandwritingPrompt(prompt);
    const ocrPrompt = promptRequestedHandwriting ? DEEPSEEK_PROMPTS.handwriting : DEEPSEEK_PROMPTS.default;

    log('第一步：ImageOCR 识别...', 'INFO');
    const ocrResult = await callImageOCR(config.imageocr.token, config.imageocr.endpoint, imageBase64, ocrPrompt);
    const ocrContent = ocrResult?.choices?.[0]?.message?.content || '';

    const ocrValidation = validateResult(ocrContent);
    const handwritingDecision = await shouldUseHandwritingMode(imageBase64, ocrContent, prompt, token);
    const handwritingMode = handwritingDecision.enabled;
    log(`手写自动判定：${handwritingMode ? '启用' : '关闭'}（依据：${handwritingDecision.reason}）`, 'INFO');
    let finalResult = null;
    let outputTitle = '识别结果';

    if (handwritingMode) {
      finalResult = await recognizeHandwritingDocument(imageBase64, ocrContent, token, prompt);

      if (!finalResult?.choices?.[0]?.message?.content && !ocrValidation.valid) {
        log(`OCR 未识别出有效内容：${ocrValidation.reason}`, 'WARN');
        log('手写模式识别失败，切换到多模态图片描述...', 'INFO');
        outputTitle = '图片描述';
        finalResult = await callQwen(token, imageBase64, IMAGE_DESCRIPTION_PROMPT, false, null);
      }

      if (!finalResult?.choices?.[0]?.message?.content && ocrContent.trim()) {
        log('手写模式整合失败，回退到 OCR 原始结果', 'WARN');
        finalResult = wrapContentAsResult(ocrContent);
      }
    } else if (!ocrValidation.valid) {
      log(`OCR 未识别出有效内容：${ocrValidation.reason}`, 'WARN');
      log('第二步：切换到多模态图片描述...', 'INFO');
      outputTitle = '图片描述';
      finalResult = await callQwen(token, imageBase64, IMAGE_DESCRIPTION_PROMPT, false, null);

      if (!finalResult?.choices?.[0]?.message?.content && ocrContent.trim()) {
        log('多模态描述失败，回退到 OCR 原始结果', 'WARN');
        outputTitle = '识别结果';
        finalResult = wrapContentAsResult(ocrContent);
      }
    } else {
      log('第二步：发送 OCR Markdown 和原图给大模型，输出最终 Markdown...', 'INFO');
      const multimodalPrompt = buildDocumentIntegrationPrompt(ocrContent, prompt);
      finalResult = await callQwen(token, imageBase64, multimodalPrompt, false, null);

      if (!finalResult?.choices?.[0]?.message?.content) {
        log('大模型整合失败，回退到 OCR 结果', 'WARN');
        finalResult = wrapContentAsResult(ocrContent);
      }
    }

    if (!finalResult) {
      throw new Error('识别失败');
    }

    log('识别完成', 'INFO');
    const finalContent = sanitizeModelOutput(finalResult.choices?.[0]?.message?.content || finalResult.text || JSON.stringify(finalResult, null, 2));

    if (finalResult?.choices?.[0]?.message) {
      finalResult.choices[0].message.content = finalContent;
    }

    console.log(`\n--- ${outputTitle} ---`);
    console.log(finalContent);

    const markdown = `# ${path.basename(imagePath)}\n\n## ${outputTitle}\n\n${finalContent}\n\n---\n\n*识别时间：${new Date().toLocaleString('zh-CN')}*\n`;
    const markdownPath = path.join(TEMP_DIR, 'result.md');
    if (!fs.existsSync(TEMP_DIR)) {
      fs.mkdirSync(TEMP_DIR, { recursive: true });
    }
    fs.writeFileSync(markdownPath, markdown);
    console.log(`\n📄 Markdown 文件已保存：${markdownPath}`);

    const imageDuration = Date.now() - imageStart;
    performanceStats.steps.push({ step: '图片识别总耗时', duration: imageDuration });
    if (showProgress) {
      printPerformanceStats();
    }

    const sentToFeishu = await handleMarkdownDelivery(markdownPath, config, sendToFeishu, sessionRecipient);
    return {
      success: true,
      type: 'image',
      content: finalContent,
      markdownPath,
      sentToFeishu,
      sendAttempted: sendToFeishu ?? config?.autoSendToFeishu ?? true
    };
  }

  log('图片类型为照片/图片，直接输出描述...', 'INFO');
  const descriptionPrompt = '请详细描述这张图片的内容，包括场景、物体、人物、颜色等可见元素。';
  const result = await callQwen(token, imageBase64, descriptionPrompt, false, null);
  if (!result?.choices?.[0]?.message?.content) {
    throw new Error('图片描述失败');
  }

  log('描述完成', 'INFO');
  result.choices[0].message.content = sanitizeModelOutput(result.choices[0].message.content);
  console.log('\n--- 图片描述 ---');
  console.log(result.choices[0].message.content);

  const imageDuration = Date.now() - imageStart;
  performanceStats.steps.push({ step: '图片描述总耗时', duration: imageDuration });
  if (showProgress) {
    printPerformanceStats();
  }

  return {
    success: true,
    type: 'photo',
    content: result.choices[0].message.content,
    sentToFeishu: false,
    sendAttempted: false
  };
}

// ==================== 主函数 ====================

// 添加进程退出钩子，确保临时文件清理
process.on('exit', () => {
  cleanupTempDir();
});

// 添加进程异常退出钩子
process.on('uncaughtException', (error) => {
  log(`未捕获异常：${error.message}`, 'ERROR');
  cleanupTempDir(true);
  process.exit(1);
});

async function main() {
  const args = process.argv.slice(2);
  
  let imagePath = null;
  let prompt = null;
  let promptType = null;
  let pdfOption = null;
  let confirm = false;
  let useApiTypeDetection = false; // 是否使用 API 进行类型判断
  let showProgress = false; // 显示进度
  let updateConfig = false; // 更新配置
  let checkConfig = false; // 仅检查配置
  let forceConfigUpdate = false; // 强制更新配置
  let sendToFeishu = null; // 显式控制是否发送到飞书
  let selectedImageMode = null; // 交互式选择的图片处理方式
  let imageMode = null;
  let toRecipient = null; // --to 参数指定的接收者
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--image' && args[i + 1]) imagePath = args[i + 1];
    else if (args[i] === '--prompt' && args[i + 1]) prompt = args[i + 1];
    else if (args[i] === '--prompt-type' && args[i + 1]) promptType = args[i + 1];
    else if (args[i] === '--pdf-option' && args[i + 1]) pdfOption = args[i + 1];
    else if (args[i] === '--confirm') confirm = true;
    else if (args[i] === '--auto') confirm = true; // 跳过确认，自动处理
    else if (args[i] === '--use-api-detection') useApiTypeDetection = true;
    else if (args[i] === '--progress') showProgress = true;
    else if (args[i] === '--update-config') updateConfig = true;
    else if (args[i] === '--check') checkConfig = true;
    else if (args[i] === '--force') forceConfigUpdate = true;
    else if (args[i] === '--send-to-feishu') sendToFeishu = true;
    else if (args[i] === '--no-send-to-feishu') sendToFeishu = false;
    else if (args[i] === '--image-mode' && args[i + 1]) imageMode = args[i + 1];
    else if (args[i] === '--to' && args[i + 1]) toRecipient = args[i + 1];
    else if (args[i].startsWith('--image=')) imagePath = args[i].split('=')[1];
    else if (args[i].startsWith('--prompt=')) prompt = args[i].split('=')[1];
    else if (args[i].startsWith('--prompt-type=')) promptType = args[i].split('=')[1];
    else if (args[i].startsWith('--pdf-option=')) pdfOption = args[i].split('=')[1];
    else if (args[i].startsWith('--confirm=')) confirm = args[i].split('=')[1] === 'true';
    else if (args[i].startsWith('--auto=')) confirm = args[i].split('=')[1] !== 'false';
    else if (args[i].startsWith('--use-api-detection=')) useApiTypeDetection = args[i].split('=')[1] === 'true';
    else if (args[i].startsWith('--progress=')) showProgress = args[i].split('=')[1] === 'true';
    else if (args[i].startsWith('--update-config=')) updateConfig = args[i].split('=')[1] === 'true';
    else if (args[i].startsWith('--check=')) checkConfig = args[i].split('=')[1] === 'true';
    else if (args[i].startsWith('--force=')) forceConfigUpdate = args[i].split('=')[1] === 'true';
    else if (args[i].startsWith('--send-to-feishu=')) sendToFeishu = args[i].split('=')[1] === 'true';
    else if (args[i].startsWith('--image-mode=')) imageMode = args[i].split('=')[1];
    else if (args[i].startsWith('--to=')) toRecipient = args[i].split('=')[1];
    else if (args[i].startsWith('--show-progress=')) showProgress = args[i].split('=')[1] === 'true';
  }

  // 如果请求更新配置
  if (updateConfig) {
    const updateScript = path.join(__dirname, 'update-config.js');
    const updateArgs = [];
    if (checkConfig) updateArgs.push('--check');
    if (forceConfigUpdate) updateArgs.push('--force');

    log(checkConfig ? '正在检查配置...' : '正在更新配置...', 'INFO');
    try {
      execFileSync('node', [updateScript, ...updateArgs], { stdio: 'inherit' });
      log(checkConfig ? '配置检查完成！' : '配置更新完成！', 'SUCCESS');
      process.exit(0);
    } catch (error) {
      log(`配置更新失败：${error.message}`, 'ERROR');
      process.exit(1);
    }
  }

  if (!imagePath) {
    console.log('用法：');
    console.log('  node index.js --image /path/to/image.jpg');
    console.log('  node index.js --image /path/to/file.pdf --pdf-option ocr_full');
    console.log('  node index.js --image /path/to/image.jpg --confirm');
    console.log('  node index.js --image /path/to/file.pdf --progress');
    console.log('  node index.js --update-config              智能检测并更新配置（仅在必要时）');
    console.log('  node index.js --update-config --check      仅检查配置状态');
    console.log('  node index.js --image /path/to/image.jpg --confirm --send-to-feishu');
    console.log('  node index.js --image /path/to/image.jpg --confirm --no-send-to-feishu');
    console.log('  或在 OpenClaw 中直接说：识别图片 /path/to/image.jpg');
    console.log('');
    console.log('PDF 选项：');
    for (const [key, label] of Object.entries(PDF_OPTIONS)) {
      console.log(`  --pdf-option=${key}  ${label}`);
    }
    console.log('');
    console.log('其他选项：');
    console.log('  --progress              显示进度和性能统计');
    console.log('  --update-config         智能检测并更新配置（仅在必要时）');
    console.log('  --update-config --check 仅检查配置状态');
    console.log('  --update-config --force 强制同步 multimodal 配置');
    console.log('  --use-api-detection     使用 API 进行类型判断（默认使用扩展名）');
    console.log('  --send-to-feishu        显式开启自动发送识别结果到飞书');
    console.log('  --no-send-to-feishu     显式关闭自动发送识别结果到飞书');
    console.log('  --to "open_id:ou_xxx"   指定接收者 ID（支持 open_id:xxx 或 chat:xxx）');
    console.log('');
    console.log('Prompt 类型选项：');
    console.log('  default, table, plain, tech, finance, invoice, math');
    console.log('');
    console.log('配置更新说明:');
    console.log('  配置更新仅在必要时触发（首次安装、配置缺失、配置变更等）');
    console.log('  不会覆盖手动修改的有效配置');
    process.exit(1);
  }
  
  try {
    // 尝试从环境变量获取会话接收者（OpenClaw 集成场景）
    const sessionRecipient = parseToArg() || getRuntimeSessionRecipient();
    
    const result = await executeRecognitionRequest({
      imagePath,
      prompt,
      promptType,
      pdfOption,
      confirm,
      useApiTypeDetection,
      showProgress,
      sendToFeishu,
      imageMode,
      interactive: true,
      sessionRecipient
    });

    if (result?.cancelled) {
      console.log('已取消处理。');
      process.exit(0);
    }

    cleanupTempDir();
  } catch (error) {
    cleanupTempDir(true);
    throw error;
  }
}

async function run(context) {
  const session = context?.session || {};
  const userInput = (context?.message?.text || '').trim();
  const imagePath = extractInputFilePath(userInput);
  const explicitRecipient = parseRecipientOverrideFromText(userInput);

  if (!imagePath) {
    await context?.replyText?.('⚠️ 未识别到可处理的图片或 PDF 路径，请提供绝对路径，或把文件放到 workspace 后重试。');
    return;
  }

  // 优先使用 --to 参数，然后尝试从多种来源获取 senderId
  const sessionRecipient = explicitRecipient || 
    resolveSessionRecipientFromContext(session) || 
    getRuntimeSessionRecipient();
  try {
    await context?.replyText?.(`开始识别：${path.basename(imagePath)}`);

    const result = await executeRecognitionRequest({
      imagePath,
      prompt: null,
      promptType: null,
      pdfOption: imagePath.toLowerCase().endsWith('.pdf') ? inferPdfOptionFromText(userInput) : null,
      confirm: true,
      useApiTypeDetection: false,
      showProgress: false,
      sendToFeishu: shouldDisableFeishuDelivery(userInput) ? false : null,
      imageMode: imagePath.toLowerCase().endsWith('.pdf') ? null : inferImageModeFromText(userInput),
      interactive: false,
      sessionRecipient
    });

    if (!result?.cancelled) {
      await context?.replyText?.(buildRobotReplyFromResult(result, sessionRecipient));
    }

    cleanupTempDir();
  } catch (error) {
    cleanupTempDir(true);
    const detail = error.message || '未知错误';
    await context?.replyText?.(`❌ 识别失败：${detail}`);
  }
}

module.exports = {
  analyzeRecognitionLayout,
  buildHandwritingIntegrationPrompt,
  buildHandwritingVisionPrompt,
  buildDocumentIntegrationPrompt,
  buildFeishuTarget,
  classifyHandwritingLikelihoodFromOCR,
  detectImageTypeByExtension,
  extractInputFilePath,
  hasUsableRecognitionContent,
  isLikelyHandwritingDominantDocument,
  isLikelyShortHandwrittenNote,
  parseHandwritingDetectionResponse,
  parseRecipientOverrideFromText,
  isHandwritingPrompt,
  optimizePrompt,
  parseImageModeChoice,
  parsePdfOptionChoice,
  resolveSessionRecipientFromContext,
  run,
  sanitizeModelOutput
};

if (require.main === module) {
  main().catch(error => {
    log(`程序异常：${error.message}`, 'ERROR');
    console.error(error);
    process.exit(1);
  });
}
