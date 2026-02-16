---
description: [Brief description of what this agent does]
name: [Agent Name]
tools: ['fetch', 'search']  # List of available tools
model: ['Claude Sonnet 4.5', 'GPT-5.2']  # Optional: prioritized list of models
handoffs:  # Optional: workflow transitions
  - label: Next Step
    agent: next-agent
    prompt: Continue with the next phase
---
# Agent Instructions

You are a specialized agent for [specific task or role].

## Guidelines
- [List key behaviors and instructions]
- [Include any specific workflows or processes]

## Tools Available
- Use the available tools listed in the frontmatter
- Reference tools with #tool:tool-name syntax

## Output Format
- [Specify expected output structure if needed]