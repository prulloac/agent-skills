---
name: git-commit-workflow
description: Skill for committing git changes following repository guidelines. Use when needing to commit staged or unstaged changes by reading CONTRIBUTING files for standards, analyzing changes with git status and diff, grouping related files, and performing commits according to guidelines or conventional commits as fallback.
---

# Git Commit Workflow

## Overview

This skill provides a structured workflow for committing git changes that respects repository-specific guidelines and falls back to conventional commits when no guidelines exist. It ensures commits are logical, well-grouped, and follow established standards.

## Workflow

Follow these steps to commit changes:

### 1. Read Repository Guidelines
- Look for CONTRIBUTING, CONTRIBUTING.md, or similar files in the repository root
- Extract commit message standards, guidelines, and any specific requirements
- If no guidelines found, prepare to use conventional commits as fallback

### 2. Assess Current Changes
- Run `git status` to see all modified, added, and untracked files
- Note staged vs unstaged changes

### 3. Analyze Changes in Detail
- Run `git diff` (and `git diff --staged` if needed) to understand what changes were made
- Review the nature of changes: bug fixes, features, refactoring, documentation, etc.

### 4. Group Related Changes
- Logically group files by related changes
- See [references/grouping_changes.md](references/grouping_changes.md) for guidance on grouping strategies
- Avoid mixing unrelated changes in the same commit

### 5. Perform Commits
- If CONTRIBUTING guidelines exist, follow their commit message format and grouping requirements
- If no guidelines, use conventional commits standard: See [references/conventional_commits.md](references/conventional_commits.md)
- Stage appropriate files for each commit
- Write descriptive commit messages
- Run `git commit` with proper messages

## Resources

### references/
- `grouping_changes.md`: Guidance on how to group related file changes into logical commits
- `conventional_commits.md`: Reference for conventional commits specification
