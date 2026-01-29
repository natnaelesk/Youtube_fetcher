/**
 * Video grid component for displaying multiple videos.
 */

import React from 'react';
import VideoCard from './VideoCard';

const VideoGrid = ({ videos }) => {
  if (!videos || videos.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">No videos found</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      {videos.map((video) => (
        <VideoCard key={video.video_id} video={video} />
      ))}
    </div>
  );
};

export default VideoGrid;

