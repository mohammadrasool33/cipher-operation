from typing import Dict

def create_substitution_key(shift: int) -> Dict[str, str]:
    """
    Create a substitution key for the monoalphabetic cipher
    Parameters:
        shift (int): The shift value to create the substitution alphabet
    Returns:
        Dict[str, str]: Dictionary mapping each letter to its substitution
    """
    # Create substitution for uppercase and lowercase letters
    substitution = {}
    
    # Create mapping for uppercase letters (A-Z)
    for i in range(26):
        original = chr(ord('A') + i)
        substituted = chr(ord('A') + ((i + shift) % 26))
        substitution[original] = substituted
    
    # Create mapping for lowercase letters (a-z)
    for i in range(26):
        original = chr(ord('a') + i)
        substituted = chr(ord('a') + ((i + shift) % 26))
        substitution[original] = substituted
    
    return substitution

def monoalphabetic_encrypt(plaintext: str, shift: int) -> str:
    """
    Encrypt text using monoalphabetic substitution cipher
    Parameters:
        plaintext (str): The text to encrypt
        shift (int): The shift value to create substitution alphabet
    Returns:
        str: The encrypted text
    """
    # Create the substitution key
    substitution_key = create_substitution_key(shift)
    
    # Encrypt the text using the substitution key
    encrypted_text = ""
    for char in plaintext:
        if char.isalpha():
            # Use the substitution key for alphabetic characters
            encrypted_text += substitution_key[char]
        else:
            # Keep non-alphabetic characters unchanged
            encrypted_text += char
    
    return encrypted_text

if __name__ == "__main__":
    # Test the encryption function
    test_text = "HELLO World! 123"
    shift = 3
    
    # Show the substitution key
    key = create_substitution_key(shift)
    print("Substitution Key:")
    print("Uppercase:", {k: v for k, v in key.items() if k.isupper()})
    print("Lowercase:", {k: v for k, v in key.items() if k.islower()})
    
    # Perform encryption
    encrypted = monoalphabetic_encrypt(test_text, shift)
    print(f"\nOriginal text: {test_text}")
    print(f"Encrypted text (shift={shift}): {encrypted}") 