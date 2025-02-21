from caesar_decryption import caesar_decrypt
from typing import List, Dict

def caesar_attack(ciphertext: str) -> List[Dict[str, any]]:
    """
    Perform a brute force attack on Caesar cipher encrypted text
    Parameters:
        ciphertext (str): The encrypted text to attack
    Returns:
        List[Dict]: List of dictionaries containing shift values and corresponding decrypted text
    """
    results = []
    # Try all possible shifts (0-25)
    for shift in range(26):
        decrypted = caesar_decrypt(ciphertext, shift)
        results.append({
            "shift": shift,
            "plaintext": decrypted
        })
    return results

def print_attack_results(results: List[Dict[str, any]]) -> None:
    """
    Print the results of the brute force attack in a readable format
    """
    print("\nBrute Force Attack Results:")
    print("-" * 50)
    for result in results:
        print(f"Shift {result['shift']:2d}: {result['plaintext']}")
    print("-" * 50)

if __name__ == "__main__":
    # Test the attack function
    test_text = "KHOOR Zruog! 123"  # "HELLO World! 123" encrypted with shift=3
    print(f"Encrypted text: {test_text}")
    
    # Perform the attack
    results = caesar_attack(test_text)
    
    # Print results
    print_attack_results(results) 