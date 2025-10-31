# RELAI Architecture Documentation

## 🏗️ System Overview

RELAI is a full-stack web application that generates personalized AI videos for social media using multiple AI services.

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────────┐
│  React Frontend │ (Vite + TailwindCSS)
│   Port: 3000    │
└────────┬────────┘
         │ REST API
         ▼
┌─────────────────┐
│  FastAPI Backend│ (Python)
│   Port: 8000    │
└────────┬────────┘
         │
         ├──► OpenAI Sora 2 API (Video Generation)
         ├──► ElevenLabs API (Voice Generation)
         ├──► Suno API (Music Generation)
         └──► OpenAI GPT-4 API (Suggestions)
```

---

## 📦 Component Architecture

### Frontend Architecture

```
frontend/
├── src/
│   ├── main.jsx              # App entry point
│   ├── App.jsx               # Main application component
│   ├── index.css             # Global styles
│   └── App.css               # Component styles
├── public/                   # Static assets
├── package.json              # Dependencies
├── vite.config.js            # Vite configuration
└── tailwind.config.js        # Tailwind configuration
```

#### Component Structure

```
App
├── Header
├── ImageUploadStep (step 1)
├── PromptCreationStep (step 2)
│   ├── PromptInput
│   ├── SuggestionGenerator
│   ├── VoiceSelector
│   └── GenerateButton
├── GeneratingStep (step 3)
│   └── ProgressIndicator
└── DownloadStep (step 4)
    ├── VideoPreview
    └── DownloadButton
```

### Backend Architecture

```
backend/
├── main.py                   # FastAPI app & routes
├── services/
│   ├── sora_service.py       # Video generation
│   ├── voice_service.py      # Voice synthesis
│   ├── music_service.py      # Music generation
│   └── suggestion_service.py # Content suggestions
├── uploads/                  # User uploads (temp)
└── generated_videos/         # Generated videos (temp)
```

#### Service Layer Pattern

Each service is independent and handles specific functionality:

```python
class SoraService:
    - generate_video()
    - get_video_status()
    - _enhance_prompt()
    - _monitor_video_generation()

class VoiceService:
    - generate_voice()
    - clone_voice()
    - get_available_voices()
    - _create_narration()

class MusicService:
    - generate_music()
    - _create_music_prompt()
    - _wait_for_music()

class SuggestionService:
    - generate_suggestions()
    - enhance_prompt()
    - _parse_suggestions()
```

---

## 🔄 Data Flow

### Complete Video Generation Flow

```
1. User uploads image
   Frontend → Backend /api/upload/image
   └─► Saves to uploads/ directory
   └─► Returns file_id

2. User creates prompt (optional: gets AI suggestions)
   Frontend → Backend /api/suggestions/generate
   └─► GPT-4 generates creative ideas
   └─► Returns suggestions array

3. User clicks "Generate Video"
   Frontend → Backend /api/video/generate
   ├─► SoraService.generate_video()
   │   ├─► Reads user image
   │   ├─► Enhances prompt
   │   └─► Calls Sora 2 API
   │
   ├─► VoiceService.generate_voice() / clone_voice()
   │   ├─► Creates narration script
   │   ├─► Calls ElevenLabs API
   │   └─► Returns audio file
   │
   ├─► MusicService.generate_music()
   │   ├─► Determines music style
   │   ├─► Calls Suno API
   │   └─► Returns music file
   │
   └─► Combines all (Sora 2 does this)
       └─► Returns video_id

4. Frontend polls status
   Frontend → Backend /api/video/status/{video_id}
   └─► Checks generation status
   └─► Returns: processing | completed | failed

5. Video ready
   Frontend → Backend /api/video/download/{video_id}
   └─► Returns video file (MP4)
```

---

## 🗄️ Data Models

### Request Models

```python
class VideoRequest(BaseModel):
    user_image_id: str          # UUID from upload
    prompt: str                 # Video description
    voice_type: str = "ai"      # "ai" or "custom"
    voice_file_id: Optional[str] = None
    duration: int = 30          # 15-60 seconds

class SuggestionRequest(BaseModel):
    context: str                # User context
    user_preferences: Optional[str] = None
```

### Response Models

```python
# Upload Response
{
    "file_id": "uuid",
    "filename": "photo.jpg",
    "message": "Image uploaded successfully"
}

# Video Generation Response
{
    "video_id": "uuid",
    "status": "processing",
    "message": "Video generation started"
}

# Video Status Response
{
    "status": "completed",
    "video_path": "/path/to/video.mp4",
    "sora_job_id": "sora-job-id",
    "prompt": "original prompt"
}

# Suggestions Response
{
    "suggestions": [
        {
            "title": "Video Title",
            "description": "Detailed description",
            "duration": 30,
            "platforms": ["TikTok", "Instagram"],
            "hashtags": ["#tag1", "#tag2"],
            "hook": "Opening description"
        }
    ]
}
```

---

## 🔌 API Integration Details

### Sora 2 API (OpenAI)

```python
# Video Generation Request
await client.videos.generate(
    model="sora-2.0",
    prompt=enhanced_prompt,
    image=image_data,           # User's photo
    duration=30,
    resolution="1080p",
    fps=30,
    audio={
        "voice": voice_data,    # From ElevenLabs
        "music": music_data     # From Suno
    }
)

# Response
{
    "id": "job_id",
    "status": "processing",
    "output": {
        "url": "video_url"      # When completed
    }
}
```

### ElevenLabs API

```python
# Voice Generation
await client.text_to_speech.convert(
    voice_id="voice_id",
    text=narration_text,
    model_id="eleven_multilingual_v2",
    voice_settings={
        "stability": 0.5,
        "similarity_boost": 0.75
    }
)

