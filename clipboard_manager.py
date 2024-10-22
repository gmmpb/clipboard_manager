import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import time
import pyautogui
from PIL import Image, ImageTk, UnidentifiedImageError
import io
from pynput import keyboard  # Using pynput for key detection
import logging

# Configure logging
logging.basicConfig(filename='/var/log/clipboard_manager.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class ClipboardManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Clipboard History")
        self.history = []
        self.history_limit = 25
        self.root.configure(bg='#1e1e1e')

        self.root.geometry("350x450")  # Adjusted window size for a more professional look
        self.root.resizable(False, False)  # Disable resizing
        self.root.wait_visibility(self.root)
        self.root.wm_attributes('-alpha', 0.8)  # Set window transparency
        self.root.overrideredirect(True)  # Remove window decorations

        # Create a main frame for content
        self.main_frame = tk.Frame(root, bg='#1e1e1e')
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create a custom close button
        close_button = tk.Button(self.main_frame, text="X", command=self.on_close, fg="#ffffff", bg="#ff5f5f", 
                                 font=("Segoe UI", 10, "bold"), relief="flat", bd=0, padx=5, pady=2)
        close_button.pack(anchor="ne", pady=5)

        # Create a canvas for clipboard items
        self.canvas = tk.Canvas(self.main_frame, bg='#1e1e1e', bd=0, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Enable scrolling with the mouse wheel
        self.canvas.bind_all("<Button-4>", self.on_mouse_scroll)  # Linux scroll up
        self.canvas.bind_all("<Button-5>", self.on_mouse_scroll)  # Linux scroll down
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_scroll)  # Windows and MacOS

        # Create an inner frame to hold the items
        self.inner_frame = tk.Frame(self.canvas, bg='#1e1e1e')
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Bind the scrollregion to the inner frame size
        self.inner_frame.bind("<Configure>", self.on_frame_configure)

        # Store image references
        self.rendered_images = []

        self.monitoring = True
        self.last_clipboard_text = ""
        self.last_clipboard_image = b""
        self.updating_clipboard = False  # Flag to prevent self-triggering

        # Start clipboard monitoring in a background thread
        self.monitor_thread = threading.Thread(target=self.monitor_clipboard)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

        # Hide the window initially
        self.root.withdraw()

        # Start listening for hotkeys using pynput
        self.start_hotkey_listener()

    def start_hotkey_listener(self):
        """Start a listener for the Alt+Y hotkey using pynput."""
        listener_thread = threading.Thread(target=self.listen_for_hotkey)
        listener_thread.daemon = True
        listener_thread.start()

    def listen_for_hotkey(self):
        """Listen for the Alt+Y hotkey and display the UI when pressed."""
        def on_press(key):
            try:
                if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                    self.alt_pressed = True
                elif key.char == 'y' and self.alt_pressed:
                    self.show_ui()
            except AttributeError:
                pass

        def on_release(key):
            if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                self.alt_pressed = False

        self.alt_pressed = False
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    def show_ui(self):
        """Show the UI near the cursor position."""
        x, y = pyautogui.position()
        self.root.geometry(f"+{x}+{y}")
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.root.wm_attributes("-topmost", True)
        logging.info("UI shown at position (%d, %d)", x, y)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_scroll(self, event):
        """Handle mouse scroll event for scrolling through the canvas."""
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

    def monitor_clipboard(self):
        """Monitor the clipboard for changes and update the history."""
        while self.monitoring:
            try:
                if self.updating_clipboard:
                    time.sleep(0.1)  # Short delay to ensure clipboard is updated
                    self.updating_clipboard = False
                    continue

                current_clipboard_text = self.get_clipboard_text()
                current_clipboard_image = self.get_clipboard_image()

                if current_clipboard_text and current_clipboard_text != self.last_clipboard_text:
                    self.add_to_history(current_clipboard_text, "text")
                    self.last_clipboard_text = current_clipboard_text
                    self.last_clipboard_image = b""  # Reset image since text is now in clipboard
                elif current_clipboard_image and current_clipboard_image != self.last_clipboard_image:
                    self.add_to_history(current_clipboard_image, "image")
                    self.last_clipboard_image = current_clipboard_image
                    self.last_clipboard_text = ""  # Reset text since image is now in clipboard

            except Exception as e:
                logging.error(f"Error accessing clipboard: {e}")

            time.sleep(0.5)  # Check clipboard every 0.5 seconds

    def get_clipboard_text(self):
        """Get clipboard text content using xclip."""
        try:
            result = subprocess.run(['xclip', '-selection', 'clipboard', '-o', '-t', 'text/plain'],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            content = result.stdout.strip()
            return content if content else None
        except subprocess.CalledProcessError as e:
            logging.error(f"Error getting clipboard text: {e}")
            return None

    def get_clipboard_image(self):
        """Get clipboard image content using xclip and validate it."""
        image_formats = ['image/png', 'image/jpeg', 'image/bmp', 'image/gif']
        for fmt in image_formats:
            try:
                result = subprocess.run(['xclip', '-selection', 'clipboard', '-o', '-t', fmt],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                if result.stdout:
                    # Validate if the data is a valid image
                    try:
                        image = Image.open(io.BytesIO(result.stdout))
                        image.verify()  # Verify the image is valid
                        logging.debug(f"Image format {fmt} is valid.")
                        return result.stdout
                    except (UnidentifiedImageError, Image.DecompressionBombError, OSError) as e:
                        logging.error(f"Image format {fmt} is not valid: {e}")
                        continue  # Try the next format
            except subprocess.CalledProcessError as e:
                logging.error(f"Error accessing clipboard image with format {fmt}: {e}")
                continue
        return None

    def add_to_history(self, item, content_type):
        """Add new item to clipboard history without duplication."""
        if not any(content_type == item_type and item == existing_item for item_type, existing_item in self.history):
            self.history.insert(0, (content_type, item))
            if len(self.history) > self.history_limit:
                self.history.pop()  # Ensure we don't exceed the history limit
            self.update_canvas()

    def update_canvas(self):
        """Update the canvas with the clipboard history."""
        # Clear previous items
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        self.rendered_images.clear()

        # Recreate items
        for index, (item_type, item) in enumerate(self.history):
            # Create a frame for each item with fixed size
            item_frame = tk.Frame(self.inner_frame, bg='#1e1e1e', bd=0, relief="solid", width=320, height=100)
            item_frame.pack_propagate(False)  # Prevent frame from resizing to fit content
            item_frame.pack(fill="x", padx=5, pady=5)

            # Bind double-click event
            item_frame.bind("<Double-Button-1>", lambda e, idx=index: self.on_item_double_click(idx))

            if item_type == "text":
                truncated_text = self.truncate_text(item, 40)
                label = tk.Label(item_frame, text=truncated_text, fg="#ffffff", bg=item_frame['bg'],
                                 font=("Segoe UI", 12, "normal"), anchor="center", justify="center")
                label.pack(fill="both", expand=True, padx=10, pady=8)
                label.bind("<Double-Button-1>", lambda e, idx=index: self.on_item_double_click(idx))
            elif item_type == "image":
                try:
                    img = self.display_image_in_list(item)
                    self.rendered_images.append(img)  # Keep reference to prevent garbage collection
                    label = tk.Label(item_frame, image=img, bg='#1e1e1e')  # Set solid background color
                    label.pack(fill="both", expand=True, padx=10, pady=8)
                    label.bind("<Double-Button-1>", lambda e, idx=index: self.on_item_double_click(idx))
                except Exception as e:
                    logging.error(f"Unable to display image: {e}")
                    # Show a placeholder or skip displaying the image
                    error_label = tk.Label(item_frame, text="[Image cannot be displayed]", fg="#ffffff", bg=item_frame['bg'],
                                           font=("Segoe UI", 12, "italic"), anchor="center", justify="center")
                    error_label.pack(fill="both", expand=True, padx=10, pady=8)
                    error_label.bind("<Double-Button-1>", lambda e, idx=index: self.on_item_double_click(idx))

            # Add a divider (horizontal line) between items
            if index < len(self.history) - 1:
                divider = tk.Frame(self.inner_frame, height=1, bg='#3a3a3c')
                divider.pack(fill="x", padx=5, pady=5)

    def truncate_text(self, text, max_length):
        """Truncate text to fit within a specified length."""
        return text[:max_length] + "..." if len(text) > max_length else text

    def display_image_in_list(self, image_bytes):
        """Convert image to a thumbnail and display it."""
        try:
            image = Image.open(io.BytesIO(image_bytes))
            image.thumbnail((80, 80))  # Resize for thumbnail
            return ImageTk.PhotoImage(image)
        except Exception as e:
            logging.error(f"Error: Image format not supported. {e}")
            raise

    def on_item_double_click(self, index):
        """Handle double-click event: Move item to top and add to clipboard."""
        item_type, item = self.history.pop(index)
        self.history.insert(0, (item_type, item))
        self.update_canvas()

        # Set the item in the clipboard
        if item_type == "text":
            self.set_clipboard_content(item)
        elif item_type == "image":
            self.set_clipboard_image(item)

    def set_clipboard_content(self, text):
        """Set clipboard text content using xclip."""
        try:
            self.updating_clipboard = True
            subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode('utf-8'), check=True)
            self.last_clipboard_text = text  # Update last clipboard text
            self.last_clipboard_image = b""  # Clear last image
        except subprocess.CalledProcessError as e:
            logging.error(f"Error setting clipboard content: {e}")
        finally:
            self.updating_clipboard = False

    def set_clipboard_image(self, image_bytes):
        """Set clipboard image content using xclip."""
        try:
            self.updating_clipboard = True
            # Save image bytes as PNG format to ensure compatibility
            image = Image.open(io.BytesIO(image_bytes))
            output = io.BytesIO()
            image.save(output, format='PNG')
            png_data = output.getvalue()
            subprocess.run(['xclip', '-selection', 'clipboard', '-t', 'image/png'], input=png_data, check=True)
            self.last_clipboard_image = png_data  # Update last clipboard image
            self.last_clipboard_text = ""  # Clear last text
        except subprocess.CalledProcessError as e:
            logging.error(f"Error setting clipboard image: {e}")
        finally:
            self.updating_clipboard = False

    def on_close(self):
        """Handle app closure."""
        self.root.withdraw()  # Hide the window instead of destroying it

# Main function to run the clipboard history app
def main():
    root = tk.Tk()
    clipboard_manager = ClipboardManager(root)
    root.protocol("WM_DELETE_WINDOW", clipboard_manager.on_close)
    root.mainloop()

if __name__ == "__main__":
    main()