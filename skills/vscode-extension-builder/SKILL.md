---
name: vscode-extension-builder
description: Guide for creating Visual Studio Code extensions/plugins. Use when users want to build VS Code extensions, add functionality to VS Code, create language support, add themes, build webviews, implement debuggers, or any VS Code plugin development task. Helps navigate VS Code Extension API documentation and provides guidance on extension capabilities, project setup, and best practices.
---

# VS Code Extension Builder

## Overview

This skill guides the development of Visual Studio Code extensions by helping navigate the extensive VS Code Extension API documentation and providing structured guidance for common extension development tasks.

## Documentation Base

All VS Code extension development guidance is based on the official documentation at:
**https://code.visualstudio.com/api**

When assisting users, fetch relevant documentation pages to provide accurate, up-to-date information.

## Core Workflow

### 1. Understand User Intent

First, determine what the user wants to accomplish with their extension:

**Common extension types:**
- **Commands & UI extensions** - Add commands, menus, keybindings, status bar items
- **Language support** - Syntax highlighting, IntelliSense, diagnostics, formatting
- **Themes** - Color themes, file icon themes, product icon themes
- **Webviews** - Custom UI panels with HTML/CSS/JavaScript
- **Debuggers** - Debug adapter integrations
- **Source control** - SCM provider integrations
- **Tree views** - Custom sidebar explorers
- **AI/Chat extensions** - Chat participants, language model tools
- **Testing** - Test provider integrations
- **Notebook support** - Custom notebook renderers

### 2. Fetch Relevant Documentation

Based on the user's intent, fetch the appropriate documentation:

**For getting started:**
- https://code.visualstudio.com/api/get-started/your-first-extension
- https://code.visualstudio.com/api/get-started/extension-anatomy

**For capability planning:**
- https://code.visualstudio.com/api/extension-capabilities/overview
- https://code.visualstudio.com/api/extension-guides/overview

**For specific features, use the extension guides:**
- AI features: https://code.visualstudio.com/api/extension-guides/ai/
- Commands: https://code.visualstudio.com/api/extension-guides/command
- Webviews: https://code.visualstudio.com/api/extension-guides/webview
- Tree views: https://code.visualstudio.com/api/extension-guides/tree-view
- Language features: https://code.visualstudio.com/api/language-extensions/overview
- Debuggers: https://code.visualstudio.com/api/extension-guides/debugger-extension
- Themes: https://code.visualstudio.com/api/extension-guides/color-theme

**For UX best practices:**
- https://code.visualstudio.com/api/ux-guidelines/overview

**For API reference:**
- VS Code API: https://code.visualstudio.com/api/references/vscode-api
- Contribution Points: https://code.visualstudio.com/api/references/contribution-points
- Extension Manifest: https://code.visualstudio.com/api/references/extension-manifest

**For publishing:**
- https://code.visualstudio.com/api/working-with-extensions/publishing-extension

### 3. Guide Implementation

After fetching documentation, provide step-by-step guidance:

1. **Project setup** - Use Yeoman generator or guide manual setup
2. **Package.json configuration** - Help define contribution points
3. **Core implementation** - Provide code guidance based on documentation
4. **Testing** - Help set up extension testing
5. **Debugging** - Guide F5 debugging setup
6. **Publishing** - Assist with vsce packaging

## Quick Start Pattern

For new extensions, always start with:

```bash
# Install dependencies (if needed)
npm install -g yo generator-code

# Or use npx without global install
npx --package yo --package generator-code -- yo code
```

Guide users through the prompts based on their extension type.

## Key Concepts to Explain

### Contribution Points
Static declarations in `package.json` that extend VS Code:
- commands
- menus
- keybindings
- views
- viewsContainers
- configuration
- languages
- grammars
- themes
- debuggers

### Activation Events
When extensions are loaded:
- `onCommand:` - When a command is invoked
- `onLanguage:` - When a file of specific language is opened
- `onView:` - When a view is expanded
- `workspaceContains:` - When workspace matches a pattern
- `*` - On startup (use sparingly)

### Extension Anatomy
- `package.json` - Extension manifest with metadata and contribution points
- `extension.js/ts` - Main entry point with `activate()` and `deactivate()` functions
- `.vscode/launch.json` - Debug configuration for F5 debugging

## Common Patterns

### Registering a Command
```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    let disposable = vscode.commands.registerCommand('extension.commandName', () => {
        vscode.window.showInformationMessage('Hello World!');
    });
    
    context.subscriptions.push(disposable);
}
```

### Creating a Tree View
Refer to: https://code.visualstudio.com/api/extension-guides/tree-view

### Building a Webview
Refer to: https://code.visualstudio.com/api/extension-guides/webview

### Language Server Protocol
For advanced language features, refer to:
https://code.visualstudio.com/api/language-extensions/language-server-extension-guide

## Fetching Documentation Strategy

1. **Start broad** - Fetch overview pages to understand scope
2. **Go specific** - Fetch detailed guides for the exact feature needed
3. **Check references** - Fetch API references for specific types/methods
4. **Review examples** - Point users to sample extensions at https://github.com/microsoft/vscode-extension-samples

## Important Guidelines

### What Extensions Can Do
- Extend VS Code UI (sidebars, panels, status bar, etc.)
- Add commands and keybindings
- Create custom views with TreeView API
- Build custom UI with Webview API
- Provide language features (IntelliSense, diagnostics, etc.)
- Integrate debuggers and test frameworks
- Add themes and icons
- Register configuration settings

### Restrictions
- **No DOM access** - Extensions cannot access VS Code's DOM directly
- **No custom CSS** - Cannot inject custom stylesheets
- Extensions run in a separate Extension Host process
- Must use provided Extension APIs only

### Best Practices
1. Follow the UX Guidelines: https://code.visualstudio.com/api/ux-guidelines/overview
2. Use TypeScript for better type safety
3. Minimize activation events for faster startup
4. Properly dispose of resources (add to `context.subscriptions`)
5. Test extensions thoroughly
6. Bundle extensions for production (webpack/esbuild)

## Progressive Assistance

**For beginners:**
- Start with "Your First Extension" walkthrough
- Explain core concepts (activation, contribution points, commands)
- Guide through Yeoman scaffolding
- Help with basic command registration

**For intermediate users:**
- Navigate to specific extension guide documentation
- Explain API patterns and best practices
- Help integrate VS Code APIs
- Assist with debugging and testing

**For advanced users:**
- Point to proposed APIs and advanced topics
- Help with Language Server Protocol
- Guide multi-extension architecture
- Assist with marketplace publishing

## Reference Documentation

For comprehensive guides on specific extension types and advanced patterns, see:
- [Extension Development Guide](references/extension-guide.md) - Detailed guide for common extension patterns
- [API Quick Reference](references/api-quick-reference.md) - Quick lookup for common VS Code APIs

Read these references when users need deeper guidance on specific topics.
