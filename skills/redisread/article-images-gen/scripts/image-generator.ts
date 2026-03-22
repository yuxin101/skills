import process from "node:process";

const DEFAULT_MODEL = "qwen-image-2.0-pro";
const DEFAULT_SIZE = "1280*720";
const DEFAULT_AR = "16:9";

const SIZE_MAP: Record<string, string> = {
  "1:1": "1024*1024",
  "16:9": "1280*720",
  "9:16": "720*1280",
  "4:3": "1280*960",
  "3:4": "960*1280",
  "2:3": "768*1152",
  "3:2": "1152*768",
  "4:5": "800*1000",
  "9:19.5": "720*1560",
  "21:9": "1344*576",
};

type SocialPlatform = "default" | "social-cover" | "instagram" | "xiaohongshu" | "twitter";

const SOCIAL_PLATFORM_SETTINGS: Record<SocialPlatform, { ar: string; style: string }> = {
  default: { ar: "16:9", style: "standard" },
  "social-cover": { ar: "4:5", style: "social" },
  instagram: { ar: "4:5", style: "social" },
  xiaohongshu: { ar: "3:4", style: "social" },
  twitter: { ar: "16:9", style: "social" },
};

function getApiKey(): string | null {
  return process.env.DASHSCOPE_API_KEY || null;
}

function getBaseUrl(): string {
  const base = process.env.DASHSCOPE_BASE_URL || "https://dashscope.aliyuncs.com";
  return base.replace(/\/+$/g, "");
}

function validateSize(size: string): { width: number; height: number } {
  const match = size.replace("x", "*").match(/^(\d+)\*(\d+)$/);
  if (!match) {
    throw new Error(`Invalid size "${size}". Expected <width>x<height>.`);
  }
  const width = Number(match[1]);
  const height = Number(match[2]);
  const totalPixels = width * height;
  if (totalPixels < 512 * 512 || totalPixels > 2048 * 2048) {
    throw new Error(`Size must be between 512*512 and 2048*2048.`);
  }
  return { width, height };
}

function resolveSize(aspectRatio: string | null, size: string | null): string {
  if (size) {
    const validated = validateSize(size);
    return `${validated.width}*${validated.height}`;
  }
  const ar = aspectRatio || DEFAULT_AR;
  return SIZE_MAP[ar] || SIZE_MAP["16:9"];
}

