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
        # Convert to ASCII, apply shift, and wrap around 256
        ascii_val = ord(char)
        shifted = (ascii_val + shift) % 256
        result += chr(shifted)
    return result

def caesar_decrypt(text: str, shift: int) -> str:
    return caesar_encrypt(text, -shift)

def caesar_attack(text: str) -> List[dict]:
    results = []
    # Try all possible shifts (0-255)
    for shift in range(256):
        decrypted = caesar_decrypt(text, shift)
        results.append({
            "shift": shift,
            "plaintext": decrypted
        })
    return results

# Monoalphabetic Cipher Implementation
def create_substitution_key(shift: int) -> Dict[str, str]:
    substitution = {}
    # Create mapping for all ASCII characters (0-255)
    for i in range(256):
        original = chr(i)
        substituted = chr((i + shift) % 256)
        substitution[original] = substituted
    return substitution

def monoalphabetic_encrypt(text: str, shift: int) -> str:
    key = create_substitution_key(shift)
    return ''.join(key[char] for char in text)

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
    
    # Try all possible shifts (0-255)
    for shift in range(256):
        decrypted = monoalphabetic_decrypt(text, shift)
        
        # Add the result with its shift value
        results.append({
            "shift": shift,
            "plaintext": decrypted
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
@app.post("/caesar/encrypt", response_model=CipherResponse)
async def api_caesar_encrypt(request: CipherRequest):
    """Encrypt text using Caesar cipher"""
    if not 0 <= request.shift <= 255:
        raise HTTPException(status_code=400, detail="Shift must be between 0 and 255")
    result = caesar_encrypt(request.text, request.shift)
    return CipherResponse(result=result)

@app.post("/caesar/decrypt", response_model=CipherResponse)
async def api_caesar_decrypt(request: CipherRequest):
    """Decrypt text using Caesar cipher"""
    if not 0 <= request.shift <= 255:
        raise HTTPException(status_code=400, detail="Shift must be between 0 and 255")
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
    if not 0 <= request.shift <= 255:
        raise HTTPException(status_code=400, detail="Shift must be between 0 and 255")
    result = monoalphabetic_encrypt(request.text, request.shift)
    return CipherResponse(result=result)

@app.post("/monoalphabetic/decrypt", response_model=CipherResponse)
async def api_monoalphabetic_decrypt(request: CipherRequest):
    """Decrypt text using Monoalphabetic cipher"""
    if not 0 <= request.shift <= 255:
        raise HTTPException(status_code=400, detail="Shift must be between 0 and 255")
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