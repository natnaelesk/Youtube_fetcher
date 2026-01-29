/**
 * Results page component displaying channel videos.
 */

import React, { useState, useMemo } from 'react';
import VideoGrid from '../components/VideoGrid';
import SearchAndSort from '../components/SearchAndSort';
import { sortVideosByDate } from '../utils/dateUtils';

const ResultsPage = ({ data, onReset, channelUrl, loadMore, loadingMore }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [sortOrder, setSortOrder] = useState('desc');

  // Filter and sort videos
  const filteredAndSortedVideos = useMemo(() => {
    let videos = data.videos || [];

    // Filter by search query
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      videos = videos.filter(
        (video) =>
          video.title.toLowerCase().includes(query) ||
          video.description.toLowerCase().includes(query)
      );
    }

    // Sort by date
    videos = sortVideosByDate(videos, sortOrder);

    return videos;
  }, [data.videos, searchQuery, sortOrder]);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                {data.channel_title}
              </h1>
              <p className="text-gray-600 mt-1">
                Showing {data.videos?.length || 0} of {data.total_videos} total videos
                {data.has_more && (
                  <span className="ml-2 text-blue-600 font-medium">
                    ({data.total_videos - (data.videos?.length || 0)} more available)
                  </span>
                )}
              </p>
            </div>
            <button
              onClick={onReset}
              className="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 rounded-lg transition-colors duration-200 font-medium"
            >
              New Search
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <SearchAndSort
          searchQuery={searchQuery}
          onSearchChange={setSearchQuery}
          sortOrder={sortOrder}
          onSortChange={setSortOrder}
          totalVideos={filteredAndSortedVideos.length}
        />

        {filteredAndSortedVideos.length > 0 ? (
          <>
            <VideoGrid videos={filteredAndSortedVideos} />
            
            {data.has_more && !searchQuery && (
              <div className="mt-8 text-center">
                <button
                  onClick={() => loadMore(channelUrl)}
                  disabled={loadingMore}
                  className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-colors duration-200 flex items-center mx-auto"
                >
                  {loadingMore ? (
                    <>
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
                      Loading more videos...
                    </>
                  ) : (
                    `Load More Videos (${data.total_videos - (data.videos?.length || 0)} remaining)`
                  )}
                </button>
                <p className="text-sm text-gray-500 mt-2">
                  Loads 500 videos at a time for faster performance
                </p>
              </div>
            )}
          </>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">
              {searchQuery
                ? 'No videos match your search'
                : 'No videos found'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultsPage;

