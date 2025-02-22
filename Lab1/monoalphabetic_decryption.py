from typing import Dict

def create_reverse_substitution_key(substitution_key: Dict[str, str]) -> Dict[str, str]:

    return {v: k for k, v in substitution_key.items()}

def monoalphabetic_decrypt(ciphertext: str, substitution_key: Dict[str, str]) -> str:
    """
    Decrypt text encrypted with monoalphabetic substitution cipher
    Parameters:
        ciphertext (str): The encrypted text to decrypt
        substitution_key (Dict[str, str]): The encryption substitution key
    Returns:
        str: The decrypted text
    """
    # Create the reverse substitution key
    reverse_key = create_reverse_substitution_key(substitution_key)
    
    # Decrypt the text using the reverse substitution key
    decrypted_text = ""
    try:
        for char in ciphertext:
            if char in reverse_key:
                decrypted_text += reverse_key[char]
            else:
                # If character not in key, keep it unchanged
                decrypted_text += char
    except Exception as e:
        print(f"Error during decryption: {e}")
        print(f"Problem character: {char}")
        print(f"Reverse key sample: {dict(list(reverse_key.items())[:5])}")
        raise
    
    return decrypted_text

if __name__ == "__main__":
    # Test the decryption function with a sample substitution key
    test_text = "HELLO World! 123"
    from monoalphabetic_encryption import monoalphabetic_encrypt
    
    # First encrypt the text
    encrypted, key = monoalphabetic_encrypt(test_text)
    
    # Then decrypt it
    decrypted = monoalphabetic_decrypt(encrypted, key)
    
    print(f"Original text: {test_text}")
    print(f"Encrypted text: {encrypted}")
    print(f"Decrypted text: {decrypted}")
    print("\nSample of substitution key used:")
    sample = {k: v for k, v in key.items() if k in test_text}
    print(sample) 