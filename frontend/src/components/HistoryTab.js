import React, { useState, useEffect } from 'react';
import { getQuizHistory, getQuizDetails } from '../services/api';
import QuizDisplay from './QuizDisplay';
import './HistoryTab.css';

function HistoryTab() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedQuiz, setSelectedQuiz] = useState(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const data = await getQuizHistory();
      setHistory(data);
    } catch (err) {
      setError(err.toString());
    } finally {
      setLoading(false);
    }
  };

  const handleViewDetails = async (quizId) => {
    try {
      const data = await getQuizDetails(quizId);
      setSelectedQuiz(data.full_quiz_data);
      setShowModal(true);
    } catch (err) {
      alert('Failed to load quiz details: ' + err);
    }
  };

  const closeModal = () => {
    setShowModal(false);
    setSelectedQuiz(null);
  };

  if (loading) return <div className="loading">Loading history...</div>;
  if (error) return <div className="error-message">❌ {error}</div>;

  return (
    <div className="history-tab">
      <h2>Past Quizzes</h2>
      {history.length === 0 ? (
        <p className="no-history">No quizzes generated yet. Create one in the Generate Quiz tab!</p>
      ) : (
        <table className="history-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>URL</th>
              <th>Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {history.map((quiz) => (
              <tr key={quiz.id}>
                <td>{quiz.id}</td>
                <td>{quiz.title}</td>
                <td className="url-cell">
                  <a href={quiz.url} target="_blank" rel="noopener noreferrer">
                    View Article
                  </a>
                </td>
                <td>{new Date(quiz.date_generated).toLocaleString()}</td>
                <td>
                  <button 
                    onClick={() => handleViewDetails(quiz.id)}
                    className="details-button"
                  >
                    View Details
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {showModal && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-button" onClick={closeModal}>✕</button>
            <QuizDisplay data={selectedQuiz} />
          </div>
        </div>
      )}
    </div>
  );
}

export default HistoryTab;
