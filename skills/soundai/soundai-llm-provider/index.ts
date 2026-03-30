// Direct export, no openclaw SDK import needed here at runtime for basic config
const soundAiProvider: any = {
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
    run: async (ctx: any) => {
      // Get the API key from context (either from ENV or UI settings)
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
              contextWindow: 128000,
              maxTokens: 20000,
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

export default {
  id: "soundai-llm-provider",
  name: "SoundAI LLM Provider",
  description: "Native SoundAI LLM Provider",
  register: (api: any) => {
    api.registerProvider(soundAiProvider);
  }
};
