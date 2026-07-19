#!/usr/bin/env python3
"""
Two-Factor Authentication (TOTP) Demo
Generates a secret, displays a QR code, and verifies TOTP codes.
"""

import pyotp
import qrcode
import sys
import time
from io import BytesIO

# Optional: try to use terminal image display (for iTerm, etc.)
try:
    from PIL import Image
    import os
    if os.name == 'posix':
        # For iTerm2 or other terminals that support inline images
        import subprocess
        def display_qr_terminal(img):
            # Use img2txt or just print using ASCII art (simpler)
            # We'll fall back to ASCII QR if possible
            pass
except ImportError:
    pass

def generate_qr_ascii(provisioning_uri):
    """Generate a QR code and print it as ASCII art in the terminal."""
    qr = qrcode.QRCode(box_size=2, border=1)
    qr.add_data(provisioning_uri)
    qr.make(fit=True)
    # Print ASCII art
    print(qr.print_ascii())
    # Also save as PNG
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("2fa_qr.png")
    print("QR code also saved as '2fa_qr.png' for scanning.")


def main():
    print("=== TOTP 2FA Demo ===\n")

    # 1. Generate a secret (base32 string)
    secret = pyotp.random_base32()
    print(f"Your secret key (keep it safe!): {secret}")

    # 2. Create a TOTP object
    totp = pyotp.TOTP(secret, interval=30)

    # 3. Generate provisioning URI (for authenticator apps)
    issuer = "2FADemo"
    account = "user@example.com"
    provisioning_uri = totp.provisioning_uri(name=account, issuer_name=issuer)

    print(f"\nProvisioning URI:\n{provisioning_uri}\n")

    # 4. Display QR code
    print("Scan this QR code with Google Authenticator, Authy, etc.")
    try:
        generate_qr_ascii(provisioning_uri)
    except Exception as e:
        print(f"Could not generate QR code: {e}")
        print("You can manually enter the secret key into your app.")

    # 5. Verification loop
    print("\nThe app will now show a 6‑digit code that refreshes every 30 seconds.")
    print("Enter the current code to verify (or type 'exit' to quit).")

    while True:
        # Show remaining time for current interval
        remaining = totp.interval - (time.time() % totp.interval)
        print(f"\n[Code changes in {int(remaining)} seconds]")
        code = input("Enter 6-digit code: ").strip()
        if code.lower() == "exit":
            print("Goodbye!")
            break

        # Verify the code (allow a small drift by using verify with valid_window)
        # For production, allow 1 interval drift (30 sec) to account for clock skew.
        if totp.verify(code, valid_window=1):
            print("✅ Code verified! 2FA authentication successful.")
        else:
            print("❌ Invalid code. Try again.")

        # Optional: show current valid code for testing (remove in production)
        current = totp.now()
        print(f"(Current valid code: {current})")


if __name__ == "__main__":
    main()
