# YouTube Channel Video Fetcher

A production-ready web application that allows users to paste a YouTube channel link and instantly retrieve all videos published by that channel using the YouTube Data API v3.

## 🎯 Features

- **Fast Channel Analysis**: Retrieve all videos from any YouTube channel instantly
- **Multiple URL Formats**: Supports channel IDs, custom URLs, handles (@username), and user URLs
- **Structured Data**: Clean, structured video metadata with thumbnails, dates, and links
- **Search & Sort**: Search videos by title/description and sort by publish date
- **Responsive UI**: Modern, clean interface that works on all devices
- **API Quota Aware**: Intelligent caching to minimize API calls
- **Error Handling**: Graceful error handling for all edge cases
- **Production Ready**: Clean architecture, modular code, and comprehensive documentation

## 🛠 Tech Stack

### Backend
- **Django 4.2.7**: Web framework
- **Django REST Framework**: API development
- **python-dotenv**: Environment variable management
- **requests**: HTTP client for YouTube API
- **django-cors-headers**: CORS handling

### Frontend
- **React 18**: UI library
- **Tailwind CSS**: Styling
- **Axios**: HTTP client

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- YouTube Data API v3 key ([Get one here](https://console.cloud.google.com/apis/credentials))

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Youtube_extact_video
```

### 2. Backend Setup

#### Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and add your configuration:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
YOUTUBE_API_KEY=your-youtube-api-key-here
```

**Important**: Get your YouTube API key from [Google Cloud Console](https://console.cloud.google.com/apis/credentials). Make sure to enable the YouTube Data API v3.

#### Run Database Migrations

```bash
python manage.py migrate
```

#### Start Django Server

```bash
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

#### Navigate to Frontend Directory

```bash
cd frontend
```

#### Install Dependencies

```bash
npm install
```

#### Configure API URL (Optional)

Create a `.env` file in the `frontend` directory if you need to change the API URL:

```env
REACT_APP_API_URL=http://localhost:8000
```

#### Start React Development Server

```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## 📁 Project Structure

```
Youtube_extact_video/
├── youtube_channel_fetcher/      # Django project
│   ├── settings.py               # Django settings
│   ├── urls.py                   # Main URL routing
│   └── ...
├── videos/                        # Django app
│   ├── services/
│   │   └── youtube_service.py    # YouTube API service
│   ├── utils/
│   │   └── url_parser.py         # URL parsing utilities
│   ├── views.py                  # API views
│   ├── serializers.py            # API serializers
│   └── urls.py                   # App URL routing
├── frontend/                      # React application
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── pages/                # Page components
│   │   ├── services/             # API services
│   │   ├── hooks/                # Custom hooks
│   │   └── utils/                # Utility functions
│   └── public/
├── requirements.txt               # Python dependencies
├── .env.example                  # Environment variables template
└── README.md                     # This file
```

## 🔌 API Endpoints

### POST `/api/channel/videos/`

Fetch all videos from a YouTube channel.

**Request Body:**
```json
{
  "channel_url": "https://www.youtube.com/@channelname"
}
```

**Response:**
```json
{
  "channel_title": "Channel Name",
  "channel_id": "UC...",
  "total_videos": 100,
  "videos": [
    {
      "video_id": "dQw4w9WgXcQ",
      "title": "Video Title",
      "description": "Video description...",
      "thumbnail": "https://...",
      "published_at": "2024-01-01T00:00:00Z",
      "video_url": "https://www.youtube.com/watch?v=..."
    }
  ]
}
```

## 🎨 Usage

1. **Start the backend server** (Django)
2. **Start the frontend server** (React)
3. **Open** `http://localhost:3000` in your browser
4. **Paste** a YouTube channel URL (supports various formats):
   - `https://www.youtube.com/@channelname`
   - `https://www.youtube.com/channel/UC...`
   - `https://www.youtube.com/c/ChannelName`
   - `https://www.youtube.com/user/username`
5. **Click** "Fetch Videos"
6. **Browse, search, and sort** the results

## 🔒 Security

- API keys are stored server-side only
- All user inputs are validated
- CORS is configured for development
- Error messages don't expose sensitive information

## ⚡ Performance

- **Caching**: API responses are cached for 10 minutes
- **Pagination**: Handles channels with 1000+ videos efficiently
- **Lazy Loading**: Images load lazily for better performance

## 🧪 Testing

### Backend Tests

```bash
python manage.py test
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 🐛 Troubleshooting

### API Quota Exceeded

If you see "API quota exceeded" errors:
- Check your YouTube API quota in Google Cloud Console
- The app caches responses to minimize API calls
- Consider upgrading your API quota if needed

### CORS Errors

If you see CORS errors:
- Ensure `django-cors-headers` is installed
- Check `CORS_ALLOWED_ORIGINS` in `settings.py`
- Verify frontend is running on the correct port

### Channel Not Found

If a channel is not found:
- Verify the channel URL is correct
- Some channels may be private or deleted
- Try using the channel ID format instead

## 📝 Supported URL Formats

The application supports multiple YouTube channel URL formats:

- **Channel ID**: `https://www.youtube.com/channel/UC...`
- **Handle**: `https://www.youtube.com/@channelname`
- **Custom URL**: `https://www.youtube.com/c/ChannelName`
- **User**: `https://www.youtube.com/user/username`

## 🔄 Future Enhancements

Potential improvements for production:

- User authentication
- Export functionality (CSV, JSON)
- Video analytics
- Batch channel processing
- Rate limiting
- Database persistence
- Advanced filtering options

## 📄 License

This project is open source and available for use.

## 🤝 Contributing

Contributions are welcome! Please ensure:
- Code follows existing style
- Tests are included
- Documentation is updated

## 📧 Support

For issues or questions, please open an issue in the repository.

---

**Built with ❤️ for developers, researchers, and content creators**

