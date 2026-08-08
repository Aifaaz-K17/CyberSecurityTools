import re
import sys

def check_password_strength(password):
    """
    Evaluate a password and return a score (0-6), a strength label,
    and a list of feedback messages in this.
    """
    score = 0
    feedback = []

    # 1. Length
    length = len(password)
    if length >= 12:
        score += 2
        feedback.append("✔ Good length (≥ 12 characters).")
    elif length >= 8:
        score += 1
        feedback.append("✔ Length is adequate (≥ 8 characters).")
    else:
        feedback.append("✗ Password is too short (minimum 8 characters recommended).")

    # 2. Lowercase
    if re.search(r'[a-z]', password):
        score += 1
        feedback.append("✔ Contains lowercase letters.")
    else:
        feedback.append("✗ Add lowercase letters (a-z).")

    # 3. Uppercase
    if re.search(r'[A-Z]', password):
        score += 1
        feedback.append("✔ Contains uppercase letters.")
    else:
        feedback.append("✗ Add uppercase letters (A-Z).")

    # 4. Digits
    if re.search(r'\d', password):
        score += 1
        feedback.append("✔ Contains digits.")
    else:
        feedback.append("✗ Add numbers (0-9).")

    # 5. Special characters
    special_chars = r'[!@#$%^&*(),.?":{}|<>]'
    if re.search(special_chars, password):
        score += 1
        feedback.append("✔ Contains special characters.")
    else:
        feedback.append("✗ Add special characters (!@#$%^&*(),.?\":{}|<>).")

    # Extra warnings (common patterns)
    warnings = []
    # Repeating characters (e.g., "aaa")
    if re.search(r'(.)\1{2,}', password):
        warnings.append("⚠️ Contains repeated characters (e.g., 'aaa').")
    # Sequential characters (e.g., "1234", "abcd")
    if re.search(r'(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()):
        warnings.append("⚠️ Contains sequential characters (e.g., '1234' or 'abcd').")
    # Keyboard walks (e.g., "qwerty", "asdf")
    if re.search(r'(qwerty|asdf|zxcv|qwertyuiop|asdfghjkl|zxcvbnm)', password.lower()):
        warnings.append("⚠️ Contains a keyboard pattern (e.g., 'qwerty').")
    # Common words (simple list)
    common = ['password', '123456', 'qwerty', 'admin', 'letmein', 'welcome', 'monkey', 'dragon']
    if any(word in password.lower() for word in common):
        warnings.append("⚠️ Contains a common password word/phrase.")

    # Determine strength label
    if score >= 6:
        label = "Very Strong"
    elif score >= 5:
        label = "Strong"
    elif score >= 4:
        label = "Moderate"
    elif score >= 3:
        label = "Weak"
    else:
        label = "Very Weak"

    return score, label, feedback, warnings


def main():
    print("=== Password Complexity Checker ===")
    print("Enter a password to evaluate (or 'quit' to exit).")
    while True:
        pwd = input("\nPassword: ").strip()
        if pwd.lower() == 'quit':
            print("Goodbye!")
            break
        if not pwd:
            print("Please enter a password.")
            continue

        score, label, feedback, warnings = check_password_strength(pwd)

        print(f"\nScore: {score}/6")
        print(f"Strength: {label}")
        print("\nFeedback:")
        for msg in feedback:
            print(f"  {msg}")
        if warnings:
            print("\nWarnings:")
            for warn in warnings:
                print(f"  {warn}")
        else:
            print("\nNo obvious weak patterns detected.")

        # Improvement suggestions
        if score < 6:
            print("\nSuggestions for improvement:")
            if score < 3:
                print("  - Make it longer (≥ 12 characters).")
            if not re.search(r'[a-z]', pwd):
                print("  - Include lowercase letters.")
            if not re.search(r'[A-Z]', pwd):
                print("  - Include uppercase letters.")
            if not re.search(r'\d', pwd):
                print("  - Include digits.")
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', pwd):
                print("  - Include special characters.")
            if warnings:
                print("  - Avoid common patterns and dictionary words.")


if __name__ == "__main__":
    main()
