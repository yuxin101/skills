import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { generateSoundAiAudio } from "./audio.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function runTest() {
  console.log("Starting SoundAI TTS local test...");
  
  const textToSynthesize = "This is a test";
  console.log(`Text to synthesize: "${textToSynthesize}"`);
  
  try {
    const result = await generateSoundAiAudio({
      text: textToSynthesize,
    }, {
      apiKey: "63QhBJB24nrg9sbhcy5yMlK/D+/3f5BaMNvWdmGsySbTnNpc5k4sdhBasd/k24udo+fzy+YebR/L8xr3xx4pjQ==",
    });
    
    const outputPath = path.resolve(__dirname, "test-output.mp3");
    fs.writeFileSync(outputPath, result.buffer);

    console.log(`\n=== TTS Generation Result ===`);
    console.log(`Successfully generated audio and saved to: ${outputPath}`);
    console.log(`Audio size: ${(result.buffer.length / 1024).toFixed(2)} KB`);
    console.log(`Mime type: ${result.mime}`);
    console.log(`===========================\n`);
    console.log("Test passed! 🎉");
  } catch (error) {
    console.error("\n❌ Test failed with error:");
    console.error(error);
  }
}

runTest();