import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

/**
 * Generate a quiz from a Wikipedia URL
 * @param {string} url - Wikipedia article URL
 * @returns {Promise<Object>} Quiz data
 */
export const generateQuiz = async (url) => {
    const response = await api.post('/quiz/generate', { url });
    return response.data;
};

/**
 * Get quiz history
 * @param {number} skip - Number of items to skip
 * @param {number} limit - Maximum number of items to return
 * @returns {Promise<Object>} History data with quizzes array and total count
 */
export const getQuizHistory = async (skip = 0, limit = 50) => {
    const response = await api.get('/quiz/history', {
        params: { skip, limit },
    });
    return response.data;
};

/**
 * Get quiz details by ID
 * @param {number} quizId - Quiz ID
 * @returns {Promise<Object>} Full quiz data
 */
export const getQuizDetails = async (quizId) => {
    const response = await api.get(`/quiz/${quizId}`);
    return response.data;
};

/**
 * Delete a quiz by ID
 * @param {number} quizId - Quiz ID
 * @returns {Promise<void>}
 */
export const deleteQuiz = async (quizId) => {
    await api.delete(`/quiz/${quizId}`);
};

export default api;
