# Basic Linux (Ubuntu GNOME) Setup

---

## 1. Workspaces

### Set 3 Fixed Workspaces
```bash
gsettings set org.gnome.mutter dynamic-workspaces false
gsettings set org.gnome.desktop.wm.preferences num-workspaces 3
```

### Workspace Indicator (Space Bar extension)
Shows `1  2  3` in the top-left panel — highlights the active workspace.

1. Open **Extension Manager** (pre-installed on Ubuntu)
2. Browse tab -> search **"Space Bar"** by Christopher Schnett
3. Install it

If Extension Manager is not installed:
```bash
sudo apt install gnome-shell-extension-manager
```

### Workspace Shortcuts
| Action | Shortcut |
|--------|----------|
| Switch to workspace above | `Super + Page Up` |
| Switch to workspace below | `Super + Page Down` |
| Move window to workspace above | `Super + Shift + Page Up` |
| Move window to workspace below | `Super + Shift + Page Down` |
| Activities overview (all workspaces) | `Super` |

---

## 2. System Monitor in Top Bar

### Vitals Extension
Shows CPU temp, CPU usage, RAM usage, network speed in the top-right panel.

1. Open **Extension Manager**
2. Browse tab -> search **"Vitals"** by CoreCoding
3. Install it

Right-click the Vitals indicator in the top bar to configure which sensors to show/hide.

---

## 3. Flameshot (Screenshot Tool)

### Install
```bash
sudo apt install flameshot
```

### Bind to `Ctrl+Shift+S`
```bash
gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings \
  "['/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/']"

gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:\
/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ \
  name 'Flameshot Screenshot'

gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:\
/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ \
  command 'flameshot gui'

gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:\
/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ \
  binding '<Super><Shift>s'
```

Press `Super+Shift+S` to take a screenshot — select area, annotate, copy/save.

---

## 4. Ulauncher (Spotlight-like App Launcher)

### Install
```bash
sudo add-apt-repository ppa:agornostal/ulauncher
sudo apt update
sudo apt install ulauncher
```

### Setup
1. Run `ulauncher` once to create config
2. Open Ulauncher settings (gear icon)
3. Set **Hotkey** to `Alt+Space`
4. Enable **Launch at Login**

### Free up Alt+Space (taken by GNOME window menu)
```bash
gsettings set org.gnome.desktop.wm.keybindings activate-window-menu '[]'
```

Press `Alt+Space` to launch — type to search apps, files, calculations, etc.

---

## 5. Clipboard Indicator (Clipboard History)

Keeps a history of everything you copy — never lose a copied item again.

### Install
1. Open **Extension Manager**
2. Browse tab -> search **"Clipboard Indicator"** by Tudmotu
3. Install it

A clipboard icon appears in the top bar. Click it to see your copy history and pick any previous item to paste.
