# Quick Start Guide

## 🚀 Running the Application

### Step 1: Set Up Environment Variables

Create a `.env` file in the root directory (copy from `env.example`):

```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
YOUTUBE_API_KEY=your-youtube-api-key-here
```

**Important**: Get your YouTube API key from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)

### Step 2: Start Backend (Django)

Open a terminal in the project root:

```bash
# Activate virtual environment (if using one)
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Run migrations (first time only)
python manage.py migrate

# Start server
python manage.py runserver
```

Backend will run at: `http://localhost:8000`

### Step 3: Start Frontend (React)

Open a **new terminal** in the `frontend` directory:

```bash
cd frontend
npm start
```

Frontend will run at: `http://localhost:3000`

### Step 4: Use the Application

1. Open `http://localhost:3000` in your browser
2. Paste a YouTube channel URL (e.g., `https://www.youtube.com/@channelname`)
3. Click "Fetch Videos"
4. Browse, search, and sort the results!

## ✅ Verification

- Backend API: `http://localhost:8000/api/channel/videos/`
- Frontend: `http://localhost:3000`

## 🐛 Troubleshooting

- **CORS errors**: Ensure backend is running on port 8000
- **API errors**: Check your YouTube API key is valid and has quota
- **Module errors**: Run `pip install -r requirements.txt` and `npm install` in frontend

