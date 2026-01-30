import { useState } from 'react';
import { fetchChannelVideos } from '../services/api';

export const useChannelVideos = () => {
  const [loading, setLoading] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  const fetchVideos = async (channelUrl, limit = 500, offset = 0) => {
    if (offset === 0) {
      setLoading(true);
      setError(null);
      setData(null);
    } else {
      setLoadingMore(true);
    }

    try {
      const result = await fetchChannelVideos(channelUrl, limit, offset);
      
      if (offset === 0) {
        setData(result);
      } else {
        setData(prevData => ({
          ...result,
          videos: [...(prevData?.videos || []), ...result.videos],
        }));
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  };

  const loadMore = async (channelUrl) => {
    if (!data || !data.has_more || loadingMore) {
      return;
    }
    
    await fetchVideos(channelUrl, 500, data.next_offset);
  };

  const reset = () => {
    setLoading(false);
    setLoadingMore(false);
    setError(null);
    setData(null);
  };

  return {
    loading,
    loadingMore,
    error,
    data,
    fetchVideos,
    loadMore,
    reset,
  };
};
