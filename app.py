from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from collections import Counter

app = FastAPI(
    title="Cipher API",
    description="API for Caesar and Monoalphabetic Cipher operations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Allow both ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request and Response Models
class CipherRequest(BaseModel):
    text: str
    shift: int

class AttackRequest(BaseModel):
    text: str

class CipherResponse(BaseModel):
    result: str

class AttackResponse(BaseModel):
    results: List[dict]

# Common English letter frequencies (from most to least common)
ENGLISH_FREQUENCIES = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'.lower()

# Caesar Cipher Implementation
def caesar_encrypt(text: str, shift: int) -> str:
    result = ""
    for char in text:
        if char.isalpha():
            # Determine the case and base ASCII value
            ascii_base = ord('A') if char.isupper() else ord('a')
            # Convert to 0-25 range, apply shift, and convert back
            shifted = (ord(char) - ascii_base + shift) % 26
            result += chr(ascii_base + shifted)
        else:
            result += char
    return result

def caesar_decrypt(text: str, shift: int) -> str:
    return caesar_encrypt(text, -shift)

def caesar_attack(text: str) -> List[dict]:
    results = []
    for shift in range(26):
        decrypted = caesar_decrypt(text, shift)
        results.append({
            "shift": shift,
            "plaintext": decrypted
        })
    return results

# Monoalphabetic Cipher Implementation
def create_substitution_key(shift: int) -> Dict[str, str]:
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

def monoalphabetic_encrypt(text: str, shift: int) -> str:
    key = create_substitution_key(shift)
    result = ""
    for char in text:
        if char.isalpha():
            result += key[char]
        else:
            result += char
    return result

def monoalphabetic_decrypt(text: str, shift: int) -> str:
    return monoalphabetic_encrypt(text, -shift)

def get_frequency_order(text: str) -> str:
    """Get the frequency order of letters in the text"""
    # Count only alphabetic characters
    text = ''.join(c.lower() for c in text if c.isalpha())
    frequencies = Counter(text)
    # Sort letters by frequency (most frequent first)
    sorted_chars = sorted(frequencies.items(), key=lambda x: (-x[1], x[0]))
    return ''.join(char for char, _ in sorted_chars)

def monoalphabetic_attack(text: str) -> List[dict]:
    """Perform frequency analysis attack on monoalphabetic cipher"""
    results = []
    
    # Get frequency order of the ciphertext
    cipher_freq_order = get_frequency_order(text)
    
    # Try all possible shifts and score them based on frequency analysis
    for shift in range(26):
        decrypted = monoalphabetic_decrypt(text, shift)
        
        # Calculate match score based on letter frequencies
        match_score = 0
        for i, letter in enumerate(cipher_freq_order[:6]):  # Check first 6 most common letters
            expected_pos = ENGLISH_FREQUENCIES.find(chr(((ord(letter) - ord('a') - shift) % 26) + ord('a')))
            if expected_pos < 6:  # If the letter is among the 6 most common in English
                match_score += 1 - (expected_pos / 6)
        
        results.append({
            "shift": shift,
            "plaintext": decrypted,
            "likelihood_score": round(match_score, 3)
        })
    
    # Sort results by likelihood score (highest first)
    results.sort(key=lambda x: x["likelihood_score"], reverse=True)
    return results

# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "Welcome to the Cipher API",
        "endpoints": {
            "caesar": ["/caesar/encrypt", "/caesar/decrypt", "/caesar/attack"],
            "monoalphabetic": ["/monoalphabetic/encrypt", "/monoalphabetic/decrypt", "/monoalphabetic/attack"]
        }
    }

# Caesar Cipher Endpoints
@app.post("/caesar/encrypt", response_model=CipherResponse)
async def api_caesar_encrypt(request: CipherRequest):
    """Encrypt text using Caesar cipher"""
    if not 0 <= request.shift <= 25:
        raise HTTPException(status_code=400, detail="Shift must be between 0 and 25")
    result = caesar_encrypt(request.text, request.shift)
    return CipherResponse(result=result)

@app.post("/caesar/decrypt", response_model=CipherResponse)
async def api_caesar_decrypt(request: CipherRequest):
    """Decrypt text using Caesar cipher"""
    if not 0 <= request.shift <= 25:
        raise HTTPException(status_code=400, detail="Shift must be between 0 and 25")
    result = caesar_decrypt(request.text, request.shift)
    return CipherResponse(result=result)

@app.post("/caesar/attack", response_model=AttackResponse)
async def api_caesar_attack(request: AttackRequest):
    """Perform brute force attack on Caesar cipher text"""
    results = caesar_attack(request.text)
    return AttackResponse(results=results)

# Monoalphabetic Cipher Endpoints
@app.post("/monoalphabetic/encrypt", response_model=CipherResponse)
async def api_monoalphabetic_encrypt(request: CipherRequest):
    """Encrypt text using Monoalphabetic cipher"""
    if not 0 <= request.shift <= 25:
        raise HTTPException(status_code=400, detail="Shift must be between 0 and 25")
    result = monoalphabetic_encrypt(request.text, request.shift)
    return CipherResponse(result=result)

@app.post("/monoalphabetic/decrypt", response_model=CipherResponse)
async def api_monoalphabetic_decrypt(request: CipherRequest):
    """Decrypt text using Monoalphabetic cipher"""
    if not 0 <= request.shift <= 25:
        raise HTTPException(status_code=400, detail="Shift must be between 0 and 25")
    result = monoalphabetic_decrypt(request.text, request.shift)
    return CipherResponse(result=result)

@app.post("/monoalphabetic/attack", response_model=AttackResponse)
async def api_monoalphabetic_attack(request: AttackRequest):
    """Perform frequency analysis attack on Monoalphabetic cipher text"""
    results = monoalphabetic_attack(request.text)
    return AttackResponse(results=results)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 