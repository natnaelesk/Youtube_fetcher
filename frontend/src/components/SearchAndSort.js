/**
 * Search and sort controls component.
 */

import React from 'react';

const SearchAndSort = ({ searchQuery, onSearchChange, sortOrder, onSortChange, totalVideos }) => {
  return (
    <div className="flex flex-col sm:flex-row gap-4 mb-6">
      <div className="flex-1">
        <input
          type="text"
          placeholder="Search videos..."
          value={searchQuery}
          onChange={(e) => onSearchChange(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>
      <div className="flex gap-4 items-center">
        <label className="text-sm text-gray-600 whitespace-nowrap">
          Sort by date:
        </label>
        <select
          value={sortOrder}
          onChange={(e) => onSortChange(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="desc">Newest First</option>
          <option value="asc">Oldest First</option>
        </select>
        <span className="text-sm text-gray-600 whitespace-nowrap">
          {totalVideos} videos
        </span>
      </div>
    </div>
  );
};

export default SearchAndSort;

