# Example Feature Summary: Customization Feature

This example demonstrates how to document a **customization** feature. This is the "Customizable Formatting" feature from the git-blame-vsc extension.

---

# Customizable Formatting Feature

## Overview

The Customizable Formatting feature allows users to design their own blame display format using a flexible pattern-based system. Users can choose which information to display, in what order, and with custom separators.

## Status

- **Status**: ✅ Current (v0.0.2)
- **Version**: 0.0.2
- **Since**: 0.0.1

## Feature Type

**Category**: Customization  
**Type**: Extended functionality that allows users to personalize the core feature

This feature enables users to customize the appearance and content of blame overlays, adapting the extension to different team standards, workflows, and personal preferences without requiring code changes.

## Business Value

Different development teams and workflows have different information needs. By allowing users to customize the format, the extension adapts to various development practices without requiring separate configuration tools or workarounds.

**Benefits**:
- **Team standardization**: Define org-wide blame format standards
- **Workflow flexibility**: Show information that matters for your process
- **Minimalism options**: Display only what you need
- **Detail control**: Full format control with simple patterns

## What It Does

The feature provides a template system where users define a pattern string with placeholders that get replaced with actual blame information. This allows maximum flexibility with minimal configuration complexity.

### User Experience

Users can:
1. Open VS Code Settings
2. Search for "Git Blame Overlay"
3. Modify the "Output Pattern" setting
4. See changes apply instantly to active overlays

### Example Output

```
Default: [25418bf] John Doe (2024-02-20): Add feature support
Custom:  John: Add feature support
Custom:  [25418bf] John Doe | 2024-02-20 | Add feature support
```

## Key Features

### Pattern System
- **Flexible placeholders**: `<hash>`, `<author>`, `<date>`, `<message>`, and more
- **Custom separators**: Use any separator you prefer
- **Reusable placeholders**: Reference the same data multiple times
- **Live updates**: Changes apply immediately without restarting

### Message Truncation
- **Configurable length**: Set maximum characters for commit messages
- **Automatic ellipsis**: `...` added when truncated
- **Flexible sizing**: From single character to unlimited

## Configuration

### Available Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `outputPattern` | String | `[<hash>] <author> (<date>): <message>` | Template for blame display |
| `maxMessageLength` | Number | 24 | Max commit message characters |

### Supported Placeholders

| Placeholder | Replacement | Example |
|-------------|-------------|---------|
| `<hash>` | 7-character commit hash | `25418bf` |
| `<author>` | Full author name | `John Doe` |
| `<authorShort>` | First word of author name | `John` |
| `<authorEmail>` | Author email address | `john@example.com` |
| `<date>` | Commit date (YYYY-MM-DD) | `2024-02-20` |
| `<message>` | Commit message subject | `Add feature support` |

### Configuration Examples

#### Minimal and Subtle (Recommended for Clean Code)
```json
{
  "gitBlameOverlay.outputPattern": "<authorShort>: <message>",
  "gitBlameOverlay.maxMessageLength": 24
}
```
**Output**: `John: Add feature support`
**Use case**: Minimalist developers who want just the author and message

#### Detailed Format with Email
```json
{
  "gitBlameOverlay.outputPattern": "[<hash>] <author> (<authorEmail>) <date>: <message>",
  "gitBlameOverlay.maxMessageLength": 40
}
```
**Output**: `[25418bf] John Doe (john@example.com) 2024-02-20: Add feature support`
**Use case**: Teams that need comprehensive attribution

#### Short Name Format
```json
{
  "gitBlameOverlay.outputPattern": "<message> (<authorShort>, <date>)",
  "gitBlameOverlay.maxMessageLength": 50
}
```
**Output**: `Add feature support (John, 2024-02-20)`
**Use case**: Teams focused on commit messages

### How to Apply Configuration

#### Via VS Code Settings UI
1. Open Settings (Cmd+, or Ctrl+,)
2. Search for "Git Blame Overlay"
3. Modify "Output Pattern" and "Max Message Length"
4. Changes apply immediately

#### Via settings.json
```json
{
  "gitBlameOverlay.outputPattern": "<hash> <author>(<date>): <message>",
  "gitBlameOverlay.maxMessageLength": 24
}
```

#### Workspace-Specific Settings
Add to `.vscode/settings.json` for project-wide standards:
```json
{
  "gitBlameOverlay.outputPattern": "<authorShort>: <message>",
  "gitBlameOverlay.maxMessageLength": 20
}
```

## Technical Implementation

### Related Source Code
- **Formatting Logic**: [src/extension.ts#L54-L75](../../src/extension.ts) - `formatBlameText()` function
- **Configuration Reading**: [src/extension.ts#L30-L36](../../src/extension.ts) - `getBlameFormatConfig()` function

### How It Works

1. User sets output pattern in configuration
2. Extension reads pattern when displaying overlay
3. Pattern placeholders replaced with actual values
4. Commit message truncated if needed
5. Formatted string displayed in overlay

### Example Processing

```
Pattern:  "[<hash>] <author> (<date>): <message>"
Values:   hash=25418bf, author=John, date=2024-02-20, message=Add feature
Result:   "[25418bf] John (2024-02-20): Add feature"
```

## User Interactions

### Primary Workflow
1. User opens VS Code Settings
2. Searches for "Git Blame Overlay"
3. Modifies pattern or message length
4. Overlay updates immediately on active lines
5. User clicks lines to see new format

### Alternative Workflows
- **Team configuration**: Add settings to `.vscode/settings.json`
- **Multiple profiles**: Save different pattern configs and switch between them
- **Testing patterns**: Make changes and click lines to see results instantly

## Status and Roadmap

### Current Status
- ✅ Pattern-based formatting system
- ✅ Configurable message truncation
- ✅ All placeholder types supported
- ✅ Live configuration updates
- ✅ Multiple configuration locations

### Known Limitations
1. **Placeholder handling**: Unknown placeholders left as-is
2. **Case sensitivity**: Placeholders are case-sensitive (`<hash>` works, `<Hash>` doesn't)
3. **No custom placeholders**: Cannot create user-defined placeholders
4. **No conditional formatting**: Cannot use if/else logic in patterns

### Future Enhancements (Out of Scope - v0.0.2)

- [ ] Custom date format specifiers
- [ ] Support for relative dates (e.g., "2 days ago")
- [ ] Branch information in pattern
- [ ] Multiple blame formats (toggle between saved profiles)
- [ ] User-defined variables/aliases
- [ ] Conditional formatting (if/else logic)
- [ ] Preset patterns library
- [ ] Visual pattern builder

## Related Features

- [Git Blame Overlay](../git-blame-overlay/README.md) - Provides the data being formatted
- [Theme-Aware Styling](../theme-aware-styling/README.md) - Visual presentation of formatted text
- [Overlay Management](../overlay-management/README.md) - Display of formatted output
