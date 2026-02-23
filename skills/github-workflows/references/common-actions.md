# Common GitHub Actions Reference

## Table of Contents

- [Checkout and Setup](#checkout-and-setup)
- [Caching](#caching)
- [Artifacts](#artifacts)
- [Deployment and Publishing](#deployment-and-publishing)
- [Notifications and Comments](#notifications-and-comments)
- [Security and Analysis](#security-and-analysis)

## Checkout and Setup

### actions/checkout@v4

```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0            # Full history (default: 1)
    ref: ${{ github.head_ref }} # Specific ref
    token: ${{ secrets.PAT }}  # For private submodules
    submodules: recursive      # Clone submodules
    lfs: true                  # Fetch LFS objects
```

### actions/setup-node@v4

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'                        # Or: node-version-file: '.nvmrc'
    cache: 'npm'                              # Or: 'yarn', 'pnpm'
    registry-url: 'https://npm.pkg.github.com' # For publishing
```

### actions/setup-python@v5

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'                    # Or: python-version-file: '.python-version'
    cache: 'pip'                              # Or: 'poetry', 'pipenv'
```

### actions/setup-go@v5

```yaml
- uses: actions/setup-go@v5
  with:
    go-version: '1.22'                        # Or: go-version-file: 'go.mod'
    cache: true
```

### actions/setup-java@v4

```yaml
- uses: actions/setup-java@v4
  with:
    distribution: 'temurin'                    # Or: 'corretto', 'zulu'
    java-version: '21'
    cache: 'maven'                             # Or: 'gradle'
```

### dtolnay/rust-toolchain@stable

```yaml
- uses: dtolnay/rust-toolchain@stable
  with:
    components: clippy, rustfmt
    targets: wasm32-unknown-unknown
```

## Caching

### actions/cache@v4

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cache/pip
      node_modules
    key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-deps-
```

Common cache paths:

| Tool | Path | Key Hash File |
|---|---|---|
| npm | `~/.npm` | `**/package-lock.json` |
| yarn | `~/.cache/yarn` | `**/yarn.lock` |
| pnpm | `~/.local/share/pnpm/store` | `**/pnpm-lock.yaml` |
| pip | `~/.cache/pip` | `**/requirements*.txt` |
| Go | `~/go/pkg/mod` | `**/go.sum` |
| Cargo | `~/.cargo/registry`, `~/.cargo/git`, `target` | `**/Cargo.lock` |
| Gradle | `~/.gradle/caches` | `**/*.gradle*`, `**/gradle-wrapper.properties` |
| Maven | `~/.m2/repository` | `**/pom.xml` |

Note: Most `actions/setup-*` actions have built-in caching via `cache:` parameter, which is preferred over manual `actions/cache` when available.

## Artifacts

### actions/upload-artifact@v4

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: build-output
    path: |
      dist/
      !dist/**/*.map
    retention-days: 7          # Default: 90
    if-no-files-found: error   # Or: 'warn', 'ignore'
    compression-level: 6       # 0-9, default: 6
```

### actions/download-artifact@v4

```yaml
- uses: actions/download-artifact@v4
  with:
    name: build-output
    path: ./dist

# Download all artifacts
- uses: actions/download-artifact@v4
  with:
    path: ./artifacts
    merge-multiple: true       # Merge into single directory
```

## Deployment and Publishing

### actions/deploy-pages@v4

```yaml
# Requires pages build and deployment permissions
permissions:
  pages: write
  id-token: write

environment:
  name: github-pages
  url: ${{ steps.deployment.outputs.page_url }}

steps:
  - uses: actions/configure-pages@v5
  - uses: actions/upload-pages-artifact@v3
    with:
      path: './dist'
  - id: deployment
    uses: actions/deploy-pages@v4
```

### docker/build-push-action@v6

```yaml
- uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}

- uses: docker/metadata-action@v5
  id: meta
  with:
    images: ghcr.io/${{ github.repository }}
    tags: |
      type=ref,event=branch
      type=ref,event=pr
      type=semver,pattern={{version}}
      type=sha

- uses: docker/build-push-action@v6
  with:
    context: .
    push: ${{ github.event_name != 'pull_request' }}
    tags: ${{ steps.meta.outputs.tags }}
    labels: ${{ steps.meta.outputs.labels }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

### softprops/action-gh-release@v2

```yaml
- uses: softprops/action-gh-release@v2
  with:
    files: |
      dist/*.tar.gz
      dist/*.zip
    generate_release_notes: true
    draft: false
    prerelease: ${{ contains(github.ref, '-rc') }}
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Notifications and Comments

### actions/github-script@v7

```yaml
- uses: actions/github-script@v7
  with:
    script: |
      await github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: 'Build succeeded! :white_check_mark:'
      });
```

### slackapi/slack-github-action@v2

```yaml
- uses: slackapi/slack-github-action@v2
  with:
    webhook: ${{ secrets.SLACK_WEBHOOK_URL }}
    webhook-type: incoming-webhook
    payload: |
      {
        "text": "Deploy to ${{ inputs.environment }}: ${{ job.status }}"
      }
```

## Security and Analysis

### github/codeql-action

```yaml
- uses: github/codeql-action/init@v3
  with:
    languages: javascript, python

- uses: github/codeql-action/autobuild@v3

- uses: github/codeql-action/analyze@v3
  with:
    category: '/language:javascript'
```

### actions/dependency-review-action@v4

```yaml
# Runs on pull_request only
- uses: actions/dependency-review-action@v4
  with:
    fail-on-severity: moderate
    deny-licenses: GPL-3.0, AGPL-3.0
```

### OIDC for Cloud Providers

#### AWS

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789:role/github-actions
      aws-region: us-east-1
```

#### GCP

```yaml
- uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: projects/123/locations/global/workloadIdentityPools/pool/providers/provider
    service_account: sa@project.iam.gserviceaccount.com
```

#### Azure

```yaml
- uses: azure/login@v2
  with:
    client-id: ${{ secrets.AZURE_CLIENT_ID }}
    tenant-id: ${{ secrets.AZURE_TENANT_ID }}
    subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```
