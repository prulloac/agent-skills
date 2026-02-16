# VS Code API Quick Reference

Quick lookup for commonly used VS Code APIs.

## Window API

### Show Messages

```typescript
// Information message
vscode.window.showInformationMessage('Info message');

// Warning message
vscode.window.showWarningMessage('Warning message');

// Error message
vscode.window.showErrorMessage('Error message');

// Message with actions
vscode.window.showInformationMessage('Choose an option', 'Option 1', 'Option 2')
    .then(selection => {
        if (selection === 'Option 1') {
            // Handle Option 1
        }
    });
```

### Quick Pick

```typescript
// Simple quick pick
const items = ['Item 1', 'Item 2', 'Item 3'];
const selected = await vscode.window.showQuickPick(items, {
    placeHolder: 'Select an item'
});

// Quick pick with custom items
interface MyQuickPickItem extends vscode.QuickPickItem {
    value: string;
}

const items: MyQuickPickItem[] = [
    { label: 'Option 1', description: 'First option', value: 'opt1' },
    { label: 'Option 2', description: 'Second option', value: 'opt2' }
];

const selected = await vscode.window.showQuickPick(items);
```

### Input Box

```typescript
const input = await vscode.window.showInputBox({
    prompt: 'Enter your name',
    placeHolder: 'Name',
    validateInput: (value) => {
        return value.length < 3 ? 'Name must be at least 3 characters' : undefined;
    }
});
```

### Open Dialog

```typescript
// Open file dialog
const fileUris = await vscode.window.showOpenDialog({
    canSelectMany: false,
    openLabel: 'Select',
    filters: {
        'Text files': ['txt'],
        'All files': ['*']
    }
});

// Save dialog
const saveUri = await vscode.window.showSaveDialog({
    saveLabel: 'Save',
    filters: {
        'JSON files': ['json']
    }
});
```

### Output Channel

```typescript
const outputChannel = vscode.window.createOutputChannel('My Extension');
outputChannel.appendLine('Log message');
outputChannel.show();
```

### Status Bar

```typescript
const statusBarItem = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Left,
    100
);
statusBarItem.text = '$(sync~spin) Loading...';
statusBarItem.tooltip = 'Loading data';
statusBarItem.command = 'myextension.command';
statusBarItem.show();
```

### Progress

```typescript
vscode.window.withProgress({
    location: vscode.ProgressLocation.Notification,
    title: "Loading...",
    cancellable: true
}, async (progress, token) => {
    token.onCancellationRequested(() => {
        console.log("User canceled the operation");
    });

    progress.report({ increment: 0 });

    for (let i = 0; i < 100; i++) {
        await new Promise(resolve => setTimeout(resolve, 100));
        progress.report({ 
            increment: 1,
            message: `${i}% complete`
        });
    }
});
```

## Workspace API

### Get Configuration

```typescript
const config = vscode.workspace.getConfiguration('myextension');
const value = config.get<string>('setting');

// Update configuration
await config.update('setting', 'new value', vscode.ConfigurationTarget.Global);
```

### File System

```typescript
// Read file
const uri = vscode.Uri.file('/path/to/file.txt');
const content = await vscode.workspace.fs.readFile(uri);
const text = Buffer.from(content).toString('utf8');

// Write file
const writeData = Buffer.from('Hello World', 'utf8');
await vscode.workspace.fs.writeFile(uri, writeData);

// Check if file exists
try {
    await vscode.workspace.fs.stat(uri);
    // File exists
} catch {
    // File doesn't exist
}

// Delete file
await vscode.workspace.fs.delete(uri);
```

### Find Files

```typescript
// Find all TypeScript files
const files = await vscode.workspace.findFiles('**/*.ts', '**/node_modules/**');

// Find with limit
const limitedFiles = await vscode.workspace.findFiles('**/*.ts', null, 10);
```

### Text Documents

```typescript
// Get active editor's document
const document = vscode.window.activeTextEditor?.document;

// Open document
const doc = await vscode.workspace.openTextDocument('/path/to/file.txt');

// Show document in editor
await vscode.window.showTextDocument(doc);

// Get all open documents
const documents = vscode.workspace.textDocuments;
```

### Workspace Folders

```typescript
// Get workspace folders
const folders = vscode.workspace.workspaceFolders;

if (folders && folders.length > 0) {
    const rootPath = folders[0].uri.fsPath;
}
```

### Events

```typescript
// Document changed
vscode.workspace.onDidChangeTextDocument(event => {
    console.log('Document changed:', event.document.uri);
});

// Document opened
vscode.workspace.onDidOpenTextDocument(document => {
    console.log('Document opened:', document.uri);
});

// Document saved
vscode.workspace.onDidSaveTextDocument(document => {
    console.log('Document saved:', document.uri);
});

// Configuration changed
vscode.workspace.onDidChangeConfiguration(event => {
    if (event.affectsConfiguration('myextension')) {
        console.log('Configuration changed');
    }
});
```

