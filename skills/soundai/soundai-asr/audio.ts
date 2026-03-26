import path from "node:path";
import type {
  AudioTranscriptionRequest,
  AudioTranscriptionResult,
} from "openclaw/plugin-sdk/media-understanding";
import {
  assertOkOrThrowHttpError,
  normalizeBaseUrl,
  postTranscriptionRequest,
  requireTranscriptionText,
} from "openclaw/plugin-sdk/media-understanding";

export const DEFAULT_SOUNDAI_AUDIO_BASE_URL = "https://openapi-gateway-azero.soundai.com";
export const DEFAULT_SOUNDAI_AUDIO_MODEL = "AzeroAsr-V1-Gasr";

function resolveModel(model?: string): string {
  const trimmed = model?.trim();
  return trimmed || DEFAULT_SOUNDAI_AUDIO_MODEL;
}

export async function transcribeSoundAiAudio(
  params: AudioTranscriptionRequest,
): Promise<AudioTranscriptionResult> {
  const fetchFn = params.fetchFn ?? fetch;
  // Allows user to override baseUrl in config, otherwise defaults to the gateway union url
  const baseUrl = normalizeBaseUrl(params.baseUrl, DEFAULT_SOUNDAI_AUDIO_BASE_URL);
  const allowPrivate = Boolean(params.baseUrl?.trim());
  const url = `${baseUrl}/api/asr/recognize`;

  const model = resolveModel(params.model);
  const form = new FormData();
  
  const fileName = params.fileName?.trim() || path.basename(params.fileName || "") || "audio.m4a";
  const bytes = new Uint8Array(params.buffer);
  const blob = new Blob([bytes], {
    type: params.mime ?? "application/octet-stream",
  });
  // Node 18 fetch / FormData compat: attach name correctly 
  // Node 18 lacks native `File`, so we attach it as a Blob but `form.append` will still use the 3rd argument as filename
  
  const ext = path.extname(fileName).slice(1).toLowerCase() || "mp3";

  // Construct the specific SoundAI JSON payload
  const requestPayload = {
    provider: "soundai",
    model: model,
    audioType: "file",
    audioFormat: ext,
    sampleRate: 16000,
    language: params.language?.trim() || "zh",
    enablePunctuation: true, // Typically we want punctuation for OpenClaw ASR
    enableITN: true,
    extraParams: {},
  };

  form.append("request", JSON.stringify(requestPayload));
  form.append("file", blob, fileName);

  const headers = new Headers(params.headers);
  if (!headers.has("authorization")) {
    // Note: the curl example uses SaiApi token format
    headers.set("authorization", `SaiApi ${params.apiKey}`);
  }
  // DO NOT set Content-Type header manually when using FormData, fetch will automatically set it with the correct boundary.

  const { response: res, release } = await postTranscriptionRequest({
    url,
    headers,
    body: form,
    timeoutMs: params.timeoutMs,
    fetchFn,
    allowPrivateNetwork: allowPrivate,
  });

  try {
    await assertOkOrThrowHttpError(res, "SoundAI Audio transcription failed");

    const payload = (await res.json()) as any;
    
    // Extract the text from SoundAI's response format: {"result":{"text":"..."}}
    const rawText = payload?.result?.text ?? payload?.text;
    
    const transcript = requireTranscriptionText(
      rawText,
      "SoundAI Audio transcription response missing text field",
    );
    return { text: transcript, model };
  } finally {
    await release();
  }
}
