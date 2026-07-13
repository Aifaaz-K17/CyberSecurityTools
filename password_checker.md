A complete **Password Complexity Checker** – a Python tool that evaluates password strength based on common criteria and gives clear, actionable feedback. It assigns a score (0‑5) and labels the password as **Very Weak**, **Weak**, **Moderate**, **Strong**, or **Very Strong**.

---

## 🔍 How It Works

The checker analyses a password against five criteria:

| Criterion                    | Points | Description                         |
|------------------------------|--------|-------------------------------------|
| **Length**                   | up to 2 | ≥ 8 characters → 1 point, ≥ 12 → 2 |
| **Lowercase letters**        | 1      | At least one `a‑z`                  |
| **Uppercase letters**        | 1      | At least one `A‑Z`                  |
| **Digits**                   | 1      | At least one `0‑9`                  |
| **Special characters**       | 1      | At least one of `!@#$%^&*(),.?":{}|<>` |

A perfect score of 6 means the password meets all criteria **and** is at least 12 characters long. The tool also detects common patterns like repeated characters, sequences (`1234`, `abcd`), and keyboard walks (`qwerty`), issuing warnings.

---

## 🧠 Features

- **Scoring system** – transparent and easy to understand.
- **Detailed feedback** – tells you exactly what’s missing and how to improve.
- **Pattern detection** – warns against obvious weak patterns.
- **No external dependencies** – uses only Python’s standard library.

---

## 🚀 Usage

1. Save the code as `password_checker.py`.
2. Run it from the terminal:
   ```bash
   python password_checker.py
   ```
3. Enter a password when prompted. The tool will display:
   - A score out of 6.
   - A strength label.
   - Specific feedback on what’s good and what’s missing.
   - Warnings about common weak patterns.
   - Improvement suggestions if the password isn’t perfect.

### Example Session

```
=== Password Complexity Checker ===
Enter a password to evaluate (or 'quit' to exit).

Password: P@ssw0rd

Score: 5/6
Strength: Strong

Feedback:
  ✔ Length is adequate (≥ 8 characters).
  ✔ Contains lowercase letters.
  ✔ Contains uppercase letters.
  ✔ Contains digits.
  ✔ Contains special characters.

Warnings:
  ⚠️ Contains a common password word/phrase.

Suggestions for improvement:
  - Make it longer (≥ 12 characters).
  - Avoid common patterns and dictionary words.
```

---

## 📝 Extending the Checker

You can easily add more rules:

- **More character classes** (e.g., Unicode letters).
- **Blacklist** of passwords (from known breaches).
- **Entropy calculation** (bits of entropy).
- **Integration** with `zxcvbn` (a popular strength estimator) – but that requires an external library.

For now, this tool provides a solid, transparent foundation for password strength assessment – perfect for educational or basic security‑awareness purposes.
