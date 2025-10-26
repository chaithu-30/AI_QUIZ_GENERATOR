import React, { useState } from 'react';
import { generateQuiz } from '../services/api';
import QuizDisplay from './QuizDisplay';
import './GenerateQuizTab.css';

function GenerateQuizTab() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [quizData, setQuizData] = useState(null);
  const [cacheMessage, setCacheMessage] = useState(null);

const handleSubmit = async (e) => {
  e.preventDefault();
  
  if (!url.startsWith('https://en.wikipedia.org/wiki/')) {
    setError('Please enter a valid Wikipedia URL');
    return;
  }

  setLoading(true);
  setError(null);
  setQuizData(null);
  setCacheMessage(null);

  try {
    const data = await generateQuiz(url);
    
    if (data.cached && data.message) {
      setCacheMessage(data.message);
    }

    setQuizData(data.full_quiz_data);
  } catch (err) {
    setError(err.toString());
  } finally {
    setLoading(false);
  }
};


  return (
    <div className="generate-quiz-tab">
      <form onSubmit={handleSubmit} className="url-form">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://en.wikipedia.org/wiki/Alan_Turing"
          className="url-input"
          disabled={loading}
        />
        <button type="submit" disabled={loading} className="generate-button">
          {loading ? 'Generating...' : 'Generate Quiz'}
        </button>
      </form>

      {error && <div className="error-message">❌ {error}</div>}

      {loading && (
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Scraping Wikipedia and generating quiz with AI...</p>
        </div>
      )}

      {quizData && <QuizDisplay data={quizData} />}
    </div>
  );
}

export default GenerateQuizTab;
