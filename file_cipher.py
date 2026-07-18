#!/usr/bin/env python3
"""
File Encryption and Decryption Tool
Uses Fernet (AES-128-CBC with HMAC-SHA256) with a password-derived key.
"""

import os
import argparse
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from cryptography.exceptions import InvalidSignature
import sys

# --- Constants ---
SALT_LENGTH = 16          # bytes
ITERATIONS = 100_000      # PBKDF2 iterations (increase for slower, more secure)
CHUNK_SIZE = 64 * 1024    # 64 KB per chunk


def derive_key(password: str, salt: bytes) -> bytes:
    """
    Derive a Fernet-compatible key (32 bytes, base64 encoded) from a password and salt.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,          # Fernet uses 32-byte keys
        salt=salt,
        iterations=ITERATIONS,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
    return key


def encrypt_file(input_path: str, output_path: str, password: str):
    """
    Encrypt a file using the given password.
    The encrypted file will contain: [salt (16B)] + [Fernet ciphertext].
    """
    # Generate a random salt
    salt = os.urandom(SALT_LENGTH)
    key = derive_key(password, salt)
    fernet = Fernet(key)

    # Read entire input file (works for moderate-sized files)
    # For large files, we could stream, but Fernet requires the whole data in memory.
    # However, we can process in chunks by encrypting chunk by chunk with the same Fernet object? Fernet's encrypt expects bytes.
    # Alternative: use AES in CBC mode with HMAC for streaming, but Fernet is simpler.
    # We'll read the whole file; if you need streaming, see notes below.
    try:
        with open(input_path, 'rb') as f_in:
            plaintext = f_in.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_path}' not found.", file=sys.stderr)
        sys.exit(1)

    # Encrypt the data
    ciphertext = fernet.encrypt(plaintext)

    # Write salt + ciphertext to output
    with open(output_path, 'wb') as f_out:
        f_out.write(salt)
        f_out.write(ciphertext)

    print(f"Encrypted '{input_path}' -> '{output_path}'")


def decrypt_file(input_path: str, output_path: str, password: str):
    """
    Decrypt a file encrypted with encrypt_file().
    Expects: [salt (16B)] + [Fernet ciphertext].
    """
    try:
        with open(input_path, 'rb') as f_in:
            salt = f_in.read(SALT_LENGTH)
            ciphertext = f_in.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_path}' not found.", file=sys.stderr)
        sys.exit(1)

    # Check salt length
    if len(salt) != SALT_LENGTH:
        print("Error: Invalid file format (bad salt).", file=sys.stderr)
        sys.exit(1)

    # Derive key from password and salt
    key = derive_key(password, salt)
    fernet = Fernet(key)

    # Decrypt
    try:
        plaintext = fernet.decrypt(ciphertext)
    except InvalidSignature:
        print("Error: Wrong password or corrupted file.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error during decryption: {e}", file=sys.stderr)
        sys.exit(1)

    # Write decrypted data
    with open(output_path, 'wb') as f_out:
        f_out.write(plaintext)

    print(f"Decrypted '{input_path}' -> '{output_path}'")


def main():
    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt a file with a password.",
        epilog="Example: python file_cipher.py encrypt secret.txt secret.enc -p mypassword"
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Encrypt subcommand
    parser_enc = subparsers.add_parser('encrypt', help='Encrypt a file')
    parser_enc.add_argument('input', help='Path to the input file')
    parser_enc.add_argument('output', help='Path to the output encrypted file')
    parser_enc.add_argument('-p', '--password', help='Encryption password (if omitted, prompt will ask)')
    parser_enc.add_argument('--overwrite', action='store_true', help='Overwrite output file if it exists')

    # Decrypt subcommand
    parser_dec = subparsers.add_parser('decrypt', help='Decrypt a file')
    parser_dec.add_argument('input', help='Path to the encrypted file')
    parser_dec.add_argument('output', help='Path to the decrypted output file')
    parser_dec.add_argument('-p', '--password', help='Decryption password (if omitted, prompt will ask)')
    parser_dec.add_argument('--overwrite', action='store_true', help='Overwrite output file if it exists')

    args = parser.parse_args()

    # Check if output file exists and handle overwrite
    if os.path.exists(args.output) and not args.overwrite:
        print(f"Error: Output file '{args.output}' already exists. Use --overwrite to replace.", file=sys.stderr)
        sys.exit(1)

    # Get password (from command line or prompt)
    password = args.password
    if password is None:
        import getpass
        password = getpass.getpass("Enter password: ")

    if args.command == 'encrypt':
        encrypt_file(args.input, args.output, password)
    elif args.command == 'decrypt':
        decrypt_file(args.input, args.output, password)


if __name__ == '__main__':
    main()
