# RELAI - Relax AI Video Generator

**Relax and let AI create your social media content!**

RELAI is a web application that uses Sora 2 API to generate personalized videos for social media. Upload your photo and let AI create engaging content based on your ideas.

![Status](https://img.shields.io/badge/status-MVP%20Complete-success)
![Version](https://img.shields.io/badge/version-1.0.0--MVP-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🎯 What is RELAI?

Upload your photo once, and generate unlimited personalized social media videos with AI. No filming, no editing, no stress - just describe what you want and RELAI creates it.

### Perfect For:
- 💪 Fitness influencers
- 📱 Content creators
- 🎬 Social media managers
- 🏢 Business owners
- 🎨 Anyone creating video content

---

## ✨ Features

- 🎥 **AI Video Generation** - Powered by Sora 2 API
- 🤖 **Smart Suggestions** - AI generates creative video ideas for your social media
- 🎤 **Voice Options** - Use your own voice or generate AI voices
- 🎵 **AI Music** - Perfect background music generated automatically
- 📱 **Social Media Ready** - Optimized for Instagram, TikTok, YouTube Shorts
- 🖼️ **Photo-to-Video** - Your photo becomes the base for all videos

---

## 📸 Example Use Case

**Input:**
- Your photo
- Prompt: "Show me doing a chest workout at a luxury Miami gym, 5 exercises, all for chest, wearing black athletic gear, with my puppy as my spotter"

**Output:**
- Professional 30-second video
- AI-generated voice narration
- Perfect gym workout music
- Ready to post on Instagram/TikTok

---

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

## 🛠️ Tech Stack

- **Frontend**: React + Vite + TailwindCSS
- **Backend**: FastAPI (Python)
- **AI APIs**: Sora 2, ElevenLabs, Suno AI, GPT-4
- **Video Processing**: Sora 2 (built-in)

---

## 📚 Documentation

- **[Setup Guide](SETUP.md)** - Detailed installation instructions
- **[API Documentation](docs/API_DOCUMENTATION.md)** - Complete API reference
- **[Architecture](docs/ARCHITECTURE.md)** - System design and structure
- **[Deployment](docs/DEPLOYMENT.md)** - Production deployment guide
- **[Contributing](CONTRIBUTING.md)** - How to contribute
- **[TODO](TODO.md)** - Planned features and improvements
- **[Status](STATUS.md)** - Current project status

---

## 🚀 Roadmap

### ✅ Completed (v1.0.0-MVP)
- Complete backend with all AI integrations
- Modern React frontend
- AI suggestion system
- Voice generation (AI + custom)
- Music generation
- Video download

### 🔄 In Progress
- Testing with real API keys
- Bug fixes and refinements
- Performance optimization

### 📋 Planned
- User authentication
- Video templates
- Social media direct upload
- Analytics dashboard
- Mobile apps
- See [TODO.md](TODO.md) for complete list

---

## 💰 Cost Estimate

Approximate cost per video:
- Sora 2: $0.20-0.40
- Voice: $0.02
- Music: $0.10
- **Total: ~$0.30-0.50 per video**

---

## 🤝 Contributing

We welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

---

## 🙏 Credits

**Created by:** Pedro Meza
**Repository:** [GYMTOPZ/RELAI](https://github.com/GYMTOPZ/RELAI)
**Date:** October 31, 2025

Powered by Sora 2 (OpenAI), ElevenLabs, Suno AI, and GPT-4

---

## 📞 Support

- **Issues:** [Report a bug](https://github.com/GYMTOPZ/RELAI/issues)
- **Discussions:** [Ask questions](https://github.com/GYMTOPZ/RELAI/discussions)
- **Status:** Check [STATUS.md](STATUS.md) for current project state

---

**Ready to create amazing videos? Get started with [SETUP.md](SETUP.md)!**
