import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Generate a new quiz from Wikipedia URL
export const generateQuiz = async (url, force = false) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/generate_quiz/`, {
      url,
      force
    });
    return response.data;
  } catch (error) {
    throw error.response?.data?.error || 'Failed to generate quiz';
  }
};

// Get list of all quizzes
export const getQuizHistory = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/history/`);
    return response.data;
  } catch (error) {
    throw error.response?.data?.error || 'Failed to fetch history';
  }
};

// Get details of a specific quiz by ID
export const getQuizDetails = async (quizId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/quiz/${quizId}/`);
    return response.data;
  } catch (error) {
    throw error.response?.data?.error || 'Failed to fetch quiz details';
  }
};
