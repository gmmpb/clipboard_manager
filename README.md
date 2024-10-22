# Clipboard Manager
A Python-based clipboard manager with a graphical user interface (GUI) built using Tkinter. This tool allows you to keep track of your clipboard history, including both text and images, and easily access previous clipboard entries.

**Note: This clipboard manager is primarily intended for Ubuntu.**

## Features

- **Clipboard History**: Keeps a history of the last 25 clipboard entries.
- **Text and Image Support**: Supports both text and image clipboard entries.
- **Global Hotkey**: Show the clipboard history UI using the global hotkey `Alt+Y`.
- **Scroll Support**: Scroll through the clipboard history using the mouse wheel.
- **Transparency**: The UI window is semi-transparent for a sleek look.
- **Logging**: Logs events and errors to `/var/log/clipboard_manager.log`.

## Requirements

- Python 3.x
- Tkinter
- PyAutoGUI
- Pillow
- Pynput
- xclip (Linux)

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/gmmpb/clipboard_manager.git
    cd clipboard_manager
    ```

2. **Install the required Python packages**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Ensure `xclip` and `tkinter` are installed** (Linux):
    ```sh
    sudo apt-get install xclip python3-tk
    ```

## Usage

Run the script to start the clipboard manager:
```sh
python 