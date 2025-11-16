import React from 'react';

function LoadingSpinner({ message = "Generating quiz..." }) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="relative">
        <div className="w-16 h-16 border-4 border-purple-200 border-t-purple-600 rounded-full animate-spin"></div>
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-10 h-10 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin" style={{ animationDirection: 'reverse', animationDuration: '0.8s' }}></div>
        </div>
      </div>
      <p className="mt-6 text-lg font-medium text-gray-700 animate-pulse">{message}</p>
      <p className="mt-2 text-sm text-gray-500">This may take 20-30 seconds...</p>
    </div>
  );
}

export default LoadingSpinner;
