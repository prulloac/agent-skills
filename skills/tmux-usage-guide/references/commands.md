# Tmux Commands Reference

## Session Management

### Creating Sessions
```bash
tmux                                    # Start new session
tmux new -s <session-name>              # Start new session with name
tmux new -s <name> -n <window-name>     # Start with named window
tmux new -d -s <name>                   # Start detached session
```

### Attaching to Sessions
```bash
tmux attach                             # Attach to last session
tmux attach -t <session-name>           # Attach to named session
tmux a -t <name>                        # Short form
tmux attach -d -t <name>                # Detach others and attach
```

### Session Operations
```bash
tmux ls                                 # List sessions
tmux list-sessions                      # List sessions (long form)
tmux kill-session -t <name>             # Kill specific session
tmux kill-session -a                    # Kill all but current
tmux kill-server                        # Kill all sessions
tmux rename-session -t <old> <new>      # Rename session
```

## Window Management

### Creating and Closing Windows
```bash
Prefix c                                # Create new window
Prefix ,                                # Rename current window
Prefix &                                # Kill current window
Prefix n                                # Next window
Prefix p                                # Previous window
Prefix 0-9                              # Switch to window by number
Prefix w                                # List windows (interactive)
Prefix f                                # Find window by name
```

### Window Navigation
```bash
Prefix l                                # Last (previously selected) window
Prefix .                                # Move window (prompted for index)
Prefix '                                # Select window by index (prompted)
```

## Pane Management

### Splitting Panes
```bash
Prefix %                                # Split pane vertically (left/right)
Prefix "                                # Split pane horizontally (top/bottom)
tmux split-window -h                    # Split vertically (command form)
tmux split-window -v                    # Split horizontally (command form)
```

### Navigating Panes
```bash
Prefix o                                # Cycle through panes
Prefix ;                                # Toggle between current and last pane
Prefix Up/Down/Left/Right               # Move to pane in direction
Prefix q                                # Show pane numbers (briefly)
Prefix q <number>                       # Show numbers and select by number
```

### Resizing Panes
```bash
Prefix Ctrl-Up/Down/Left/Right          # Resize by 1 cell
Prefix Alt-Up/Down/Left/Right           # Resize by 5 cells
tmux resize-pane -U 10                  # Resize up 10 cells
tmux resize-pane -D 10                  # Resize down 10 cells
tmux resize-pane -L 10                  # Resize left 10 cells
tmux resize-pane -R 10                  # Resize right 10 cells
```

### Pane Layouts
```bash
Prefix Space                            # Cycle through preset layouts
Prefix Alt-1                            # Even horizontal layout
Prefix Alt-2                            # Even vertical layout
Prefix Alt-3                            # Main horizontal layout
Prefix Alt-4                            # Main horizontal mirrored
Prefix Alt-5                            # Main vertical layout
```

### Pane Operations
```bash
Prefix x                                # Kill current pane
Prefix !                                # Break pane to new window
Prefix z                                # Toggle pane zoom
Prefix {                                # Swap with previous pane
Prefix }                                # Swap with next pane
Prefix Ctrl-o                           # Rotate panes forward
Prefix Alt-o                            # Rotate panes backward
```

## Copy Mode

### Entering and Exiting
```bash
Prefix [                                # Enter copy mode
q                                       # Exit copy mode (in copy mode)
Escape                                  # Exit copy mode (in copy mode)
```

### Navigation in Copy Mode (vi mode)
```bash
h, j, k, l                              # Move cursor left, down, up, right
w                                       # Next word
b                                       # Previous word
0                                       # Start of line
$                                       # End of line
g                                       # Top of history
G                                       # Bottom of history
Ctrl-f                                  # Page down
Ctrl-b                                  # Page up
Ctrl-d                                  # Half page down
Ctrl-u                                  # Half page up
/                                       # Search forward
?                                       # Search backward
n                                       # Next search result
N                                       # Previous search result
```

### Selecting and Copying (vi mode)
```bash
Space                                   # Start selection
Enter                                   # Copy selection and exit
v                                       # Toggle rectangle selection
```

### Pasting
```bash
Prefix ]                                # Paste most recent buffer
Prefix =                                # Choose buffer to paste
Prefix #                                # List all paste buffers
```

## Session Control (from within tmux)

### Detaching and Switching
```bash
Prefix d                                # Detach from session
Prefix D                                # Choose client to detach
Prefix (                                # Switch to previous session
Prefix )                                # Switch to next session
Prefix s                                # List and switch sessions
Prefix L                                # Switch to last session
```

## Miscellaneous

### Information and Help
```bash
Prefix ?                                # List all key bindings
Prefix i                                # Display window information
Prefix t                                # Show time
Prefix ~                                # Show previous messages
tmux info                               # Show server information
tmux list-keys                          # List all key bindings
tmux list-commands                      # List all commands
```

### Command Prompt
```bash
Prefix :                                # Enter command mode
# Examples:
:new-window -n logs                     # Create window named "logs"
:split-window -h                        # Split horizontally
:set -g status-bg cyan                  # Set status bar color
```

### Reloading Configuration
```bash
Prefix :source-file ~/.tmux.conf        # Reload config from command mode
tmux source-file ~/.tmux.conf           # Reload config from shell
```

## Common Command-Line Operations

### Sending Commands
```bash
tmux send-keys -t <target> "command" Enter  # Send command to target
tmux send-keys -t mysession:1.0 "ls" Enter  # Send to specific pane
```

### Targeting Syntax
```bash
# Session
tmux <command> -t mysession

# Window
tmux <command> -t mysession:1
tmux <command> -t mysession:windowname

# Pane
tmux <command> -t mysession:1.0
tmux <command> -t mysession:windowname.0
```

## Notes

- **Prefix Key**: Default is `Ctrl-b` (written as `C-b` or `Prefix`)
- **vi vs emacs mode**: Set with `set -g mode-keys vi` or `set -g mode-keys emacs`
- **Target Notation**: Sessions use `:`, windows use `.`, panes use numbers
- **Index Starting**: Panes, windows, and sessions start at 0 by default
