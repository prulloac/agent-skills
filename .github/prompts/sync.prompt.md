---
description: Sync local and remote git repositories with conflict resolution
agent: agent
tools: [execute]
---

Your task is to sync the local git repository with the remote, following this exact workflow:

1. Always begin with a git fetch to get the latest remote changes.
2. Check if the remote branch is ahead by any amount of commits using `git rev-list --count HEAD..origin/$(git branch --show-current)`.
3. If the remote is ahead (count > 0):
   - Stash current changes: `git stash`
   - Perform a pull with rebase: `git pull --rebase origin $(git branch --show-current)`
   - Resolve any merge conflicts that arise during rebase.
   - Continue the rebase: `git rebase --continue` after resolving.
4. Apply the stashed changes: `git stash pop`
5. Resolve any conflicts from applying the stash.
6. Now that there are no pending remote changes, use the git-commit-workflow skill to commit the current workspace changes.
7. Once there are no changes pending to be committed, push to sync: `git push origin $(git branch --show-current)`

Execute each step sequentially, resolving conflicts as needed. Use the terminal tool for git commands.