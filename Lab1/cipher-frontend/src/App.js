import React, { useState } from 'react';
import './App.css';
import CaesarCipher from './components/CaesarCipher';
import MonoalphabeticCipher from './components/MonoalphabeticCipher';

function App() {
  const [activeCipher, setActiveCipher] = useState('caesar');

  return (
    <div className="App">
      <header className="App-header">
        <h1>Cipher Operations</h1>
        <div className="cipher-selector">
          <button 
            className={activeCipher === 'caesar' ? 'active' : ''} 
            onClick={() => setActiveCipher('caesar')}
          >
            Caesar Cipher
          </button>
          <button 
            className={activeCipher === 'monoalphabetic' ? 'active' : ''} 
            onClick={() => setActiveCipher('monoalphabetic')}
          >
            Monoalphabetic Cipher
          </button>
        </div>
      </header>
      <main>
        {activeCipher === 'caesar' ? <CaesarCipher /> : <MonoalphabeticCipher />}
      </main>
    </div>
  );
}

export default App; 