#!/usr/bin/env python3
"""
Secure Password Generator
Generate strong, customizable passwords with entropy estimation.
"""

import random
import string
import argparse
import sys

# --- Default character sets ---
LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
# Common special characters (avoid ambiguous ones by default)
SPECIAL = "!@#$%^&*()_+-=[]{}|;:,.<>?"
# Ambiguous characters to exclude when requested
AMBIGUOUS = "lI1O0"

def generate_password(length=16, use_upper=True, use_lower=True, use_digits=True,
                      use_special=True, exclude_ambiguous=False):
    """
    Generate a random password.

    :param length:           Length of the password.
    :param use_upper:        Include uppercase letters.
    :param use_lower:        Include lowercase letters.
    :param use_digits:       Include digits.
    :param use_special:      Include special characters.
    :param exclude_ambiguous: Exclude ambiguous characters (l, I, 1, O, 0).
    :return:                 A random password string.
    """
    # Build the character pool
    pool = ""
    if use_lower:
        pool += LOWERCASE
    if use_upper:
        pool += UPPERCASE
    if use_digits:
        pool += DIGITS
    if use_special:
        pool += SPECIAL

    if not pool:
        raise ValueError("At least one character set must be selected.")

    # Remove ambiguous characters if requested
    if exclude_ambiguous:
        pool = ''.join(c for c in pool if c not in AMBIGUOUS)

    # Ensure the password contains at least one character from each selected set
    # (to guarantee minimum diversity)
    required_chars = []
    if use_lower and exclude_ambiguous:
        # Remove ambiguous from lower as well
        lower_clean = ''.join(c for c in LOWERCASE if c not in AMBIGUOUS)
        if lower_clean:
            required_chars.append(random.choice(lower_clean))
    elif use_lower:
        required_chars.append(random.choice(LOWERCASE))

    if use_upper and exclude_ambiguous:
        upper_clean = ''.join(c for c in UPPERCASE if c not in AMBIGUOUS)
        if upper_clean:
            required_chars.append(random.choice(upper_clean))
    elif use_upper:
        required_chars.append(random.choice(UPPERCASE))

    if use_digits and exclude_ambiguous:
        digits_clean = ''.join(c for c in DIGITS if c not in AMBIGUOUS)
        if digits_clean:
            required_chars.append(random.choice(digits_clean))
    elif use_digits:
        required_chars.append(random.choice(DIGITS))

    if use_special:
        # Special chars don't have ambiguous equivalents in our set, but we'll still check
        special_clean = ''.join(c for c in SPECIAL if c not in AMBIGUOUS) if exclude_ambiguous else SPECIAL
        if special_clean:
            required_chars.append(random.choice(special_clean))
        else:
            # If special set becomes empty, just skip
            pass

    # Now fill the remaining length with random choices from the pool
    remaining = length - len(required_chars)
    if remaining < 0:
        raise ValueError(f"Length {length} is too short to satisfy all character requirements.")

    # Generate remaining characters
    filler = [random.choice(pool) for _ in range(remaining)]

    # Combine required and filler, then shuffle to avoid predictable order
    password_list = required_chars + filler
    random.shuffle(password_list)

    return ''.join(password_list)


def estimate_entropy(pool_size, length):
    """
    Estimate the entropy of a password in bits.
    Entropy = log2(pool_size ^ length) = length * log2(pool_size)
    """
    import math
    if pool_size <= 0:
        return 0
    return length * math.log2(pool_size)


def main():
    parser = argparse.ArgumentParser(
        description="Generate strong, customizable passwords.",
        epilog="Example: python password_generator.py -l 20 -u -d -s -e"
    )
    parser.add_argument("-l", "--length", type=int, default=16,
                        help="Password length (default: 16)")
    parser.add_argument("-u", "--no-upper", action="store_true",
                        help="Exclude uppercase letters (default: include)")
    parser.add_argument("-L", "--no-lower", action="store_true",
                        help="Exclude lowercase letters (default: include)")
    parser.add_argument("-d", "--no-digits", action="store_true",
                        help="Exclude digits (default: include)")
    parser.add_argument("-s", "--no-special", action="store_true",
                        help="Exclude special characters (default: include)")
    parser.add_argument("-e", "--exclude-ambiguous", action="store_true",
                        help="Exclude ambiguous characters (l, I, 1, O, 0)")
    parser.add_argument("-n", "--count", type=int, default=1,
                        help="Number of passwords to generate (default: 1)")
    parser.add_argument("--entropy", action="store_true",
                        help="Show entropy estimation in bits")
    args = parser.parse_args()

    # Determine which sets to include
    use_upper = not args.no_upper
    use_lower = not args.no_lower
    use_digits = not args.no_digits
    use_special = not args.no_special

    # Build the pool for entropy estimation (same logic as generation)
    pool = ""
    if use_lower:
        pool += LOWERCASE
    if use_upper:
        pool += UPPERCASE
    if use_digits:
        pool += DIGITS
    if use_special:
        pool += SPECIAL
    if args.exclude_ambiguous:
        pool = ''.join(c for c in pool if c not in AMBIGUOUS)

    if not pool:
        print("Error: At least one character set must be selected.", file=sys.stderr)
        sys.exit(1)

    # Generate passwords
    passwords = []
    try:
        for _ in range(args.count):
            pwd = generate_password(
                length=args.length,
                use_upper=use_upper,
                use_lower=use_lower,
                use_digits=use_digits,
                use_special=use_special,
                exclude_ambiguous=args.exclude_ambiguous
            )
            passwords.append(pwd)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Output
    for i, pwd in enumerate(passwords, 1):
        if args.count > 1:
            print(f"{i}: {pwd}")
        else:
            print(pwd)

    # Entropy information
    if args.entropy:
        pool_size = len(pool)
        bits = estimate_entropy(pool_size, args.length)
        print(f"\nEntropy: {bits:.1f} bits (pool size {pool_size})", file=sys.stderr)

if __name__ == "__main__":
    main()
