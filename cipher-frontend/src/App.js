import React, { useState } from 'react';
import './App.css';
import CaesarCipher from './components/CaesarCipher';
import MonoalphabeticCipher from './components/MonoalphabeticCipher';

function App() {
  const [activeTab, setActiveTab] = useState('caesar');

  return (
    <div className="App">
      <header className="App-header">
        <h1>Cipher Operations</h1>
        <div className="tab-buttons">
          <button 
            className={activeTab === 'caesar' ? 'active' : ''} 
            onClick={() => setActiveTab('caesar')}
          >
            Caesar Cipher
          </button>
          <button 
            className={activeTab === 'monoalphabetic' ? 'active' : ''} 
            onClick={() => setActiveTab('monoalphabetic')}
          >
            Monoalphabetic Cipher
          </button>
        </div>
      </header>
      <main>
        {activeTab === 'caesar' ? (
          <CaesarCipher />
        ) : (
          <MonoalphabeticCipher />
        )}
      </main>
    </div>
  );
}

export default App; 