## Commands API

### Register Command

```typescript
const disposable = vscode.commands.registerCommand('myextension.command', 
    async (...args: any[]) => {
        // Command implementation
    }
);

context.subscriptions.push(disposable);
```

### Execute Command

```typescript
await vscode.commands.executeCommand('workbench.action.files.save');
await vscode.commands.executeCommand('vscode.open', vscode.Uri.file('/path'));
```

### Get All Commands

```typescript
const commands = await vscode.commands.getCommands();
```

## Languages API

### Completion Provider

```typescript
vscode.languages.registerCompletionItemProvider('typescript', {
    provideCompletionItems(document, position) {
        const item = new vscode.CompletionItem('myFunction');
        item.kind = vscode.CompletionItemKind.Function;
        item.insertText = new vscode.SnippetString('myFunction($1)$0');
        item.documentation = new vscode.MarkdownString('**myFunction**\n\nDescription');
        return [item];
    }
});
```

### Hover Provider

```typescript
vscode.languages.registerHoverProvider('typescript', {
    provideHover(document, position) {
        const markdown = new vscode.MarkdownString();
        markdown.appendCodeblock('function myFunc(): void', 'typescript');
        markdown.appendMarkdown('\n\nDescription of the function');
        return new vscode.Hover(markdown);
    }
});
```

### Diagnostic Provider

```typescript
const diagnosticCollection = vscode.languages.createDiagnosticCollection('myextension');

function updateDiagnostics(document: vscode.TextDocument) {
    const diagnostics: vscode.Diagnostic[] = [];
    
    const range = new vscode.Range(0, 0, 0, 10);
    const diagnostic = new vscode.Diagnostic(
        range,
        'Error message',
        vscode.DiagnosticSeverity.Error
    );
    diagnostic.code = 'ERROR_CODE';
    diagnostic.source = 'myextension';
    
    diagnostics.push(diagnostic);
    diagnosticCollection.set(document.uri, diagnostics);
}
```

### Code Actions

```typescript
vscode.languages.registerCodeActionsProvider('typescript', {
    provideCodeActions(document, range, context) {
        const fixes: vscode.CodeAction[] = [];
        
        for (const diagnostic of context.diagnostics) {
            if (diagnostic.code === 'ERROR_CODE') {
                const fix = new vscode.CodeAction(
                    'Fix this error',
                    vscode.CodeActionKind.QuickFix
                );
                fix.edit = new vscode.WorkspaceEdit();
                fix.edit.replace(document.uri, range, 'fixed text');
                fix.diagnostics = [diagnostic];
                fixes.push(fix);
            }
        }
        
        return fixes;
    }
});
```

### Formatting

```typescript
// Document formatter
vscode.languages.registerDocumentFormattingEditProvider('typescript', {
    provideDocumentFormattingEdits(document) {
        const edits: vscode.TextEdit[] = [];
        // Add formatting edits
        return edits;
    }
});

// Range formatter
vscode.languages.registerDocumentRangeFormattingEditProvider('typescript', {
    provideDocumentRangeFormattingEdits(document, range) {
        const edits: vscode.TextEdit[] = [];
        // Add formatting edits for range
        return edits;
    }
});
```

### Definition Provider

```typescript
vscode.languages.registerDefinitionProvider('typescript', {
    provideDefinition(document, position) {
        const range = document.getWordRangeAtPosition(position);
        const word = document.getText(range);
        
        // Find definition location
        const definitionUri = vscode.Uri.file('/path/to/definition.ts');
        const definitionPosition = new vscode.Position(10, 5);
        
        return new vscode.Location(definitionUri, definitionPosition);
    }
});
```

### Reference Provider

```typescript
vscode.languages.registerReferenceProvider('typescript', {
    provideReferences(document, position, context) {
        const locations: vscode.Location[] = [];
        
        // Find all references
        const uri = vscode.Uri.file('/path/to/file.ts');
        locations.push(new vscode.Location(uri, new vscode.Position(5, 10)));
        
        return locations;
    }
});
```

## Text Editor API

### Get Active Editor

```typescript
const editor = vscode.window.activeTextEditor;
if (editor) {
    const document = editor.document;
    const selection = editor.selection;
}
```

### Edit Document

```typescript
const editor = vscode.window.activeTextEditor;
if (editor) {
    await editor.edit(editBuilder => {
        // Insert text
        editBuilder.insert(new vscode.Position(0, 0), 'Hello ');
        
        // Replace text
        const range = new vscode.Range(0, 0, 0, 5);
        editBuilder.replace(range, 'Hi');
        
        // Delete text
        editBuilder.delete(range);
    });
}
```

