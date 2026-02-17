# VS Code Official Documentation Map

**Source:** https://code.visualstudio.com/api
**Last Updated:** February 2026

This document maps the official VS Code Extension API documentation structure to help guide users to the right resources based on their needs.

## Quick Navigation Index

### Getting Started Track
Perfect for new extension developers.

| Topic | URL | Key Content |
|-------|-----|-------------|
| Your First Extension | https://code.visualstudio.com/api/get-started/your-first-extension | Yeoman generator setup, scaffolding, quick debugging with F5 |
| Extension Anatomy | https://code.visualstudio.com/api/get-started/extension-anatomy | File structure, package.json, activate/deactivate functions |
| Wrapping Up | https://code.visualstudio.com/api/get-started/wrapping-up | Next steps, testing, publishing resources |

### Extension Capabilities
Understanding what your extension can do.

| Category | Overview | Details |
|----------|----------|---------|
| Common | https://code.visualstudio.com/api/extension-capabilities/overview | Commands, configurations, notifications, quick picks, file pickers, progress, storage |
| Theming | https://code.visualstudio.com/api/extension-capabilities/theming | Color themes, file icons, product icons |
| Workbench | https://code.visualstudio.com/api/extension-capabilities/extending-workbench | UI extensions, tree views, webviews, custom editors |
| Language | https://code.visualstudio.com/api/language-extensions/overview | Syntax highlighting, IntelliSense, diagnostics, formatting |
| Debugging | https://code.visualstudio.com/api/extension-guides/debugger-extension | Debug adapters, debug configuration, breakpoints |

### Extension Guides
Detailed implementation guides for specific features.

#### Core Features
- **Commands**: https://code.visualstudio.com/api/extension-guides/command
- **Tree View**: https://code.visualstudio.com/api/extension-guides/tree-view
- **Webview**: https://code.visualstudio.com/api/extension-guides/webview
- **Custom Editors**: https://code.visualstudio.com/api/extension-guides/custom-editors

#### Theming & UI
- **Color Theme**: https://code.visualstudio.com/api/extension-guides/color-theme
- **File Icon Theme**: https://code.visualstudio.com/api/extension-guides/file-icon-theme
- **Product Icon Theme**: https://code.visualstudio.com/api/extension-guides/product-icon-theme

#### Language Features
- **Syntax Highlighting**: https://code.visualstudio.com/api/language-extensions/syntax-highlight-guide
- **Semantic Highlighting**: https://code.visualstudio.com/api/language-extensions/semantic-highlight-guide
- **Language Configuration**: https://code.visualstudio.com/api/language-extensions/language-configuration-guide
- **Programmatic Features**: https://code.visualstudio.com/api/language-extensions/programmatic-language-features
- **Language Server**: https://code.visualstudio.com/api/language-extensions/language-server-extension-guide
- **Snippets**: https://code.visualstudio.com/api/language-extensions/snippet-guide

#### AI & Emerging
- **AI Extensibility**: https://code.visualstudio.com/api/extension-guides/ai/ai-extensibility-overview
- **Language Model**: https://code.visualstudio.com/api/extension-guides/ai/language-model
- **Language Model Tutorial**: https://code.visualstudio.com/api/extension-guides/ai/language-model-tutorial
- **Chat Participant**: https://code.visualstudio.com/api/extension-guides/ai/chat
- **Chat Tutorial**: https://code.visualstudio.com/api/extension-guides/ai/chat-tutorial
- **Language Model Tool**: https://code.visualstudio.com/api/extension-guides/ai/tools
- **MCP Dev Guide**: https://code.visualstudio.com/api/extension-guides/ai/mcp
- **Prompt TSX**: https://code.visualstudio.com/api/extension-guides/ai/prompt-tsx

#### Advanced Workbench
- **Notebook**: https://code.visualstudio.com/api/extension-guides/notebook
- **Virtual Documents**: https://code.visualstudio.com/api/extension-guides/virtual-documents
- **Virtual Workspaces**: https://code.visualstudio.com/api/extension-guides/virtual-workspaces
- **Web Extensions**: https://code.visualstudio.com/api/extension-guides/web-extensions
- **Workspace Trust**: https://code.visualstudio.com/api/extension-guides/workspace-trust
- **Task Provider**: https://code.visualstudio.com/api/extension-guides/task-provider
- **Source Control**: https://code.visualstudio.com/api/extension-guides/scm-provider
- **Markdown Extension**: https://code.visualstudio.com/api/extension-guides/markdown-extension
- **Test Extension**: https://code.visualstudio.com/api/extension-guides/testing
- **Custom Data Extension**: https://code.visualstudio.com/api/extension-guides/custom-data-extension
- **Telemetry**: https://code.visualstudio.com/api/extension-guides/telemetry

### UX Guidelines
Best practices for extension UI/UX.

| Component | URL |
|-----------|-----|
| Overview | https://code.visualstudio.com/api/ux-guidelines/overview |
| Activity Bar | https://code.visualstudio.com/api/ux-guidelines/activity-bar |
| Sidebars | https://code.visualstudio.com/api/ux-guidelines/sidebars |
| Panel | https://code.visualstudio.com/api/ux-guidelines/panel |
| Status Bar | https://code.visualstudio.com/api/ux-guidelines/status-bar |
| Views | https://code.visualstudio.com/api/ux-guidelines/views |
| Editor Actions | https://code.visualstudio.com/api/ux-guidelines/editor-actions |
| Quick Picks | https://code.visualstudio.com/api/ux-guidelines/quick-picks |
| Command Palette | https://code.visualstudio.com/api/ux-guidelines/command-palette |
| Notifications | https://code.visualstudio.com/api/ux-guidelines/notifications |
| Webviews | https://code.visualstudio.com/api/ux-guidelines/webviews |
| Context Menus | https://code.visualstudio.com/api/ux-guidelines/context-menus |
| Walkthroughs | https://code.visualstudio.com/api/ux-guidelines/walkthroughs |
| Settings | https://code.visualstudio.com/api/ux-guidelines/settings |

