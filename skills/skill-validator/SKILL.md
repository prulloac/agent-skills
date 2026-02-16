---
name: skill-validator
description: Validate agent skills for correctness, readability, workflow clarity, and isolation, ensuring they can be installed independently without dependencies on other skills.
---

# Skill Validator

## When to use this skill
Use this skill when you need to validate an agent skill folder, checking its structure, content, and adherence to best practices. This includes verifying frontmatter, readability, workflow definitions, validation steps, cross-references, and isolation from other skills.

## Validation steps

1. **Read the skill folder structure**: Ensure the folder contains a `SKILL.md` file. Check for optional subdirectories like `scripts/`, `references/`, `assets/`, but note that the skill must work in isolation without relying on other skills.

2. **Validate frontmatter**:
   - The `SKILL.md` file must start with YAML frontmatter containing at least `name` (short identifier) and `description` (clear indication of when to use the skill).
   - The description must be clear enough for agents to determine relevance without ambiguity.
   - The description should include either "When to use" or "Use this skill when" to clearly indicate applicability. If this phrasing is missing, it can lead to confusion about when the skill should be applied. To fix this, ensure the description contains a clear statement of the conditions or scenarios in which the skill is relevant, using one of the recommended phrases for clarity.

3. **Check cross-references**: Parse the markdown content for links and references. Ensure internal links (e.g., to headings) point to existing sections. For file references, verify they exist within the skill's directory.

4. **Assess readability and conciseness**:
   - Instructions should use clear, concise language.
   - Avoid overly verbose explanations; aim for direct, actionable content.
   - Check for grammar, spelling, and logical flow.

5. **Verify clear workflow definitions**:
   - The skill should provide step-by-step instructions for performing the task.
   - Workflows must be unambiguous, with clear prerequisites, steps, and expected outcomes.

6. **Check for validation steps**:
   - The skill must include steps at the end to validate that it was correctly executed (e.g., verify output, check for side effects).
   - This ensures the skill can confirm success or failure.

7. **Detect hallucinations**:
   - Ensure instructions do not assume or reference non-existent tools, libraries, or capabilities.
   - All referenced tools or methods must be realistic and available in standard environments.

8. **Confirm isolation**:
   - The skill should not reference or depend on other skills.
   - All necessary assets, scripts, and references must be bundled within the skill's directory.

9. **Summarize and validate execution**:
   - After completing all checks, provide a concise summary of the validation results, confirming the skill's status (valid or invalid), listing any issues, and suggesting fixes.
   - Categorize issues by severity (Critical 🚨, Warning ⚠️, Info ℹ️) and group them accordingly.
   - If issues are found, include examples and suggestions for fixes. If no issues, confirm validity with a positive note.
   - This step ensures the validation process itself was correctly executed and provides closure.

10. **Check for user information presentation examples**:
    - If the skill involves displaying or outputting information to the user (e.g., validation results, reports, or checklists), IT IS MANDATORY for it to include concrete examples of output formats.
    - Specify sample outputs, such as validation summaries with categorized issues (Critical 🚨, Warning ⚠️, Info ℹ️), checklists, or formatted messages.
    - This sets clear expectations and improves user experience by demonstrating the exact presentation style.

## Examples

### When issues are found:
🚨 **Critical Issues:**
- Missing required frontmatter (e.g., no `name` field): Fix by adding the missing field to the YAML frontmatter.

⚠️ **Warnings:**
- Unclear description: Improve by making it more specific about when to use the skill.

ℹ️ **Info:**
- Minor readability suggestions: Consider shortening verbose sections for conciseness.

### When no issues are found:
✅ **No issues found.** The skill is valid and ready for use.

## Tools to use
- File reading and parsing tools to examine `SKILL.md` and associated files.
- Markdown parsing for cross-reference checking.
- Text analysis for readability assessment.
