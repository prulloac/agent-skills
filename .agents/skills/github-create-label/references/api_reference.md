# GitHub Label Creation Reference

## Tool Precedence & Capabilities

The skill attempts label creation in this order:

### 1. GitHub MCP Server
**When**: Available in Claude context with GitHub tools
**Capabilities**: Full label management including updates and deletions
**Auth**: Automatic via MCP context
**Supported Fields**: name, description, color

### 2. GitHub CLI (gh)
**When**: `gh` command installed and authenticated
**Capabilities**: Create labels with name, description, and color
**Auth**: Via `gh auth login`
**Command**: `gh label create --name --description --color`

**Requirements**:
- `gh` CLI installed
- Authenticated: `gh auth login`

**Example**:
```bash
gh label create \
  --name "bug" \
  --description "Something isn't working" \
  --color "d73a4a"
```

### 3. GitHub REST API
**When**: GITHUB_TOKEN environment variable set
**Endpoint**: `POST /repos/{owner}/{repo}/labels`
**Auth**: Bearer token
**Supported Fields**: name, description, color

**Requirements**:
- `GITHUB_TOKEN` or `GH_TOKEN` environment variable
- Token must have `repo` scope

**Example Payload**:
```json
{
  "name": "bug",
  "description": "Something isn't working",
  "color": "d73a4a"
}
```

## Label Parameters

### Required
- **name** (string): Label name (max 50 characters)
  - Example: "bug", "enhancement", "documentation"

### Optional
- **description** (string): Label description (max 100 characters)
  - Example: "Something isn't working"
  - Default: empty

- **color** (string): Hex color code (6 characters, no #)
  - Example: "d73a4a" (red), "a2eeef" (cyan), "0075ca" (blue)
  - Default: random color

## Common Label Examples

| Name | Color | Description |
|------|-------|-------------|
| bug | d73a4a | Something isn't working |
| enhancement | a2eeef | New feature or request |
| documentation | 0075ca | Improvements or additions to documentation |
| good first issue | 7057ff | Good for newcomers |
| help wanted | 008672 | Extra attention is needed |
| question | cc317c | Further information is requested |
| wontfix | ffffff | This will not be worked on |
| invalid | e4e669 | This doesn't seem right |

## Color Palette Reference

**Common Colors** (without # prefix):
- Red: `d73a4a`, `ff0000`
- Blue: `0075ca`, `0000ff`
- Green: `28a745`, `00ff00`
- Yellow: `ffd700`, `ffff00`
- Purple: `6f42c1`, `800080`
- Cyan: `a2eeef`, `00ffff`
- Gray: `999999`, `cccccc`
- White: `ffffff`

## Error Handling

### Common Errors

- **"gh: not found"** → Install GitHub CLI
- **"Not authenticated"** → Run `gh auth login`
- **"GITHUB_TOKEN not set"** → Set environment variable
- **"Label already exists"** → Use different name or update existing label
- **"Invalid color format"** → Use 6-character hex (e.g., "d73a4a")
- **"Name too long"** → Keep label name under 50 characters

## Batch Label Creation

To create multiple labels efficiently:
1. Prepare list of label definitions (name, description, color)
2. Call label creation tool multiple times
3. Or use GitHub MCP Server for batch operations if available

## Repository Detection

The skill automatically detects:
- Repository owner and name from git remote URL
- Current directory as repository root
- Available authentication methods

## Environment Setup

```bash
# GitHub CLI authentication
gh auth login

# REST API authentication
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
# or
export GH_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```
