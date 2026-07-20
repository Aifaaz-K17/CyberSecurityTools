#!/usr/bin/env python3
"""
Secure Password Manager – store and retrieve passwords in an encrypted vault.
"""

import os
import json
import base64
import sys
import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidSignature
import bcrypt

# --- Constants ---
VAULT_FILE = "vault.json"
SALT_FILE = "salt.bin"
ITERATIONS = 100_000
KEY_LENGTH = 32  # Fernet uses 32-byte keys

# --- Helper functions ---

def load_salt():
    """Load the salt from file, or create a new one if not exists."""
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, 'rb') as f:
            return f.read()
    else:
        salt = os.urandom(16)
        with open(SALT_FILE, 'wb') as f:
            f.write(salt)
        return salt

def derive_key(master_password: str, salt: bytes) -> bytes:
    """Derive a Fernet-compatible base64 key from master password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=ITERATIONS,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode('utf-8')))
    return key

def load_vault(key):
    """Load and decrypt the vault. Returns dict or None if decryption fails."""
    if not os.path.exists(VAULT_FILE):
        return {"entries": []}
    with open(VAULT_FILE, 'rb') as f:
        encrypted_data = f.read()
    fernet = Fernet(key)
    try:
        decrypted = fernet.decrypt(encrypted_data)
        return json.loads(decrypted.decode('utf-8'))
    except (InvalidSignature, Exception):
        return None  # wrong password or corrupted

def save_vault(vault_data, key):
    """Encrypt and save the vault."""
    fernet = Fernet(key)
    json_str = json.dumps(vault_data, indent=2)
    encrypted = fernet.encrypt(json_str.encode('utf-8'))
    with open(VAULT_FILE, 'wb') as f:
        f.write(encrypted)

def initialize_master_password():
    """Set up the master password hash (only on first run)."""
    if os.path.exists(SALT_FILE) and os.path.exists(VAULT_FILE):
        # Already initialized? We'll just assume.
        return
    print("First time setup – create a master password.")
    pwd1 = getpass.getpass("Enter master password: ")
    pwd2 = getpass.getpass("Confirm master password: ")
    if pwd1 != pwd2:
        print("Passwords do not match. Exiting.")
        sys.exit(1)
    # Hash the master password using bcrypt for verification
    hashed = bcrypt.hashpw(pwd1.encode('utf-8'), bcrypt.gensalt())
    # Store hash in a file (or you could store it elsewhere)
    with open("master.hash", 'wb') as f:
        f.write(hashed)
    # Create empty vault
    salt = os.urandom(16)
    with open(SALT_FILE, 'wb') as f:
        f.write(salt)
    key = derive_key(pwd1, salt)
    save_vault({"entries": []}, key)
    print("Vault initialized.")

def verify_master_password(master_password):
    """Verify the master password against stored hash."""
    if not os.path.exists("master.hash"):
        print("No master password set. Run with 'init' to create one.")
        sys.exit(1)
    with open("master.hash", 'rb') as f:
        stored_hash = f.read()
    return bcrypt.checkpw(master_password.encode('utf-8'), stored_hash)

def get_vault_and_key():
    """Prompt for master password, verify, and return (vault_data, key)."""
    password = getpass.getpass("Enter master password: ")
    if not verify_master_password(password):
        print("Invalid master password.")
        sys.exit(1)
    salt = load_salt()
    key = derive_key(password, salt)
    vault = load_vault(key)
    if vault is None:
        print("Decryption failed – possibly wrong password or corrupted vault.")
        sys.exit(1)
    return vault, key

# --- Commands ---

def cmd_add(args):
    vault, key = get_vault_and_key()
    service = input("Service: ").strip()
    if not service:
        print("Service cannot be empty.")
        return
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    notes = input("Notes (optional): ").strip()
    entry = {
        "service": service,
        "username": username,
        "password": password,
        "notes": notes
    }
    vault["entries"].append(entry)
    save_vault(vault, key)
    print(f"Added entry for '{service}'.")

def cmd_list(args):
    vault, _ = get_vault_and_key()
    if not vault["entries"]:
        print("No entries found.")
        return
    for i, entry in enumerate(vault["entries"], 1):
        print(f"{i}. {entry['service']} – {entry['username']}")

def cmd_get(args):
    vault, key = get_vault_and_key()
    if not args.service:
        print("Please specify a service name (e.g., get github).")
        return
    for entry in vault["entries"]:
        if entry["service"].lower() == args.service.lower():
            print(f"Service: {entry['service']}")
            print(f"Username: {entry['username']}")
            print(f"Password: {entry['password']}")
            if entry.get("notes"):
                print(f"Notes: {entry['notes']}")
            # Optionally copy to clipboard if pyperclip is available
            try:
                import pyperclip
                pyperclip.copy(entry['password'])
                print("(Password copied to clipboard)")
            except ImportError:
                pass
            return
    print(f"No entry found for '{args.service}'.")

def cmd_delete(args):
    vault, key = get_vault_and_key()
    if not args.service:
        print("Please specify a service name (e.g., delete github).")
        return
    original_len = len(vault["entries"])
    vault["entries"] = [e for e in vault["entries"] if e["service"].lower() != args.service.lower()]
    if len(vault["entries"]) == original_len:
        print(f"No entry found for '{args.service}'.")
    else:
        save_vault(vault, key)
        print(f"Deleted entry for '{args.service}'.")

def cmd_change_master(args):
    print("Changing master password.")
    # Verify current master password
    current = getpass.getpass("Current master password: ")
    if not verify_master_password(current):
        print("Invalid current password.")
        return
    new1 = getpass.getpass("New master password: ")
    new2 = getpass.getpass("Confirm new master password: ")
    if new1 != new2:
        print("Passwords do not match.")
        return

    # Re-encrypt vault with new key
    salt = load_salt()
    old_key = derive_key(current, salt)
    vault = load_vault(old_key)
    if vault is None:
        print("Could not decrypt vault with current password.")
        return

    # Update master password hash
    hashed = bcrypt.hashpw(new1.encode('utf-8'), bcrypt.gensalt())
    with open("master.hash", 'wb') as f:
        f.write(hashed)

    # New key (same salt, new password) – we keep the same salt for simplicity
    new_key = derive_key(new1, salt)
    save_vault(vault, new_key)
    print("Master password changed successfully.")

def cmd_export(args):
    vault, key = get_vault_and_key()
    # Simple export to plain JSON (dangerous – only for backup)
    if not args.file:
        print("Please specify output file (e.g., export backup.json)")
        return
    with open(args.file, 'w') as f:
        json.dump(vault, f, indent=2)
    print(f"Vault exported to {args.file} (UNENCRYPTED – handle with care)")

# --- Main CLI ---

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Secure Password Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Init command
    subparsers.add_parser("init", help="Initialize a new vault (sets master password)")

    # Add command
    subparsers.add_parser("add", help="Add a new entry")

    # List command
    subparsers.add_parser("list", help="List all services")

    # Get command
    get_parser = subparsers.add_parser("get", help="Retrieve a password for a service")
    get_parser.add_argument("service", nargs="?", help="Service name")

    # Delete command
    del_parser = subparsers.add_parser("delete", help="Delete an entry")
    del_parser.add_argument("service", nargs="?", help="Service name")

    # Change master password
    subparsers.add_parser("change-master", help="Change the master password")

    # Export (unencrypted, for backup)
    exp_parser = subparsers.add_parser("export", help="Export vault in plain JSON (UNENCRYPTED)")
    exp_parser.add_argument("file", nargs="?", help="Output file")

    args = parser.parse_args()

    if args.command == "init":
        initialize_master_password()
    elif args.command == "add":
        cmd_add(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "get":
        cmd_get(args)
    elif args.command == "delete":
        cmd_delete(args)
    elif args.command == "change-master":
        cmd_change_master(args)
    elif args.command == "export":
        cmd_export(args)
    else:
        print("Unknown command.")
        sys.exit(1)

if __name__ == "__main__":
    main()
