import axios from 'axios';

// Use production URL if available, fallback to local
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api';

console.log('API Base URL:', API_BASE_URL);

// Create axios instance with defaults
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 second timeout for quiz generation
});

// Generate a new quiz from Wikipedia URL
export const generateQuiz = async (url, force = false) => {
  try {
    const response = await apiClient.post('/generate_quiz/', {
      url,
      force
    });
    return response.data;
  } catch (error) {
    console.error('API Error:', error.response?.data || error.message);
    throw error.response?.data?.detail || 'Failed to generate quiz. Please try again.';
  }
};

// Get list of all quizzes
export const getQuizHistory = async () => {
  try {
    const response = await apiClient.get('/history/');
    return response.data;
  } catch (error) {
    console.error('API Error:', error.response?.data || error.message);
    throw error.response?.data?.detail || 'Failed to fetch history';
  }
};

// Get details of a specific quiz by ID
export const getQuizDetails = async (quizId) => {
  try {
    const response = await apiClient.get(`/quiz/${quizId}/`);
    return response.data;
  } catch (error) {
    console.error('API Error:', error.response?.data || error.message);
    throw error.response?.data?.detail || 'Failed to fetch quiz details';
  }
};

export default apiClient;
