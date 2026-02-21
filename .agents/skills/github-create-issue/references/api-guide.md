# GitHub Issue Creation Reference

## Tool Precedence

The skill follows this tool precedence order:

1. **GitHub MCP Server** - When available in MCP context (Claude can use native GitHub tools)
2. **GitHub CLI (gh)** - Command-line tool if installed and authenticated
3. **GitHub REST API** - Direct HTTP API calls with GITHUB_TOKEN

## GitHub CLI (gh)

### Requirements
- `gh` command installed and in PATH
- Authenticated with `gh auth login`

### Basic Issue Creation
```bash
gh issue create --title "Title" --body "Description"
```

### With Metadata
```bash
gh issue create \
  --title "Title" \
  --body "Description" \
  --label "bug,urgent" \
  --assignee "@username" \
  --milestone "v1.0"
```

### Limitations
- GitHub CLI doesn't support direct project assignment in create command
- Use `gh issue edit` to add projects after creation

## GitHub REST API

### Requirements
- `GITHUB_TOKEN` or `GH_TOKEN` environment variable set
- Token must have `repo` scope

### Endpoint
```
POST /repos/{owner}/{repo}/issues
```

### Payload Example
```json
{
  "title": "Found a bug",
  "body": "I'm having a problem with this.",
  "labels": ["bug", "urgent"],
  "assignees": ["octocat"],
  "milestone": 1
}
```

### Response
Returns Issue object with `html_url`, `number`, `id`, and other fields.

## GitHub MCP Server

When using Claude with GitHub MCP Server tools:
- Claude can directly call issue creation tools
- No authentication or CLI installation needed
- Best option when available

## Issue Template Detection

### Template Locations
Templates are detected in: `.github/ISSUE_TEMPLATE/`

### Supported Formats

**Markdown (.md)**
```markdown
---
name: Bug Report
title: "[Bug]: "
description: "Report a bug"
labels: ["bug"]
---

## Describe the bug
...
```

**YAML (.yml / .yaml)**
```yaml
name: Feature Request
description: Suggest an idea
labels: ["enhancement"]
```

### Template Matching Algorithm

1. Extract keywords from template names and metadata (bug, feature, documentation, etc.)
2. Score templates based on keyword overlap with user's issue description
3. Templates with score > 0 ranked highest
4. If top template has significantly higher score, auto-select it
5. Otherwise, present options to user

## Common Issue Fields

| Field | Type | Notes |
|-------|------|-------|
| title | string | Required. Issue title/summary |
| body | string | Required. Issue description/details |
| labels | array | Optional. Label names (must exist in repo) |
| assignees | array | Optional. GitHub usernames to assign |
| milestone | string | Optional. Milestone title or number |
| project | string | Optional. Project name (gh CLI doesn't support in create) |

## Error Handling

### Common Errors

- **"gh: not found"** - GitHub CLI not installed
- **"Not authenticated"** - Run `gh auth login`
- **"GITHUB_TOKEN not set"** - Set environment variable
- **"404 Not Found"** - Repository not found or wrong owner/name
- **"422 Validation Failed"** - Invalid labels, assignees, or milestone

## Authentication

### GitHub CLI
```bash
gh auth login
```

### REST API
```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
# or
export GH_TOKEN=ghp_xxxxxxxxxxxx
```

## Repository Detection

The skill automatically detects repository info from:
1. Git remote URL (`git config --get remote.origin.url`)
2. Extracts owner and repo name from URL format
