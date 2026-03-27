import { definePluginEntry } from "openclaw/plugin-sdk";
import { soundAiTTSProvider } from "./audio.js";

export default definePluginEntry({
  mediaGeneration: {
    "soundai-tts": soundAiTTSProvider
  }
});