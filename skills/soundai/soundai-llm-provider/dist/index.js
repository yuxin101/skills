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
var soundAiProvider = {
  id: "soundai",
  label: "SoundAI",
  auth: [
    {
      id: "api-key",
      label: "API Key",
      type: "secret",
      hint: "Enter your SoundAI API Key (e.g. CqTMsc...)"
    }
  ],
  catalog: {
    run: async (ctx) => {
      const auth = ctx.resolveProviderApiKey("soundai");
      return {
        provider: {
          baseUrl: "https://openapi-gateway-azero.soundai.com",
          api: "openai-completions",
          apiKey: auth.apiKey,
          models: [
            {
              id: "soundai/azerogpt",
              name: "AzeroGPT",
              reasoning: false,
              input: ["text"],
              cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
              contextWindow: 128e3,
              maxTokens: 2e4,
              compat: {
                supportsTools: false
              }
            }
          ]
        }
      };
    }
  }
};
var index_default = {
  id: "soundai-llm-provider",
  name: "SoundAI LLM Provider",
  description: "Native SoundAI LLM Provider",
  register: (api) => {
    api.registerProvider(soundAiProvider);
  }
};
