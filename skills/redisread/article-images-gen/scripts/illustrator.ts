#!/usr/bin/env bun
/**
 * article-images-gen - 文案插图专家
 *
 * 专业的文章配图生成工具，专注于生成高质量的手绘风格插图
 * 使用阿里百炼 Qwen-Image 生成
 */

import path from "node:path";
import process from "node:process";
import { readFile, writeFile, mkdir, access, copyFile } from "node:fs/promises";
import { homedir } from "node:os";
import { generateImage } from "./image-generator";
import { analyzeArticleContent, generateOutline, generatePromptFiles } from "./article-analyzer";

type CliArgs = {
  articlePath: string | null;
  density: "minimal" | "balanced" | "per-section" | "rich" | null;
  outputDir: string | null;
  help: boolean;
};

type ExtendConfig = {
  default_output_dir?: "same-dir" | "imgs-subdir" | "illustrations-subdir" | "independent";
  language?: string;
  watermark?: {
    enabled: boolean;
    content: string;
    position: string;
  };
};

const DENSITY_OPTIONS = ["minimal", "balanced", "per-section", "rich"] as const;

function printUsage(): void {
  console.log(`Usage:
  bun scripts/illustrator.ts path/to/article.md
  bun scripts/illustrator.ts path/to/article.md --density balanced
  bun scripts/illustrator.ts --help

Options:
  --density <level>    Image density: minimal (1-2), balanced (3-4), per-section, rich (5+)
  --output-dir <path>  Override output directory
  -h, --help           Show help

Density Levels:
  minimal      Core concepts only (1-2 images)
  balanced     Major sections (3-4 images)
  per-section  At least 1 per section (recommended)
  rich         Comprehensive coverage (5+ images)
`);
}

function parseArgs(argv: string[]): CliArgs {
  const args: CliArgs = {
    articlePath: null,
    density: null,
    outputDir: null,
    help: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const current = argv[i]!;
    if (current === "--density") {
      args.density = argv[++i] as CliArgs["density"];
    } else if (current === "--output-dir") {
      args.outputDir = argv[++i] ?? null;
    } else if (current === "--help" || current === "-h") {
      args.help = true;
    } else if (!current.startsWith("-") && !args.articlePath) {
      args.articlePath = current;
    }
  }

  return args;
}

