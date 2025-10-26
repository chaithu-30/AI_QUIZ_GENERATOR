import React from 'react';
import './QuizDisplay.css';

function QuizDisplay({ data }) {
  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'easy': return '#4caf50';
      case 'medium': return '#ff9800';
      case 'hard': return '#f44336';
      default: return '#666';
    }
  };

  return (
    <div className="quiz-display">
      <div className="quiz-header">
        <h2>{data.title}</h2>
        <p className="summary">{data.summary}</p>
      </div>

      {data.key_entities && (
        <div className="key-entities">
          <h3>Key Entities</h3>
          <div className="entities-grid">
            {data.key_entities.people?.length > 0 && (
              <div className="entity-group">
                <strong>People:</strong>
                {data.key_entities.people.map((p, i) => (
                  <span key={i} className="entity-chip">{p}</span>
                ))}
              </div>
            )}
            {data.key_entities.organizations?.length > 0 && (
              <div className="entity-group">
                <strong>Organizations:</strong>
                {data.key_entities.organizations.map((o, i) => (
                  <span key={i} className="entity-chip">{o}</span>
                ))}
              </div>
            )}
            {data.key_entities.locations?.length > 0 && (
              <div className="entity-group">
                <strong>Locations:</strong>
                {data.key_entities.locations.map((l, i) => (
                  <span key={i} className="entity-chip">{l}</span>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      <div className="quiz-section">
        <h3>Quiz Questions ({data.quiz?.length || 0})</h3>
        {data.quiz?.map((q, index) => (
          <div key={index} className="question-card">
            <div className="question-header">
              <span className="question-number">Question {index + 1}</span>
              <span 
                className="difficulty-badge"
                style={{ backgroundColor: getDifficultyColor(q.difficulty) }}
              >
                {q.difficulty}
              </span>
            </div>
            <p className="question-text">{q.question}</p>
         <div className="options">
  {q.options?.map((option, i) => (
    <div key={i} className="option">
      <span className="option-letter">{String.fromCharCode(65 + i)}.</span> {option.slice(3)}
    </div>
  ))}
</div>

            <div className="answer-section">
              <strong>Answer:</strong> {q.answer}
              <p className="explanation">{q.explanation}</p>
            </div>
          </div>
        ))}
      </div>

      {data.related_topics?.length > 0 && (
        <div className="related-topics">
          <h3>Related Topics</h3>
          <div className="topics-list">
            {data.related_topics.map((topic, i) => (
              <span key={i} className="topic-chip">{topic}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default QuizDisplay;
