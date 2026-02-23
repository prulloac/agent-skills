---
description: Sync local and remote git repositories with conflict resolution and full change preservation
agent: build
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
```
git fetch
```

### Step 2: Check Remote Status
```
git rev-list --count HEAD..origin/$(git branch --show-current)
```
**If the count is 0:** Remote is up-to-date, proceed to Step 4
**If the count > 0:** Remote has new commits, proceed to Step 3

### Step 3: Handle Remote Updates (Only if remote is ahead)

**3a. Create a backup branch (safety measure):**
```
git branch backup-$(git branch --show-current)-$(date +%s)
```

**3b. Stash tracked changes only (preserve untracked files):**
```
git stash push -m "backup: local changes before rebase"
```

**3c. Pull with rebase:**
```
git pull --rebase origin $(git branch --show-current)
```

**3d. If rebase conflicts occur:**
- Display the conflicts to the user
- Ask user for conflict resolution approach
- User must manually resolve conflicts (or abort rebase if desired)
- Run: `git rebase --continue` or `git rebase --abort` (user choice)

**3e. Restore stashed changes:**
```
git stash pop
```

**3f. If stash conflicts occur:**
- Display conflicts clearly
- User must manually resolve or can run: `git checkout --theirs .` or `git checkout --ours .`
- Ask user before auto-resolving

### Step 4: Preserve and Prepare Untracked Files
```
git status --porcelain
```
- **Report any untracked files to user** - ask which ones to include in commits
- **Report any deleted files** - ask user if deletion was intentional
  - If unintentional: offer to restore with `git restore <file>`
  - If intentional: do NOT restore (user decision)
- **For untracked files user wants to include:**
  - Stage them: `git add <untracked-file>`
  - They will be included in the next commit
- **For untracked files user wants to keep but NOT commit:**
  - Leave them unstaged (they will be preserved but not committed)

### Step 5: Commit Workflow
- Display current changes: `git status`
- Use git-commit-workflow skill to commit all staged changes (tracked + untracked)
- User must explicitly approve each commit group
- User can choose which untracked files to include per commit
- Do NOT auto-commit without user interaction

### Step 6: Push to Remote
```
git push origin $(git branch --show-current)
```

## Key Differences from Simple Workflows

| Aspect | This Workflow | Unsafe Workflows |
|--------|---------------|------------------|
| **Untracked Files** | ✅ User decides: commit or preserve | ❌ Silently ignored or lost |
| **Deleted Files** | ✅ User confirms if accidental | ❌ Silently restored without approval |
| **Conflicts** | ✅ User resolves, decision-based | ❌ Auto-resolved, might lose data |
| **Change Approval** | ✅ Explicit user confirmation | ❌ Silent auto-commits |
| **Backup Branch** | ✅ Created before risky operations | ❌ No safety net |
| **Conflict Display** | ✅ Clear reporting to user | ❌ Automatic resolution |

## User Decision Points (MANDATORY)

The following steps REQUIRE explicit user input:

1. ✅ **Before rebasing:** Show what files will be affected
2. ✅ **During conflicts:** Ask how to resolve (manual or abort)
3. ✅ **For deleted files:** Confirm if deletion was intentional
4. ✅ **For untracked files:** Ask which files to include in commits (and which to preserve)
5. ✅ **Before committing:** Show changes and ask for approval
6. ✅ **Before pushing:** Confirm ready to publish

## Example Execution Flow

```
$ sync

[Step 1] Fetching from remote...
✅ Done

[Step 2] Checking remote status...
ℹ️  Remote is 3 commits ahead

[Step 3a] Creating backup branch...
✅ backup-main-1708445432 created

[Step 3b] Stashing tracked changes...
✅ Saved 2 file changes

[Step 3c] Pulling with rebase...
⚠️  Rebase conflict in src/config.ts
   - Ask user: (a) resolve manually, (b) abort rebase

[User chooses (a) - resolve manually]

[Step 3d] Resolving conflict...
✅ User resolved conflict

[Step 3e] Restoring stashed changes...
ℹ️  Restored 2 files

[Step 3f] Checking for stash conflicts...
✅ No conflicts

[Step 4] Checking untracked files...
⚠️  Found 2 untracked files:
   - new-feature.ts
   - config.env

User decision: "Include new-feature.ts in commit, but preserve config.env"
$ git add new-feature.ts

✅ new-feature.ts staged for commit

[Step 5] Checking for deleted files...
✅ No deleted files detected

[Step 6] Committing changes...
(User reviews and approves commits via git-commit-workflow)
✅ Committed 2 changes (including new-feature.ts)

[Step 7] Pushing to remote...
✅ Pushed 2 commits

[Result] Untracked files:
- new-feature.ts ✅ COMMITTED
- config.env ✅ PRESERVED (not committed)
```

## Safety Checklist Before Running

- [ ] All important work is saved in files (nothing in memory only)
- [ ] You have reviewed untracked files listed
- [ ] You understand which files are about to be pushed
- [ ] You have a backup if needed (backup branch will be created automatically)

## Abort Points

At any time during this workflow, if something seems wrong:
- **During rebase conflicts:** Run `git rebase --abort` to cancel the rebase
- **During stash conflicts:** Use `git diff` to review conflicts, then `git checkout` to resolve
- **Before push:** Run `git reset --soft HEAD~N` to undo recent commits (where N is the number of commits)