# ⚠️ Ethical Warning – Read First

**This project is provided for educational and authorised security testing purposes ONLY.**  
Unauthorised use of keyloggers is **illegal** in most jurisdictions and violates privacy laws.  
You **must** obtain explicit, written consent from any user whose keystrokes you record.  
**Never** use this tool on systems or devices you do not own or lack permission to monitor.

---

## 🔐 Simple Keylogger (Python)

This is a basic keylogger that records every keystroke and saves them to a log file. It runs in the background, captures both regular and special keys (e.g., Shift, Enter, Space), and stops when you press the **`Esc`** key.

---

### 📦 Requirements

- Python 3.6+
- The `pynput` library (for low‑level keyboard monitoring)

Install it with:

```bash
pip install pynput
```

---

### 🚀 How to Use

1. Save the code as `keylogger.py`.
2. Run it from the terminal:
   ```bash
   python keylogger.py
   ```
3. The script starts listening for keyboard input. Every key press is logged to `keylog.txt` with a timestamp.
4. Press the **`Esc`** key to stop the logger and exit.

---

### 📂 Log File Format

Each log entry looks like:

```
[2026-07-11 14:32:10] H
[2026-07-11 14:32:10] e
[2026-07-11 14:32:10] l
[2026-07-11 14:32:10] l
[2026-07-11 14:32:10] o
[2026-07-11 14:32:11] <space>
[2026-07-11 14:32:11] W
[2026-07-11 14:32:11] o
[2026-07-11 14:32:11] r
[2026-07-11 14:32:11] l
[2026-07-11 14:32:11] d
[2026-07-11 14:32:12] <shift>
[2026-07-11 14:32:12] ! 
```

Special keys appear in angle brackets (e.g., `<space>`, `<shift>`, `<ctrl>`, `<enter>`).

---

### 🔧 Customisation Options

You can easily modify the script:

- **Change log file** – update the `LOG_FILE` variable.
- **Change stop key** – set `STOP_KEY` to another key, e.g., `keyboard.Key.f1`.
- **Hide console output** – remove the `print(f"Logged: {key_str}")` line.
- **Run silently** – you can run it as a background process (but that may be considered more intrusive).

---

### ⚠️ Important Ethical & Legal Reminders

- **Always obtain consent** before running this on any machine.
- **Do not use** for spying, stealing passwords, or any malicious purpose.
- **Use only** on systems you own or have explicit permission to test.
- **Respect privacy** – logs can contain sensitive information (passwords, personal messages). Handle them securely.
- **Disclose** the presence of the logger if it’s part of a security assessment.

This code is a **demonstration** of how low‑level keyboard input can be captured. It is **not** a complete, production‑ready tool – real keyloggers often use more advanced techniques to avoid detection and capture more context (window titles, clipboard, etc.). Those are **not** covered here to discourage misuse.

---

### 📚 Further Enhancements (For Educational Use Only)

- Log window titles to know which application was in focus.
- Send logs via email or network (requires permission and security measures).
- Encrypt the log file for protection.
- Implement a start/stop hotkey combination.

But again – **only with proper authorisation and in a controlled environment**.

---

**Stay ethical, stay legal.** 🛡️
