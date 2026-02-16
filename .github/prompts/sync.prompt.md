---
description: Sync local and remote repositories with fetch, rebase, stash handling, commit, and push
---

Always begin with a git fetch, then check if the remote branch is ahead by any amount of commits. If it is, then you should stash current changes, do a pull --rebase from the remote branch, resolve any conflict, then apply the stashed changes, again resolve any conflicts. After that, now that you have no pending changes from the remote repository, you can use the git-commit-workflow skill to commit the current workspace changes. Once there are no changes pending to be committed, you can do a git push to sync both local and remote repositories.