# RELAI - Relax AI Video Generator

**Relax and let AI create your social media content!**

RELAI is a web application that uses Sora 2 API to generate personalized videos for social media. Upload your photo and let AI create engaging content based on your ideas.

## Features

- 🎥 **AI Video Generation** - Powered by Sora 2 API
- 🤖 **Smart Suggestions** - AI generates creative video ideas for your social media
- 🎤 **Voice Options** - Use your own voice or generate AI voices
- 🎵 **AI Music** - Perfect background music generated automatically
- 📱 **Social Media Ready** - Optimized for Instagram, TikTok, YouTube Shorts
- 🖼️ **Photo-to-Video** - Your photo becomes the base for all videos

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- Sora 2 API Key (OpenAI)
- ElevenLabs API Key (for voice)
- Suno API Key (for music)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/GYMTOPZ/RELAI.git
cd RELAI
```

2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. Run the application:

Backend:
```bash
cd backend
python main.py
```

Frontend:
```bash
cd frontend
npm run dev
```

6. Open http://localhost:3000 in your browser

## Usage

1. Upload your photo
2. Describe the video you want (e.g., "gym workout routine in Miami")
3. Choose voice option (yours or AI-generated)
4. Generate video
5. Download and share on social media!

## Tech Stack

- **Frontend**: React + Vite + TailwindCSS
- **Backend**: FastAPI (Python)
- **AI APIs**: Sora 2, ElevenLabs, Suno AI
- **Video Processing**: FFmpeg

## License

MIT License
