# Tmux Configuration Reference

## Configuration File

The tmux configuration file is located at `~/.tmux.conf`. Commands in this file are executed when tmux starts.

## Essential Configuration Options

### General Settings
```bash
# Set prefix key to Ctrl-a instead of Ctrl-b
set -g prefix C-a
unbind C-b
bind C-a send-prefix

# Enable mouse support
set -g mouse on

# Set default terminal
set -g default-terminal "screen-256color"

# Increase scrollback buffer size
set -g history-limit 10000

# Start window and pane numbering at 1
set -g base-index 1
setw -g pane-base-index 1

# Renumber windows when one is closed
set -g renumber-windows on

# Don't rename windows automatically
set -g allow-rename off

# Reduce escape time for better vim responsiveness
set -sg escape-time 0

# Enable activity alerts
setw -g monitor-activity on
set -g visual-activity on
```

### Window and Pane Settings
```bash
# Split panes with | and - (more intuitive)
bind | split-window -h
bind - split-window -v
unbind '"'
unbind %

# Switch panes with vim-like keybindings
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R

# Resize panes with vim-like keybindings
bind -r H resize-pane -L 5
bind -r J resize-pane -D 5
bind -r K resize-pane -U 5
bind -r L resize-pane -R 5

# Easier pane reordering
bind -r "<" swap-window -d -t -1
bind -r ">" swap-window -d -t +1
```

### Copy Mode Settings
```bash
# Use vi keybindings in copy mode
setw -g mode-keys vi

# vi-like copy/paste bindings
bind -T copy-mode-vi v send -X begin-selection
bind -T copy-mode-vi y send -X copy-selection-and-cancel
bind -T copy-mode-vi C-v send -X rectangle-toggle

# Copy to system clipboard (Linux)
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "xclip -in -selection clipboard"

# Copy to system clipboard (macOS)
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "pbcopy"
```

### Status Bar Customization
```bash
# Position status bar at top
set -g status-position top

# Update status bar every N seconds
set -g status-interval 5

# Center window list
set -g status-justify centre

# Status bar colors
set -g status-style bg=black,fg=white

# Current window style
setw -g window-status-current-style bg=red,fg=white,bold

# Window status format
setw -g window-status-format " #I:#W "
setw -g window-status-current-format " #I:#W "

# Left status: session name
set -g status-left-length 40
set -g status-left "#[fg=green]Session: #S #[fg=yellow]#I #[fg=cyan]#P"

# Right status: date and time
set -g status-right "#[fg=cyan]%d %b %R"

# Pane border colors
set -g pane-border-style fg=colour238
set -g pane-active-border-style fg=colour51
```

### Advanced Options
```bash
# Enable focus events for better terminal integration
set -g focus-events on

# Set terminal title
set -g set-titles on
set -g set-titles-string "#T - #W"

# Aggressive resize (useful for grouped sessions)
setw -g aggressive-resize on

# Enable RGB colour
set -ga terminal-overrides ",*256col*:Tc"
```

## Common Configuration Patterns

### Session Management Workflow
```bash
# Create new session in current directory
bind C-c new-session -c "#{pane_current_path}"

# Create new window in current directory
bind c new-window -c "#{pane_current_path}"

# Split in current directory
bind '"' split-window -c "#{pane_current_path}"
bind % split-window -h -c "#{pane_current_path}"
```

### Quick Reload
```bash
# Reload config with prefix + r
bind r source-file ~/.tmux.conf \; display-message "Config reloaded!"
```

### Synchronized Panes Toggle
```bash
# Toggle sending input to all panes
bind S set-window-option synchronize-panes\; display-message "synchronize-panes is now #{?pane_synchronized,on,off}"
```

### Break and Join Panes
```bash
# Break pane to new window
bind b break-pane -d

# Join pane from another window
bind j command-prompt -p "join pane from: " "join-pane -h -s '%%'"
```

## Format Variables Reference

Common variables for status bar and window formats:

- `#S` - Session name
- `#I` - Window index
- `#W` - Window name
- `#P` - Pane index
- `#T` - Pane title
- `#h` - Hostname
- `#H` - Hostname (long)
- `#{pane_current_path}` - Current directory
- `#{window_activity}` - Window activity time
- `#{?pane_synchronized,SYNC,}` - Conditional formatting

## Plugin Management with TPM

Tmux Plugin Manager (TPM) allows easy plugin installation:

```bash
# Installation
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

# In ~/.tmux.conf:
# List of plugins
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'

# Initialize plugin manager (keep at bottom of config)
run '~/.tmux/plugins/tpm/tpm'

# Usage:
# prefix + I - Install plugins
# prefix + U - Update plugins
# prefix + alt + u - Uninstall plugins
```

## Scope of Settings

- `set -g` - Set global option
- `set -s` - Set server option
- `setw -g` or `set -w` - Set window option
- `set -a` - Append to option
- `set -u` - Unset option

## Notes

- Options can be set globally (`-g`) or for a specific session/window
- Use `show-options` to see current settings
- Use `show-options -g` to see global settings
- Configuration is not automatically reloaded; use `source-file` command
