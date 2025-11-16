import React from 'react';

function QuizDisplay({ data }) {
  const getDifficultyClass = (difficulty) => {
    const classes = {
      easy: 'badge-easy',
      medium: 'badge-medium',
      hard: 'badge-hard'
    };
    return `badge ${classes[difficulty] || 'badge-easy'}`;
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header Section */}
      <div className="border-b border-gray-200 pb-6">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">{data.title}</h2>
        <p className="text-lg text-gray-700 leading-relaxed">{data.summary}</p>
      </div>

      {/* Key Entities */}
      {data.key_entities && (
        <div className="card bg-gradient-to-br from-purple-50 to-blue-50">
          <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
            <svg className="w-6 h-6 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
            Key Entities
          </h3>
          <div className="space-y-3">
            {data.key_entities.people?.length > 0 && (
              <div>
                <span className="font-semibold text-purple-700 mr-2">People:</span>
                <div className="flex flex-wrap gap-2 mt-1">
                  {data.key_entities.people.map((person, idx) => (
                    <span key={idx} className="badge bg-purple-100 text-purple-800">{person}</span>
                  ))}
                </div>
              </div>
            )}
            {data.key_entities.organizations?.length > 0 && (
              <div>
                <span className="font-semibold text-blue-700 mr-2">Organizations:</span>
                <div className="flex flex-wrap gap-2 mt-1">
                  {data.key_entities.organizations.map((org, idx) => (
                    <span key={idx} className="badge bg-blue-100 text-blue-800">{org}</span>
                  ))}
                </div>
              </div>
            )}
            {data.key_entities.locations?.length > 0 && (
              <div>
                <span className="font-semibold text-green-700 mr-2">Locations:</span>
                <div className="flex flex-wrap gap-2 mt-1">
                  {data.key_entities.locations.map((loc, idx) => (
                    <span key={idx} className="badge bg-green-100 text-green-800">{loc}</span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Quiz Questions */}
      <div>
        <h3 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
          <svg className="w-7 h-7 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Quiz Questions ({data.quiz?.length || 0})
        </h3>
        
        <div className="space-y-4">
          {data.quiz?.map((q, index) => (
            <div key={index} className="card hover:scale-[1.01] transition-transform">
              <div className="flex justify-between items-start mb-3">
                <h4 className="text-lg font-semibold text-gray-900 flex-1">
                  {index + 1}. {q.question}
                </h4>
                <span className={getDifficultyClass(q.difficulty)}>
                  {q.difficulty}
                </span>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mb-4">
                {q.options?.map((option, optIdx) => (
                  <div
                    key={optIdx}
                    className={`p-3 rounded-lg border-2 transition-all ${
                      option === q.answer
                        ? 'border-green-500 bg-green-50'
                        : 'border-gray-200 bg-gray-50'
                    }`}
                  >
                    <span className="font-medium text-gray-700">
                      {String.fromCharCode(65 + optIdx)}.
                    </span>{' '}
                    <span className={option === q.answer ? 'text-green-700 font-medium' : 'text-gray-700'}>
                      {option}
                    </span>
                    {option === q.answer && (
                      <span className="ml-2 text-green-600">✓</span>
                    )}
                  </div>
                ))}
              </div>
              
              <div className="bg-blue-50 border-l-4 border-blue-500 p-3 rounded">
                <p className="text-sm font-medium text-blue-900">
                  <span className="font-semibold">Explanation:</span> {q.explanation}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Related Topics */}
      {data.related_topics?.length > 0 && (
        <div className="card bg-gradient-to-br from-blue-50 to-purple-50">
          <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
            <svg className="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            Related Topics
          </h3>
          <div className="flex flex-wrap gap-2">
            {data.related_topics.map((topic, idx) => (
              <span key={idx} className="badge bg-white text-blue-700 border border-blue-200 hover:bg-blue-100 transition-colors cursor-pointer">
                {topic}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default QuizDisplay;
