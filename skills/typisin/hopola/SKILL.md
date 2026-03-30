---
name: "Hopola"
description: "Runs web research and orchestrates image/video/3D generation, logo and product visuals, upload, and Markdown reporting. Use when users need an end-to-end multimodal production and delivery workflow."
---

# Hopola

## Purpose
Hopola turns "web research → image/video/3D generation → result upload → report output" into a reusable workflow, supporting both one-shot end-to-end execution and stage-based execution.

## When to Use
- The user needs content production based on web information and also needs visual outputs and delivery.
- The user wants one-pass execution for research, generation, upload, and consolidated reporting.
- The user only needs a specific stage (search only / generation only / upload only / report only).
- The user needs video or 3D outputs included in the same report.

## Prerequisites
- `web-access` is available for web search and page reading.
- OpenClaw Gateway is reachable.
- `OPENCLOW_KEY` is configured in the runtime environment.

## ClawHub Release Structure
- `SKILL.md`: Main orchestration and strategy
- `subskills/search/SKILL.md`: Search subskill
- `subskills/generate-image/SKILL.md`: Image generation subskill
- `subskills/generate-video/SKILL.md`: Video generation subskill
- `subskills/generate-3d/SKILL.md`: 3D generation subskill
- `subskills/logo-design/SKILL.md`: Logo design subskill
- `subskills/product-image/SKILL.md`: Product image subskill
- `subskills/upload/SKILL.md`: Upload subskill
- `subskills/report/SKILL.md`: Report subskill
- `playbooks/design-intake.md`: Design intake template and proposal framework
- `scripts/`: Release validation and packaging scripts
- `assets/`: Logo, cover, and flow diagram
- `README.zh-CN.md` / `README.en.md`: Bilingual documentation

## Execution Modes

### Mode A: Single-Entry Full Pipeline
Execute in order:
1. Search: Invoke the search subskill to extract usable facts.
2. Discover: Query Gateway MCP tools and identify image/video/3D tools.
3. Generate: Invoke the corresponding generation subskill by task type.
4. Upload: Invoke the upload subskill to submit images or result links.
5. Report: Invoke the report subskill to output a Markdown report.

### Mode B: Stage-Based Execution
Execute only one stage based on user instruction:
- SearchOnly
- GenerateImageOnly
- GenerateVideoOnly
- Generate3DOnly
- GenerateLogoOnly
- GenerateProductImageOnly
- UploadOnly
- ReportOnly

## Standard Inputs
- `query`: Search topic or target question.
- `search_scope`: Search scope and constraints (optional).
- `image_prompt`: Prompt for image generation (optional, required in GenerateImageOnly).
- `video_prompt`: Prompt for video generation (optional, required in GenerateVideoOnly).
- `model3d_prompt`: Prompt for 3D generation (optional, required in Generate3DOnly).
- `logo_prompt`: Prompt for logo generation (optional, required in GenerateLogoOnly).
- `product_prompt`: Prompt for product image generation (optional, required in GenerateProductImageOnly).
- `image_style`: Style preference (optional).
- `image_size`: Image size (optional).
- `video_ratio`: Video aspect ratio (optional).
- `video_duration`: Video duration (optional).
- `model3d_quality`: 3D quality level (optional).
- `upload_enabled`: Whether to upload results (default `true`).
- `report_format`: Fixed as `markdown`.
- `mode`: `pipeline` or `stage`.
- `task_type`: `image|video|3d|logo|product-image`.
- `stage`: When `mode=stage`, use one of `search|generate-image|generate-video|generate-3d|generate-logo|generate-product-image|upload|report`.
- `gateway_base_url`: Default `https://hopola.ai`.
- `openclaw_key_env`: Default `OPENCLOW_KEY`.

## Standard Output (Markdown)
The report must include at least:
1. Summary of search findings
2. Generation outputs (image/video/3D)
3. Upload results
4. Security status and error alerts
5. Final conclusion and next-step suggestions

