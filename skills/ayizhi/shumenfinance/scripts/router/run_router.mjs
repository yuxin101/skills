import { isMain, parseCommonArgs, printJson } from "../core/cli.mjs";
import { runDataRequest } from "../flows/run_data_request.mjs";
import { runMovementAnalysis } from "../flows/run_movement_analysis.mjs";

export async function runRouter(positionals, values) {
  const command = positionals[0] ?? "data-request";

  if (command === "data-request") {
    return runDataRequest(values);
  }

  if (command === "movement-analysis") {
    return runMovementAnalysis(values);
  }

  throw new Error(`Unsupported router command: ${command}`);
}

if (isMain(import.meta)) {
  const { values, positionals } = parseCommonArgs({ allowPositionals: true });
  const result = await runRouter(positionals, values);
  printJson(result);
}
