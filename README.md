# YabaDuma Config (In Progress).

## Tested on Macbook Air M4 with MacOS 26.2 Tahoe.

### Yabai WM + SKHD Keyboard Shortcuts.

#### **[Keybinds.md](Keybinds.md)** - Complete keybind guide.

### Visual & UX
- Minimal gaps 10px
- Window opacity (active: 1.0, inactive: 0.9)
- **JankyBorders** - Animated window borders with Gruvbox gradient
  - Active: White-beige gradient (Gruvbox light theme)
  - Width: 3px, rounded corners
- No window animations (macOS limitation)
- **Pywal integration** - Dynamic colors from wallpaper (In Progress)

### Input
- 4-finger MacOS gestures for workspace switch

---

## Components

- **yabai** - Tiling window manager with scripting addition
- **skhd** - Hotkey daemon for keyboard shortcuts
- **borders** (JankyBorders) - Window border system with gradient support

---

## Installation Guide

### Prerequisites
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add FelixKratz tap for borders
brew tap FelixKratz/formulae
```

### Install Components
```bash
# Install yabai and skhd
brew install koekeishiya/formulae/yabai
brew install koekeishiya/formulae/skhd

# Install borders
brew install borders
```

### Setup
```bash
# Clone this config
git clone https://github.com/duma799/yabaduma-config.git ~/.config/yabaduma-config

# Link configs (or copy files to appropriate locations)
ln -s ~/.config/yabaduma-config/yabairc ~/.yabairc
# ... add skhd linking when available

# Create borders config directory and link
mkdir -p ~/.config/borders
ln -s ~/.config/yabaduma-config/bordersrc ~/.config/borders/bordersrc

# Start services
brew services start yabai
brew services start skhd
brew services start borders
```

### Post-Installation
- Disable SIP (System Integrity Protection) partially for yabai scripting addition
- Configure accessibility permissions for yabai and skhd
- Restart services after configuration changes

**Full installation guide in progress.**