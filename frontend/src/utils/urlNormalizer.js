/**
 * Utility to normalize YouTube channel URLs to a standard format.
 * Handles various input formats:
 * - @handle
 * - www.youtube.com/@handle
 * - https://www.youtube.com/@handle
 * - youtube.com/@handle
 * - Full channel URLs
 */

/**
 * Normalize YouTube channel URL to standard format.
 * 
 * @param {string} input - User input (can be handle, partial URL, or full URL)
 * @returns {string} Normalized YouTube channel URL
 */
export const normalizeChannelUrl = (input) => {
  if (!input || !input.trim()) {
    return '';
  }

  let url = input.trim();

  // If it's just a handle (starts with @)
  if (url.startsWith('@')) {
    return `https://www.youtube.com/${url}`;
  }

  // If it's a handle without @
  if (!url.includes('youtube.com') && !url.includes('youtu.be') && !url.includes('/')) {
    // Assume it's a handle
    return `https://www.youtube.com/@${url}`;
  }

  // Add protocol if missing
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    url = 'https://' + url;
  }

  // Normalize www
  url = url.replace(/^https?:\/\/(www\.)?/, 'https://www.');

  // Ensure it's a YouTube URL
  if (!url.includes('youtube.com') && !url.includes('youtu.be')) {
    // If it doesn't contain youtube, assume it's a handle
    if (url.startsWith('https://www.')) {
      return `https://www.youtube.com/@${url.replace('https://www.', '')}`;
    }
    return `https://www.youtube.com/@${url}`;
  }

  // Remove trailing slashes
  url = url.replace(/\/+$/, '');

  return url;
};

/**
 * Validate if input looks like a valid YouTube channel identifier.
 * 
 * @param {string} input - User input
 * @returns {boolean} True if input looks valid
 */
export const isValidChannelInput = (input) => {
  if (!input || !input.trim()) {
    return false;
  }

  const trimmed = input.trim();
  
  // Handle format
  if (trimmed.startsWith('@')) {
    return trimmed.length > 1;
  }

  // URL format
  if (trimmed.includes('youtube.com') || trimmed.includes('youtu.be')) {
    return true;
  }

  // Plain handle (without @)
  if (trimmed.length > 0 && !trimmed.includes(' ')) {
    return true;
  }

  return false;
};