## Configuration Placeholders
- `GATEWAY_BASE_URL`: Gateway domain
- `GATEWAY_MCP_TOOLS_ENDPOINT`: `/api/gateway/mcp/tools`
- `GATEWAY_MCP_CALL_ENDPOINT`: `/api/gateway/mcp/call`
- `GATEWAY_UPLOAD_IMAGE_ENDPOINT`: `/api/gateway/upload/image`
- `GATEWAY_KEY_HEADER`: `X-OpenClaw-Key`
- `IMAGE_PREFERRED_TOOL_NAME`: Preferred fixed tool for image generation
- `VIDEO_PREFERRED_TOOL_NAME`: Preferred fixed tool for video generation
- `MODEL3D_PREFERRED_TOOL_NAME`: Preferred fixed tool for 3D generation
- `MODEL3D_SECONDARY_PREFERRED_TOOL_NAME`: Secondary preferred tool for 3D generation
- `LOGO_PREFERRED_TOOL_NAME`: Preferred fixed tool for logo generation
- `PRODUCT_IMAGE_PREFERRED_TOOL_NAME`: Preferred fixed tool for product image generation
- `IMAGE_MCP_TOOL_MATCH_RULES`: Auto-discovery rules for image tools
- `VIDEO_MCP_TOOL_MATCH_RULES`: Auto-discovery rules for video tools
- `MODEL3D_MCP_TOOL_MATCH_RULES`: Auto-discovery rules for 3D tools
- `IMAGE_MCP_ARGS_SCHEMA`: Argument mapping schema for image tools
- `VIDEO_MCP_ARGS_SCHEMA`: Argument mapping schema for video tools
- `MODEL3D_MCP_ARGS_SCHEMA`: Argument mapping schema for 3D tools
- `LOGO_MCP_ARGS_SCHEMA`: Argument mapping schema for logo tools
- `PRODUCT_IMAGE_MCP_ARGS_SCHEMA`: Argument mapping schema for product image tools
- `REQUEST_TIMEOUT_MS`: Request timeout
- `RETRY_MAX`: Max retries

## Execution Rules
- In the search stage, prioritize strategic online retrieval with `web-access`; combine search and page reading when necessary.
- For all generation tasks, use "preferred fixed tool first; auto-discovery fallback if unavailable".
- For logo design, default to `aiflow_nougat_create`; for product image, default to `api_product_background_replace`.
- Logo tasks must invoke an actual generation tool and return image links, not text-only plans.
- For 3D generation, default to `3d_hy_image_generate`; for single-image input, prioritize `fal_tripo_image_to_3d`.
- In the discover stage, call `GET /api/gateway/mcp/tools` first and build arguments from returned `tool_schema`.
- In the generate stage, call `POST /api/gateway/mcp/call` with `tool_name` and `args`.
- In the upload stage, call `POST /api/gateway/upload/image` and submit the `image` field as multipart/form-data.
- All Gateway requests must include `X-OpenClaw-Key` in headers, and keys must be read only from environment variables.
- The report stage must output Markdown consistently and explicitly mark missing fields.

## Failure Handling
- Intra-stage failure: Retry by configuration, up to `RETRY_MAX`.
- Inter-stage degradation: If one stage fails, continue producing available outputs and document failure reasons in the report.
- Traceability: Record failed stage, input summary, and retry conclusion in the report.
- Permission interception: If response is `403` with `code=403001`, return `data.redirect_url` directly and prompt the user to activate membership.
- Tool unavailable: If the fixed tool is missing, automatically enable discovery fallback and record the fallback path.

## Security and Compliance
- Never expose keys, tokens, or cookies in outputs.
- Validate image format and size before upload (max 20MB).
- Return only necessary results and publicly accessible links.
- Run the release security validation script before packaging to detect plaintext keys and block packaging.
