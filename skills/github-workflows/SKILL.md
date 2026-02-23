---
name: github-workflows
description: Create, edit, and troubleshoot GitHub Actions workflow files (.github/workflows/*.yml). Use when the user needs to set up CI/CD pipelines, PR automation, release workflows, scheduled tasks, Docker builds, deployment pipelines, or any GitHub Actions workflow. Covers workflow syntax, common actions, best practices, security hardening, and reusable workflow patterns. Includes starter templates for common workflow types.
---

# GitHub Workflows

## Overview

Create and maintain GitHub Actions workflow YAML files in `.github/workflows/`. Includes starter templates for common workflow types and reference documentation for syntax, actions, and best practices.

## Workflow

1. **Determine workflow type** -- Identify which type(s) the user needs (CI, deploy, release, PR automation, scheduled, Docker).
2. **Start from template** -- Copy the matching template from `assets/` to `.github/workflows/` as a starting point.
3. **Customize for the project** -- Adapt the template to the project's language, framework, and requirements. Detect the project's ecosystem by examining files like `package.json`, `go.mod`, `Cargo.toml`, `pyproject.toml`, `Makefile`, `Dockerfile`, etc.
4. **Apply best practices** -- Consult [references/best-practices.md](references/best-practices.md) to harden security, optimize performance, and improve reliability.
5. **Validate** -- Check for common syntax issues (see Validation section below).

## Templates

Start from these templates in `assets/`:

| Template | File | Use Case |
|---|---|---|
| CI | `assets/ci.yml` | Build, lint, and test on push/PR |
| Deploy | `assets/deploy.yml` | Deploy to staging/production environments |
| Release | `assets/release.yml` | Create releases on tag push, publish packages |
| PR Checks | `assets/pr-checks.yml` | Auto-label, size checks, PR automation |
| Scheduled | `assets/scheduled.yml` | Cron-based maintenance, cleanup, reports |
| Docker | `assets/docker.yml` | Build and push container images to GHCR |

Copy the relevant template, then replace `TODO` comments with project-specific configuration.

## Customization Guide

### Language/Framework Detection

Detect the project ecosystem and apply appropriate setup:

| Indicator File | Setup Action | Cache | Lockfile |
|---|---|---|---|
| `package.json` | `actions/setup-node@v4` | `npm`/`yarn`/`pnpm` | `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` |
| `pyproject.toml`, `requirements.txt` | `actions/setup-python@v5` | `pip`/`poetry` | `requirements.txt`, `poetry.lock` |
| `go.mod` | `actions/setup-go@v5` | `true` | `go.sum` |
| `Cargo.toml` | `dtolnay/rust-toolchain@stable` | manual | `Cargo.lock` |
| `pom.xml` | `actions/setup-java@v4` | `maven` | N/A |
| `build.gradle` | `actions/setup-java@v4` | `gradle` | N/A |
| `Dockerfile` | `docker/setup-buildx-action@v3` | `type=gha` | N/A |

### Common CI Commands by Ecosystem

**Node.js**: `npm ci`, `npm run lint`, `npm test`, `npm run build`
**Python**: `pip install -e ".[dev]"`, `ruff check .`, `pytest`, `python -m build`
**Go**: `go vet ./...`, `golangci-lint run`, `go test ./...`, `go build ./...`
**Rust**: `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test`, `cargo build --release`

## Key Patterns

### Concurrency Control

Always add concurrency to prevent redundant runs:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.head_ref || github.ref }}
  cancel-in-progress: true  # false for deploy workflows
```

### Minimal Permissions

```yaml
permissions: read-all  # Workflow-level default

jobs:
  deploy:
    permissions:
      contents: read
      id-token: write  # Escalate only where needed
```

### Reusable Workflows

Extract shared logic into `.github/workflows/reusable-*.yml` using `workflow_call` trigger. Callers invoke with `uses: ./.github/workflows/reusable-build.yml`.

### Environment Protection

For deployment workflows, use GitHub environments with protection rules:

```yaml
jobs:
  deploy:
    environment:
      name: production
      url: ${{ steps.deploy.outputs.url }}
```

## Validation

After creating or editing a workflow, verify:

1. **YAML syntax** -- Valid YAML with correct indentation (2 spaces)
2. **Required keys** -- `on` and `jobs` are present at top level
3. **Trigger correctness** -- Branch names and event types match the project
4. **Permissions** -- Set explicitly, following least privilege
5. **Timeouts** -- Every job has `timeout-minutes` set
6. **Action versions** -- Actions use specific versions (e.g., `@v4`), not `@main`/`@master`
7. **Secret references** -- All `${{ secrets.* }}` references correspond to configured secrets
8. **Path filters** -- `paths` and `paths-ignore` are not used together on the same trigger
9. **Concurrency** -- Present on workflows triggered by push/PR to prevent redundant runs
10. **Shell consistency** -- Cross-platform workflows explicitly set `shell: bash`

## Reference Documentation

- [Workflow Syntax Reference](references/workflow-syntax.md) -- Complete YAML syntax: triggers, jobs, steps, expressions, matrix, reusable workflows, and common pitfalls
- [Common Actions Reference](references/common-actions.md) -- Popular actions for checkout, setup, caching, artifacts, deployment, Docker, security, and cloud auth (OIDC)
- [Best Practices](references/best-practices.md) -- Security hardening, performance optimization, reliability patterns, and maintainability guidelines

Load these references when:
- Looking up specific syntax or configuration options
- Configuring actions not covered in the templates
- Applying security or performance best practices
- Setting up cloud provider authentication (OIDC)