### API References
Detailed technical references.

| Reference | URL | Purpose |
|-----------|-----|---------|
| VS Code API | https://code.visualstudio.com/api/references/vscode-api | Complete API documentation |
| Contribution Points | https://code.visualstudio.com/api/references/contribution-points | package.json contribution declarations |
| Activation Events | https://code.visualstudio.com/api/references/activation-events | Extension activation triggers |
| Extension Manifest | https://code.visualstudio.com/api/references/extension-manifest | package.json schema and fields |
| Built-In Commands | https://code.visualstudio.com/api/references/commands | Commands provided by VS Code |
| When Clause Contexts | https://code.visualstudio.com/api/references/when-clause-contexts | Conditional expressions for UI visibility |
| Theme Color | https://code.visualstudio.com/api/references/theme-color | Color definitions for theming |
| Product Icon Reference | https://code.visualstudio.com/api/references/icons-in-labels | Icon identifiers for UI |
| Document Selector | https://code.visualstudio.com/api/references/document-selector | Language/file matching patterns |

### Testing & Publishing
Deployment and quality assurance.

| Topic | URL |
|-------|-----|
| Testing Extensions | https://code.visualstudio.com/api/working-with-extensions/testing-extension |
| Publishing Extensions | https://code.visualstudio.com/api/working-with-extensions/publishing-extension |
| Bundling Extensions | https://code.visualstudio.com/api/working-with-extensions/bundling-extension |
| Continuous Integration | https://code.visualstudio.com/api/working-with-extensions/continuous-integration |

### Advanced Topics
For complex extension scenarios.

| Topic | URL | Use Case |
|-------|-----|----------|
| Extension Host | https://code.visualstudio.com/api/advanced-topics/extension-host | Understanding extension process architecture |
| Remote Development | https://code.visualstudio.com/api/advanced-topics/remote-extensions | Remote and Codespaces support |
| Using Proposed API | https://code.visualstudio.com/api/advanced-topics/using-proposed-api | Access experimental/unreleased APIs |
| TSLint to ESLint | https://code.visualstudio.com/api/advanced-topics/tslint-eslint-migration | Migration guide for linting |
| Python Extension Template | https://code.visualstudio.com/api/advanced-topics/python-extension-template | Template for Python-based extensions |

## Documentation Organization Summary

The VS Code API documentation is organized in a **feature-first** approach:

1. **Get Started** - Sequential learning path for new developers
2. **Extension Capabilities** - Organize features by category (UI, Language, Theming, etc.)
3. **Extension Guides** - Deep dives into specific features with examples
4. **UX Guidelines** - Best practices for user experience
5. **References** - Technical specifications and schemas
6. **Advanced Topics** - Specialized scenarios and integrations
7. **Testing & Publishing** - Quality assurance and distribution

## Key Documentation Highlights

### Modern VS Code Features (1.74.0+)

- **Implicit Activation Events**: Commands in `contributes.commands` automatically activate extensions
- **Web Extensions**: Support for running in browser-based VS Code
- **Workspace Trust**: Extensions respect user trust decisions
- **AI Integration**: Chat Participants, Language Models, MCP support

### Extension Manifest Best Practices

The [Extension Manifest](https://code.visualstudio.com/api/references/extension-manifest) reference covers:
- Required fields (name, version, publisher, engines)
- Marketplace presentation (displayName, description, categories, icon)
- Capability declarations (activationEvents, contributes)
- Resource linking (repository, bugs, homepage, license)
- Advanced features (extensionPack, extensionDependencies, extensionKind)

### Testing Strategies

The [Testing Extensions](https://code.visualstudio.com/api/working-with-extensions/testing-extension) guide covers:
- **Modern approach**: @vscode/test-cli with .vscode-test.js configuration
- **Legacy approach**: @vscode/test-electron with custom runner
- **Mocha framework**: Default test framework with full VS Code API access
- **Debugging**: Full debugger support for tests

## Extension Sample Repository

Official samples available at: https://github.com/microsoft/vscode-extension-samples

Examples include implementations of every extension type and guides many specific features.

## When to Fetch Which Docs

### User asks: "How do I build my first extension?"
→ https://code.visualstudio.com/api/get-started/your-first-extension

### User asks: "How does package.json work?"
→ https://code.visualstudio.com/api/references/extension-manifest

### User asks: "How do I add AI features?"
→ https://code.visualstudio.com/api/extension-guides/ai/ai-extensibility-overview

### User asks: "What can extensions do?"
→ https://code.visualstudio.com/api/extension-capabilities/overview

### User asks: "How do I test my extension?"
→ https://code.visualstudio.com/api/working-with-extensions/testing-extension

### User asks: "How do I publish to Marketplace?"
→ https://code.visualstudio.com/api/working-with-extensions/publishing-extension

### User asks: "What's the best way to implement [feature]?"
→ First check Extension Capabilities overview, then specific guide

### User asks: "What APIs are available?"
→ https://code.visualstudio.com/api/references/vscode-api

