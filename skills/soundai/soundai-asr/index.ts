import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { soundaiMediaUnderstandingProvider } from "./media-understanding-provider.js";

export default definePluginEntry({
  id: "soundai",
  name: "SoundAI Media Understanding",
  description: "SoundAI audio transcription provider",
  register(api) {
    api.registerMediaUnderstandingProvider(soundaiMediaUnderstandingProvider);
  },
});
