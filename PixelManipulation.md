Here’s a complete Python‑based tool for **image encryption using pixel manipulation**. It supports three simple operations – **XOR**, **addition/subtraction**, and **channel swapping** – all of which are reversible for decryption. The program works with common image formats (PNG, JPG, etc.) and preserves the image mode (RGB, RGBA).

---

## 🔧 Dependencies

- [Pillow](https://python-pillow.org/) – Python Imaging Library.  
  Install via pip:  
  ```bash
  pip install Pillow
  ```

---

## 🧠 How It Works

The tool processes every pixel of the image and alters its colour channels.  
Three methods are provided:

| Method   | Encryption                               | Decryption                               |
|----------|------------------------------------------|------------------------------------------|
| `xor`    | XOR each channel with a key byte (0‑255) | Same operation (XOR is self‑inverse)     |
| `add`    | Add the key modulo 256 to each channel   | Subtract the key modulo 256 from each    |
| `swap`   | Swap the Red and Blue channels           | Swap them back (same operation)          |

> **Note:** For `xor` and `add`, the key must be an integer between 0 and 255.  
> The alpha channel (if present) is also processed – you can easily skip it by modifying the code.

---

## 🚀 Usage

The script is designed as a command‑line tool. Run it with:

```bash
python PixelManipulation.py <mode> <input_image> <output_image> [options]
```

### Arguments

| Argument        | Description |
|-----------------|-------------|
| `mode`          | Operation: `xor`, `add`, or `swap` |
| `input_image`   | Path to the original/encrypted image |
| `output_image`  | Path where the result will be saved |
| `-k, --key`     | Key (integer 0‑255) – required for `xor` and `add` |
| `-d, --decrypt` | Flag to perform decryption (for `add`; for `xor` it’s optional, for `swap` it’s ignored) |

### Examples

1. **Encrypt** with XOR (key=42):
   ```bash
   python PixelManipulation.py xor photo.png encrypted.png -k 42
   ```

2. **Decrypt** the XOR‑encrypted image (same key):
   ```bash
   python PixelManipulation.py xor encrypted.png decrypted.png -k 42
   ```

3. **Encrypt** with addition (key=100):
   ```bash
   python PixelManipulation.py add photo.png encrypted.png -k 100
   ```

4. **Decrypt** addition‑encrypted image (subtract the same key):
   ```bash
   python PixelManipulation.py add encrypted.png decrypted.png -k 100 -d
   ```

5. **Swap** red and blue channels (no key needed):
   ```bash
   python PixelManipulation.py swap photo.png swapped.png
   ```
   Run again on `swapped.png` to restore the original.
   
---

## ⚠️ Important Notes

- **Security**: This tool is for **educational purposes only**. The methods used are trivial and **not secure** against any form of cryptanalysis. Do not use them to protect sensitive data.
- **Lossy formats**: If you use JPEG, repeated encryption/decryption may degrade quality due to compression artefacts. Prefer PNG or BMP.
- **Large images**: The script loads the entire image into memory – for very large images you may want to process them in chunks.
- **Alpha channel**: The current implementation processes the alpha channel as well, which may affect transparency. To keep alpha unchanged, modify the loop to apply operations only to the first three channels.

---

## 🔄 Extending the Tool

You can easily add more pixel operations, e.g.:

- **Bit‑wise NOT** on each channel.
- **Swapping adjacent pixels** (requires storing a permutation key).
- **Adding a pseudo‑random pattern** generated from a seed.

Feel free to adapt the code to your needs!
