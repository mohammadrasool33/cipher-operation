from typing import Dict, List, Tuple
from collections import Counter
from monoalphabetic_decryption import monoalphabetic_decrypt

# Common letter frequencies in English text (from most to least common)
ENGLISH_FREQUENCIES = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'.lower()

def get_frequency_order(text: str) -> str:
    """
    Get the frequency order of letters in the text
    Parameters:
        text (str): The text to analyze
    Returns:
        str: Letters ordered by frequency (most to least frequent)
    """
    # Count only alphabetic characters
    text = ''.join(c.lower() for c in text if c.isalpha())
    
    # Count frequencies
    frequencies = Counter(text)
    
    # Sort letters by frequency (most frequent first)
    sorted_chars = sorted(frequencies.items(), key=lambda x: (-x[1], x[0]))
    
    # Return just the letters in order
    return ''.join(char for char, _ in sorted_chars)

def calculate_possible_shifts(ciphertext: str) -> List[Tuple[int, float]]:
    """
    Calculate possible shift values based on frequency analysis
    Parameters:
        ciphertext (str): The encrypted text to analyze
    Returns:
        List[Tuple[int, float]]: List of (shift, match_score) pairs
    """
    # Get frequency order of the ciphertext
    cipher_freq_order = get_frequency_order(ciphertext)
    
    possible_shifts = []
    
    # Try matching the frequency patterns
    for i in range(26):
        match_score = 0
        for j, letter in enumerate(cipher_freq_order[:6]):  # Check first 6 most common letters
            expected_pos = ENGLISH_FREQUENCIES.find(chr(((ord(letter) - ord('a') - i) % 26) + ord('a')))
            if expected_pos < 6:  # If the letter is among the 6 most common in English
                match_score += 1 - (expected_pos / 6)
        
        possible_shifts.append((i, match_score))
    
    # Sort by match score, highest first
    return sorted(possible_shifts, key=lambda x: x[1], reverse=True)

def monoalphabetic_attack(ciphertext: str) -> List[Dict[str, any]]:
    """
    Perform a frequency analysis attack on monoalphabetic cipher
    Parameters:
        ciphertext (str): The encrypted text to attack
    Returns:
        List[Dict]: List of dictionaries containing shift values and corresponding decrypted text,
                   ordered by likelihood (most likely first)
    """
    # Get possible shifts based on frequency analysis
    possible_shifts = calculate_possible_shifts(ciphertext)
    
    # Try decryption with each shift, ordered by likelihood
    results = []
    for shift, score in possible_shifts:
        decrypted = monoalphabetic_decrypt(ciphertext, shift)
        results.append({
            "shift": shift,
            "likelihood_score": round(score, 3),
            "plaintext": decrypted
        })
    
    return results

def print_attack_results(results: List[Dict[str, any]]) -> None:
    """
    Print the results of the frequency analysis attack in a readable format
    """
    print("\nFrequency Analysis Attack Results:")
    print("-" * 70)
    print(f"{'Shift':>6} {'Score':>8} {'Decrypted Text':<50}")
    print("-" * 70)
    
    for result in results:
        print(f"{result['shift']:6d} {result['likelihood_score']:8.3f} {result['plaintext'][:50]}")
    print("-" * 70)

if __name__ == "__main__":
    # Test the attack function
    test_text = "KHOOR Zruog! 123"  # "HELLO World! 123" encrypted with shift=3
    print(f"Encrypted text: {test_text}")
    
    # Show frequency analysis
    freq_order = get_frequency_order(test_text)
    print(f"\nLetter frequencies in ciphertext (most to least common): {freq_order}")
    
    # Perform the attack
    results = monoalphabetic_attack(test_text)
    
    # Print results
    print_attack_results(results) 