export const normalizeChannelUrl = (input) => {
  if (!input || !input.trim()) {
    return '';
  }

  let url = input.trim();

  if (url.startsWith('@')) {
    return `https://www.youtube.com/${url}`;
  }

  if (!url.includes('youtube.com') && !url.includes('youtu.be') && !url.includes('/')) {
    return `https://www.youtube.com/@${url}`;
  }

  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    url = 'https://' + url;
  }

  url = url.replace(/^https?:\/\/(www\.)?/, 'https://www.');

  if (!url.includes('youtube.com') && !url.includes('youtu.be')) {
    if (url.startsWith('https://www.')) {
      return `https://www.youtube.com/@${url.replace('https://www.', '')}`;
    }
    return `https://www.youtube.com/@${url}`;
  }

  url = url.replace(/\/+$/, '');
  return url;
};

export const isValidChannelInput = (input) => {
  if (!input || !input.trim()) {
    return false;
  }

  const trimmed = input.trim();
  
  if (trimmed.startsWith('@')) {
    return trimmed.length > 1;
  }

  if (trimmed.includes('youtube.com') || trimmed.includes('youtu.be')) {
    return true;
  }

  if (trimmed.length > 0 && !trimmed.includes(' ')) {
    return true;
  }

  return false;
};
