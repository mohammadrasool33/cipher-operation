from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from collections import Counter
import random
import string

app = FastAPI(
    title="Cipher API",
    description="API for Monoalphabetic Cipher operations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request and Response Models
class CipherRequest(BaseModel):
    text: str

class DecryptRequest(BaseModel):
    text: str
    key: Dict[str, str]

class CipherResponse(BaseModel):
    result: str
    key: Dict[str, str]

class AttackRequest(BaseModel):
    text: str

class AttackResponse(BaseModel):
    results: List[dict]

# English letter frequencies (from most to least common)
ENGLISH_FREQUENCIES = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'.lower()

def create_substitution_key() -> Dict[str, str]:
    """Create a random substitution key for printable characters"""
    # Use printable ASCII characters
    characters = list(string.printable)
    shuffled = characters.copy()
    random.shuffle(shuffled)
    return dict(zip(characters, shuffled))

def monoalphabetic_encrypt(text: str) -> tuple[str, Dict[str, str]]:
    """Encrypt using random substitution"""
    key = create_substitution_key()
    result = ''.join(key.get(char, char) for char in text)
    return result, key

def monoalphabetic_decrypt(text: str, key: Dict[str, str]) -> str:
    """Decrypt using provided substitution key"""
    reverse_key = {v: k for k, v in key.items()}
    return ''.join(reverse_key.get(char, char) for char in text)

def get_frequency_order(text: str) -> str:
    """Get the frequency order of letters in the text"""
    text = ''.join(c.lower() for c in text if c.isalpha())
    frequencies = Counter(text)
    sorted_chars = sorted(frequencies.items(), key=lambda x: (-x[1], x[0]))
    return ''.join(char for char, _ in sorted_chars)

def try_common_mappings(ciphertext: str) -> List[dict]:
    """Try to decrypt using common English letter frequencies"""
    cipher_freq = get_frequency_order(ciphertext)
    results = []
    
    # Try mapping most frequent letters to common English letters
    for i in range(min(len(cipher_freq), len(ENGLISH_FREQUENCIES))):
        mapping = {}
        # Map each cipher letter to corresponding frequency-based English letter
        for j in range(min(len(cipher_freq), len(ENGLISH_FREQUENCIES))):
            if j < len(cipher_freq):
                mapping[cipher_freq[j]] = ENGLISH_FREQUENCIES[j]
        
        # Create decryption attempt
        decrypted = ''.join(mapping.get(c.lower(), c) for c in ciphertext)
        results.append({
            "mapping": mapping,
            "decrypted": decrypted,
            "description": f"Mapping based on letter frequency (rotation {i})"
        })
        
        # Rotate English frequencies for next attempt
        ENGLISH_FREQUENCIES = ENGLISH_FREQUENCIES[1:] + ENGLISH_FREQUENCIES[0]
    
    return results

def monoalphabetic_attack(text: str) -> List[dict]:
    """Perform cryptanalysis attack on monoalphabetic cipher text"""
    results = []
    
    # Add frequency analysis
    cipher_freq = get_frequency_order(text)
    results.append({
        "description": "Letter frequencies in ciphertext",
        "frequencies": cipher_freq,
        "decrypted": text  # Original text for reference
    })
    
    # Try common English letter mappings
    results.extend(try_common_mappings(text))
    
    return results

# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "Welcome to the Cipher API",
        "endpoints": {
            "monoalphabetic": ["/monoalphabetic/encrypt", "/monoalphabetic/decrypt", "/monoalphabetic/attack"]
        }
    }

@app.post("/monoalphabetic/encrypt", response_model=CipherResponse)
async def api_monoalphabetic_encrypt(request: CipherRequest):
    """Encrypt text using monoalphabetic substitution cipher"""
    result, key = monoalphabetic_encrypt(request.text)
    key = {str(k): str(v) for k, v in key.items()}
    return CipherResponse(result=result, key=key)

@app.post("/monoalphabetic/decrypt", response_model=CipherResponse)
async def api_monoalphabetic_decrypt(request: DecryptRequest):
    """Decrypt text using monoalphabetic substitution cipher"""
    key = {str(k): str(v) for k, v in request.key.items()}
    result = monoalphabetic_decrypt(request.text, key)
    return CipherResponse(result=result, key=key)

@app.post("/monoalphabetic/attack", response_model=AttackResponse)
async def api_monoalphabetic_attack(request: AttackRequest):
    """Perform cryptanalysis attack on monoalphabetic cipher text"""
    results = monoalphabetic_attack(request.text)
    return AttackResponse(results=results)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 