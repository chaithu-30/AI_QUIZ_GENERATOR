import axios from 'axios';

// Production API URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api';

console.log('Using API Base URL:', API_BASE_URL);

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 seconds for quiz generation
});

// Add request interceptor for debugging
apiClient.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for debugging
apiClient.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('Response Error:', error.response?.status, error.response?.data);
    return Promise.reject(error);
  }
);

// Generate a new quiz from Wikipedia URL
export const generateQuiz = async (url, force = false) => {
  try {
    const response = await apiClient.post('/generate_quiz/', {
      url,
      force
    });
    return response.data;
  } catch (error) {
    const errorMessage = error.response?.data?.detail || 
                        error.message || 
                        'Failed to generate quiz. Please try again.';
    console.error('Generate Quiz Error:', errorMessage);
    throw errorMessage;
  }
};

// Get list of all quizzes
export const getQuizHistory = async () => {
  try {
    const response = await apiClient.get('/history/');
    return response.data;
  } catch (error) {
    const errorMessage = error.response?.data?.detail || 
                        'Failed to fetch quiz history';
    console.error('Get History Error:', errorMessage);
    throw errorMessage;
  }
};

// Get details of a specific quiz by ID
export const getQuizDetails = async (quizId) => {
  try {
    const response = await apiClient.get(`/quiz/${quizId}/`);
    return response.data;
  } catch (error) {
    const errorMessage = error.response?.data?.detail || 
                        'Failed to fetch quiz details';
    console.error('Get Quiz Details Error:', errorMessage);
    throw errorMessage;
  }
};

export default apiClient;
