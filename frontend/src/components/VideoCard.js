/**
 * Video card component for displaying individual video information.
 */

import React from 'react';
import { formatDate } from '../utils/dateUtils';

const VideoCard = ({ video }) => {
  const handleCardClick = () => {
    window.open(video.video_url, '_blank', 'noopener,noreferrer');
  };

  return (
    <div
      onClick={handleCardClick}
      className="bg-white rounded-lg shadow-md overflow-hidden cursor-pointer hover:shadow-lg transition-shadow duration-200 border border-gray-200"
    >
      <div className="relative w-full aspect-video bg-gray-200">
        {video.thumbnail ? (
          <img
            src={video.thumbnail}
            alt={video.title}
            className="w-full h-full object-cover"
            loading="lazy"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-400">
            No thumbnail
          </div>
        )}
      </div>
      <div className="p-4">
        <h3 className="font-semibold text-gray-900 line-clamp-2 mb-2">
          {video.title}
        </h3>
        <p className="text-sm text-gray-500">
          {formatDate(video.published_at)}
        </p>
      </div>
    </div>
  );
};

export default VideoCard;

