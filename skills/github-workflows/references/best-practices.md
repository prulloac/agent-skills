# GitHub Workflows Best Practices

## Table of Contents

- [Security](#security)
- [Performance](#performance)
- [Reliability](#reliability)
- [Maintainability](#maintainability)

## Security

### Principle of Least Privilege

Set minimal permissions at the workflow level and escalate per job:

```yaml
permissions: read-all  # Workflow-level: minimal

jobs:
  build:
    # No extra permissions needed - inherits read-all
    steps: [...]

  deploy:
    permissions:
      contents: read
      id-token: write  # Only this job needs OIDC
    steps: [...]
```

### Pin Actions by SHA

Pin third-party actions to full commit SHAs, not tags. Tags can be moved to point to different commits.

```yaml
# Secure
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1

# Insecure - tag can be reassigned
- uses: actions/checkout@v4
```

Exception: Official `actions/*` from GitHub are lower risk and may be pinned to major version tags for readability.

### Secrets Handling

- Never echo, log, or write secrets to files that are uploaded as artifacts.
- Use `environment` protection rules for deployment secrets.
- Prefer OIDC (`id-token: write`) over long-lived credentials when deploying to cloud providers.
- Scope secrets to specific environments when possible.

### Fork and PR Security

- `pull_request` trigger runs in the fork's context with read-only token -- safe for untrusted code.
- `pull_request_target` runs in the base repo's context with write token -- dangerous with untrusted code.
- Never use `pull_request_target` with `actions/checkout` pointing at the PR head ref, as this allows arbitrary code execution with repo write access.

## Performance

### Caching

Use built-in caching in setup actions when available:

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'  # Automatic caching
```

For custom caching, use descriptive keys with restore fallbacks:

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/custom-tool
    key: ${{ runner.os }}-custom-${{ hashFiles('config.json') }}
    restore-keys: |
      ${{ runner.os }}-custom-
```

### Concurrency

Cancel redundant runs for branches and PRs:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.head_ref || github.ref }}
  cancel-in-progress: true
```

For deployment workflows, queue instead of cancel:

```yaml
concurrency:
  group: deploy-${{ inputs.environment }}
  cancel-in-progress: false
```

### Path Filtering

Limit workflow runs to relevant file changes:

```yaml
on:
  push:
    paths:
      - 'src/**'
      - 'package.json'
      - 'package-lock.json'
      - '.github/workflows/ci.yml'
```

### Job Dependency Optimization

Run independent jobs in parallel; only use `needs` for true dependencies:

```yaml
jobs:
  lint:    { ... }
  test:    { ... }
  build:   { ... }
  # These three run in parallel

  deploy:
    needs: [lint, test, build]  # Waits for all three
```

### Minimize Checkout Depth

Use shallow clone unless full history is needed:

```yaml
- uses: actions/checkout@v4  # fetch-depth: 1 (default)
```

Use `fetch-depth: 0` only when required (e.g., changelog, version detection from tags).

## Reliability

### Timeouts

Always set `timeout-minutes` on jobs to prevent hung workflows from consuming minutes:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps: [...]
```

### Retry Strategies

Use `continue-on-error` for flaky non-critical steps, combined with status checks:

```yaml
- name: Flaky integration test
  id: integration
  run: npm run test:integration
  continue-on-error: true

- name: Report flaky failure
  if: steps.integration.outcome == 'failure'
  run: echo "Integration test failed but continuing"
```

### Status Checks

Use `if:` conditions with status functions for cleanup or notification:

```yaml
- name: Cleanup on failure
  if: failure()
  run: ./cleanup.sh

- name: Notify on completion
  if: always()
  run: ./notify.sh ${{ job.status }}
```

### Idempotent Steps

Design steps to be safely re-runnable. This is important because workflows can be re-triggered:

- Use `--if-not-exists` flags when creating resources.
- Check state before modifying.
- Use `terraform plan` before `terraform apply`.

## Maintainability

### Reusable Workflows

Extract common patterns into reusable workflows:

```yaml
# .github/workflows/reusable-build.yml
on:
  workflow_call:
    inputs:
      node-version:
        type: string
        default: '20'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci && npm run build
```

### Composite Actions

For reusable step sequences, create composite actions:

```yaml
# .github/actions/setup-project/action.yml
name: Setup Project
inputs:
  node-version:
    default: '20'
runs:
  using: composite
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: npm
    - run: npm ci
      shell: bash
```

### Workflow Organization

Suggested file structure for `.github/workflows/`:

```
.github/
├── workflows/
│   ├── ci.yml              # Main CI pipeline
│   ├── cd.yml              # Deployment pipeline
│   ├── release.yml         # Release automation
│   ├── pr-checks.yml       # PR-specific checks
│   ├── scheduled.yml       # Cron jobs
│   └── reusable-*.yml      # Reusable workflows
└── actions/
    └── setup-project/      # Composite actions
        └── action.yml
```

### Naming Conventions

- **Workflow names**: Descriptive, title case (`CI`, `Deploy to Production`, `Release`)
- **Job IDs**: Lowercase, hyphenated (`build-and-test`, `deploy-staging`)
- **Step names**: Imperative verbs (`Checkout code`, `Run tests`, `Upload artifact`)
- **File names**: Lowercase, hyphenated, descriptive (`ci.yml`, `deploy-production.yml`)
