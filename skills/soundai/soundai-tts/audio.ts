import { 
  MediaGenerationProvider,
  MediaGenerationAudioOptions,
  MediaGenerationAudioResult
} from "openclaw/plugin-sdk/media-generation";

export const DEFAULT_SOUNDAI_TTS_BASE_URL = "https://openapi-gateway-azero.soundai.com";
export const DEFAULT_SOUNDAI_TTS_VOICE = "zh-CN-XiaoxiaoNeural";

export interface SoundAITTSSettings {
  baseUrl?: string;
  apiKey?: string;
  voice?: string;
  speed?: number;
  volume?: number;
  format?: string;
  timeoutMs?: number;
}

export async function generateSoundAiAudio(
  options: MediaGenerationAudioOptions,
  settings: SoundAITTSSettings = {}
): Promise<MediaGenerationAudioResult> {
  const baseUrl = settings.baseUrl || DEFAULT_SOUNDAI_TTS_BASE_URL;
  const url = `${baseUrl}/tts-api/v3/speech`;
  const apiKey = settings.apiKey || process.env.SOUNDAI_API_KEY;
  
  if (!apiKey) {
    throw new Error("SoundAI API key is missing. Please set SOUNDAI_API_KEY in your environment or provide it in settings.");
  }

  // 构建请求体，基于提供的 curl
  const requestBody = {
    text: options.text,
    voice: settings.voice || DEFAULT_SOUNDAI_TTS_VOICE,
    speed: settings.speed ?? 1,
    volume: settings.volume ?? 80,
    format: settings.format || "mp3"
  };

  const timeoutMs = settings.timeoutMs || 30000;
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
      signal: controller.signal as any
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
        // ignore
      }
      throw new Error(`SoundAI TTS failed: ${errorMessage}`);
    }

    // TTS 接口返回的直接是音频流 (二进制数据)
    const arrayBuffer = await response.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);

    return {
      buffer,
      mime: "audio/mp3"
    };

  } catch (error: any) {
    clearTimeout(timeoutId);
    if (error.name === "AbortError") {
      throw new Error(`SoundAI TTS request timed out after ${timeoutMs}ms`);
    }
    throw error;
  }
}

export const soundAiTTSProvider: MediaGenerationProvider = {
  async generateAudio(options: MediaGenerationAudioOptions) {
    return generateSoundAiAudio(options);
  }
};