### Set Selection

```typescript
const editor = vscode.window.activeTextEditor;
if (editor) {
    const position = new vscode.Position(5, 10);
    editor.selection = new vscode.Selection(position, position);
    
    // Reveal position
    editor.revealRange(
        new vscode.Range(position, position),
        vscode.TextEditorRevealType.InCenter
    );
}
```

### Decorations

```typescript
const decorationType = vscode.window.createTextEditorDecorationType({
    backgroundColor: 'rgba(255, 0, 0, 0.3)',
    border: '1px solid red'
});

const editor = vscode.window.activeTextEditor;
if (editor) {
    const ranges = [new vscode.Range(0, 0, 0, 10)];
    editor.setDecorations(decorationType, ranges);
}
```

## Extension Context

### Global State

```typescript
// Save state
await context.globalState.update('key', 'value');

// Read state
const value = context.globalState.get<string>('key');

// Get all keys
const keys = context.globalState.keys();
```

### Workspace State

```typescript
// Save workspace-specific state
await context.workspaceState.update('key', 'value');

// Read workspace state
const value = context.workspaceState.get<string>('key');
```

### Secrets

```typescript
// Store secret
await context.secrets.store('api-key', 'secret-value');

// Retrieve secret
const secret = await context.secrets.get('api-key');

// Delete secret
await context.secrets.delete('api-key');
```

### Extension Path

```typescript
// Extension root path
const extensionPath = context.extensionPath;

// Extension URI
const extensionUri = context.extensionUri;

// Storage paths
const globalStoragePath = context.globalStorageUri.fsPath;
const workspaceStoragePath = context.storageUri?.fsPath;
```

## URI Utilities

```typescript
// File URI
const fileUri = vscode.Uri.file('/path/to/file.txt');

// Parse URI
const uri = vscode.Uri.parse('file:///path/to/file.txt');

// Join paths
const joined = vscode.Uri.joinPath(baseUri, 'subfolder', 'file.txt');

// Get file system path
const fsPath = uri.fsPath;

// Convert to string
const uriString = uri.toString();
```

## Disposables

```typescript
// Create disposable
const disposable = new vscode.Disposable(() => {
    // Cleanup code
});

// Add to subscriptions for automatic disposal
context.subscriptions.push(disposable);

// Dispose manually
disposable.dispose();

// Composite disposable
const disposables: vscode.Disposable[] = [];
disposables.push(subscription1);
disposables.push(subscription2);

// Dispose all
vscode.Disposable.from(...disposables).dispose();
```

## Common Patterns

### Check if File is Open

```typescript
function isFileOpen(uri: vscode.Uri): boolean {
    return vscode.workspace.textDocuments.some(doc => 
        doc.uri.toString() === uri.toString()
    );
}
```

### Get Workspace Root

```typescript
function getWorkspaceRoot(): string | undefined {
    const folders = vscode.workspace.workspaceFolders;
    return folders && folders.length > 0 ? folders[0].uri.fsPath : undefined;
}
```

### Debounce Function

```typescript
function debounce<T extends (...args: any[]) => any>(
    func: T,
    wait: number
): (...args: Parameters<T>) => void {
    let timeout: NodeJS.Timeout | undefined;
    return (...args: Parameters<T>) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), wait);
    };
}

// Usage
const debouncedUpdate = debounce((document: vscode.TextDocument) => {
    // Update logic
}, 300);

vscode.workspace.onDidChangeTextDocument(event => {
    debouncedUpdate(event.document);
});
```

### Get Selected Text

```typescript
function getSelectedText(): string | undefined {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        return undefined;
    }
    
    const selection = editor.selection;
    return editor.document.getText(selection);
}
```

### Replace Selected Text

```typescript
async function replaceSelectedText(newText: string): Promise<void> {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        return;
    }
    
    await editor.edit(editBuilder => {
        editBuilder.replace(editor.selection, newText);
    });
}
```

## Icons

VS Code uses Codicons. Reference them with `$(icon-name)`:

```typescript
// In status bar
statusBarItem.text = '$(sync~spin) Loading...';

// In quick pick
const item: vscode.QuickPickItem = {
    label: '$(file) My File',
    description: '$(folder) /path/to/folder'
};

// Common icons
// $(check) ✓
// $(x) ✗
// $(warning) ⚠
// $(info) ℹ
// $(gear) ⚙
// $(folder) 📁
// $(file) 📄
// $(sync) 🔄
```

Full icon reference: https://code.visualstudio.com/api/references/icons-in-labels
