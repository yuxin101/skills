import { buildCommonRequest, isMain, parseCommonArgs, printJson } from "../core/cli.mjs";
import { buildMovementBundle } from "../analysis/movement/bundle_builder.mjs";
import { buildMovementPromptPackage } from "../analysis/movement/prompt_builder.mjs";

export async function runMovementAnalysis(values) {
  const request = buildCommonRequest(values);
  const bundle = await buildMovementBundle(request);
  const promptPackage = buildMovementPromptPackage(bundle);

  return {
    ...bundle,
    prompt_package: promptPackage
  };
}

if (isMain(import.meta)) {
  const { values } = parseCommonArgs();
  const result = await runMovementAnalysis(values);
  printJson(result);
}
