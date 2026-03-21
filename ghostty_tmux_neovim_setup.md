# Ubuntu Dev Environment Setup

## Overview
Modern, minimal terminal setup for neovim + tmux on Ubuntu.

---

## 1. Install Prerequisites
```bash
sudo apt install fonts-jetbrains-mono zsh curl git
```

## 2. Install Ghostty
Download from https://ghostty.org and install.

## 3. Ghostty Config
Create the file `~/.config/ghostty/config` (NOT `config.ghostty`):

```
# Font
font-family = JetBrains Mono
font-size = 13
font-thicken = true
adjust-cell-height = 2

# Theme
theme = Catppuccin Mocha
background-opacity = 0.85
background-blur-radius = 30

# Window
window-padding-x = 16
window-padding-y = 10
window-padding-balance = true
window-padding-color = extend
window-decoration = true
confirm-close-surface = false
gtk-titlebar = true

# Cursor
cursor-style = block
cursor-style-blink = false
cursor-color = #f5e0dc

# Mouse
mouse-hide-while-typing = true

# Clipboard
copy-on-select = clipboard
clipboard-paste-protection = false

# Bold is bright
bold-is-bright = true

# Shell
command = /usr/bin/zsh

# Shell integration
shell-integration = detect

# Neovim/tmux compatibility
window-inherit-working-directory = true
```

## 4. Oh My Zsh Setup
```bash
# Install Oh My Zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Set zsh as default shell
chsh -s $(which zsh)
```
- **Theme**: robbyrussell (default — same as ThePrimeagen)
- Config: `~/.zshrc` — change `ZSH_THEME="robbyrussell"` to switch themes

## 5. Ghostty Keyboard Shortcuts
| Action | Shortcut |
|--------|----------|
| New window | `Ctrl+Shift+N` |
| New tab | `Ctrl+Shift+T` |
| Close tab/window | `Ctrl+Shift+W` |
| Quit Ghostty | `Ctrl+Shift+Q` |

---

## 6. tmux Setup (ThePrimeagen-inspired)

### Install
```bash
sudo apt install tmux xclip
```

### Config
Create `~/.tmux.conf`:

```bash
# Fix colors and enable true color
set -ga terminal-overrides ",screen-256color*:Tc"
set-option -g default-terminal "screen-256color"

# Use zsh (fixes Oh My Zsh not loading inside tmux)
set-option -g default-shell /usr/bin/zsh

# No delay after pressing Escape (critical for neovim)
set -s escape-time 0

# Remap prefix from C-b to C-a
unbind C-b
set-option -g prefix C-a
bind-key C-a send-prefix

# Status bar style
set -g status-style 'bg=#333333 fg=#5eacd3'

# Reload config with prefix + r
bind r source-file ~/.tmux.conf \; display "Config reloaded!"

# Windows start at 1, not 0
set -g base-index 1
set-window-option -g pane-base-index 1

# Renumber windows when one is closed
set -g renumber-windows on

# Vi mode for copy
set-window-option -g mode-keys vi
bind -T copy-mode-vi v send-keys -X begin-selection
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel 'xclip -in -selection clipboard'

# Vim-like pane switching
bind -r ^ last-window
bind -r k select-pane -U
bind -r j select-pane -D
bind -r h select-pane -L
bind -r l select-pane -R

# Split panes with | and - (in current path)
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"

# New window in current path
bind c new-window -c "#{pane_current_path}"

# Mouse support
set -g mouse on

# Increase scrollback
set -g history-limit 50000
```

### Dev Session Launcher
Saved at `~/.local/bin/dev` — just type `dev` from any directory to start.
All 3 windows open in the directory you launched from (e.g. `cd ~/projects/myapp && dev`).

```bash
#!/usr/bin/env bash
# Dev session launcher — starts tmux with 3 windows:
#   1: neovim (empty)   2: claude   3: terminal

SESSION="dev"

# If already in the session, bail
if tmux has-session -t "$SESSION" 2>/dev/null; then
    tmux attach-session -t "$SESSION"
    exit 0
fi

# Create session with first window: neovim (empty shell)
tmux new-session -d -s "$SESSION" -n "neovim" -c "$(pwd)"

# Window 2: claude
tmux new-window -t "$SESSION:2" -n "claude" -c "$(pwd)"

# Window 3: terminal
tmux new-window -t "$SESSION:3" -n "terminal" -c "$(pwd)"

# Start on window 1 (nvim)
tmux select-window -t "$SESSION:1"

# Attach
tmux attach-session -t "$SESSION"
```

### Session Management

| What you want | Command |
|---|---|
| Start/reattach dev session | `dev` |
| Detach (keep running in background) | `C-a d` |
| List all sessions | `tmux ls` |
| Kill the dev session | `tmux kill-session -t dev` |
| Kill ALL sessions | `tmux kill-server` |

### tmux Keyboard Shortcuts
Prefix is `Ctrl+a` (not the default `Ctrl+b`).

| Action | Shortcut |
|--------|----------|
| Switch to window 1/2/3 | `C-a 1` / `C-a 2` / `C-a 3` |
| Last window | `C-a ^` |
| New window | `C-a c` |
| Split horizontal | `C-a \|` |
| Split vertical | `C-a -` |
| Pane left/down/up/right | `C-a h` / `C-a j` / `C-a k` / `C-a l` |
| Reload config | `C-a r` |
| Copy mode (vi) | `C-a [` then `v` to select, `y` to yank |
| Detach | `C-a d` |
| Kill pane | `C-a x` |

---

## Gotchas
- Ghostty does **NOT** hot-reload config — restart the terminal to apply changes.
- Theme names use spaces and capitals (e.g. `Catppuccin Mocha`, not `catppuccin-mocha`).
- To list available themes: `ls /usr/share/ghostty/themes/`
- If zsh doesn't load, make sure `command = /usr/bin/zsh` is in the Ghostty config — it may default to bash.
- If Oh My Zsh doesn't load inside tmux, make sure `set-option -g default-shell /usr/bin/zsh` is in `~/.tmux.conf`.
- tmux prefix is `C-a` (ThePrimeagen style), NOT the default `C-b`.
- After editing `~/.tmux.conf`, reload with `C-a r` or `tmux source-file ~/.tmux.conf`.
