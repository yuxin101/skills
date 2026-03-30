# Contributing to Doc Web Assistant Skill

This skill provides a local documentation crawler and query utility for OpenClaw.

## Use this skill when

- You need to turn a documentation URL into local JSON files
- You want OpenClaw to answer from documentation content
- You want to extract terminal commands from documentation pages

## Before reporting issues

1. Verify Python and pip are available.
2. Install dependencies from `requirements.txt`.
3. Run the script manually with `python doc_web_assistant.py --help`.
4. Test a single documentation URL before crawling many pages.

## Issue report template

```markdown
### Description
[Describe the problem]

### Reproduction Steps
1. [First step]
2. [Second step]
3. [Observed result]

### Expected Behavior
[What should happen]

### Environment
- **Skill Version:** [e.g. 0.1.0]
- **Python Version:** [output of python --version]
- **Operating System:** [e.g. Windows 11, Ubuntu 22.04]

### Additional Context
- [Input URL]
- [Error output]
- [Generated JSON examples]
```

## Updating the skill

Keep `SKILL.md` aligned with the Python command interface.
If new retrieval or execution behaviors are added, update the examples and safety rules.
