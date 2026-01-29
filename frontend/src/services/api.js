/**
 * API service for communicating with Django backend.
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Fetch videos from a YouTube channel with pagination.
 * 
 * @param {string} channelUrl - YouTube channel URL
 * @param {number} limit - Number of videos to fetch (default: 500)
 * @param {number} offset - Offset for pagination (default: 0)
 * @returns {Promise} API response with channel info and videos
 */
export const fetchChannelVideos = async (channelUrl, limit = 500, offset = 0) => {
  try {
    const response = await api.post('/api/channel/videos/', {
      channel_url: channelUrl,
      limit: limit,
      offset: offset,
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      // Server responded with error status
      const errorData = error.response.data;
      const errorMessage = errorData?.message || 
                          errorData?.help || 
                          'Failed to fetch channel videos';
      throw new Error(errorMessage);
    } else if (error.request) {
      // Request made but no response
      throw new Error('Network error: Could not reach server. Please check your internet connection.');
    } else {
      // Error in request setup
      throw new Error(error.message || 'An unexpected error occurred');
    }
  }
};

export default api;

