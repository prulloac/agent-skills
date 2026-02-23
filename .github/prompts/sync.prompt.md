---
description: Sync local and remote git repositories with conflict resolution and full change preservation
agent: agent
tools: [execute]
---

Safely synchronize local and remote git repositories while preserving all user changes (including untracked files and intentional deletions). This workflow includes explicit user approval before any changes are reverted or modified.

## Important Safety Guidelines

⚠️ **NEVER revert changes without explicit user approval**
- If a user has deleted a file, DO NOT restore it without asking
- If a user has modified a file, DO NOT discard changes without confirmation
- Always show what will happen before executing risky operations
- Untracked files are user changes and must be preserved

## Execution Workflow

Execute this workflow step by step:

### Step 1: Fetch Remote Changes
Run `git fetch` to get latest updates.

### Step 2: Check Remote Status
Check if the remote is ahead: `git rev-list --count HEAD..origin/$(git branch --show-current)`
- **If the count is 0:** Remote is up-to-date, proceed to Step 4.
- **If the count > 0:** Remote has new commits, proceed to Step 3.

### Step 3: Handle Remote Updates (Only if remote is ahead)

**3a. Create a backup branch (safety measure):**
`git branch backup-$(git branch --show-current)-$(date +%s)`

**3b. Stash tracked changes only (preserve untracked files):**
`git stash push -m "backup: local changes before rebase"`

**3c. Pull with rebase:**
`git pull --rebase origin $(git branch --show-current)`

**3d. If rebase conflicts occur:**
- Display the conflicts to the user.
- Ask user for conflict resolution approach.
- User must manually resolve conflicts (or abort rebase if desired).
- After resolution, run: `git rebase --continue` or `git rebase --abort` (user choice).

**3e. Restore stashed changes:**
`git stash pop`

**3f. If stash conflicts occur:**
- Display conflicts clearly.
- User must manually resolve or can run: `git checkout --theirs .` or `git checkout --ours .`
- Ask user before auto-resolving.

### Step 4: Preserve Untracked Files
Check for untracked files: `git status --porcelain`
- **Report any untracked files to user** - these must be preserved.
- **Report any deleted files** - ask user if deletion was intentional.
  - If unintentional: offer to restore with `git restore <file>`.
  - If intentional: do NOT restore.

### Step 5: Commit Workflow
- Display current changes: `git status`.
- Use the **git-commit-workflow** skill to commit ONLY approved changes.
- User must explicitly approve each commit group.
- Do NOT auto-commit without user interaction.

### Step 6: Push to Remote
Sync all changes: `git push origin $(git branch --show-current)`

## Key Differences from Simple Workflows

| Aspect | This Workflow | Unsafe Workflows |
|--------|---------------|------------------|
| **Untracked Files** | ✅ Preserved, reported to user | ❌ Silently ignored or lost |
| **Deleted Files** | ✅ User confirms if accidental | ❌ Silently restored without approval |
| **Conflicts** | ✅ User resolves, decision-based | ❌ Auto-resolved, might lose data |
| **Change Approval** | ✅ Explicit user confirmation | ❌ Silent auto-commits |
| **Backup Branch** | ✅ Created before risky operations | ❌ No safety net |

## User Decision Points (MANDATORY)

The following steps REQUIRE explicit user input:

1. ✅ **Before rebasing:** Show what files will be affected.
2. ✅ **During conflicts:** Ask how to resolve (manual or abort).
3. ✅ **For deleted files:** Confirm if deletion was intentional.
4. ✅ **Before committing:** Show changes and ask for approval.
5. ✅ **Before pushing:** Confirm ready to publish.

## Abort Points

At any time during this workflow, if something seems wrong:
- **During rebase conflicts:** Run `git rebase --abort` to cancel.
- **During stash conflicts:** Use `git diff` to review, then `git checkout` to resolve.
- **Before push:** Run `git reset --soft HEAD~N` to undo recent commits.
