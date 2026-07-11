def caesar_cipher(text: str, shift: int, decrypt: bool = False) -> str:
    """
    Encrypt or decrypt text using the Caesar Cipher.
    
    :param text:   The input string (may include non‑letters).
    :param shift:  The shift value (positive integer). If decrypt is True,
                   the shift is reversed internally.
    :param decrypt: If True, decrypt the text; otherwise encrypt.
    :return:       The transformed string.
    """
    if decrypt:
        shift = -shift          # decryption = shift in opposite direction
    shift %= 26                 # handle shifts larger than 26

    result = []
    for char in text:
        if 'a' <= char <= 'z':
            # Shift lowercase letter and keep within 'a'..'z'
            new_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            result.append(new_char)
        elif 'A' <= char <= 'Z':
            # Shift uppercase letter and keep within 'A'..'Z'
            new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            result.append(new_char)
        else:
            # Non‑alphabetical characters remain unchanged
            result.append(char)
    return ''.join(result)


def main():
    print("=== Caesar Cipher ===")
    while True:
        print("\nOptions:")
        print("1. Encrypt a message")
        print("2. Decrypt a message")
        print("3. Quit")
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '3':
            print("Goodbye!")
            break

        if choice not in ('1', '2'):
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue

        message = input("Enter the message: ")
        try:
            shift = int(input("Enter the shift value (integer): "))
        except ValueError:
            print("Shift must be an integer. Please try again.")
            continue

        if choice == '1':
            result = caesar_cipher(message, shift, decrypt=False)
            print(f"Encrypted message: {result}")
        else:  # choice == '2'
            result = caesar_cipher(message, shift, decrypt=True)
            print(f"Decrypted message: {result}")


if __name__ == "__main__":
    main()
