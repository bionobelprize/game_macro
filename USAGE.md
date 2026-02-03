# Quick Usage Guide

## Getting Started

### 1. Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### 2. Recording Your First Macro

1. Launch the application
2. Click **"Start Recording"** button
3. Perform your actions (mouse movements, clicks, keyboard inputs)
4. Click **"Stop Recording"** button
5. Enter a name for your macro (e.g., "My First Macro")
6. Click **"Save Macro"**

### 3. Playing Back a Macro

**Method 1: Manual Playback**
1. Select your macro from the list
2. Click **"Play Macro"** button

**Method 2: Hotkey Playback**
1. Select your macro from the list
2. Enter a hotkey combination (e.g., "ctrl+shift+1")
3. Click **"Save Macro"**
4. Press your hotkey anytime to trigger the macro

### 4. Managing Macros

**Rename a Macro**
1. Select the macro
2. Change the name in the "Name" field
3. Click "Save Macro"

**Delete a Macro**
1. Select the macro
2. Click "Delete Macro"
3. Confirm deletion

**Export a Macro**
1. Select the macro
2. Click "Export Macro"
3. Choose save location

**Import a Macro**
1. Click "Import Macro"
2. Select the JSON file
3. The macro will be added to your list

### 5. Adjusting Playback Speed

Use the speed slider to control playback:
- **0.1x - 0.9x**: Slower playback (useful for precise actions)
- **1.0x**: Normal speed (default)
- **1.1x - 5.0x**: Faster playback (useful for quick repetitive tasks)

## Tips

- Test macros in safe environments first
- Use descriptive names for your macros
- Save important macros with "Export Macro"
- Use simple hotkey combinations to avoid conflicts
- Adjust speed based on your needs (slower for accuracy, faster for efficiency)

## Hotkey Examples

### Basic Single Keys
- `1`, `2`, `3` - Number keys
- `a`, `b`, `c` - Letter keys
- `f1`, `f2`, `f3` - Function keys

### Modifier + Key Combinations (Recommended)
- `alt+1`, `alt+2`, `alt+3` - Alt with numbers
- `ctrl+1`, `ctrl+2`, `ctrl+3` - Ctrl with numbers
- `shift+1`, `shift+2`, `shift+3` - Shift with numbers
- `alt+a`, `alt+q`, `alt+e` - Alt with letters

### Multiple Modifiers + Key
- `ctrl+shift+1` - Combat macro 1
- `ctrl+shift+2` - Combat macro 2
- `ctrl+alt+1` - Special combo 1
- `ctrl+alt+f1` - Advanced macro

### Tips for Choosing Hotkeys
- **Recommended**: Use combinations like `alt+1`, `ctrl+shift+2` to avoid conflicts
- **Avoid**: Single keys (like just `1` or `a`) as they may conflict with normal typing
- **Best Practice**: Test your hotkeys don't conflict with game/application shortcuts

## Troubleshooting

**Problem**: Hotkeys not working
- Ensure no other application uses the same hotkey
- Try simpler combinations
- Check application has necessary permissions

**Problem**: Playback is too fast/slow
- Adjust the speed slider
- Re-record at a different pace

**Problem**: Mouse position is off
- Make sure screen resolution matches when recording/playing
- Use relative positions if possible

## Linux Users

You may need to run with sudo:
```bash
sudo python main.py
```

Or configure permissions:
```bash
sudo groupadd -f uinput
sudo usermod -a -G uinput $USER
```

Then logout and login again.
