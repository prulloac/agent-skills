# VS Code Extension Development Guide

This guide provides detailed patterns and examples for common VS Code extension development tasks.

## Table of Contents

1. [Project Setup](#project-setup)
2. [Command Extensions](#command-extensions)
3. [Tree View Extensions](#tree-view-extensions)
4. [Webview Extensions](#webview-extensions)
5. [Language Extensions](#language-extensions)
6. [Theme Extensions](#theme-extensions)
7. [Configuration and Settings](#configuration-and-settings)
8. [Testing Extensions](#testing-extensions)
9. [Publishing Extensions](#publishing-extensions)

## Project Setup

### Using Yeoman Generator

The recommended way to start a new extension:

```bash
npx --package yo --package generator-code -- yo code
```

Options:
- **New Extension (TypeScript)** - Full-featured TypeScript extension
- **New Extension (JavaScript)** - JavaScript-based extension
- **New Color Theme** - Color theme extension
- **New Language Support** - Language grammar extension
- **New Code Snippets** - Snippet extension
- **New Keymap** - Keyboard shortcut mappings
- **New Extension Pack** - Bundle multiple extensions

### Manual Setup

For custom setups, minimum requirements:

```json
// package.json
{
  "name": "my-extension",
  "displayName": "My Extension",
  "description": "Description",
  "version": "0.0.1",
  "engines": {
    "vscode": "^1.80.0"
  },
  "categories": ["Other"],
  "activationEvents": [],
  "main": "./out/extension.js",
  "contributes": {},
  "scripts": {
    "vscode:prepublish": "npm run compile",
    "compile": "tsc -p ./",
    "watch": "tsc -watch -p ./"
  },
  "devDependencies": {
    "@types/vscode": "^1.80.0",
    "@types/node": "16.x",
    "typescript": "^5.0.0"
  }
}
```

## Command Extensions

Commands are the building blocks of VS Code extensions.

### Basic Command Registration

```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    // Register a command
    let disposable = vscode.commands.registerCommand('myextension.helloWorld', () => {
        vscode.window.showInformationMessage('Hello World from My Extension!');
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {}
```

### Declaring Commands in package.json

```json
{
  "contributes": {
    "commands": [
      {
        "command": "myextension.helloWorld",
        "title": "Hello World",
        "category": "My Extension"
      }
    ]
  }
}
```

### Adding Keybindings

```json
{
  "contributes": {
    "keybindings": [
      {
        "command": "myextension.helloWorld",
        "key": "ctrl+shift+h",
        "mac": "cmd+shift+h",
        "when": "editorTextFocus"
      }
    ]
  }
}
```

### Adding Menu Items

```json
{
  "contributes": {
    "menus": {
      "editor/context": [
        {
          "command": "myextension.helloWorld",
          "group": "navigation",
          "when": "editorHasSelection"
        }
      ],
      "explorer/context": [
        {
          "command": "myextension.processFile",
          "group": "2_workspace"
        }
      ]
    }
  }
}
```

## Tree View Extensions

Tree views create custom explorers in the sidebar.

### Basic Tree View Implementation

```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    const treeDataProvider = new MyTreeDataProvider();
    
    vscode.window.registerTreeDataProvider('myTreeView', treeDataProvider);
    
    vscode.commands.registerCommand('myextension.refreshTree', () => {
        treeDataProvider.refresh();
    });
}

class MyTreeDataProvider implements vscode.TreeDataProvider<TreeItem> {
    private _onDidChangeTreeData = new vscode.EventEmitter<TreeItem | undefined>();
    readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

    refresh(): void {
        this._onDidChangeTreeData.fire(undefined);
    }

    getTreeItem(element: TreeItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: TreeItem): Thenable<TreeItem[]> {
        if (!element) {
            // Return root items
            return Promise.resolve([
                new TreeItem('Item 1', vscode.TreeItemCollapsibleState.None),
                new TreeItem('Item 2', vscode.TreeItemCollapsibleState.None)
            ]);
        }
        return Promise.resolve([]);
    }
}

class TreeItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState
    ) {
        super(label, collapsibleState);
    }
}
```

### Declaring Tree View in package.json

```json
{
  "contributes": {
    "viewsContainers": {
      "activitybar": [
        {
          "id": "myContainer",
          "title": "My Container",
          "icon": "resources/icon.svg"
        }
      ]
    },
    "views": {
      "myContainer": [
        {
          "id": "myTreeView",
          "name": "My Tree View"
        }
      ]
    }
  }
}
```

## Webview Extensions

Webviews allow building custom UI with HTML/CSS/JavaScript.

### Creating a Webview Panel

```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    context.subscriptions.push(
        vscode.commands.registerCommand('myextension.openWebview', () => {
            const panel = vscode.window.createWebviewPanel(
                'myWebview',
                'My Webview',
                vscode.ViewColumn.One,
                {
                    enableScripts: true,
                    localResourceRoots: [vscode.Uri.joinPath(context.extensionUri, 'media')]
                }
            );

            panel.webview.html = getWebviewContent(panel.webview, context.extensionUri);

            // Handle messages from webview
            panel.webview.onDidReceiveMessage(
                message => {
                    switch (message.command) {
                        case 'alert':
                            vscode.window.showInformationMessage(message.text);
                            return;
                    }
                },
                undefined,
                context.subscriptions
            );
        })
    );
}

function getWebviewContent(webview: vscode.Webview, extensionUri: vscode.Uri): string {
    const scriptUri = webview.asWebviewUri(vscode.Uri.joinPath(extensionUri, 'media', 'main.js'));
    const styleUri = webview.asWebviewUri(vscode.Uri.joinPath(extensionUri, 'media', 'style.css'));

    return `<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="${styleUri}" rel="stylesheet">
        <title>My Webview</title>
    </head>
    <body>
        <h1>Hello from Webview!</h1>
        <button onclick="sendMessage()">Click me</button>
        <script src="${scriptUri}"></script>
    </body>
    </html>`;
}
```

### Webview JavaScript (media/main.js)

```javascript
const vscode = acquireVsCodeApi();

function sendMessage() {
    vscode.postMessage({
        command: 'alert',
        text: 'Button clicked!'
    });
}
```

## Language Extensions

Language extensions provide IDE features for programming languages.

### Declarative Language Features

Syntax highlighting and basic editing support via grammar files:

```json
{
  "contributes": {
    "languages": [
      {
        "id": "mylanguage",
        "aliases": ["MyLanguage", "mylang"],
        "extensions": [".mylang"],
        "configuration": "./language-configuration.json"
      }
    ],
    "grammars": [
      {
        "language": "mylanguage",
        "scopeName": "source.mylang",
        "path": "./syntaxes/mylang.tmLanguage.json"
      }
    ]
  }
}
```

### Programmatic Language Features

For IntelliSense, diagnostics, and other advanced features:

```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    // Completion provider
    const completionProvider = vscode.languages.registerCompletionItemProvider(
        'mylanguage',
        {
            provideCompletionItems(document: vscode.TextDocument, position: vscode.Position) {
                const completionItem = new vscode.CompletionItem('myFunction');
                completionItem.kind = vscode.CompletionItemKind.Function;
                completionItem.detail = 'My function description';
                completionItem.insertText = new vscode.SnippetString('myFunction($1)$0');
                return [completionItem];
            }
        }
    );

    // Hover provider
    const hoverProvider = vscode.languages.registerHoverProvider('mylanguage', {
        provideHover(document, position) {
            return new vscode.Hover('**myFunction** - Does something useful');
        }
    });

    // Diagnostic provider
    const diagnosticCollection = vscode.languages.createDiagnosticCollection('mylanguage');
    context.subscriptions.push(diagnosticCollection);

    // Update diagnostics on document change
    vscode.workspace.onDidChangeTextDocument(event => {
        if (event.document.languageId === 'mylanguage') {
            updateDiagnostics(event.document, diagnosticCollection);
        }
    });

    context.subscriptions.push(completionProvider, hoverProvider);
}

function updateDiagnostics(document: vscode.TextDocument, collection: vscode.DiagnosticCollection) {
    const diagnostics: vscode.Diagnostic[] = [];
    
    // Example: Find 'TODO' comments
    const text = document.getText();
    const pattern = /TODO:/g;
    let match;
    
    while ((match = pattern.exec(text)) !== null) {
        const startPos = document.positionAt(match.index);
        const endPos = document.positionAt(match.index + match[0].length);
        const range = new vscode.Range(startPos, endPos);
        
        const diagnostic = new vscode.Diagnostic(
            range,
            'TODO found',
            vscode.DiagnosticSeverity.Information
        );
        diagnostics.push(diagnostic);
    }
    
    collection.set(document.uri, diagnostics);
}
```

## Theme Extensions

Create color themes for VS Code.

### Color Theme Structure

```json
// package.json
{
  "contributes": {
    "themes": [
      {
        "label": "My Dark Theme",
        "uiTheme": "vs-dark",
        "path": "./themes/my-dark-theme.json"
      }
    ]
  }
}
```

### Theme File (themes/my-dark-theme.json)

```json
{
  "name": "My Dark Theme",
  "type": "dark",
  "colors": {
    "editor.background": "#1e1e1e",
    "editor.foreground": "#d4d4d4",
    "activityBar.background": "#2c2c2c",
    "sideBar.background": "#252526",
    "statusBar.background": "#007acc"
  },
  "tokenColors": [
    {
      "scope": "comment",
      "settings": {
        "foreground": "#6A9955"
      }
    },
    {
      "scope": "keyword",
      "settings": {
        "foreground": "#569cd6"
      }
    }
  ]
}
```

## Configuration and Settings

Allow users to configure extension behavior.

### Declaring Configuration

```json
{
  "contributes": {
    "configuration": {
      "title": "My Extension",
      "properties": {
        "myextension.enable": {
          "type": "boolean",
          "default": true,
          "description": "Enable or disable the extension"
        },
        "myextension.maxItems": {
          "type": "number",
          "default": 10,
          "description": "Maximum number of items to display"
        },
        "myextension.customPath": {
          "type": "string",
          "default": "",
          "description": "Custom path for resources"
        }
      }
    }
  }
}
```

### Reading Configuration

```typescript
const config = vscode.workspace.getConfiguration('myextension');
const isEnabled = config.get<boolean>('enable');
const maxItems = config.get<number>('maxItems', 10);

// Listen for configuration changes
vscode.workspace.onDidChangeConfiguration(event => {
    if (event.affectsConfiguration('myextension.enable')) {
        const newValue = vscode.workspace.getConfiguration('myextension').get('enable');
        console.log('Setting changed:', newValue);
    }
});
```

## Testing Extensions

Test your extension with the VS Code Extension Test Runner.

### Test Setup

```typescript
// src/test/suite/extension.test.ts
import * as assert from 'assert';
import * as vscode from 'vscode';

suite('Extension Test Suite', () => {
    vscode.window.showInformationMessage('Start all tests.');

    test('Sample test', () => {
        assert.strictEqual(-1, [1, 2, 3].indexOf(5));
        assert.strictEqual(0, [1, 2, 3].indexOf(1));
    });

    test('Extension should be present', () => {
        assert.ok(vscode.extensions.getExtension('publisher.extension-name'));
    });
});
```

### Running Tests

```bash
npm test
```

## Publishing Extensions

Package and publish extensions to the VS Code Marketplace.

### Prerequisites

1. Install vsce: `npm install -g @vscode/vsce`
2. Create a publisher account at https://marketplace.visualstudio.com

### Package Extension

```bash
vsce package
# Creates extension-name-0.0.1.vsix
```

### Publish Extension

```bash
# Create Personal Access Token on Azure DevOps
vsce login <publisher-name>

# Publish
vsce publish
```

### Publishing Checklist

- [ ] Update version in package.json
- [ ] Add README.md with description and usage
- [ ] Add CHANGELOG.md
- [ ] Add LICENSE file
- [ ] Test extension thoroughly
- [ ] Add icon (128x128 PNG)
- [ ] Bundle extension for smaller size
- [ ] Review package contents with `vsce ls`

## Best Practices

1. **Use TypeScript** for better type safety and IntelliSense
2. **Dispose resources** properly by adding to `context.subscriptions`
3. **Minimize activation events** to reduce startup impact
4. **Bundle for production** using webpack or esbuild
5. **Follow UX guidelines** from https://code.visualstudio.com/api/ux-guidelines/overview
6. **Handle errors gracefully** and provide helpful messages
7. **Test across platforms** (Windows, macOS, Linux)
8. **Version VS Code API** appropriately in engines.vscode
9. **Document configuration** options clearly
10. **Provide samples** and documentation for users
