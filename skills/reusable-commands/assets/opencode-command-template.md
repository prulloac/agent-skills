---
description: Brief description of what this command does
agent: agent-name  # optional: e.g., build, plan, etc.
model: model-name  # optional: e.g., anthropic/claude-3-5-sonnet-20241022
subtask: false  # optional: true to force subagent
---

# Command Prompt

Your prompt instructions here.

Use placeholders like $ARGUMENTS, $1, $2, etc. for arguments.

Use !`command` to include shell output.
<!-- Security: Only use read-only, project-scoped shell commands (e.g., git diff, npm test). -->
<!-- Avoid write operations (rm, mv, chmod) or network commands that could exfiltrate data (curl, wget, nc). -->

Use @filename to reference file content.
<!-- Security: Only reference files within the project workspace. -->
<!-- Never use .. traversal or reference sensitive files (.env, private keys, credentials). -->