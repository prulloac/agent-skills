---
description: Sync local and remote git repositories with conflict resolution
agent: build
---

Always begin with a git fetch, then check if the remote branch is ahead by any amount of commits. If it is, then you should stash current changes, do a pull --rebase from the remote branch, resolve any conflict, then apply the stashed changes, again resolve any conflicts. After that, now that you have no pending changes from the remote repository, you can use the git-commit-workflow skill to commit the current workspace changes. Once there are no changes pending to be committed, you can do a git push to sync both local and remote repositories.

Execute this workflow step by step:

1. `git fetch`
2. Check if remote branch is ahead: `git rev-list --count HEAD..origin/$(git branch --show-current)`
3. If ahead > 0:
   - `git stash`
   - `git pull --rebase origin $(git branch --show-current)`
   - Resolve any merge conflicts manually
   - `git rebase --continue`
4. `git stash pop`
5. Resolve any conflicts from stash application
6. Use git-commit-workflow skill to commit changes
7. `git push origin $(git branch --show-current)`