export async function generateImage(
  prompt: string,
  options?: {
    aspectRatio?: string | null;
    size?: string | null;
    model?: string;
    socialPlatform?: SocialPlatform;
    style?: "standard" | "social";
  }
): Promise<Uint8Array> {
  const apiKey = getApiKey();
  if (!apiKey) {
    throw new Error(
      "DASHSCOPE_API_KEY environment variable is required.\n" +
        "Set it in your shell or add to .baoyu-skills/.env file."
    );
  }

  const model = options?.model || DEFAULT_MODEL;
  const socialPlatform = options?.socialPlatform || "default";
  const style = options?.style || (socialPlatform !== "default" ? "social" : "standard");

  // Override aspect ratio based on social platform if specified
  let size: string;
  if (options?.size) {
    const validated = validateSize(options.size);
    size = `${validated.width}*${validated.height}`;
  } else if (socialPlatform !== "default" && SOCIAL_PLATFORM_SETTINGS[socialPlatform]) {
    const platformAr = SOCIAL_PLATFORM_SETTINGS[socialPlatform].ar;
    size = SIZE_MAP[platformAr] || SIZE_MAP["4:5"];
  } else {
    const ar = options?.aspectRatio || DEFAULT_AR;
    size = SIZE_MAP[ar] || SIZE_MAP["16:9"];
  }

  const url = `${getBaseUrl()}/api/v1/services/aigc/multimodal-generation/generation`;

  // Build the hand-drawn style prompt
  let stylePrompt: string;

  if (style === "social") {
    // Social media optimized prompt - more engaging, emotional, story-driven
    stylePrompt = `${prompt}

【风格】手绘插画风格，具有艺术感和手工质感
【视觉吸引力】强烈的视觉焦点，清晰的视觉层次，引人注目的构图
【情感共鸣】温暖、有故事感、能引发情感共鸣的画面
【色彩】精心调配的色调，统一且有辨识度，适合社交媒体展示
【构图】专业级构图，视觉平衡，重点突出，留白适当
【细节】精致的细节处理，值得反复品味，有深度
【质感】避免 AI 生成感，追求艺术家手绘的温暖质感
【社交媒体优化】适合在手机上观看，在小屏幕上依然清晰有吸引力
【画面要求】不要任何文字、水印或签名`;
  } else {
    // Standard article illustration
    stylePrompt = `${prompt}

【风格】手绘
【氛围】简约
【画面要求】整洁、留白、构图平衡、色调统一、风格统一，不要文字`;
  }

  const body = {
    model,
    input: {
      messages: [
        {
          role: "user",
          content: [{ text: stylePrompt }],
        },
      ],
    },
    parameters: {
      prompt_extend: false,
      size,
      watermark: false,
      negative_prompt: style === "social"
        ? "文字，水印，签名，logo，品牌标识，低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有 AI 感，构图混乱，扭曲，照片写实，真实感，3D 渲染，矢量图，复杂背景，拥挤，杂乱，色彩过饱和，暗色调，阴沉，廉价感，塑料质感，游戏渲染，低质量阴影，过度锐化，噪点，模糊，色偏，比例失调，透视错误，结构错误，视觉焦点混乱，元素过多，拥挤不堪，信息过载，缺乏美感，平庸构图，俗气配色"
        : "文字，水印，签名，低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有 AI 感，构图混乱，扭曲，照片写实，真实感，3D 渲染，矢量图，复杂背景，拥挤，杂乱，色彩过饱和，暗色调，阴沉",
    },
  };

  console.log(`Generating with DashScope (${model}) - Size: ${size}`);

  // Retry logic with exponential backoff for rate limits
  const maxRetries = 3;
  let lastError: Error | null = null;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const res = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${apiKey}`,
        },
        body: JSON.stringify(body),
      });

      if (!res.ok) {
        const errText = await res.text();

        // Handle rate limiting (429)
        if (res.status === 429) {
          const retryAfter = res.headers.get("Retry-After");
          const waitTime = retryAfter ? parseInt(retryAfter, 10) * 1000 : 2000 * attempt;

          if (attempt < maxRetries) {
            console.log(`  Rate limit hit, waiting ${waitTime}ms before retry ${attempt}/${maxRetries}...`);
            await sleep(waitTime);
            continue;
          }
        }

        throw new Error(`DashScope API error (${res.status}): ${errText}`);
      }

      const result = await res.json();
      let imageData: string | null = null;

      // Extract image from response
      if (result.output?.result_image) {
        imageData = result.output.result_image;
      } else if (result.output?.choices?.[0]?.message?.content) {
        const content = result.output.choices[0].message.content;
        if (Array.isArray(content)) {
          for (const item of content) {
            if (item.image) {
              imageData = item.image;
              break;
            }
          }
        }
      }

      if (!imageData) {
        console.error("Response:", JSON.stringify(result, null, 2));
        throw new Error("No image in response");
      }

      // Download or decode image
      if (imageData.startsWith("http://") || imageData.startsWith("https://")) {
        const imgRes = await fetch(imageData);
        if (!imgRes.ok) throw new Error("Failed to download image");
        const buf = await imgRes.arrayBuffer();
        return new Uint8Array(buf);
      }

      return Uint8Array.from(Buffer.from(imageData, "base64"));
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));
      if (attempt < maxRetries && lastError.message.includes("429")) {
        continue;
      }
      throw lastError;
    }
  }

  throw lastError || new Error("Failed to generate image");
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function getDefaultModel(): string {
  return process.env.DASHSCOPE_IMAGE_MODEL || DEFAULT_MODEL;
}

export function getDefaultAspectRatio(): string {
  return DEFAULT_AR;
}

export function getDefaultSize(): string {
  return DEFAULT_SIZE;
}

export function getSocialPlatformSettings(platform: SocialPlatform): { ar: string; style: string } {
  return SOCIAL_PLATFORM_SETTINGS[platform];
}

export function getAvailableSocialPlatforms(): SocialPlatform[] {
  return Object.keys(SOCIAL_PLATFORM_SETTINGS) as SocialPlatform[];
}
