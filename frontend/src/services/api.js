import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://youtube-fetcher.fly.dev';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

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
      const errorData = error.response.data;
      const errorMessage = errorData?.message || 
                          errorData?.help || 
                          'Failed to fetch channel videos';
      throw new Error(errorMessage);
    } else if (error.request) {
      throw new Error('Network error: Could not reach server. Please check your internet connection.');
    } else {
      throw new Error(error.message || 'An unexpected error occurred');
    }
  }
};

export default api;
