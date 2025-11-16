import React, { useState } from 'react';
import { generateQuiz } from '../services/api';
import QuizDisplay from '../components/QuizDisplay';
import LoadingSpinner from '../components/LoadingSpinner';
import Modal from '../components/Modal';
import TakeQuizMode from '../components/TakeQuizMode';

function GenerateQuizTab() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [quizData, setQuizData] = useState(null);
  const [showTakeQuiz, setShowTakeQuiz] = useState(false);

  const validateUrl = (url) => {
    const pattern = /^https:\/\/en\.wikipedia\.org\/wiki\/.+$/;
    return pattern.test(url);
  };

  const handleGenerate = async (e) => {
    e.preventDefault();
    
    // Validation
    if (!url.trim()) {
      setError('Please enter a Wikipedia URL');
      return;
    }
    
    if (!validateUrl(url)) {
      setError('Please enter a valid English Wikipedia article URL (https://en.wikipedia.org/wiki/...)');
      return;
    }

    setError(null);
    setLoading(true);
    setQuizData(null);

    try {
      const data = await generateQuiz(url, false);
      setQuizData(data);
      setError(null);
    } catch (err) {
      setError(err.toString());
      setQuizData(null);
    } finally {
      setLoading(false);
    }
  };

  const handleTakeQuiz = () => {
    setShowTakeQuiz(true);
  };

  const closeTakeQuizModal = () => {
    setShowTakeQuiz(false);
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Input Section */}
      <div className="card mb-8 animate-fade-in">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
          <svg className="w-8 h-8 mr-3 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
          Generate AI-Powered Quiz
        </h2>
        
        <form onSubmit={handleGenerate} className="space-y-4">
          <div>
            <label htmlFor="url" className="block text-sm font-semibold text-gray-700 mb-2">
              Wikipedia Article URL
            </label>
            <input
              id="url"
              type="text"
              className="input-field"
              placeholder="https://en.wikipedia.org/wiki/Python_(programming_language)"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              disabled={loading}
            />
            <p className="mt-2 text-sm text-gray-500 flex items-start">
              <svg className="w-4 h-4 mr-1 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Enter any English Wikipedia article URL to generate a quiz. The AI will create 7-10 questions based on the article content.
            </p>
          </div>

          {/* Example URLs */}
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm font-medium text-gray-700 mb-2">Try these examples:</p>
            <div className="flex flex-wrap gap-2">
              {[
                { text: 'Python', url: 'https://en.wikipedia.org/wiki/Python_(programming_language)' },
                { text: 'AI', url: 'https://en.wikipedia.org/wiki/Artificial_intelligence' },
                { text: 'Einstein', url: 'https://en.wikipedia.org/wiki/Albert_Einstein' },
              ].map((example, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => setUrl(example.url)}
                  className="text-sm px-3 py-1 bg-white border border-gray-300 rounded-full hover:border-purple-500 hover:text-purple-600 transition-colors"
                  disabled={loading}
                >
                  {example.text}
                </button>
              ))}
            </div>
          </div>

          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded animate-fade-in">
              <div className="flex">
                <svg className="w-5 h-5 text-red-500 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div>
                  <p className="text-sm font-medium text-red-800">{error}</p>
                </div>
              </div>
            </div>
          )}

          <button
            type="submit"
            className="btn-primary w-full"
            disabled={loading}
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Generating Quiz...
              </span>
            ) : (
              <span className="flex items-center justify-center">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                Generate Quiz
              </span>
            )}
          </button>
        </form>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="animate-fade-in">
          <LoadingSpinner message="Generating your quiz..." />
          <div className="card mt-6 bg-blue-50 border-blue-200">
            <div className="flex items-start">
              <svg className="w-6 h-6 text-blue-600 mr-3 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <p className="text-sm font-medium text-blue-900 mb-1">What's happening?</p>
                <ul className="text-sm text-blue-800 space-y-1">
                  <li>• Scraping Wikipedia article content</li>
                  <li>• Analyzing article with Google Gemini AI</li>
                  <li>• Generating questions, answers, and explanations</li>
                  <li>• Extracting key entities and related topics</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Quiz Display */}
      {quizData && !loading && (
        <div className="space-y-6 animate-slide-up">
          {/* Success Message */}
          <div className="card bg-green-50 border-green-200">
            <div className="flex justify-between items-start">
              <div className="flex items-start">
                <svg className="w-6 h-6 text-green-600 mr-3 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div>
                  <h3 className="text-lg font-bold text-green-900 mb-1">Quiz Generated Successfully!</h3>
                  <p className="text-sm text-green-800">
                    Created {quizData.quiz?.length || 0} questions • 
                    {quizData.key_entities?.people?.length || 0} people • 
                    {quizData.key_entities?.organizations?.length || 0} organizations • 
                    {quizData.related_topics?.length || 0} related topics
                  </p>
                </div>
              </div>
              {quizData.cached && (
                <span className="badge bg-yellow-100 text-yellow-800 flex items-center">
                  <svg className="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
                  </svg>
                  Cached
                </span>
              )}
            </div>
          </div>

          {/* Main Quiz Display Card */}
          <div className="card">
            <QuizDisplay data={quizData} />
          </div>

          {/* Action Buttons */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Take Quiz Button */}
            <button
              onClick={handleTakeQuiz}
              className="btn-primary flex items-center justify-center py-4"
            >
              <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="text-lg font-semibold">Take This Quiz</span>
            </button>

            {/* Generate Another Button */}
            <button
              onClick={() => {
                setUrl('');
                setQuizData(null);
                setError(null);
              }}
              className="btn-secondary flex items-center justify-center py-4"
            >
              <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <span className="text-lg font-semibold">Generate Another Quiz</span>
            </button>
          </div>

          {/* Stats Card */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="card text-center">
              <div className="text-3xl font-bold text-purple-600 mb-1">
                {quizData.quiz?.length || 0}
              </div>
              <div className="text-sm text-gray-600">Questions</div>
            </div>
            <div className="card text-center">
              <div className="text-3xl font-bold text-blue-600 mb-1">
                {quizData.quiz?.filter(q => q.difficulty === 'easy').length || 0}
              </div>
              <div className="text-sm text-gray-600">Easy</div>
            </div>
            <div className="card text-center">
              <div className="text-3xl font-bold text-yellow-600 mb-1">
                {quizData.quiz?.filter(q => q.difficulty === 'medium').length || 0}
              </div>
              <div className="text-sm text-gray-600">Medium</div>
            </div>
            <div className="card text-center">
              <div className="text-3xl font-bold text-red-600 mb-1">
                {quizData.quiz?.filter(q => q.difficulty === 'hard').length || 0}
              </div>
              <div className="text-sm text-gray-600">Hard</div>
            </div>
          </div>
        </div>
      )}

      {/* Take Quiz Modal */}
      {showTakeQuiz && quizData && (
        <Modal
          isOpen={showTakeQuiz}
          onClose={closeTakeQuizModal}
          title={`Take Quiz: ${quizData.title}`}
        >
          <TakeQuizMode quizData={quizData} onClose={closeTakeQuizModal} />
        </Modal>
      )}
    </div>
  );
}

export default GenerateQuizTab;
