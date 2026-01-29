/**
 * Utility functions for date formatting.
 */

/**
 * Format ISO date string to readable format.
 * 
 * @param {string} isoDate - ISO date string
 * @returns {string} Formatted date string
 */
export const formatDate = (isoDate) => {
  if (!isoDate) return '';
  
  const date = new Date(isoDate);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

/**
 * Sort videos by published date.
 * 
 * @param {Array} videos - Array of video objects
 * @param {string} order - 'asc' or 'desc'
 * @returns {Array} Sorted videos array
 */
export const sortVideosByDate = (videos, order = 'desc') => {
  const sorted = [...videos].sort((a, b) => {
    const dateA = new Date(a.published_at);
    const dateB = new Date(b.published_at);
    
    if (order === 'asc') {
      return dateA - dateB;
    } else {
      return dateB - dateA;
    }
  });
  
  return sorted;
};

