import type { MediaUnderstandingProvider } from "openclaw/plugin-sdk/media-understanding";
import { transcribeSoundAiAudio } from "./audio.js";

export const soundaiMediaUnderstandingProvider: MediaUnderstandingProvider = {
  id: "soundai",
  capabilities: ["audio"],
  transcribeAudio: transcribeSoundAiAudio,
};
