var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// index.ts
var index_exports = {};
__export(index_exports, {
  default: () => index_default
});
module.exports = __toCommonJS(index_exports);
var import_plugin_sdk = require("openclaw/plugin-sdk");

// audio.ts
var DEFAULT_SOUNDAI_TTS_BASE_URL = "https://openapi-gateway-azero.soundai.com";
var DEFAULT_SOUNDAI_TTS_VOICE = "zh-CN-XiaoxiaoNeural";
async function generateSoundAiAudio(options, settings = {}) {
  const baseUrl = settings.baseUrl || DEFAULT_SOUNDAI_TTS_BASE_URL;
  const url = `${baseUrl}/tts-api/v3/speech`;
  const apiKey = settings.apiKey || process.env.SOUNDAI_API_KEY;
  if (!apiKey) {
    throw new Error("SoundAI API key is missing. Please set SOUNDAI_API_KEY in your environment or provide it in settings.");
  }
  const requestBody = {
    text: options.text,
    voice: settings.voice || DEFAULT_SOUNDAI_TTS_VOICE,
    speed: settings.speed ?? 1,
    volume: settings.volume ?? 80,
    format: settings.format || "mp3"
  };
  const timeoutMs = settings.timeoutMs || 3e4;
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Authorization": `SaiApi ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(requestBody),
      signal: controller.signal
    });
    clearTimeout(timeoutId);
    if (!response.ok) {
      let errorMessage = `HTTP ${response.status} ${response.statusText}`;
      try {
        const errorText = await response.text();
        if (errorText) {
          errorMessage += ` - ${errorText}`;
        }
      } catch (e) {
      }
      throw new Error(`SoundAI TTS failed: ${errorMessage}`);
    }
    const arrayBuffer = await response.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);
    return {
      buffer,
      mime: "audio/mp3"
    };
  } catch (error) {
    clearTimeout(timeoutId);
    if (error.name === "AbortError") {
      throw new Error(`SoundAI TTS request timed out after ${timeoutMs}ms`);
    }
    throw error;
  }
}
var soundAiTTSProvider = {
  async generateAudio(options) {
    return generateSoundAiAudio(options);
  }
};

// index.ts
var index_default = (0, import_plugin_sdk.definePluginEntry)({
  mediaGeneration: {
    "soundai-tts": soundAiTTSProvider
  }
});
