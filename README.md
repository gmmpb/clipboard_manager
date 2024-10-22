# Clipboard Manager
A Python-based clipboard manager with a graphical user interface (GUI) built using Tkinter. This tool allows you to keep track of your clipboard history, including both text and images, and easily access previous clipboard entries.

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
python clipboard_manager.py
```

## How to Use

- **Show UI**: Press `Alt+Y` to show the clipboard history UI near the cursor position.
- **Scroll**: Use the mouse wheel to scroll through the clipboard history.
- **Select Entry**: Double-click on an entry to move it to the top and set it as the current clipboard content.

## Building with PyInstaller

To build the clipboard manager into a standalone executable using PyInstaller, run the following command:
```sh
pyinstaller --onefile --windowed --hidden-import=PIL --hidden-import=PIL.Image --hidden-import=PIL.ImageTk --hidden-import=tkinter --hidden-import=PIL._tkinter_finder clipboard_manager.py
```

Move the executable to the desired location:
```sh
mv dist/clipboard_manager /usr/local/bin/clipboard_manager
```

This will generate a single executable file in the `dist` directory.

## Running on Boot (Linux)

To run the clipboard manager on boot, you can create a systemd service:

1. **Create a service file**:
    ```sh
    sudo nano /etc/systemd/system/clipboard_manager.service
    ```

2. **Add the following content**:
    ```ini
    [Unit]
    Description=Clipboard Manager Service
    After=network.target

    [Service]
    ExecStart=/usr/local/bin/clipboard_manager
    WorkingDirectory=/usr/local/bin
    StandardOutput=inherit
    StandardError=inherit
    Restart=always
    User=m<yourusername>
    Environment="DISPLAY=:0" "XAUTHORITY=/home/<yourusername>/.Xauthority"

    [Install]
    WantedBy=multi-user.target
    ```

3. **Enable and start the service**:
    ```sh
    sudo systemctl enable clipboard_manager.service
    sudo systemctl start clipboard_manager.service
    ```

## Known Issues

- **Shortcut Issue**: The global hotkey `Alt+Y` does not work when the desktop is the active window.

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