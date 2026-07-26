#!/usr/bin/env python3
"""
Brute‑Force Attack Simulator – Educational tool to demonstrate password cracking.
Supports dictionary and brute‑force attacks with configurable hash algorithms.
"""

import itertools
import hashlib
import time
import sys
import argparse
from typing import Optional

# --- Default character sets ---
LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
SYMBOLS = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"

DEFAULT_CHARSET = LOWERCASE + DIGITS  # for brute‑force

# --- Hash helper ---
def hash_password(password: str, algorithm: str = "plain") -> str:
    """Hash a password using the specified algorithm (or return plaintext)."""
    if algorithm == "plain":
        return password
    try:
        hasher = hashlib.new(algorithm)
        hasher.update(password.encode('utf-8'))
        return hasher.hexdigest()
    except ValueError:
        print(f"Unsupported hash algorithm: {algorithm}. Falling back to plain.")
        return password

# --- Dictionary attack ---
def dictionary_attack(target_hash: str, wordlist_path: str, algorithm: str = "plain") -> Optional[str]:
    """Try each word in a wordlist against the target hash."""
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            words = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Wordlist file '{wordlist_path}' not found.")
        return None

    print(f"[*] Dictionary attack with {len(words)} words, algorithm: {algorithm}")
    start = time.time()
    attempts = 0
    for word in words:
        attempts += 1
        hashed = hash_password(word, algorithm)
        if hashed == target_hash:
            elapsed = time.time() - start
            print(f"[+] Found! Password: '{word}' (attempts: {attempts}, time: {elapsed:.2f}s)")
            return word
        # Optional: show progress every 1000 attempts
        if attempts % 1000 == 0:
            print(f"    Attempts: {attempts} ...")
    elapsed = time.time() - start
    print(f"[-] Password not found in dictionary. Attempts: {attempts}, time: {elapsed:.2f}s")
    return None

# --- Brute‑force attack ---
def brute_force_attack(target_hash: str, max_length: int, charset: str = DEFAULT_CHARSET,
                       algorithm: str = "plain") -> Optional[str]:
    """Try all combinations of characters up to max_length."""
    print(f"[*] Brute‑force attack (max length {max_length}, charset size {len(charset)}, algorithm: {algorithm})")
    start = time.time()
    attempts = 0

    for length in range(1, max_length + 1):
        for guess_tuple in itertools.product(charset, repeat=length):
            guess = ''.join(guess_tuple)
            attempts += 1
            hashed = hash_password(guess, algorithm)
            if hashed == target_hash:
                elapsed = time.time() - start
                print(f"[+] Found! Password: '{guess}' (length: {length}, attempts: {attempts}, time: {elapsed:.2f}s)")
                return guess
            # Show progress periodically
            if attempts % 10000 == 0:
                print(f"    Length {length}, attempts: {attempts} ...")

    elapsed = time.time() - start
    print(f"[-] Password not found within length {max_length}. Attempts: {attempts}, time: {elapsed:.2f}s")
    return None

# --- Main CLI ---
def main():
    parser = argparse.ArgumentParser(
        description="Simulate brute‑force password cracking (educational).",
        epilog="Example: python bruteforce_sim.py -t 5d41402abc4b2a76b9719d911017c592 -a md5 -m dict -w wordlist.txt"
    )
    parser.add_argument("-t", "--target", required=True,
                        help="Target hash (or plaintext if --algorithm=plain)")
    parser.add_argument("-a", "--algorithm", default="plain",
                        help="Hash algorithm: plain, md5, sha1, sha256, etc. (default: plain)")
    parser.add_argument("-m", "--mode", choices=["dict", "brute"], required=True,
                        help="Attack mode: dict (dictionary) or brute")
    parser.add_argument("-w", "--wordlist", help="Path to wordlist file (for dict mode)")
    parser.add_argument("-l", "--max-length", type=int, default=4,
                        help="Maximum password length for brute‑force (default: 4)")
    parser.add_argument("-c", "--charset", default=DEFAULT_CHARSET,
                        help="Character set for brute‑force (default: lowercase + digits)")

    args = parser.parse_args()

    # Validate arguments based on mode
    if args.mode == "dict" and not args.wordlist:
        print("Error: Dictionary mode requires a wordlist file (--wordlist).")
        sys.exit(1)
    if args.mode == "brute" and args.max_length < 1:
        print("Error: Maximum length must be at least 1.")
        sys.exit(1)

    # Optional: print warning
    print("⚠️  This tool is for educational/authorised testing only.")
    print("    Unauthorised use against systems you don't own is illegal.\n")

    if args.mode == "dict":
        dictionary_attack(args.target, args.wordlist, args.algorithm)
    else:  # brute
        brute_force_attack(args.target, args.max_length, args.charset, args.algorithm)

if __name__ == "__main__":
    main()
