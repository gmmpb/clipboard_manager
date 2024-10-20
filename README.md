# Clipboard Manager

A Python-based clipboard manager with a graphical user interface (GUI) built using Tkinter. This tool allows you to keep track of your clipboard history, including both text and images, and easily access previous clipboard entries.

## Features

- **Clipboard History**: Keeps a history of the last 25 clipboard entries.
- **Text and Image Support**: Supports both text and image clipboard entries.
- **Global Hotkey**: Show the clipboard history UI using the global hotkey `Ctrl+Y`.
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
    git clone https://github.com/yourusername/clipboard_manager.git
    cd clipboard_manager
    ```

2. **Install the required Python packages**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Ensure `xclip` is installed** (Linux):
    ```sh
    sudo apt-get install xclip
    ```

## Usage

Run the script to start the clipboard manager:
```sh
python clipboard_manager.py
```

## How to Use

- **Show UI**: Press `Ctrl+Y` to show the clipboard history UI near the cursor position.
- **Scroll**: Use the mouse wheel to scroll through the clipboard history.
- **Select Entry**: Double-click on an entry to move it to the top and set it as the current clipboard content.

## Logging

Logs are stored in `/var/log/clipboard_manager.log`. Ensure you have the necessary permissions to write to this file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Acknowledgements

- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [PyAutoGUI](https://pyautogui.readthedocs.io/)
- [Pillow](https://python-pillow.org/)
- [Pynput](https://pynput.readthedocs.io/)
