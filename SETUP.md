# RELAI Setup Guide

## Quick Setup (5 minutes)

### 1. Get API Keys

You'll need these API keys:

- **OpenAI API Key** (for Sora 2): https://platform.openai.com/api-keys
- **ElevenLabs API Key** (for voice): https://elevenlabs.io/
- **Suno API Key** (for music): https://www.suno.ai/

### 2. Install Dependencies

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 3. Configure Environment

```bash
# In the root directory
cp .env.example .env
```

Edit `.env` and add your API keys:
```
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=...
SUNO_API_KEY=...
```

### 4. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 5. Open in Browser

Go to: http://localhost:3000

## How to Use

1. **Upload Your Photo** - This becomes the base for all videos
2. **Describe Your Video** - Write what you want or get AI suggestions
3. **Choose Voice** - Use AI voice or upload your own voice sample
4. **Generate** - Wait 1-2 minutes while AI creates your video with music
5. **Download** - Get your video ready for social media!

## Example Prompts

**Gym Content:**
```
Show me doing a chest workout at a luxury Miami gym. 5 exercises:
1. Bench press with my puppy as spotter
2. Dumbbell flyes with perfect form
3. Cable crossovers
4. Push-ups variation
5. Finishing with a flex
Wearing black athletic gear, high energy, motivational vibes
```

**Lifestyle Content:**
```
Me walking on Miami beach at sunset, wearing casual summer outfit,
talking to camera about daily routine, smooth camera following,
relaxed confident energy, golden hour lighting
```

**Tutorial Content:**
```
Me in a modern office explaining social media strategy,
pointing at invisible graphics, professional attire,
clear speaking, engaging hand gestures, bright clean lighting
```

## Troubleshooting

**Port already in use:**
```bash
# Backend
PORT=8001 python main.py

# Frontend - edit vite.config.js
```

**API Key Issues:**
- Make sure .env is in the root directory
- No spaces around the = sign
- Use the full API key including prefixes (sk-, etc.)

**Video Generation Fails:**
- Check that your image is clear and shows your face
- Keep prompts detailed but realistic
- Video duration: 15-60 seconds recommended

## API Costs (Approximate)

- Sora 2: ~$0.20-0.40 per video (30 seconds)
- ElevenLabs: ~$0.02 per video (voice)
- Suno: ~$0.10 per video (music)

**Total: ~$0.30-0.50 per video**

## Tips for Best Results

1. **Image Quality**: Use a clear, well-lit photo
2. **Prompts**: Be specific about actions, clothing, location
3. **Duration**: 15-30 seconds works best for social media
4. **Voice**: Upload 30+ seconds of clear voice for best cloning
5. **Ideas**: Use the AI suggestion feature for inspiration

## Need Help?

Check the main README.md for more details or create an issue on GitHub.
