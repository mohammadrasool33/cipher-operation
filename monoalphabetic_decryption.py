from typing import Dict

def create_reverse_substitution_key(shift: int) -> Dict[str, str]:
    """
    Create a reverse substitution key for decryption
    Parameters:
        shift (int): The shift value used for encryption
    Returns:
        Dict[str, str]: Dictionary mapping each substituted letter back to original
    """
    # Create substitution for uppercase and lowercase letters
    substitution = {}
    
    # Create reverse mapping for uppercase letters (A-Z)
    for i in range(26):
        substituted = chr(ord('A') + ((i + shift) % 26))
        original = chr(ord('A') + i)
        substitution[substituted] = original
    
    # Create reverse mapping for lowercase letters (a-z)
    for i in range(26):
        substituted = chr(ord('a') + ((i + shift) % 26))
        original = chr(ord('a') + i)
        substitution[substituted] = original
    
    return substitution

def monoalphabetic_decrypt(ciphertext: str, shift: int) -> str:
    """
    Decrypt text encrypted with monoalphabetic substitution cipher
    Parameters:
        ciphertext (str): The encrypted text to decrypt
        shift (int): The shift value used for encryption
    Returns:
        str: The decrypted text
    """
    # Create the reverse substitution key
    reverse_key = create_reverse_substitution_key(shift)
    
    # Decrypt the text using the reverse substitution key
    decrypted_text = ""
    for char in ciphertext:
        if char.isalpha():
            # Use the reverse substitution key for alphabetic characters
            decrypted_text += reverse_key[char]
        else:
            # Keep non-alphabetic characters unchanged
            decrypted_text += char
    
    return decrypted_text

if __name__ == "__main__":
    # Test the decryption function
    test_text = "KHOOR Zruog! 123"  # "HELLO World! 123" encrypted with shift=3
    shift = 3
    
    # Show the reverse substitution key
    key = create_reverse_substitution_key(shift)
    print("Reverse Substitution Key:")
    print("Uppercase:", {k: v for k, v in key.items() if k.isupper()})
    print("Lowercase:", {k: v for k, v in key.items() if k.islower()})
    
    # Perform decryption
    decrypted = monoalphabetic_decrypt(test_text, shift)
    print(f"\nEncrypted text: {test_text}")
    print(f"Decrypted text (shift={shift}): {decrypted}") 