import pluginEntry from "./index.js";

async function runTest() {
  console.log("Testing SoundAI LLM Provider Plugin configuration...");
  
  const mockCtx = {
    resolveProviderApiKey: (id: string) => {
      return { apiKey: "mock-api-key" };
    }
  };
  
  const provider = pluginEntry.register as any;
  let registeredProvider: any;
  provider({
    registerProvider: (p: any) => { registeredProvider = p; }
  });
  
  if (registeredProvider && registeredProvider.catalog) {
    const catalog = await registeredProvider.catalog.run(mockCtx);
    console.log("Successfully resolved catalog!");
    console.log(JSON.stringify(catalog, null, 2));
  } else {
    console.log("Failed to register provider.");
  }
}

runTest();
