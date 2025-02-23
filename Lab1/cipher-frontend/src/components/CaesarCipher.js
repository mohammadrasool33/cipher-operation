import React, { useState } from 'react';
import './CipherStyles.css';

function CaesarCipher() {
  const [text, setText] = useState('');
  const [shift, setShift] = useState(3);
  const [result, setResult] = useState('');
  const [attackResults, setAttackResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  const validateInputs = (isAttack = false) => {
    const newErrors = {};

    // Validate text
    if (!text.trim()) {
      newErrors.text = 'Text is required';
    } else if (text.length > 500) {
      newErrors.text = 'Text must be less than 500 characters';
    }

    // Validate shift (not needed for attack)
    if (!isAttack) {
      const shiftNum = parseInt(shift);
      if (shift === '' || isNaN(shiftNum)) {
        newErrors.shift = 'Shift value is required';
      } else if (shiftNum < 0 || shiftNum > 255) {
        newErrors.shift = 'Shift must be between 0 and 255';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleEncrypt = async () => {
    if (!validateInputs()) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/caesar/encrypt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text: text, 
          shift: parseInt(shift)
        }),
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Server error');
      }

      const data = await response.json();
      setResult(data.result);
      setAttackResults([]);
      setErrors({});
    } catch (error) {
      console.error('Error:', error);
      setErrors({ submit: error.message || 'Failed to encrypt text. Please try again.' });
    }
    setLoading(false);
  };

  const handleDecrypt = async () => {
    if (!validateInputs()) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/caesar/decrypt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text: text, 
          shift: parseInt(shift)
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Server error');
      }

      const data = await response.json();
      setResult(data.result);
      setAttackResults([]);
      setErrors({});
    } catch (error) {
      console.error('Error:', error);
      setErrors({ submit: error.message || 'Failed to decrypt text. Please try again.' });
    }
    setLoading(false);
  };

  const handleAttack = async () => {
    if (!validateInputs(true)) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/caesar/attack', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error('Server error');
      }

      const data = await response.json();
      setAttackResults(data.results);
      setResult('');
      setErrors({});
    } catch (error) {
      console.error('Error:', error);
      setErrors({ submit: 'Failed to perform attack. Please try again.' });
    }
    setLoading(false);
  };

  return (
    <div className="cipher-container">
      <h2>Caesar Cipher</h2>
      
      <div className={`input-group ${errors.text ? 'error' : ''}`}>
        <label>
          Text:
          <input
            type="text"
            value={text}
            onChange={(e) => {
              setText(e.target.value);
              setErrors({ ...errors, text: '', submit: '' });
            }}
            placeholder="Enter text..."
            className={errors.text ? 'error' : ''}
          />
        </label>
        {errors.text && <div className="error-message">{errors.text}</div>}
      </div>

      <div className={`input-group ${errors.shift ? 'error' : ''}`}>
        <label>
          Shift (0-255):
          <input
            type="number"
            min="0"
            max="255"
            value={shift}
            onChange={(e) => {
              const value = e.target.value;
              const numValue = parseInt(value);
              
              if (value === '') {
                setShift('');
                setErrors({ ...errors, shift: 'Shift value is required' });
              } else if (!isNaN(numValue)) {
                setShift(numValue);
                if (numValue >= 0 && numValue <= 255) {
                  setErrors({ ...errors, shift: '', submit: '' });
                } else {
                  setErrors({ ...errors, shift: 'Shift must be between 0 and 255' });
                }
              }
            }}
            className={errors.shift ? 'error' : ''}
          />
        </label>
        {errors.shift && <div className="error-message">{errors.shift}</div>}
      </div>

      {errors.submit && <div className="error-message submit-error">{errors.submit}</div>}

      <div className="button-group">
        <button 
          onClick={handleEncrypt} 
          disabled={loading || !text.trim() || errors.shift || shift === '' || parseInt(shift) < 0 || parseInt(shift) > 255}
        >
          Encrypt
        </button>
        <button 
          onClick={handleDecrypt} 
          disabled={loading || !text.trim() || errors.shift || shift === '' || parseInt(shift) < 0 || parseInt(shift) > 255}
        >
          Decrypt
        </button>
        <button 
          onClick={handleAttack} 
          disabled={loading || !text.trim()}
        >
          Attack
        </button>
      </div>

      {loading && <div className="loading">Processing...</div>}

      {result && (
        <div className="result">
          <h3>Result:</h3>
          <p>{result}</p>
        </div>
      )}

      {attackResults.length > 0 && (
        <div className="attack-results">
          <h3>Attack Results:</h3>
          <div className="results-container">
            {attackResults.map((result, index) => (
              <div key={index} className="result-item">
                <h4>{result.description}</h4>
                <p><strong>Decrypted Text:</strong> {result.decrypted}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default CaesarCipher; 