def caesar_encrypt(plaintext: str, shift: int) -> str:
    """
    Encrypt text using Caesar cipher, only shifting alphabetic characters
    Parameters:
        plaintext (str): The text to encrypt
        shift (int): The shift value (0-25)
    Returns:
        str: The encrypted text
    """
    encrypted_text = ""
    for char in plaintext:
        if char.isalpha():
            # Calculate shift amount (ensure it's between 0-25)
            shift_amount = shift % 26
            
            # Handle uppercase and lowercase separately
            if char.isupper():
                # Convert to 0-25 range, apply shift, and convert back to ASCII
                new_char = chr(((ord(char) - ord('A') + shift_amount) % 26) + ord('A'))
            else:
                # Convert to 0-25 range, apply shift, and convert back to ASCII
                new_char = chr(((ord(char) - ord('a') + shift_amount) % 26) + ord('a'))
            encrypted_text += new_char
        else:
            # Keep non-alphabetic characters unchanged
            encrypted_text += char
    return encrypted_text

if __name__ == "__main__":
    # Test the encryption function
    test_text = "HELLO World! 123"
    shift = 3
    encrypted = caesar_encrypt(test_text, shift)
    print(f"Original text: {test_text}")
    print(f"Encrypted text (shift={shift}): {encrypted}") 