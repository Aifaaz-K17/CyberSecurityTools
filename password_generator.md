# 🔑 Secure Password Generator

A powerful **password generator** written in Python that creates strong, random passwords with customizable complexity. You can specify length, character sets, and exclusions to fit any security policy.

---

## ✨ Features

- **Length** – choose any length (recommended ≥ 12).
- **Character sets** – include/exclude:
  - Uppercase letters (A‑Z)
  - Lowercase letters (a‑z)
  - Digits (0‑9)
  - Special symbols (`!@#$%^&*()_+-=[]{}|;:,.<>?`)
- **Exclude ambiguous characters** – avoid confusing characters like `l`, `I`, `1`, `O`, `0`.
- **Generate multiple passwords** at once.
- **Entropy estimation** – shows the strength in bits.
- **Command‑line interface** with `argparse` for scripting.
- **Interactive mode** – run without arguments for guided input.

---

## 📦 Requirements

- Python 3.6+ (no external libraries needed)
---

## 🚀 Usage Examples

### 1. Generate a default password (16 chars, all sets included)

```bash
python password_generator.py
```

Example output:
```
aB3#kL9$qRt7!wXz
```

### 2. Generate a 20‑character password with no ambiguous characters

```bash
python password_generator.py -l 20 -e
```

### 3. Generate 5 passwords of length 12, only letters (no digits, no special)

```bash
python password_generator.py -l 12 -n 5 -d -s
```

### 4. Show entropy estimation

```bash
python password_generator.py -l 20 -e --entropy
```

Output:
```
xY8#mP2$kL9@qR5^wN7
Entropy: 128.4 bits (pool size 94)
```

### 5. Exclude uppercase, include digits and special

```bash
python password_generator.py -l 16 -u -d -s
```

(Note: `-u` means no uppercase, because we use `--no-upper` flag)

---

## 🧠 How It Works

- **Character pool** is built based on the selected sets.
- **Ambiguous characters** (`l`, `I`, `1`, `O`, `0`) are removed if the `-e` flag is used.
- **Required characters** – one from each chosen set – are added to guarantee diversity.
- The rest of the password is filled with random picks from the pool.
- The final list is **shuffled** to avoid predictable ordering (e.g., uppercase first).
- **Entropy** is estimated using the formula: `bits = length * log2(pool_size)`.
  - For a 16‑character password from a pool of 94 characters, entropy ≈ 16 × log₂(94) ≈ 16 × 6.55 ≈ 104.8 bits – considered very strong.

---

## 🔐 Security Recommendations

- **Minimum length**: 12 characters for moderate security, **16+** for high security.
- **Include all character types** – uppercase, lowercase, digits, and special.
- **Avoid ambiguous characters** if the password will be manually entered.
- **Do not reuse passwords** – use a password manager.
- **Never share passwords** – use the generated ones for your accounts.

---

## 📝 Interactive Mode

If you run the script without arguments, it will use the defaults. For a guided experience, you can also create a wrapper script that asks questions, but the CLI is already simple.

---

## 🛠️ Customisation

You can modify the `SPECIAL` string to include/exclude specific symbols. For example, to allow spaces, add `' '` (space) to the SPECIAL string (though spaces can be problematic in some contexts).

---

**Stay secure – generate strong passwords!** 🔒