async function fileExists(filePath: string): Promise<boolean> {
  try {
    await access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function loadExtendConfig(): Promise<{
  source: "project" | "user" | null;
  config: ExtendConfig | null;
}> {
  const projectPath = path.join(process.cwd(), ".baoyu-skills/article-images-gen/EXTEND.md");
  const userPath = path.join(homedir(), ".baoyu-skills/article-images-gen/EXTEND.md");

  if (await fileExists(projectPath)) {
    const content = await readFile(projectPath, "utf8");
    return { source: "project", config: parseExtendMd(content) };
  }

  if (await fileExists(userPath)) {
    const content = await readFile(userPath, "utf8");
    return { source: "user", config: parseExtendMd(content) };
  }

  return { source: null, config: null };
}

function parseExtendMd(content: string): ExtendConfig {
  const yamlMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!yamlMatch) return {};

  const yaml = yamlMatch[1]!;
  const config: ExtendConfig = {};

  let currentKey: string | null = null;
  let currentObj: Record<string, unknown> = {};

  for (const line of yaml.split("\n")) {
    if (!line.trim()) continue;

    const match = line.match(/^(\s*)(\w+):\s*(.*)$/);
    if (!match) continue;

    const indent = match[1]!.length;
    const key = match[2]!;
    const value = match[3]!.replace(/^["']|["']$/g, "");

    if (indent === 0) {
      if (currentKey && Object.keys(currentObj).length > 0) {
        config[currentKey as keyof ExtendConfig] = currentObj as never;
      }
      currentKey = key;
      currentObj = {};
    } else if (currentKey) {
      currentObj[key] = value === "true" ? true : value === "false" ? false : value;
    }
  }

  if (currentKey && Object.keys(currentObj).length > 0) {
    config[currentKey as keyof ExtendConfig] = currentObj as never;
  }

  return config;
}

function determineOutputDir(
  articlePath: string,
  config: ExtendConfig | null,
  overrideDir: string | null
): string {
  if (overrideDir) {
    return overrideDir;
  }

  const articleDir = path.dirname(articlePath);
  const outputDirSetting = config?.default_output_dir || "imgs-subdir";

  switch (outputDirSetting) {
    case "same-dir":
      return articleDir;
    case "imgs-subdir":
      return path.join(articleDir, "imgs");
    case "illustrations-subdir":
      return path.join(articleDir, "illustrations");
    case "independent":
      const topicSlug = path.basename(articlePath, ".md").replace(/[^a-z0-9]+/g, "-");
      return path.join(process.cwd(), "illustrations", topicSlug);
    default:
      return path.join(articleDir, "imgs");
  }
}

async function readArticle(articlePath: string): Promise<string> {
  return readFile(articlePath, "utf8");
}

async function generateIllustrationsForArticle(
  articlePath: string,
  articleContent: string,
  density: string,
  outputDir: string
): Promise<void> {
  console.log(`\n📄 Analyzing article: ${articlePath}`);
  console.log(`📊 Density: ${density}`);
  console.log(`📁 Output: ${outputDir}\n`);

  // Step 1: Generate outline
  console.log("Step 1: Generating outline...");
  const outline = await generateOutline(articlePath, articleContent, density, outputDir);
  console.log(`  ✓ Outline saved to ${outputDir}/outline.md`);
  console.log(`  ✓ ${outline.image_count} illustrations planned\n`);

  // Step 2: Generate prompt files
  console.log("Step 2: Generating prompt files...");
  const promptFiles = await generatePromptFiles(outline, articleContent, outputDir);
  console.log(`  ✓ ${promptFiles.length} prompt files saved to ${outputDir}/prompts/\n`);

  // Step 3: Generate images
  console.log("Step 3: Generating images...");
  let successCount = 0;
  let failureCount = 0;

  for (const position of outline.positions) {
    const promptFile = promptFiles.find((f) =>
      f.includes(position.filename.replace(".png", ".md"))
    );

    if (!promptFile) {
      console.log(`  ✗ Illustration ${position.index}: prompt file not found`);
      failureCount++;
      continue;
    }

    const promptContent = await readFile(promptFile, "utf8");
    const promptText = extractPromptFromMarkdown(promptContent);

    const outputPath = path.join(outputDir, position.filename);

    try {
      const imageBuffer = await generateImage(promptText);
      await writeFile(outputPath, imageBuffer);
      console.log(`  ✓ Illustration ${position.index}: ${position.filename}`);
      successCount++;
    } catch (error) {
      console.log(
        `  ✗ Illustration ${position.index}: ${error instanceof Error ? error.message : String(error)}`
      );
      failureCount++;
    }
  }

  // Step 4: Update article
  console.log("\nStep 4: Updating article...");
  await updateArticleWithImages(articlePath, outline.positions, outputDir);
  console.log(`  ✓ Article updated with ${successCount} image references\n`);

  // Summary
  console.log("=".repeat(50));
  console.log("Article Illustration Complete!");
  console.log(`Article: ${articlePath}`);
  console.log(`Style: Hand-drawn Minimalist`);
  console.log(`Density: ${density}`);
  console.log(`Location: ${outputDir}`);
  console.log(`Images: ${successCount}/${outline.image_count} generated`);
  if (failureCount > 0) {
    console.log(`Failed: ${failureCount}`);
  }
}

function extractPromptFromMarkdown(content: string): string {
  // Remove YAML frontmatter
  const withoutFrontmatter = content.replace(/^---\n[\s\S]*?\n---\n/, "");
  return withoutFrontmatter.trim();
}

async function updateArticleWithImages(
  articlePath: string,
  positions: Array<{ index: number; section: string; filename: string }>,
  outputDir: string
): Promise<void> {
  const content = await readFile(articlePath, "utf8");
  const lines = content.split("\n");
  const newLines: string[] = [];

  // Compute relative path from article to images
  const articleDir = path.dirname(articlePath);
  const getRelativeImagePath = (filename: string) => {
    const imagePath = path.join(outputDir, filename);
    return path.relative(articleDir, imagePath);
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]!;
    newLines.push(line);

    // Check if this line is a section heading
    const headingMatch = line.match(/^##+\s+(.+)$/);
    if (headingMatch) {
      const heading = headingMatch[1]!.trim();

      // Check if any illustration should be inserted after this heading
      const position = positions.find((p) => p.section === heading);
      if (position) {
        const relativePath = getRelativeImagePath(position.filename);
        newLines.push(`![${position.section}](${relativePath})`);
        newLines.push("");
      }
    }
  }

  // Backup existing file
  const backupPath = `${articlePath}.bak-${Date.now()}`;
  await copyFile(articlePath, backupPath);
  console.log(`  Backup created: ${backupPath}`);

  await writeFile(articlePath, newLines.join("\n"));
}

async function main(): Promise<void> {
  const args = parseArgs(process.argv.slice(2));

  if (args.help || !args.articlePath) {
    printUsage();
    return;
  }

  // Validate article path
  if (!(await fileExists(args.articlePath))) {
    console.error(`Error: Article not found: ${args.articlePath}`);
    process.exit(1);
  }

  // Load config
  const { config } = await loadExtendConfig();
  if (config) {
    console.log("Loaded configuration");
  } else {
    console.log("No configuration found, using defaults");
  }

  // Determine density
  const density = args.density || "per-section";
  if (!DENSITY_OPTIONS.includes(density)) {
    console.error(`Error: Invalid density "${density}". Options: ${DENSITY_OPTIONS.join(", ")}`);
    process.exit(1);
  }

  // Determine output directory
  const outputDir = determineOutputDir(args.articlePath, config, args.outputDir);

  // Read article
  const articleContent = await readArticle(args.articlePath);

  // Generate illustrations
  await generateIllustrationsForArticle(args.articlePath, articleContent, density, outputDir);
}

main().catch((error) => {
  console.error("Fatal error:", error instanceof Error ? error.message : String(error));
  process.exit(1);
});
