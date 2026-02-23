# GitHub Actions Workflow Syntax Reference

## Table of Contents

- [Top-Level Keys](#top-level-keys)
- [Triggers (on)](#triggers-on)
- [Jobs](#jobs)
- [Steps](#steps)
- [Expressions and Contexts](#expressions-and-contexts)
- [Permissions](#permissions)
- [Concurrency](#concurrency)
- [Environment Variables and Secrets](#environment-variables-and-secrets)
- [Matrix Strategy](#matrix-strategy)
- [Reusable Workflows](#reusable-workflows)
- [Common Pitfalls](#common-pitfalls)

## Top-Level Keys

```yaml
name: Workflow Name              # Display name (optional but recommended)
run-name: Deploy ${{ inputs.env }} # Dynamic run name (optional)

on: <trigger>                    # Required: event triggers

permissions: <permissions>       # Token permissions (recommended)
env: <env-vars>                  # Workflow-level env vars
defaults:                        # Default settings
  run:
    shell: bash
    working-directory: ./src
concurrency: <concurrency>      # Concurrency control

jobs: <jobs>                     # Required: job definitions
```

## Triggers (on)

### Push / Pull Request

```yaml
on:
  push:
    branches: [main, 'release/**']
    tags: ['v*']
    paths: ['src/**', '!src/**/*.test.*']
    paths-ignore: ['docs/**', '*.md']
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]
```

- `branches` and `tags` support glob patterns.
- `paths` and `paths-ignore` are mutually exclusive.
- `pull_request` defaults to types: `[opened, synchronize, reopened]`.
- Use `pull_request_target` for workflows that need write access on fork PRs (security-sensitive).

### Other Common Triggers

```yaml
on:
  workflow_dispatch:           # Manual trigger
    inputs:
      environment:
        description: 'Target environment'
        required: true
        default: 'staging'
        type: choice
        options: [staging, production]
      dry-run:
        description: 'Dry run only'
        type: boolean
        default: false

  schedule:
    - cron: '30 5 * * 1-5'    # Weekdays at 05:30 UTC

  release:
    types: [published]

  workflow_call:               # Reusable workflow trigger
    inputs:
      config:
        required: true
        type: string
    secrets:
      token:
        required: true

  workflow_run:                # After another workflow completes
    workflows: [Build]
    types: [completed]
```

### Cron Syntax

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, Sun=0)
│ │ │ │ │
* * * * *
```

Minimum interval: every 5 minutes. Scheduled workflows run on the default branch only.

## Jobs

```yaml
jobs:
  build:
    name: Build Application
    runs-on: ubuntu-latest          # Required
    timeout-minutes: 30             # Default: 360
    needs: [lint, test]             # Job dependencies
    if: github.event_name == 'push' # Conditional execution
    environment:                    # Deployment environment
      name: production
      url: ${{ steps.deploy.outputs.url }}
    outputs:
      version: ${{ steps.version.outputs.value }}
    services:                       # Sidecar containers
      postgres:
        image: postgres:16
        ports: ['5432:5432']
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    container:                      # Run job in container
      image: node:20
      credentials:
        username: ${{ github.actor }}
        password: ${{ secrets.GHCR_TOKEN }}
    steps: []
```

### Runner Labels

| Label | OS |
|---|---|
| `ubuntu-latest` | Ubuntu 24.04 (alias updates) |
| `ubuntu-22.04` | Ubuntu 22.04 |
| `ubuntu-24.04` | Ubuntu 24.04 |
| `windows-latest` | Windows Server 2022 |
| `macos-latest` | macOS 14 (M1) |
| `macos-13` | macOS 13 (Intel) |

### Job Outputs

Declare outputs at job level; set them in steps:

```yaml
jobs:
  build:
    outputs:
      artifact-id: ${{ steps.upload.outputs.artifact-id }}
    steps:
      - id: upload
        run: echo "artifact-id=abc123" >> "$GITHUB_OUTPUT"
```

## Steps

```yaml
steps:
  - name: Checkout
    uses: actions/checkout@v4
    with:
      fetch-depth: 0

  - name: Run script
    id: script
    run: |
      echo "value=result" >> "$GITHUB_OUTPUT"
      echo "### Summary" >> "$GITHUB_STEP_SUMMARY"
    env:
      MY_VAR: ${{ secrets.MY_SECRET }}
    working-directory: ./src
    shell: bash
    continue-on-error: true
    timeout-minutes: 10
    if: success()
```

### Setting Outputs

```bash
# Single-line output
echo "name=value" >> "$GITHUB_OUTPUT"

# Multi-line output
echo "json<<EOF" >> "$GITHUB_OUTPUT"
cat result.json >> "$GITHUB_OUTPUT"
echo "EOF" >> "$GITHUB_OUTPUT"
```

### Setting Environment Variables

```bash
echo "MY_VAR=my_value" >> "$GITHUB_ENV"

# Multi-line
echo "CERT<<EOF" >> "$GITHUB_ENV"
cat cert.pem >> "$GITHUB_ENV"
echo "EOF" >> "$GITHUB_ENV"
```

### Adding to PATH

```bash
echo "/path/to/tool" >> "$GITHUB_PATH"
```

## Expressions and Contexts

### Syntax

Expressions use `${{ <expression> }}`. Inside `if:`, the `${{ }}` wrapper is optional.

### Key Contexts

| Context | Description | Example |
|---|---|---|
| `github` | Event data | `github.sha`, `github.ref_name`, `github.event.pull_request.number` |
| `env` | Environment variables | `env.MY_VAR` |
| `secrets` | Repository secrets | `secrets.DEPLOY_KEY` |
| `vars` | Repository variables | `vars.ENVIRONMENT` |
| `inputs` | Workflow inputs | `inputs.environment` |
| `steps` | Step outputs | `steps.<id>.outputs.<name>` |
| `needs` | Dependent job outputs | `needs.<job>.outputs.<name>` |
| `runner` | Runner info | `runner.os`, `runner.arch` |
| `matrix` | Matrix values | `matrix.node-version` |
| `job` | Job info | `job.status` |

### Common Functions

```yaml
# String
contains(github.event.head_commit.message, '[skip ci]')
startsWith(github.ref, 'refs/tags/')
endsWith(github.repository, '-private')
format('Hello {0}', github.actor)

# JSON
fromJSON(steps.meta.outputs.json)
toJSON(matrix)

# Status (for if: conditions)
success()    # All previous steps succeeded
failure()    # Any previous step failed
always()     # Run regardless
cancelled()  # Workflow was cancelled
```

### Common Conditionals

```yaml
# Run only on main branch
if: github.ref == 'refs/heads/main'

# Run only on tags
if: startsWith(github.ref, 'refs/tags/v')

# Run only when specific files changed
if: contains(github.event.head_commit.modified, 'src/')

# Run only when PR is merged (not just closed)
if: github.event.pull_request.merged == true

# Run on workflow_run only if triggering workflow succeeded
if: github.event.workflow_run.conclusion == 'success'

# Check actor
if: github.actor != 'dependabot[bot]'
```

## Permissions

```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
  packages: write
  id-token: write      # For OIDC (cloud auth)
  actions: read
  checks: write
  deployments: write
  statuses: write
```

Best practice: set `permissions: read-all` at workflow level, then grant specific write permissions per job.

## Concurrency

```yaml
# Cancel in-progress runs for the same branch
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

# For deployments: don't cancel, queue instead
concurrency:
  group: deploy-${{ inputs.environment }}
  cancel-in-progress: false
```

## Environment Variables and Secrets

```yaml
env:
  # Workflow-level
  NODE_ENV: production

jobs:
  build:
    env:
      # Job-level
      CI: true
    steps:
      - run: echo "$MY_VAR"
        env:
          # Step-level
          MY_VAR: ${{ secrets.MY_SECRET }}
```

### Default Environment Variables

| Variable | Description |
|---|---|
| `GITHUB_SHA` | Commit SHA |
| `GITHUB_REF` | Full ref (e.g., `refs/heads/main`) |
| `GITHUB_REF_NAME` | Short ref (e.g., `main`) |
| `GITHUB_REPOSITORY` | Owner/repo |
| `GITHUB_ACTOR` | User who triggered |
| `GITHUB_TOKEN` | Auto-generated token |
| `RUNNER_OS` | `Linux`, `Windows`, `macOS` |

## Matrix Strategy

```yaml
strategy:
  fail-fast: false           # Don't cancel other jobs on failure
  max-parallel: 4            # Limit concurrent jobs
  matrix:
    os: [ubuntu-latest, macos-latest]
    node: [18, 20, 22]
    include:
      - os: ubuntu-latest
        node: 22
        coverage: true       # Add extra variable to specific combo
    exclude:
      - os: macos-latest
        node: 18             # Skip this combination
```

### Dynamic Matrix

```yaml
jobs:
  prepare:
    outputs:
      matrix: ${{ steps.set.outputs.matrix }}
    steps:
      - id: set
        run: |
          echo 'matrix={"include":[{"project":"api"},{"project":"web"}]}' >> "$GITHUB_OUTPUT"

  build:
    needs: prepare
    strategy:
      matrix: ${{ fromJSON(needs.prepare.outputs.matrix) }}
    steps:
      - run: echo "Building ${{ matrix.project }}"
```

## Reusable Workflows

### Caller Workflow

```yaml
jobs:
  call-build:
    uses: ./.github/workflows/build.yml  # Local
    # OR: org/repo/.github/workflows/build.yml@main  # Remote
    with:
      environment: production
    secrets:
      deploy-key: ${{ secrets.DEPLOY_KEY }}
    # OR: secrets: inherit  # Pass all secrets
```

### Reusable Workflow Definition

```yaml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    outputs:
      version:
        description: 'Built version'
        value: ${{ jobs.build.outputs.version }}
    secrets:
      deploy-key:
        required: true

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.ver.outputs.version }}
    steps:
      - id: ver
        run: echo "version=1.0.0" >> "$GITHUB_OUTPUT"
```

## Common Pitfalls

1. **Quoting expressions in `if:`**: Bare expressions work, but wrap complex ones:
   ```yaml
   if: ${{ github.ref == 'refs/heads/main' && github.event_name == 'push' }}
   ```

2. **Secret masking**: Secrets are masked in logs. Never echo secrets or write them to files that get uploaded.

3. **GITHUB_TOKEN scope**: The default token has limited permissions. For cross-repo operations use a PAT or GitHub App token.

4. **Checkout depth**: `actions/checkout` defaults to `fetch-depth: 1`. Use `fetch-depth: 0` for full history (tags, changelog generation).

5. **Shell differences**: Default shell on Windows is `pwsh`. Explicitly set `shell: bash` for cross-platform scripts.

6. **Path separators**: Use `/` in paths even on Windows runners when using bash shell.

7. **Concurrency without cancel-in-progress**: Omitting `cancel-in-progress` defaults to `false`, which queues runs instead of cancelling.

8. **Schedule drift**: Scheduled workflows may be delayed during periods of high load. Don't rely on exact timing.

9. **Environment protection rules**: Deployment jobs referencing an environment with required reviewers will pause until approved.

10. **Actions version pinning**: Pin actions to full SHA for security:
    ```yaml
    uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
    ```