# Voice Cloning
await client.voices.add(
    name="user_voice",
    files=[voice_sample_data]
)
```

### Suno API

```python
# Music Generation
POST https://api.suno.ai/v1/generate
{
    "prompt": "energetic gym workout music",
    "duration": 30,
    "instrumental": true,
    "style": "modern"
}

# Response
{
    "id": "generation_id",
    "status": "processing",
    "audio_url": "url"  # When completed
}
```

### GPT-4 API (Suggestions)

```python
# Content Suggestions
await client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.8
)
```

---

## 🔐 Security Architecture

### Authentication Flow (Future)

```
User → JWT Token → Backend → Verify → Allow/Deny
```

### File Upload Security

```python
1. Validate file type
2. Check file size (< 10MB)
3. Generate unique UUID filename
4. Scan for malware (future)
5. Store temporarily
6. Clean up after video generation
```

### API Key Management

```
Environment Variables → Backend Only
- Never exposed to frontend
- Loaded from .env
- Not committed to git
```

---

## 📊 State Management

### Frontend State

```javascript
// App.jsx manages all state
const [step, setStep] = useState(1)              // Current step
const [userImage, setUserImage] = useState(null) // Image preview
const [userImageId, setUserImageId] = useState(null) // Backend ID
const [prompt, setPrompt] = useState('')         // User prompt
const [voiceType, setVoiceType] = useState('ai') // Voice option
const [videoId, setVideoId] = useState(null)     // Generated video ID
const [videoStatus, setVideoStatus] = useState(null) // Generation status
```

### Backend State

```python
# In-memory storage (current)
self.video_jobs = {
    "video_id": {
        "status": "processing",
        "sora_job_id": "job_id",
        "prompt": "original prompt"
    }
}

# Future: Database storage
- PostgreSQL for persistence
- Redis for caching
- S3/R2 for file storage
```

---

## 🚀 Performance Considerations

### Caching Strategy

```
1. Frontend
   - Image preview cached locally
   - Suggestions cached in state

2. Backend (Future)
   - Redis for API responses
   - CDN for generated videos
   - Database query caching
```

### Async Processing

```python
# Video generation runs in background
asyncio.create_task(self._monitor_video_generation(video_id))

# Frontend polls for status (every 5 seconds)
const interval = setInterval(async () => {
    const status = await checkVideoStatus(videoId)
}, 5000)
```

---

## 📁 File Storage Strategy

### Current (Local Storage)

```
uploads/
├── {uuid}.jpg              # User images
├── voice_{uuid}.mp3        # Voice samples
└── voices/
    ├── voice_{uuid}.mp3    # Generated voices
    └── voice_cloned_{uuid}.mp3

generated_videos/
└── {uuid}.mp4              # Generated videos
```

### Future (Cloud Storage)

```
Cloudflare R2 / AWS S3
├── users/{user_id}/
│   ├── images/
│   ├── voices/
│   └── videos/
└── public/
    └── videos/ (shareable links)
```

---

## 🔄 Error Handling Strategy

### Frontend

```javascript
try {
    const response = await axios.post('/api/generate', data)
} catch (error) {
    if (error.response) {
        // Server responded with error
        alert(error.response.data.detail)
    } else if (error.request) {
        // No response from server
        alert('Server not responding')
    } else {
        // Other error
        alert('An error occurred')
    }
}
```

### Backend

```python
try:
    video_id = await sora_service.generate_video(...)
except Exception as e:
    logger.error(f"Video generation failed: {str(e)}")
    raise HTTPException(
        status_code=500,
        detail=f"Error generating video: {str(e)}"
    )
```

---

## 🧪 Testing Strategy

### Unit Tests

```python
# Backend
pytest backend/tests/

test_sora_service.py
├── test_generate_video()
├── test_enhance_prompt()
└── test_video_status()

test_voice_service.py
├── test_generate_voice()
└── test_clone_voice()
```

### Integration Tests

```python
# Full workflow test
test_video_generation_workflow.py
├── test_upload_image()
├── test_generate_suggestions()
├── test_generate_video()
└── test_download_video()
```

### E2E Tests (Frontend)

```javascript
// Playwright or Cypress
describe('Video Generation Flow', () => {
  it('should generate video from start to finish', () => {
    // Upload image
    // Enter prompt
    // Generate video
    // Download video
  })
})
```

---

## 🔮 Future Architecture Improvements

### Microservices (Scale)

```
API Gateway
├── Video Service (Sora integration)
├── Audio Service (Voice + Music)
├── Suggestion Service (GPT-4)
└── User Service (Auth, profiles)
```

### Message Queue

```
Frontend → API → RabbitMQ/Redis Queue
                      ↓
                  Worker Pool
                      ↓
                  Video Generation
```

### CDN Integration

```
User → CloudFlare CDN → Cached Video
                       ↓ (cache miss)
                   Origin Server
```

---

## 📈 Monitoring & Observability

### Metrics to Track

```
- Video generation success rate
- Average generation time
- API response times
- Error rates by endpoint
- User engagement metrics
- API costs per video
```

### Logging Strategy

```python
import logging

logger.info("Video generation started", extra={
    "video_id": video_id,
    "user_id": user_id,
    "prompt_length": len(prompt)
})

logger.error("Video generation failed", extra={
    "video_id": video_id,
    "error": str(e)
})
```

---

**Architecture Version:** 1.0.0
**Last Updated:** 2025-10-31
**Status:** MVP - Production Ready
