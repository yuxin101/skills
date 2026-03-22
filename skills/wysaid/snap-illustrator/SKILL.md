---
name: snap-illustrator
description: Instantly analyze markdown articles, generate prompts, and seamlessly insert AI illustrations with zero configuration required. Supports Pollinations API (zero-config) with graceful fallback to HuggingFace.
metadata:
  openclaw:
    requires:
      env:
        - HF_TOKEN
      bins:
        - node
---

# Snap Illustrator

Instantly analyze long-form markdown articles, extract core scenes, generate prompts, and seamlessly insert AI illustrations with a snap. Designed for blogs, articles, and documentation with zero configuration required.

## Trigger Scenarios
When the user asks to "illustrate this article", "add images to this markdown", "为文章配图", or "加配图".

## Design Philosophy & Zero-Config Flow

**Default to Zero-Config Experience**:
1. By default, utilize the included Node.js script to run via the unauthenticated `Pollinations.ai` API. This process is **completely zero-config** and requires NO API tokens from the user.
2. As long as images generate successfully, DO NOT ask the user to configure any tokens. Let the user experience an instant, frictionless image insertion.
3. **ONLY IF** the Node.js script throws an exception or logs `PLEASE_ASK_USER_FOR_TOKEN`, indicating the free unauthenticated service is rate-limited or unavailable, should you proactively ask the user: "The free generation service is currently busy. Do you have a HuggingFace Token you could provide to continue?"
4. If the user provides a HuggingFace Token, instruct them to set it as an environment variable (e.g., `export HF_TOKEN="<your_token>"` in their `~/.zshrc` or `~/.bash_profile`), or temporarily use the token to run the script. AI agents should NOT permanently save tokens to disk unless explicitly requested by the user.

## Execution Workflow

**Step 1: Text Analysis & Planning**
1. **Read Content**: Read the user's target Markdown file.
2. **Segmentation**: Analyze the structural and semantic boundaries of the text and partition it into sections suitable for illustrations (e.g., placing one image per major heading or roughly one per 300 words).
3. **Propose an Outline**: Before spending time generating images, present a brief "Illustration Outline" to the user. Describe how many images you plan to insert, where they will be placed, and what concepts they represent. **Wait for the user's confirmation before proceeding.**

**Step 2: Generate Prompts**
Once the user approves the outline, design high-quality, **English-only** image generation prompts for each selected insertion point.
- Suggested format: `[Core Concept/Subject], [Setting/Background], [Style Keywords], 4k, hyper-detailed, masterpiece`
- **Avoid Text Generation Constraints**: Explicitly design prompts to avoid rendering text, letters, or numbers to prevent garbled artifacts. Append a uniform style keyword (e.g., `flat vector illustration`) unless the user specified a distinct style.

**Step 3: Execute Node.js Script**
Invoke the included Node.js script using `run_in_terminal` to perform the actual image generation.

**Locating the script**: This SKILL.md file is your reference — `scripts/generate.mjs` lives in the **same directory** as this file. You already know the absolute path to this SKILL.md (it was provided to you when the skill was loaded). Strip the filename to get the skill root directory, then append `scripts/generate.mjs`.

For example, if this skill file is at `/path/to/skills/snap-illustrator/SKILL.md`, then run:
```bash
node /path/to/skills/snap-illustrator/scripts/generate.mjs --prompt "Your English Prompt Here" --output "<workspace>/images/img_name.jpg"
```
*(Note: Ensure `<workspace>` points to the absolute path of the markdown file's directory. Images should typically be placed in an `images/` subdirectory adjacent to the markdown file)*

**Step 4: Finalize & Insert**
Insert standard Markdown image syntax referencing the generated images into the original text at the appropriate boundaries:
```markdown
## Heading

![Scene: Description...](images/img_name.jpg)
Body paragraph...
```
Notify the user once all illustrations have been successfully inserted.