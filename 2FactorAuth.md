# 🔐 Two-Factor Authentication (2FA) Demo – TOTP

This demo implements **Time‑based One‑Time Password (TOTP)** – the most common form of 2FA used by Google Authenticator, Authy, and others.  
You'll generate a secret key, get a QR code to scan into your authenticator app, and then verify a 6‑digit code that changes every 30 seconds.

---

## 📦 Requirements

Install the required libraries:

```bash
pip install pyotp qrcode[pil] pillow
```

- **[pyotp](https://github.com/pyauth/pyotp)** – generates and verifies TOTP codes.
- **[qrcode](https://github.com/lincolnloop/python-qrcode)** with Pillow – to display a QR code in the terminal (or save as an image).

---

## 🚀 Usage

1. Run the script:
   ```bash
   python 2fa_demo.py
   ```

2. You'll see:
   - A **secret key** (base32 string) – keep this safe.
   - A **QR code** printed as ASCII art (and saved as `2fa_qr.png`).

3. Open your authenticator app (Google Authenticator, Microsoft Authenticator, Authy, etc.) and **scan the QR code** (or enter the secret manually).

4. The app will start showing a 6‑digit code that refreshes every 30 seconds.

5. Enter the current code into the terminal to verify.

**Example output:**
```
=== TOTP 2FA Demo ===

Your secret key (keep it safe!): JBSWY3DPEHPK3PXP

Provisioning URI:
otpauth://totp/2FADemo:user@example.com?secret=JBSWY3DPEHPK3PXP&issuer=2FADemo

Scan this QR code with Google Authenticator, Authy, etc.
█▀▀▀▀▀█ ▄▄▄ ▀▀ █▀▀▀▀▀█
█ ███ █ ▄▀▄ █▄▄ █ ███ █
█ ▀▀▀ █ ▄▀▄ █▄ █ ▀▀▀ █
▀▀▀▀▀▀▀ ▀▄█ ▀ ▀ ▀▀▀▀▀▀▀
...
QR code also saved as '2fa_qr.png'.

The app will now show a 6‑digit code that refreshes every 30 seconds.
Enter the current code to verify (or type 'exit' to quit).

[Code changes in 12 seconds]
Enter 6-digit code: 123456
❌ Invalid code. Try again.
(Current valid code: 874203)

[Code changes in 28 seconds]
Enter 6-digit code: 874203
✅ Code verified! 2FA authentication successful.
```

---

## 🧠 How It Works

- **TOTP** (RFC 6238) generates a one‑time password based on:
  - A shared **secret key** (base32‑encoded).
  - The **current Unix timestamp** (divided by 30 seconds).
  - HMAC‑SHA1 (or SHA‑256/512) hashing.

- **pyotp** handles all the math:
  - `pyotp.random_base32()` – generates a cryptographically secure secret.
  - `totp.now()` – returns the current 6‑digit code.
  - `totp.verify(code)` – checks if the code matches for the current time window (with optional drift tolerance).
  - `provisioning_uri()` – creates a URI that authenticator apps understand (with issuer and account name).

- **QR code** – the URI is encoded into a QR code so you can scan it directly.

---

## 🔒 Integration with a Web App (Flask)

You can easily integrate this into a login flow. After the user enters their username/password, you check their 2FA code:

```python
# After successful login (password correct)
if user.has_2fa_enabled:
    secret = user.totp_secret  # stored in DB
    totp = pyotp.TOTP(secret)
    if not totp.verify(request.form['2fa_code']):
        return "Invalid 2FA code", 401
    # else proceed
```

The secret should be stored per user (encrypted at rest). You can also generate the secret during setup and show the QR code to the user.

---

## 🛡️ Important Security Considerations

- **Store secrets securely** – treat them like passwords; use encryption at rest.
- **Backup codes** – provide one‑time recovery codes in case the user loses their device.
- **Rate limiting** – prevent brute‑force attacks on the 2FA code.
- **Clock skew** – the `valid_window=1` allows a code from the previous or next interval (30 sec). This is standard to handle minor clock differences.
- **Disable 2FA** – provide a secure way to reset 2FA (e.g., email verification).

---

## 📚 Further Enhancements

- **HOTP** (counter‑based) – if you want an alternative to time‑based.
- **Recovery codes** – generate a list of 10 one‑time codes for emergencies.
- **Email/SMS 2FA** – send a code via email or SMS (less secure than TOTP).
- **Web-based demo** – you can wrap this in a Flask app with a nice UI (login + 2FA step).

---

**Stay secure – enable 2FA everywhere!** 🔐
