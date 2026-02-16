# Grouping Changes for Commits

When committing changes, it's important to group related files together to maintain a clean and logical git history. This makes it easier to understand what was changed and why.

## Principles

- **Atomic commits**: Each commit should represent a single logical change
- **Related changes together**: Files that contribute to the same feature, fix, or refactoring should be committed together
- **Separate concerns**: Different types of changes (feature, bug fix, documentation) should be in separate commits

## Common Grouping Strategies

### By Feature or Functionality
- All files implementing a new feature
- Example: UI component files, backend API, database migrations, tests for the feature

### By Bug Fix
- Files modified to fix a specific bug
- Example: Code changes, updated tests, documentation fixes related to the bug

### By Refactoring
- Files changed during code restructuring or optimization
- Example: Renamed functions across multiple files, code cleanup, performance improvements

### By Documentation
- Only documentation files (README, API docs, comments)
- Example: Updated README.md, added docstrings, wiki pages

### By Tests
- Test files related to recent changes
- Example: New test cases, updated existing tests

### By Dependencies
- Changes to package files, lock files, configuration
- Example: Updated package.json, requirements.txt, CI configuration

## When to Split Commits

- When changes affect multiple unrelated features
- When a commit would be too large (>500 lines changed)
- When mixing breaking changes with non-breaking changes

## When to Combine Commits

- When changes are interdependent and wouldn't work separately
- When changes are small and related (e.g., fixing a typo in multiple files)