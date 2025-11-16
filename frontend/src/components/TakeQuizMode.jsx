import React, { useState } from 'react';

function TakeQuizMode({ quizData }) {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);
  const [score, setScore] = useState(0);

  const handleAnswer = (questionIndex, answer) => {
    setSelectedAnswers({
      ...selectedAnswers,
      [questionIndex]: answer
    });
  };

  const handleSubmit = () => {
    let correctCount = 0;
    quizData.quiz.forEach((q, idx) => {
      if (selectedAnswers[idx] === q.answer) {
        correctCount++;
      }
    });
    setScore(correctCount);
    setShowResults(true);
  };

  const resetQuiz = () => {
    setSelectedAnswers({});
    setShowResults(false);
    setCurrentQuestion(0);
    setScore(0);
  };

  if (showResults) {
    const percentage = Math.round((score / quizData.quiz.length) * 100);
    return (
      <div className="card text-center py-12">
        <div className="mb-6">
          <div className="text-6xl font-bold text-purple-600 mb-4">
            {percentage}%
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">
            Quiz Complete!
          </h3>
          <p className="text-lg text-gray-600">
            You scored {score} out of {quizData.quiz.length} questions
          </p>
        </div>

        <div className="space-y-4 max-w-2xl mx-auto text-left mb-8">
          {quizData.quiz.map((q, idx) => {
            const isCorrect = selectedAnswers[idx] === q.answer;
            return (
              <div key={idx} className={`p-4 rounded-lg border-2 ${
                isCorrect ? 'border-green-500 bg-green-50' : 'border-red-500 bg-red-50'
              }`}>
                <div className="flex items-start">
                  <span className="text-2xl mr-3">
                    {isCorrect ? '✓' : '✗'}
                  </span>
                  <div className="flex-1">
                    <p className="font-semibold text-gray-900 mb-2">{q.question}</p>
                    <p className="text-sm">
                      <span className="font-medium">Your answer:</span>{' '}
                      <span className={isCorrect ? 'text-green-700' : 'text-red-700'}>
                        {selectedAnswers[idx] || 'Not answered'}
                      </span>
                    </p>
                    {!isCorrect && (
                      <p className="text-sm mt-1">
                        <span className="font-medium">Correct answer:</span>{' '}
                        <span className="text-green-700">{q.answer}</span>
                      </p>
                    )}
                    <p className="text-sm text-gray-600 mt-2">{q.explanation}</p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        <button onClick={resetQuiz} className="btn-primary">
          Retake Quiz
        </button>
      </div>
    );
  }

  const currentQ = quizData.quiz[currentQuestion];

  return (
    <div className="card">
      {/* Progress Bar */}
      <div className="mb-6">
        <div className="flex justify-between text-sm text-gray-600 mb-2">
          <span>Question {currentQuestion + 1} of {quizData.quiz.length}</span>
          <span>{Math.round(((currentQuestion + 1) / quizData.quiz.length) * 100)}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-gradient-to-r from-purple-600 to-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${((currentQuestion + 1) / quizData.quiz.length) * 100}%` }}
          ></div>
        </div>
      </div>

      {/* Question */}
      <div className="mb-8">
        <div className="flex justify-between items-start mb-4">
          <h3 className="text-2xl font-bold text-gray-900 flex-1">
            {currentQ.question}
          </h3>
          <span className={`badge ${
            currentQ.difficulty === 'easy' ? 'badge-easy' :
            currentQ.difficulty === 'medium' ? 'badge-medium' : 'badge-hard'
          }`}>
            {currentQ.difficulty}
          </span>
        </div>

        {/* Options */}
        <div className="space-y-3">
          {currentQ.options.map((option, idx) => (
            <button
              key={idx}
              onClick={() => handleAnswer(currentQuestion, option)}
              className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                selectedAnswers[currentQuestion] === option
                  ? 'border-purple-600 bg-purple-50 shadow-md'
                  : 'border-gray-300 hover:border-purple-300 hover:bg-gray-50'
              }`}
            >
              <span className="font-semibold text-gray-700 mr-2">
                {String.fromCharCode(65 + idx)}.
              </span>
              <span className="text-gray-900">{option}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Navigation */}
      <div className="flex justify-between items-center">
        <button
          onClick={() => setCurrentQuestion(Math.max(0, currentQuestion - 1))}
          disabled={currentQuestion === 0}
          className="btn-secondary disabled:opacity-50"
        >
          ← Previous
        </button>

        {currentQuestion === quizData.quiz.length - 1 ? (
          <button
            onClick={handleSubmit}
            disabled={Object.keys(selectedAnswers).length !== quizData.quiz.length}
            className="btn-primary disabled:opacity-50"
          >
            Submit Quiz
          </button>
        ) : (
          <button
            onClick={() => setCurrentQuestion(Math.min(quizData.quiz.length - 1, currentQuestion + 1))}
            className="btn-primary"
          >
            Next →
          </button>
        )}
      </div>

      {/* Answer Count */}
      <div className="mt-6 text-center text-sm text-gray-600">
        Answered: {Object.keys(selectedAnswers).length} / {quizData.quiz.length}
      </div>
    </div>
  );
}

export default TakeQuizMode;
