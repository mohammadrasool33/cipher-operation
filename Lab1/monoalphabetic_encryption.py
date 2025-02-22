from typing import Dict
import random

def create_substitution_key() -> Dict[str, str]:

    # Create list of all possible ASCII characters (0-255)
    characters = [chr(i) for i in range(256)]
    # Create a shuffled copy of the characters
    shuffled = characters.copy()
    random.shuffle(shuffled)
    
    # Create the substitution mapping
    substitution = {}
    for original, substituted in zip(characters, shuffled):
        substitution[original] = substituted
    
    return substitution

def monoalphabetic_encrypt(plaintext: str) -> tuple[str, Dict[str, str]]:

    # Create the substitution key
    substitution_key = create_substitution_key()
    
    # Encrypt the text using the substitution key
    encrypted_text = ""
    for char in plaintext:
        encrypted_text += substitution_key[char]
    
    return encrypted_text, substitution_key

if __name__ == "__main__":
    test_text = "HELLO World! 123"
    
    # Perform encryption
    encrypted, key = monoalphabetic_encrypt(test_text)
    print(f"\nOriginal text: {test_text}")
    print(f"Encrypted text: {encrypted}")
    print("\nSubstitution Key (sample):")
    # Print a few example mappings
    sample = {k: v for k, v in key.items() if k in test_text}
    print(sample) 