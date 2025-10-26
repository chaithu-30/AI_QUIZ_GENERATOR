import React, { useState } from 'react';
import './App.css';
import GenerateQuizTab from './components/GenerateQuizTab';
import HistoryTab from './components/HistoryTab';

function App() {
  const [activeTab, setActiveTab] = useState('generate');

  return (
    <div className="App">
      <header className="app-header">
        <h1>🧠 AI Wiki Quiz Generator</h1>
        <p>Generate quizzes from Wikipedia articles using AI</p>
      </header>

      <div className="tabs">
        <button
          className={`tab-button ${activeTab === 'generate' ? 'active' : ''}`}
          onClick={() => setActiveTab('generate')}
        >
          Generate Quiz
        </button>
        <button
          className={`tab-button ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          Past Quizzes
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'generate' ? <GenerateQuizTab /> : <HistoryTab />}
      </div>
    </div>
  );
}

export default App;
