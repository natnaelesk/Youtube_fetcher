import React, { useState } from 'react';
import { useChannelVideos } from '../hooks/useChannelVideos';
import { normalizeChannelUrl, isValidChannelInput } from '../utils/urlNormalizer';
import ResultsPage from './ResultsPage';

const HomePage = () => {
  const [channelUrl, setChannelUrl] = useState('');
  const { loading, loadingMore, error, data, fetchVideos, loadMore, reset } = useChannelVideos();

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmed = channelUrl.trim();
    if (trimmed && isValidChannelInput(trimmed)) {
      const normalizedUrl = normalizeChannelUrl(trimmed);
      fetchVideos(normalizedUrl);
    }
  };

  const handleReset = () => {
    setChannelUrl('');
    reset();
  };

  if (data) {
    const normalizedUrl = channelUrl.trim() ? normalizeChannelUrl(channelUrl.trim()) : '';
    return (
      <ResultsPage 
        data={data} 
        onReset={handleReset} 
        channelUrl={normalizedUrl}
        loadMore={loadMore}
        loadingMore={loadingMore}
      />
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        <div className="bg-white rounded-2xl shadow-xl p-8 md:p-12">
          <div className="text-center mb-8">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              YouTube Channel Fetcher
            </h1>
            <p className="text-lg text-gray-600">
              Enter a YouTube channel URL to fetch all videos instantly
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="channel-url" className="block text-sm font-medium text-gray-700 mb-2">
                Channel URL or Handle
              </label>
              <input
                id="channel-url"
                type="text"
                value={channelUrl}
                onChange={(e) => setChannelUrl(e.target.value)}
                placeholder="@channelname or youtube.com/@channelname"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg"
                disabled={loading}
              />
              <div className="mt-2 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-sm font-medium text-blue-900 mb-1">Accepted formats:</p>
                <ul className="text-xs text-blue-800 list-disc list-inside space-y-1">
                  <li><code className="bg-blue-100 px-1 rounded">@channelname</code> - Just the handle</li>
                  <li><code className="bg-blue-100 px-1 rounded">www.youtube.com/@channelname</code> - With www</li>
                  <li><code className="bg-blue-100 px-1 rounded">https://www.youtube.com/@channelname</code> - Full URL</li>
                  <li><code className="bg-blue-100 px-1 rounded">youtube.com/channel/UC...</code> - Channel ID format</li>
                </ul>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading || !channelUrl.trim()}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 text-lg"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg
                    className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  Fetching videos...
                </span>
              ) : (
                'Fetch Videos'
              )}
            </button>
          </form>

          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <div className="flex items-start">
                <svg className="w-5 h-5 text-red-600 mt-0.5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <div className="flex-1">
                  <p className="text-red-800 font-semibold mb-1">Error Fetching Videos</p>
                  <p className="text-red-700 text-sm">{error}</p>
                  <p className="text-red-600 text-xs mt-2">
                    Tip: Make sure the channel URL is correct and the channel is public.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default HomePage;

