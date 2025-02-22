import React, { useState } from 'react';
import './CipherStyles.css';

function MonoalphabeticCipher() {
  const [text, setText] = useState('');
  const [result, setResult] = useState('');
  const [currentKey, setCurrentKey] = useState(null);
  const [attackResults, setAttackResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  const validateInputs = () => {
    const newErrors = {};

    // Validate text
    if (!text.trim()) {
      newErrors.text = 'Text is required';
    } else if (text.length > 500) {
      newErrors.text = 'Text must be less than 500 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleEncrypt = async () => {
    if (!validateInputs()) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/monoalphabetic/encrypt', {
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
      setResult(data.result);
      setCurrentKey(data.key);
      setAttackResults([]);
      setErrors({});
    } catch (error) {
      console.error('Error:', error);
      setErrors({ submit: 'Failed to encrypt text. Please try again.' });
    }
    setLoading(false);
  };

  const handleDecrypt = async () => {
    if (!validateInputs()) return;
    if (!currentKey) {
      setErrors({ submit: 'No encryption key available. Please encrypt some text first.' });
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/monoalphabetic/decrypt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          key: currentKey
        }),
      });

      if (!response.ok) {
        throw new Error('Server error');
      }

      const data = await response.json();
      setResult(data.result);
      setAttackResults([]);
      setErrors({});
    } catch (error) {
      console.error('Error:', error);
      setErrors({ submit: 'Failed to decrypt text. Please try again.' });
    }
    setLoading(false);
  };

  const handleAttack = async () => {
    if (!validateInputs()) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/monoalphabetic/attack', {
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
      <h2>Monoalphabetic Cipher (Random Substitution)</h2>
      
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

      {errors.submit && <div className="error-message submit-error">{errors.submit}</div>}

      <div className="button-group">
        <button 
          onClick={handleEncrypt} 
          disabled={loading || !text.trim()}
        >
          Encrypt
        </button>
        <button 
          onClick={handleDecrypt} 
          disabled={loading || !text.trim() || !currentKey}
        >
          Decrypt
        </button>
        <button 
          onClick={handleAttack} 
          disabled={loading || !text.trim()}
        >
          Analyze
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
                {result.frequencies && (
                  <p><strong>Frequency Analysis:</strong> {result.frequencies}</p>
                )}
                {result.mapping && (
                  <div>
                    <p><strong>Letter Mappings:</strong></p>
                    <pre>{JSON.stringify(result.mapping, null, 2)}</pre>
                  </div>
                )}
                {result.decrypted && (
                  <p><strong>Decrypted Attempt:</strong> {result.decrypted}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {currentKey && (
        <div className="key-info">
          <h3>Current Encryption Key:</h3>
          <p className="key-note">This key is needed for decryption. A new random key is generated for each encryption.</p>
          <div className="key-sample">
            <p>Sample of key mappings:</p>
            <pre>{JSON.stringify(Object.fromEntries(
              Object.entries(currentKey).slice(0, 5)
            ), null, 2)}</pre>
          </div>
        </div>
      )}
    </div>
  );
}

export default MonoalphabeticCipher; 