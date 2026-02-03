# Game Macro Recorder

A powerful and easy-to-use macro recorder for any game or application. Record mouse movements, clicks, keyboard inputs, and play them back with customizable hotkeys.

## Features

- 🎮 **Universal Compatibility**: Works with any game or application
- 🖱️ **Mouse & Keyboard Recording**: Captures all mouse movements, clicks, and keyboard inputs
- ⚡ **Hotkey Support**: Trigger macros instantly with custom keyboard shortcuts
- 🎯 **Adjustable Playback Speed**: Control playback speed from 0.1x to 5.0x
- 💾 **Save & Load**: Save macros to files and share them
- 🖼️ **Graphical Interface**: Easy-to-use GUI for configuration and control
- 📝 **Multiple Macros**: Create and manage multiple macros with different hotkeys

## Installation

### Requirements

- Python 3.6 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Starting the Application

Run the main application:

```bash
python main.py
```

Or run the GUI directly:

```bash
python macro_gui.py
```

### Recording a Macro

1. Click "Start Recording" button
2. Perform your mouse and keyboard actions
3. Click "Stop Recording" when done
4. Enter a name for your macro
5. (Optional) Set a hotkey to trigger the macro
6. Click "Save Macro"

### Playing a Macro

**Method 1: Using the GUI**
1. Select a macro from the list
2. Click "Play Macro" button

**Method 2: Using Hotkey**
1. Assign a hotkey to your macro (e.g., "ctrl+shift+1")
2. Press the hotkey anywhere to trigger the macro

### Managing Macros

- **Rename**: Select a macro, change the name, and click "Save Macro"
- **Delete**: Select a macro and click "Delete Macro"
- **Export**: Save a macro to a JSON file for sharing
- **Import**: Load a macro from a JSON file
- **Adjust Speed**: Use the speed slider to control playback speed

### Hotkey Format

Use combinations like:
- `ctrl+shift+1`
- `alt+a`
- `ctrl+alt+p`
- `f1`, `f2`, etc.

## Configuration

Macros are automatically saved to `macros_config.json` in the application directory. This file contains all your macros and their settings.

## Safety Notes

⚠️ **Important**: 
- Use macros responsibly and in accordance with game/application terms of service
- Some games may have anti-cheat systems that detect automated inputs
- Always test macros in a safe environment first
- The application requires proper permissions to monitor and simulate input

## Troubleshooting

### Linux Users

You may need to run with sudo for keyboard monitoring:
```bash
sudo python main.py
```

Or configure uinput permissions:
```bash
sudo groupadd -f uinput
sudo usermod -a -G uinput $USER
```

### Hotkeys Not Working

- Ensure no other application is using the same hotkey
- Try simpler hotkey combinations
- Check that the application has necessary permissions

## Technical Details

### Project Structure

```
game_macro/
├── main.py              # Main entry point
├── macro_gui.py         # GUI implementation
├── macro_recorder.py    # Core recording/playback logic
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Dependencies

- **pynput**: For capturing and simulating mouse/keyboard events
- **keyboard**: For global hotkey support
- **tkinter**: For the graphical interface (included with Python)

## License

This project is open source. Use it responsibly and at your own risk.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Disclaimer

This tool is for educational and productivity purposes. Users are responsible for ensuring their use complies with applicable terms of service and laws.
