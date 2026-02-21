# Example Feature Summary: Core Functionality

This example demonstrates how to document a **core functionality** feature. This is the "Git Blame Overlay" feature from the git-blame-vsc extension.

---

# Git Blame Overlay Feature

## Overview

The Git Blame Overlay is the core feature of the git-blame-vsc extension. It provides users with instant access to git blame information by clicking on any line in an editor within a git repository.

## Status

- **Status**: ✅ Current (v0.0.2)
- **Version**: 0.0.2
- **Since**: 0.0.1

## Feature Type

**Category**: Core Functionality  
**Type**: Primary feature that defines the extension's main purpose

This is the foundational feature that users install the extension for. All other features (formatting, styling, management, optimization) exist to enhance or support this core capability.

## Business Value

Users can immediately understand who made changes to a line and when without leaving their editor. This streamlines code review processes, debugging, and understanding code history during development.

**Benefits**:
- **Accelerated code review**: Quickly identify commit context without switching tools
- **Efficient debugging**: Understand when and why code was changed
- **Reduced context switching**: Blame information inline within the editor
- **Team collaboration**: Answer "who knows about this code?" instantly

## What It Does

When a user clicks on a line of code in a git-tracked file:

1. The extension detects the click event
2. It queries the git repository for blame information for that specific line
3. An inline overlay appears at the end of the line showing:
   - The commit hash (7-character short hash)
   - Author name and/or email
   - Commit date
   - Commit message (truncated configurable length)

### User Experience

No need for commands or keyboard shortcuts. The interaction is intuitive:

1. Click a line of code
2. Overlay appears with blame information
3. Click another line to update the overlay
4. Use "Clear Line Overlay" command to hide it

### Example Output

```
console.log('hello');  [25418bf] John Doe (2024-02-20): Add git blame support
```

The overlay appears non-intrusively at the end of the clicked line, providing instant context about that line's origin.

## Key Features

### Core Functionality
- **Click-to-activate**: No keyboard shortcuts needed, simply click any line
- **Git integration**: Uses native `git blame` command for accuracy
- **Real-time access**: Instantly shows blame data from repository
- **Smart defaults**: Shows appropriate format without configuration

### Data Provided
- **Commit hash**: Short 7-character hash for easy reference
- **Author information**: Full name and email extracted from git config
- **Commit date**: YYYY-MM-DD format for consistency
- **Commit message**: The subject line of the commit

### Non-Git Files
For files not in a git repository:
- Overlay still appears on click (empty by default)
- No error messages or noise is generated
- Seamless user experience across tracked and untracked files

## Configuration

This feature respects the following configurations:

- `gitBlameOverlay.outputPattern`: Format of displayed information (see Customizable Formatting feature)
- `gitBlameOverlay.maxMessageLength`: Truncation length for commit messages

For detailed configuration options, see the [Customizable Formatting](../customizable-formatting/README.md) feature.

## Technical Implementation

### Related Source Code
- **Core Extension**: [src/extension.ts](../../src/extension.ts)
- **Blame Provider**: [src/blameProvider.ts](../../src/blameProvider.ts)
- **Overlay Manager**: [src/overlayManager.ts](../../src/overlayManager.ts)

### Architecture Overview

The feature uses a three-component architecture:

1. **Blame Provider** - Fetches git blame data using `git blame` command
2. **Overlay Manager** - Creates and positions VS Code decorations
3. **Extension Entry Point** - Coordinates between providers and managers

### Key Implementation Details

**BlameProvider**:
- Executes `git blame` command for files
- Parses blame output line-by-line
- Fetches full commit messages via `git log`
- Caches results for performance (30-second TTL)

**OverlayManager**:
- Creates VS Code decorations for inline display
- Positions overlays at line end
- Manages overlay lifecycle and clearing

**Extension**:
- Registers click event listeners
- Coordinates between BlameProvider and OverlayManager
- Handles configuration and formatting

## User Interactions

### Primary Workflow
1. User opens a file in a git repository
2. User clicks on a line of code
3. Extension queries git blame for that line
4. Overlay appears with formatted blame information
5. User can click another line to update the overlay

### Alternative Workflows
- **Clear overlay**: Open Command Palette, search "Clear Line Overlay"
- **Switch lines**: Click a different line; overlay updates automatically

### Commands

| Command | ID | Description |
|---------|----|----|
| Clear Line Overlay | `git-blame-vsc.clearOverlay` | Removes current overlay |

## Status and Roadmap

### Current Status

- ✅ Click-based blame display
- ✅ Git integration via native commands
- ✅ Configurable output format
- ✅ Theme-aware styling
- ✅ Performance caching (30-second TTL)
- ✅ Support for non-git files (graceful fallback)

### Known Limitations

1. **Cache limitations**: Blame data is cached for 30 seconds. External file changes may not reflect immediately.
2. **Large files**: Very large files may take a moment to compute blame on first request
3. **Recently moved files**: Renamed or moved files may show inaccurate blame until the file is saved
4. **Git requirement**: Requires git to be installed and accessible in system PATH
5. **Single overlay**: Only one overlay visible at a time

### Future Enhancements (Out of Scope - v0.0.2)

- [ ] Keyboard shortcut to show blame without clicking
- [ ] Blame history navigation (show previous versions)
- [ ] Per-file cache lifetime configuration
- [ ] Blame for uncommitted changes
- [ ] Conflict marker resolution
- [ ] Support for git submodules
- [ ] Hover-based overlay display
- [ ] Multiple overlays for selected ranges

## Related Features

- [Customizable Formatting](../customizable-formatting/README.md) - Controls how blame data is displayed
- [Theme-Aware Styling](../theme-aware-styling/README.md) - Adapts overlay appearance to VS Code theme
- [Overlay Management](../overlay-management/README.md) - Controls overlay lifecycle and visibility
- [Performance Optimization](../performance-optimization/README.md) - Caching and performance tuning
