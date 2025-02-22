def caesar_decrypt(ciphertext: str, shift: int) -> str:
    decrypted_text = ""
    for char in ciphertext:
        if char.isalpha():
            shift_amount = shift % 26
            if char.isupper():
                new_char = chr(((ord(char) - ord('A') - shift_amount) % 26) + ord('A'))
            else:
                new_char = chr(((ord(char) - ord('a') - shift_amount) % 26) + ord('a'))
            decrypted_text += new_char
        else:
            decrypted_text += char
    return decrypted_text

if __name__ == "__main__":
    test_text = "KHOOR Zruog! 123"
    shift = 3
    decrypted = caesar_decrypt(test_text, shift)
    print(f"Encrypted text: {test_text}")
    print(f"Decrypted text (shift={shift}): {decrypted}") 