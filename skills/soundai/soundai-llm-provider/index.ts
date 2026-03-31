import { defineSingleProviderPluginEntry } from "openclaw/plugin-sdk/provider-entry";

export default defineSingleProviderPluginEntry({
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
          contextWindow: 128000,
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
              contextWindow: 128000,
              maxTokens: 20000,
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
