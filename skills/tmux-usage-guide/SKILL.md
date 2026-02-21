---
name: tmux
description: Terminal multiplexer expertise for session, window, and pane management. Use when working with tmux for creating/managing sessions, splitting windows into panes, configuring tmux settings, troubleshooting tmux issues, or answering questions about tmux commands, key bindings, configuration options, and workflows.
---

# Tmux

## Overview

This skill provides comprehensive guidance for working with tmux, a terminal multiplexer that enables multiple terminal sessions to be created, accessed, and controlled from a single screen.

## Core Concepts

tmux operates on a hierarchy:
- **Server**: Single process managing all sessions
- **Session**: Collection of windows (can detach/reattach)
- **Window**: Full screen view (like tabs)
- **Pane**: Split section of a window (separate terminal)

Default prefix key: `Ctrl-b` (written as `C-b` or `Prefix`)

## Quick Start

### Basic Session Workflow
```bash
# Start new session
tmux

# Detach from session (inside tmux)
Prefix d

# Reattach to session
tmux attach

# List sessions
tmux ls
```

### Common Operations
```bash
# Split panes
Prefix %        # Split vertically (left/right)
Prefix "        # Split horizontally (top/bottom)

# Navigate panes
Prefix o        # Cycle through panes
Prefix ↑↓←→     # Move to pane in direction

# Create windows
Prefix c        # New window
Prefix n/p      # Next/previous window
Prefix 0-9      # Switch to window number

# Copy mode (scroll and copy)
Prefix [        # Enter copy mode
q               # Exit copy mode
```

## When to Use This Skill

Use this skill for:

1. **Session Management**: Creating, naming, attaching, detaching sessions
2. **Window Operations**: Creating, switching, renaming, closing windows
3. **Pane Management**: Splitting, resizing, navigating, rearranging panes
4. **Configuration**: Setting up .tmux.conf, customizing key bindings, status bar
5. **Copy/Paste**: Using copy mode, selecting text, pasting buffers
6. **Troubleshooting**: Fixing issues with key bindings, terminal colors, or behavior
7. **Scripting**: Automating tmux operations, sending commands to sessions
8. **Workflow Optimization**: Setting up efficient development environments

## Answering Questions

When answering tmux-related questions:

1. **Identify the Context**: Determine if the question is about sessions, windows, panes, configuration, or commands
2. **Check Command Syntax**: Refer to [commands.md](references/commands.md) for exact syntax
3. **Consider Configuration**: Many behaviors can be customized via .tmux.conf (see [configuration.md](references/configuration.md))
4. **Provide Examples**: Include both key binding and command-line forms when applicable
5. **Explain Concepts**: Briefly explain the underlying concept (session/window/pane) when helpful

### Common Question Patterns

**"How do I..."** → Provide the key binding and/or command
```
Q: "How do I split a pane vertically?"
A: Press Prefix % or run: tmux split-window -h
```

**"What does X do?"** → Explain the command/key binding and its effect
```
Q: "What does Prefix z do?"
A: Toggles zoom on the current pane (makes it full screen or returns to split view)
```

**"How to configure..."** → Point to configuration options and provide example
```
Q: "How do I change the prefix key?"
A: Add to ~/.tmux.conf:
   set -g prefix C-a
   unbind C-b
   bind C-a send-prefix
```

**"My tmux is..."** → Troubleshoot based on symptoms
```
Q: "My colors look wrong"
A: Set in ~/.tmux.conf:
   set -g default-terminal "screen-256color"
   Then reload: tmux source-file ~/.tmux.conf
```

## Working with Configurations

For configuration questions, consult [configuration.md](references/configuration.md) which includes:
- Common configuration options
- Key binding customization
- Status bar customization
- Plugin management
- Scope of settings (global vs session vs window)

Example workflow:
1. Read the configuration reference to find relevant options
2. Provide the configuration snippet
3. Explain how to reload config: `tmux source-file ~/.tmux.conf`
4. Mention any caveats (e.g., some options require tmux restart)

## Command Reference

For detailed command syntax, refer to [commands.md](references/commands.md) which organizes commands by category:
- Session management
- Window management
- Pane management
- Copy mode operations
- Miscellaneous commands

When providing commands:
- Include both the key binding (for use inside tmux) and command form (for scripts/automation)
- Mention the target syntax when relevant (session:window.pane)
- Explain any flags or options used

## Common Workflows

### Development Environment Setup
```bash
# Create named session
tmux new -s dev

# Split for editor and terminal
Prefix "      # Horizontal split
Prefix %      # Vertical split on bottom

# Navigate and resize as needed
Prefix ↑↓←→   # Move between panes
Prefix Ctrl-↑↓←→  # Resize panes
```

### Persistent Remote Sessions
```bash
# Start session on remote server
ssh user@server
tmux new -s work

# Detach when disconnecting
Prefix d

# Reattach later
ssh user@server
tmux attach -t work
```

### Multi-Window Project
```bash
# Create session with windows
tmux new -s project -n editor
Prefix c      # New window for logs
Prefix ,      # Rename to "logs"
Prefix c      # New window for server
Prefix ,      # Rename to "server"

# Navigate between windows
Prefix w      # Interactive window list
Prefix 0-9    # Direct window selection
```

## Scripting and Automation

When helping with tmux automation:

```bash
# Send commands to specific session
tmux send-keys -t session:window.pane "command" Enter

# Create complex layouts programmatically
tmux new-session -d -s dev
tmux split-window -v -t dev
tmux split-window -h -t dev
tmux send-keys -t dev:0.0 "vim" Enter
tmux send-keys -t dev:0.1 "npm start" Enter
tmux attach -t dev
```

## Tips and Best Practices

1. **Use named sessions** for easier management: `tmux new -s name`
2. **Enable mouse support** for easier navigation: `set -g mouse on`
3. **Use vi mode** if familiar with vi: `setw -g mode-keys vi`
4. **Keep prefix simple**: Consider changing to `Ctrl-a` for easier reach
5. **Start numbering at 1**: More intuitive keyboard access with `set -g base-index 1`
6. **Learn copy mode**: Essential for scrolling and copying text
7. **Use synchronized panes** when managing multiple servers
8. **Leverage window/pane layouts** for consistent workspaces

## Resources

This skill includes two comprehensive reference documents:

- **[commands.md](references/commands.md)**: Complete command reference organized by category (session, window, pane management, copy mode, etc.)
- **[configuration.md](references/configuration.md)**: Configuration options, customization patterns, status bar formatting, and plugin management

Load these references when detailed syntax or configuration examples are needed.
