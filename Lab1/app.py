from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from collections import Counter
import random
import string

app = FastAPI(
    title="Cipher API",
    description="API for Caesar and Monoalphabetic Cipher operations",
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
    shift: int = None  # Optional for monoalphabetic, required for Caesar

class DecryptRequest(BaseModel):
    text: str
    key: Dict[str, str] = None  # For monoalphabetic
    shift: int = None  # For Caesar

class CipherResponse(BaseModel):
    result: str
    key: Dict[str, str] = None  # For monoalphabetic

class AttackResponse(BaseModel):
    results: List[dict]

# Caesar Cipher Implementation
def caesar_encrypt(text: str, shift: int) -> str:
    result = ""
    for char in text:
        if char.isascii():  # Only encrypt ASCII characters
            # Convert to ASCII, apply shift, and wrap around 256
            ascii_val = ord(char)
            shifted = (ascii_val + shift) % 256
            result += chr(shifted)
        else:
            result += char  # Keep non-ASCII characters unchanged
    return result

def caesar_decrypt(text: str, shift: int) -> str:
    # For decryption, we use the negative of the shift value
    decrypt_shift = (256 - shift) % 256  # This ensures proper wrap-around
    return caesar_encrypt(text, decrypt_shift)

def caesar_attack(text: str) -> List[dict]:
    results = []
    # Try all possible shifts (0-255)
    for shift in range(256):
        decrypted = caesar_decrypt(text, shift)
        results.append({
            "shift": shift,
            "decrypted": decrypted,
            "description": f"Shift value: {shift}"
        })
    return results

# Monoalphabetic Cipher Implementation
def create_substitution_key() -> Dict[str, str]:
    """Create a random substitution key for printable characters"""
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

def monoalphabetic_attack(text: str) -> List[dict]:
    """Perform cryptanalysis attack on monoalphabetic cipher text"""
    results = []
    
    # Add frequency analysis
    cipher_freq = get_frequency_order(text)
    results.append({
        "description": "Letter frequencies in ciphertext",
        "frequencies": cipher_freq,
        "decrypted": text
    })
    
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
@app.post("/caesar/encrypt")
async def api_caesar_encrypt(request: CipherRequest):
    """Encrypt text using Caesar cipher"""
    if request.shift is None:
        raise HTTPException(status_code=400, detail="Shift value is required for Caesar cipher")
    if not 0 <= request.shift <= 255:
        raise HTTPException(status_code=400, detail="Shift must be between 0 and 255")
    result = caesar_encrypt(request.text, request.shift)
    return {"result": result}

@app.post("/caesar/decrypt")
async def api_caesar_decrypt(request: CipherRequest):
    """Decrypt text using Caesar cipher"""
    if request.shift is None:
        raise HTTPException(status_code=400, detail="Shift value is required for Caesar cipher")
    if not 0 <= request.shift <= 255:
        raise HTTPException(status_code=400, detail="Shift must be between 0 and 255")
    result = caesar_decrypt(request.text, request.shift)
    return {"result": result}

@app.post("/caesar/attack", response_model=AttackResponse)
async def api_caesar_attack(request: CipherRequest):
    """Perform brute force attack on Caesar cipher text"""
    results = caesar_attack(request.text)
    return AttackResponse(results=results)

# Monoalphabetic Cipher Endpoints
@app.post("/monoalphabetic/encrypt", response_model=CipherResponse)
async def api_monoalphabetic_encrypt(request: CipherRequest):
    """Encrypt text using monoalphabetic substitution cipher"""
    result, key = monoalphabetic_encrypt(request.text)
    key = {str(k): str(v) for k, v in key.items()}
    return CipherResponse(result=result, key=key)

@app.post("/monoalphabetic/decrypt", response_model=CipherResponse)
async def api_monoalphabetic_decrypt(request: DecryptRequest):
    """Decrypt text using monoalphabetic substitution cipher"""
    if not request.key:
        raise HTTPException(status_code=400, detail="Key is required for monoalphabetic decryption")
    key = {str(k): str(v) for k, v in request.key.items()}
    result = monoalphabetic_decrypt(request.text, key)
    return CipherResponse(result=result, key=key)

@app.post("/monoalphabetic/attack", response_model=AttackResponse)
async def api_monoalphabetic_attack(request: CipherRequest):
    """Perform cryptanalysis attack on monoalphabetic cipher text"""
    results = monoalphabetic_attack(request.text)
    return AttackResponse(results=results)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 