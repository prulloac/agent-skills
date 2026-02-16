---
description: Brief description of the prompt
name: command-name  # optional, defaults to file name
argument-hint: Hint for arguments  # optional
agent: agent-name  # optional: ask, agent, plan, or custom agent
model: model-name  # optional
tools: ['tool1', 'tool2']  # optional list of tools
---

Your prompt instructions here.

Use variables like ${selection}, ${file}, ${input:variableName}.

Reference files with [label](relative/path).

Use #tool:tool-name to reference tools.