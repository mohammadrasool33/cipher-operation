# Cipher API

A simple REST API implementing Caesar and Monoalphabetic ciphers with encryption, decryption, and attack capabilities.

## Setup and Installation

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Run the API server:

```bash
uvicorn app:app --reload
```

The API will be running at `http://localhost:8000`

## API Endpoints

### Caesar Cipher

1. **Encrypt Text**

   - Endpoint: `POST /caesar/encrypt`
   - Request Body:
     ```json
     {
       "text": "Hello World",
       "shift": 3
     }
     ```

2. **Decrypt Text**

   - Endpoint: `POST /caesar/decrypt`
   - Request Body:
     ```json
     {
       "text": "Khoor Zruog",
       "shift": 3
     }
     ```

3. **Brute Force Attack**
   - Endpoint: `POST /caesar/attack`
   - Request Body:
     ```json
     {
       "text": "Khoor Zruog"
     }
     ```

### Monoalphabetic Cipher

1. **Encrypt Text**

   - Endpoint: `POST /monoalphabetic/encrypt`
   - Request Body:
     ```json
     {
       "text": "Hello World",
       "shift": 3
     }
     ```

2. **Decrypt Text**
   - Endpoint: `POST /monoalphabetic/decrypt`
   - Request Body:
     ```json
     {
       "text": "Khoor Zruog",
       "shift": 3
     }
     ```

## Example Usage

Using curl:

```bash
# Caesar Cipher Encryption
curl -X POST "http://localhost:8000/caesar/encrypt" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello World", "shift": 3}'

# Caesar Cipher Decryption
curl -X POST "http://localhost:8000/caesar/decrypt" \
     -H "Content-Type: application/json" \
     -d '{"text": "Khoor Zruog", "shift": 3}'

# Caesar Cipher Attack
curl -X POST "http://localhost:8000/caesar/attack" \
     -H "Content-Type: application/json" \
     -d '{"text": "Khoor Zruog"}'
```

Using Python requests:

```python
import requests

url = "http://localhost:8000/caesar/encrypt"
data = {
    "text": "Hello World",
    "shift": 3
}

response = requests.post(url, json=data)
print(response.json())
```

## API Documentation

Interactive API documentation is available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Implementation Details

1. **Caesar Cipher**

   - Works with alphabetic characters (A-Z, a-z)
   - Preserves case (uppercase/lowercase)
   - Maintains non-alphabetic characters unchanged
   - Shift values between 0-25

2. **Monoalphabetic Cipher**
   - Uses substitution alphabet based on shift
   - Preserves case (uppercase/lowercase)
   - Maintains non-alphabetic characters unchanged
   - Shift values between 0-25

# Cipher API Setup Instructions

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Setup Steps

1. **Create and activate a virtual environment (recommended)**:

   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   uvicorn app:app --reload
   ```

The API will be available at: `http://localhost:8000`

## Testing the API

You can test the API in several ways:

1. **Using the Swagger UI**:

   - Open `http://localhost:8000/docs` in your browser
   - Try out any endpoint directly from the browser

2. **Using Postman**:

   - Import the following endpoints:
     - POST `/caesar/encrypt`
     - POST `/caesar/decrypt`
     - POST `/caesar/attack`
     - POST `/monoalphabetic/encrypt`
     - POST `/monoalphabetic/decrypt`
     - POST `/monoalphabetic/attack`

3. **Using curl**:
   ```bash
   # Example: Caesar Cipher Encryption
   curl -X POST "http://localhost:8000/caesar/encrypt" \
        -H "Content-Type: application/json" \
        -d '{"text": "Hello World", "shift": 3}'
   ```

## Common Issues

1. **Port already in use**:

   - If port 8000 is already in use, you can specify a different port:

   ```bash
   uvicorn app:app --reload --port 8001
   ```

2. **Module not found errors**:

   - Make sure you've activated the virtual environment
   - Try reinstalling dependencies: `pip install -r requirements.txt`

3. **Permission errors**:
   - On Unix-like systems, you might need to use `python3` instead of `python`
   - You might need to run commands with `sudo` (though this is not recommended)
