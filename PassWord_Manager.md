# 🔐 Secure Password Manager

A complete, encrypted password manager written in Python.  
It stores your credentials (service, username, password, notes) in an **encrypted JSON vault**.  
You protect the vault with a **master password** – the tool derives a strong encryption key using PBKDF2, so your data remains safe even if the vault file is stolen.

---

## ✨ Features

- **Master password** – required to unlock the vault.
- **Strong encryption** – AES‑256 (via Fernet) with key derived from your master password.
- **Vault stored as JSON** – human‑readable when decrypted, but encrypted at rest.
- **CRUD operations** – add, retrieve, list, and delete credentials.
- **Change master password** – re‑encrypts the vault with the new key.
- **Clipboard support** – optional copy‑to‑clipboard for the password (if `pyperclip` is installed).
- **Secure input** – uses `getpass` for password entry, no echo.
- **Salt and iterations** – PBKDF2 with 100,000 iterations and a random salt per vault.

---

## 📦 Requirements

```bash
pip install cryptography bcrypt
```

Optional (for clipboard):

```bash
pip install pyperclip
```


## 🚀 Usage Examples

### 1. Initialize the vault (first run)

```bash
python pwm.py init
```

You'll be prompted to set a master password. This creates:
- `vault.json` – encrypted data (initially empty)
- `salt.bin` – random salt for key derivation
- `master.hash` – bcrypt hash of your master password

### 2. Add a new entry

```bash
python pwm.py add
```

You'll be prompted for the master password, then for service name, username, password, and optional notes.

### 3. List all entries

```bash
python pwm.py list
```

Shows a numbered list of service names and usernames.

### 4. Retrieve a password

```bash
python pwm.py get github
```

Displays the entry details and copies the password to your clipboard (if `pyperclip` is installed).

### 5. Delete an entry

```bash
python pwm.py delete github
```

### 6. Change master password

```bash
python pwm.py change-master
```

You'll be asked for the current password and then twice for the new one. The vault is re‑encrypted with the new key.

### 7. Export vault (plain JSON, **unencrypted** – use with caution!)

```bash
python pwm.py export backup.json
```

---

## 🧠 How It Works

- **Master password** is **never stored** – only its bcrypt hash (`master.hash`) is kept.
- **Encryption key** is derived from your master password and a **random salt** (`salt.bin`) using PBKDF2‑HMAC‑SHA256 with 100,000 iterations.
- **Vault** is a JSON object `{"entries": [...]}` encrypted with **Fernet** (AES‑128‑CBC + HMAC‑SHA256) and stored in `vault.json`.
- When you unlock the vault, you enter the master password, which is verified against the bcrypt hash. If correct, the salt is used to derive the encryption key, which decrypts the vault.
- All operations (add, get, delete, etc.) load the vault into memory, modify it, and save it back encrypted.

---

## 🔒 Security Features

- **Password‑based encryption** – your data is only accessible with the master password.
- **Slow hashing** – PBKDF2 (100k iterations) + bcrypt (10 rounds) both slow down brute‑force.
- **Random salt** – ensures the same master password produces different keys; prevents rainbow table attacks.
- **Authenticated encryption** – Fernet guarantees that the vault hasn't been tampered with.
- **No plaintext storage** – passwords are never written to disk unencrypted (except when you explicitly `export`).
- **Secure input** – `getpass` hides your master password and entry passwords.

---

## 🛡️ Important Caveats

- **Master password strength** – the tool is only as secure as your master password. Use a strong, unique phrase.
- **Backup** – regularly back up your vault file (and salt/hash) – but **do not** expose them.
- **Export** – the `export` command produces a **plain JSON** file – keep it in an encrypted container (e.g., VeraCrypt) if you store it.
- **Memory** – the vault is decrypted and stored in memory while the tool runs. On a shared machine, be cautious.
- **Clipboard** – if you use `pyperclip`, the password remains in the clipboard; clear it manually or use a clipboard manager.

---

## 📚 Potential Enhancements

- **Auto‑clear clipboard** after a few seconds.
- **Search** by partial service name.
- **Categories/tags** for organisation.
- **Multiple vaults** (e.g., personal, work).
- **Secure sharing** via encryption with public keys.
- **Graphical interface** (Tkinter or a web UI).

---

**Protect your passwords – use this manager with care!** 🔐
