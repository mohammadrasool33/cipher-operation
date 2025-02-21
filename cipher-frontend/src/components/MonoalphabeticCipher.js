import React, { useState } from 'react';
import './CipherStyles.css';

function MonoalphabeticCipher() {
  const [text, setText] = useState('');
  const [shift, setShift] = useState(3);
  const [result, setResult] = useState('');
  const [attackResults, setAttackResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleEncrypt = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/monoalphabetic/encrypt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, shift }),
      });
      const data = await response.json();
      setResult(data.result);
      setAttackResults([]);
    } catch (error) {
      console.error('Error:', error);
      setResult('Error occurred while encrypting');
    }
    setLoading(false);
  };

  const handleDecrypt = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/monoalphabetic/decrypt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, shift }),
      });
      const data = await response.json();
      setResult(data.result);
      setAttackResults([]);
    } catch (error) {
      console.error('Error:', error);
      setResult('Error occurred while decrypting');
    }
    setLoading(false);
  };

  const handleAttack = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/monoalphabetic/attack', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });
      const data = await response.json();
      setAttackResults(data.results);
      setResult('');
    } catch (error) {
      console.error('Error:', error);
      setAttackResults([]);
      setResult('Error occurred during attack');
    }
    setLoading(false);
  };

  return (
    <div className="cipher-container">
      <h2>Monoalphabetic Cipher</h2>
      
      <div className="input-group">
        <label>
          Text:
          <input
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter text..."
          />
        </label>
      </div>

      <div className="input-group">
        <label>
          Shift (0-25):
          <input
            type="number"
            min="0"
            max="25"
            value={shift}
            onChange={(e) => setShift(parseInt(e.target.value))}
          />
        </label>
      </div>

      <div className="button-group">
        <button onClick={handleEncrypt} disabled={loading}>
          Encrypt
        </button>
        <button onClick={handleDecrypt} disabled={loading}>
          Decrypt
        </button>
        <button onClick={handleAttack} disabled={loading}>
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
                <strong>Shift {result.shift}</strong> 
                <span className="score">(Score: {result.likelihood_score})</span>: 
                {result.plaintext}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default MonoalphabeticCipher; 