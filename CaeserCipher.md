# 🔐 Caesar Cipher

A simple Python implementation of the **Caesar Cipher** – one of the oldest and most well‑known encryption techniques.  
This program lets you **encrypt** or **decrypt** any text by shifting each letter by a given integer value.

---

## ✨ Features

- **Encrypt** and **decrypt** messages with a user‑defined shift.
- Preserves **case** (uppercase/lowercase letters stay the same).
- Leaves **non‑alphabetic** characters (spaces, punctuation, digits) unchanged.
- Handles **large shift values** (wraps around using modulo 26).
- Interactive menu – easy to use directly from the terminal.

---

## 📦 Requirements

- Python 3.6 or higher (uses only the standard library).

No additional packages are required.

---

## 🚀 Installation

1. **Clone** or **download** the script file `caesar_cipher.py`.
2. Make sure you have Python installed on your system.
3. Run the program from your terminal: `python caesar_cipher.py`.

🧑‍💻 Usage
When you start the program, you’ll see a menu with three options:

text
=== Caesar Cipher ===

Options:
1. Encrypt a message
2. Decrypt a message
3. Quit
Encrypt – enter the message and a shift value. The program outputs the ciphertext.

Decrypt – enter the ciphertext and the same shift value used for encryption. The original plaintext is restored.

Quit – exit the program.

Example
text
Enter your choice (1/2/3): 1
Enter the message: Hello, World!
Enter the shift value (integer): 3
Encrypted message: Khoor, Zruog!
text
Enter your choice (1/2/3): 2
Enter the message: Khoor, Zruog!
Enter the shift value (integer): 3
Decrypted message: Hello, World!
Note: For decryption, you can also use a negative shift (e.g., -3) instead of choosing the decrypt option – both work.

🔍 How It Works
The Caesar Cipher replaces each letter with a letter a fixed number of positions down the alphabet. For example, with a shift of 3:

A → D

B → E

…

Z → C (wrap around)

The algorithm:

Shifts only alphabetic characters.

Uses modulo arithmetic (% 26) to handle wrapping.

Decryption applies the negative of the shift.

🤝 Contributing
Contributions are welcome! If you find a bug or have an idea for improvement, please open an issue or submit a pull request.


