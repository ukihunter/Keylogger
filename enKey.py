import uuid
import base64

print("""
 _                                      
| | __  ___  _   _    __ _   ___  _ __  
| |/ / / _ \\| | | |  / _` | / _ \\| '_ \\ 
|   < |  __/| |_| | | (_| ||  __/| | | |
|_|\\_\\ \\___| \\__, |  \\__, | \\___||_| |_|
             |___/   |___/              
                                           @uki
GitHub: https://github.com/ukihunter
      """)


def generate_machine_key():
    """Generate a Fernet-compatible key using MAC address."""
    mac_address = uuid.getnode()
    mac_str = str(mac_address).encode()
    padded = mac_str.ljust(32, b' ')  # Pad to 32 bytes with spaces
    return base64.urlsafe_b64encode(padded)


key = generate_machine_key()
print(f"Machine-Specific Key: {key.decode()}")

# Save the key
with open("key.txt", "w") as file:
    file.write(f"Machine-Specific Key: {key.decode()}")