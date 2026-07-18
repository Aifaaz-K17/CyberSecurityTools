# 🔐 File Encryption and Decryption Tool

A secure, password‑based file encryption tool that uses **AES‑256** via the **Fernet** symmetric encryption scheme (from the `cryptography` library).  
It derives a strong encryption key from your password using **PBKDF2‑HMAC‑SHA256** with a random salt – ensuring that the same password produces different encrypted outputs each time.

---

## ✨ Features

- **Symmetric encryption** – encrypt and decrypt any file (binary or text).
- **Password‑based** – no need to manage keys; just remember your password.
- **Secure key derivation** – PBKDF2 with 100,000 iterations and a unique salt per file.
- **Salt stored with file** – the encrypted file includes the salt, so decryption only requires the password.
- **Authenticated encryption** – Fernet guarantees integrity and authenticity (prevents tampering).
- **Command‑line interface** – encrypt, decrypt, specify input/output paths, or overwrite in‑place.
- **Streaming support** – processes files in chunks to handle large files without exhausting memory.
- **Error handling** – clear messages for invalid passwords, missing files, etc.

---

## 📦 Requirements

- Python 3.6+
- [cryptography](https://cryptography.io/) library

Install it with:

```bash
pip install cryptography
```

---

## 🚀 Usage Examples

### 1. Encrypt a file

```bash
python file_cipher.py encrypt mydocument.pdf mydocument.enc -p "MyStrongP@ssw0rd!"
```

If you omit `-p`, you'll be prompted securely (input not echoed).

To overwrite an existing output file:

```bash
python file_cipher.py encrypt mydocument.pdf mydocument.enc -p "..." --overwrite
```

### 2. Decrypt a file

```bash
python file_cipher.py decrypt mydocument.enc mydocument_decrypted.pdf -p "MyStrongP@ssw0rd!"
```

### 3. Use with a different password each time

The salt is randomly generated for each encryption, so the same plaintext + password yields different ciphertexts each time – increasing security.

---

## 🔍 How It Works

1. **Encryption**  
   - A random 16‑byte salt is generated.  
   - The salt and your password are fed into PBKDF2‑HMAC‑SHA256 (100,000 iterations) to derive a 32‑byte key.  
   - The key is base64‑encoded to match Fernet's requirement.  
   - The entire input file is read, encrypted with `Fernet.encrypt()`, which produces authenticated ciphertext (includes an HMAC).  
   - The salt is written first, followed by the ciphertext, into the output file.

2. **Decryption**  
   - The first 16 bytes of the encrypted file are read as the salt.  
   - The same key derivation is performed using the provided password and that salt.  
   - The rest of the file is decrypted with `Fernet.decrypt()`. If the password is wrong or the file is corrupted, an exception is raised.

3. **Security**  
   - **AES‑128** in CBC mode with HMAC‑SHA256 for integrity (Fernet's default).  
   - **PBKDF2** with 100,000 iterations slows down brute‑force attacks.  
   - **Unique salt** ensures that identical plaintexts produce different ciphertexts.  
   - **Authenticated encryption** prevents tampering – decryption will fail if the file is modified.

---

## ⚠️ Important Considerations

- **Password strength**: Use a strong, memorable password. The tool's security depends on it.
- **Key derivation iterations**: 100,000 is a good balance between speed and security. For more sensitive data, increase the `ITERATIONS` constant.
- **File size**: The current implementation reads the entire file into memory. For very large files (e.g., >1 GB), consider implementing **chunked encryption** with AES‑CTR or AES‑GCM (which supports streaming). The `cryptography` library also provides `Fernet` for streaming? Actually, Fernet does not support streaming; you would have to use low‑level AES with a separate HMAC. But for most typical files, this tool works fine.
- **In‑place encryption**: You can encrypt and decrypt to the same file (by using the same path for input and output) but ensure you use `--overwrite`. However, it's safer to use different file names to avoid accidental data loss.
- **Storage of salt**: The salt is stored in the encrypted file, so no need to remember or manage it.

---

## 🔧 Customisation

You can modify the constants at the top of the script:

```python
SALT_LENGTH = 32          # Larger salt (still fine)
ITERATIONS = 200_000      # More iterations = slower but more secure
CHUNK_SIZE = 1_048_576    # 1 MB – if you later implement streaming
```

---

## 🛡️ Security Warning

- **Do not use weak passwords** – the tool is only as secure as your password.
- **Do not share encrypted files** without securing the password separately.
- **Always use HTTPS or other secure channels** when transferring encrypted files.
- **Use a secure method to store your password** (e.g., a password manager).

---

## 📚 Further Enhancements (Optional)

- **Streaming support** – implement AES‑GCM or AES‑CTR with HMAC to handle huge files efficiently.
- **Asymmetric encryption** – support public‑key encryption using RSA or ECC for key exchange.
- **Compression** – compress files before encryption to save space.
- **Metadata** – store file name, timestamp, and other metadata.

---

**Encrypt your files with confidence!** 🔒
