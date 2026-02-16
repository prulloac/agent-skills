## General Agentic Guidelines

- Handle uncertainty by stating assumptions explicitly, asking for clarification when needed, and presenting multiple interpretations if they exist.
- Avoid training biases by prioritizing available skills and tools over improvisation; use established methods and libraries first.
- Use in-memory todo lists for tasks requiring more than 2 steps to track progress systematically.
- Respect agent-to-human output formats when present and explicit, ensuring they are not omitted by agents or subagents.

## Skill Discovery

Skills are located in the `.agents/skills/` directory. Each skill has its own subdirectory containing documentation and resources.

## Code Review

When reviewing code changes:
- Ensure changes directly address the user's request without unnecessary additions.
- Verify code follows project conventions, including style, naming, and structure.
- Check for potential bugs, security issues, and performance implications.
- Confirm tests are included or updated for new functionality.
- Provide constructive feedback with specific suggestions for improvements.

## Code Generation

When generating code:
- Write minimal, readable code that solves the problem without overcomplication.
- Follow existing project patterns, libraries, and conventions.
- Include appropriate error handling and comments where necessary.
- Ensure code is testable and maintainable.
- Prioritize simplicity and clarity over advanced features unless requested.

## Skill Creation 

When creating new skills:
- Ensure the skill is self-contained and does not introduce unnecessary dependencies.
- Provide clear documentation on the skill's purpose, usage, and any required inputs or outputs.
- Follow the established structure and naming conventions used by existing skills in `.agents/skills/`.
- Avoid creating skills that duplicate existing functionality; instead, consider improving or extending current skills when appropriate
- New Agent Skills should be created under skills directory located at repository root. `skills/` directory is intended for user-facing skills, while `.agents/skills/` is for internal agent use.
- New Agent Skills should not rely on scripts unless the user explicitly says so, to maintain modularity and ease of use.
- When adding a new skill, ensure it is well-documented and includes examples of how to use it effectively.
