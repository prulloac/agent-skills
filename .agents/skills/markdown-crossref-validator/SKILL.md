---
name: markdown-crossref-validator
description: Validate cross-references in markdown documents, ensuring links and references point to existing sections, headings, or files.
---

# Markdown Cross-Reference Validator

## When to use this skill
Use this skill when the user asks to validate or check cross-references in markdown files. This includes verifying that internal links (e.g., [text](#heading)) point to existing headings, and that file references (e.g., [text](file.md)) point to existing files.

## How to validate cross-references

1. **Parse the markdown document**: Read the markdown file and extract all links and references.
   - Look for patterns like `[text](#heading)`, `[text](file.md)`, `[text](file.md#heading)`, etc.
   - Also check for reference-style links: `[text][ref]` and their definitions `[ref]: url`

2. **Extract headings**: Scan the document for all headings (lines starting with #) and build a list of anchor IDs (usually lowercase, spaces to hyphens).

3. **Check internal links**:
   - For links starting with #, ensure the anchor matches an existing heading.
   - For links to other files (file.md or file.md#anchor), check if the file exists in the project.

4. **Check external links** (optional): For links to URLs, you may want to check if they are reachable, but focus on internal references first.

5. **Report issues**: List any broken references, missing files, or invalid anchors.

6. **Verify results**: Confirm that all links were processed and issues accurately identified and reported.

## Tools to use
- Use file reading tools to access markdown files.
- Use grep or parsing to extract links and headings.
- For file existence, use directory listing tools.

## Example validation process
- Read the target markdown file.
- Use regex to find links: `\[[^\]]+\]\([^)]+\)`
- For each link, if it's relative, check file existence; if it's an anchor, check heading existence.

### Sample output
- Valid internal link: [Introduction](#introduction) ✓
- Broken internal link: [Nonexistent](#missing) ✗ (Heading not found)
- Valid file link: [README](README.md) ✓
- Broken file link: [Missing](missing.md) ✗ (File not found)