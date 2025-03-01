import base64
from cryptography.fernet import Fernet

print("\033[32m" + r"""
██████ ███████████████    ██████████████████████ ██████  
██   ████    ██      ██  ██ ██   ██  ██  ██    ████   ██ 
██   ███████ ██       ████  ██████   ██  ██    ████████  
██   ████    ██        ██   ██       ██  ██    ████   ██ 
██████ █████████████   ██   ██       ██   ██████ ██   ██ 
                                           @uki
GitHub: https://github.com/ukihunter
   """ + "\033[0m")

Vkey = input("Enter the valid Key: ").strip()  # Remove whitespace
name = input("Choose the file name (must be in the same path): ")

try:
    cipher = Fernet(Vkey.encode())  # Pass the key directly as bytes

    def decrypt_file(filename, cipher):
        try:
            with open(filename, "rb") as file:
                encrypted_data = file.read()

            decrypted_data = cipher.decrypt(encrypted_data)

            original_filename = filename.replace(".encrypted", "")
            with open(original_filename, "wb") as file:
                file.write(decrypted_data)

            print(f"File '{original_filename}' decrypted successfully!")
        except Exception as e:
            print(f"Error: {e}")

    decrypt_file(name, cipher)

except Exception as e:
    print(f"Invalid key: {e}")