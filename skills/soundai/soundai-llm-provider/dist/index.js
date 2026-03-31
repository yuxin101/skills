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
var import_provider_entry = require("openclaw/plugin-sdk/provider-entry");
var index_default = (0, import_provider_entry.defineSingleProviderPluginEntry)({
  id: "soundai-llm",
  name: "SoundAI LLM Provider",
  description: "Native SoundAI LLM Provider",
  provider: {
    id: "soundai",
    label: "SoundAI",
    docsPath: "/providers/soundai",
    envVars: ["SOUNDAI_API_KEY"],
    augmentModelCatalog: async () => {
      return [
        {
          provider: "soundai",
          id: "azerogpt",
          name: "AzeroGPT",
          contextWindow: 128e3,
          reasoning: false,
          input: ["text"]
        }
      ];
    },
    auth: [
      {
        methodId: "api-key",
        label: "SoundAI API Key",
        hint: "AzeroGPT",
        optionKey: "soundaiApiKey",
        flagName: "--soundai-api-key",
        envVar: "SOUNDAI_API_KEY",
        promptMessage: "Enter SoundAI API key",
        defaultModel: "soundai/azerogpt",
        wizard: { groupLabel: "SoundAI" }
      }
    ],
    catalog: {
      buildProvider: async () => {
        return {
          baseUrl: "https://openapi-gateway-azero.soundai.com",
          api: "openai-completions",
          models: [
            {
              id: "azerogpt",
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
        };
      }
    }
  }
});
