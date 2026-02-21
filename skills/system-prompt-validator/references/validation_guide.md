# Validation Guide for Agent Prompts

## Criteria Details

### Objective-Driven
The prompt should clearly state the agent's purpose, goals, and intended behavior. Avoid vague or contradictory objectives.

### Clear and Readable
- Use simple, direct language
- Organize content with proper headings and structure
- Avoid jargon unless defined
- Keep sentences concise (aim for under 25 words average)

### No Duplicated Intentions
- Avoid repeating the same requirements or guidelines
- Consolidate similar instructions
- Use consistent terminology

### Valid Links
- All file references must exist in the repository
- Use relative paths for local files
- Check that links point to correct locations

### Required Sections
All agent prompts must include these sections:

1. **General Agentic Guidelines**: Core principles for agent behavior, including at least:
    - How to handle uncertainty (e.g., ask for clarification, state assumptions)
    - Avoiding training biases by prioritizing skills and tools over improvisation
    - Using in-memory todo lists for multi-step tasks (more than 2 steps)
    - Respecting agent-to-human output formats when present and explicit (ensuring they are not omitted by agents or subagents)
2. **Code Review**: Guidelines for reviewing code changes
3. **Code Generation**: Guidelines for generating code

## Common Issues and Fixes

- **Missing section**: Add the required heading and content
- **Broken link**: Update path or create the referenced file
- **Duplication**: Combine repeated statements
- **Unclear language**: Rewrite using simpler terms
- **Incomplete general guidelines**: Ensure coverage of uncertainty handling, anti-bias instructions, todo list usage, and respecting explicit output formats