# RELAI API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Health Check

**GET /**

Check if the API is running.

**Response:**
```json
{
  "message": "RELAI API - Relax and create AI videos!"
}
```

---

### 2. Upload User Image

**POST /api/upload/image**

Upload the user's photo that will be used as the base for video generation.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (image file)

**Accepted formats:** JPG, PNG, JPEG, WebP

**Response:**
```json
{
  "file_id": "uuid-string",
  "filename": "photo.jpg",
  "message": "Image uploaded successfully"
}
```

**Error Responses:**
- `400`: File must be an image
- `500`: Server error

---

### 3. Upload Voice Sample

**POST /api/upload/voice**

Upload a voice sample for voice cloning (optional).

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (audio file)

**Accepted formats:** MP3, WAV, M4A, OGG

**Recommended:** 30+ seconds of clear speech

**Response:**
```json
{
  "file_id": "uuid-string",
  "filename": "voice.mp3",
  "message": "Voice uploaded successfully"
}
```

**Error Responses:**
- `400`: File must be an audio file
- `500`: Server error

---

### 4. Generate Video Suggestions

**POST /api/suggestions/generate**

Get AI-powered creative video ideas based on context.

**Request Body:**
```json
{
  "context": "fitness content creator focused on gym workouts",
  "user_preferences": "high energy, motivational, luxury gym settings"
}
```

**Response:**
```json
{
  "suggestions": [
    {
      "title": "5-Exercise Chest Destroyer",
      "description": "Show yourself performing 5 intense chest exercises...",
      "duration": 30,
      "platforms": ["Instagram Reels", "TikTok", "YouTube Shorts"],
      "hashtags": ["#ChestDay", "#GymMotivation", "#FitnessGoals"],
      "hook": "Starting with explosive bench press movement"
    },
    // ... more suggestions
  ]
}
```

---

### 5. Generate Video

**POST /api/video/generate**

Main endpoint to generate a video with AI.

**Request Body:**
```json
{
  "user_image_id": "uuid-from-upload",
  "prompt": "Show me doing a chest workout at a luxury Miami gym...",
  "voice_type": "ai",
  "voice_file_id": "uuid-from-voice-upload-optional",
  "duration": 30
}
```

**Parameters:**
- `user_image_id` (required): UUID from image upload
- `prompt` (required): Detailed description of the video
- `voice_type` (optional): "ai" or "custom" (default: "ai")
- `voice_file_id` (optional): UUID from voice upload (required if voice_type="custom")
- `duration` (optional): Video duration in seconds (default: 30, max: 60)

**Response:**
```json
{
  "video_id": "uuid-string",
  "status": "processing",
  "message": "Video generation started"
}
```

**Error Responses:**
- `404`: User image not found
- `500`: Generation error

---

### 6. Check Video Status

**GET /api/video/status/{video_id}**

Check the status of a video generation job.

**Parameters:**
- `video_id`: UUID from generate video response

**Response (Processing):**
```json
{
  "status": "processing",
  "sora_job_id": "sora-job-id",
  "prompt": "original prompt"
}
```

**Response (Completed):**
```json
{
  "status": "completed",
  "video_path": "/path/to/video.mp4",
  "sora_job_id": "sora-job-id",
  "prompt": "original prompt"
}
```

**Response (Failed):**
```json
{
  "status": "failed",
  "error": "Error message",
  "sora_job_id": "sora-job-id"
}
```

---

### 7. Download Video

**GET /api/video/download/{video_id}**

Download the generated video file.

**Parameters:**
- `video_id`: UUID from generate video response

**Response:**
- Content-Type: `video/mp4`
- File download: `relai_video_{video_id}.mp4`

**Error Responses:**
- `404`: Video not found
- `500`: Server error

---

## Complete Workflow Example

### 1. Upload Image
```bash
curl -X POST http://localhost:8000/api/upload/image \
  -F "file=@/path/to/photo.jpg"
```

Response: `{"file_id": "abc-123", ...}`

### 2. Get Suggestions (Optional)
```bash
curl -X POST http://localhost:8000/api/suggestions/generate \
  -H "Content-Type: application/json" \
  -d '{
    "context": "fitness creator",
    "user_preferences": "gym workouts"
  }'
```

### 3. Generate Video
```bash
curl -X POST http://localhost:8000/api/video/generate \
  -H "Content-Type: application/json" \
  -d '{
    "user_image_id": "abc-123",
    "prompt": "Show me doing a chest workout...",
    "voice_type": "ai",
    "duration": 30
  }'
```

Response: `{"video_id": "xyz-789", "status": "processing"}`

### 4. Check Status (Poll every 5 seconds)
```bash
curl http://localhost:8000/api/video/status/xyz-789
```

### 5. Download Video (when status = "completed")
```bash
curl -O http://localhost:8000/api/video/download/xyz-789
```

---

## Rate Limits

Currently no rate limits implemented. In production:
- Suggested: 10 videos per hour per user
- 50 API requests per minute

---

## Error Handling

All errors follow this format:
```json
{
  "detail": "Error message description"
}
```

**Common HTTP Status Codes:**
- `200`: Success
- `400`: Bad request (invalid input)
- `404`: Resource not found
- `500`: Internal server error

---

## Best Practices

### Prompts
- Be specific about actions, clothing, location
- Include camera angles and lighting preferences
- Mention pacing and energy level
- Keep under 500 characters for best results

### Images
- Use high-quality, well-lit photos
- Face should be clearly visible
- Neutral expression works best
- Avoid sunglasses or face coverings

### Voice Samples
- 30+ seconds of clear speech
- Minimal background noise
- Consistent volume
- Natural speaking pace

### Duration
- 15-30 seconds: Best for TikTok/Reels
- 30-45 seconds: Good for all platforms
- 45-60 seconds: YouTube Shorts

---

## API Keys Required

Set these in your `.env` file:

```env
OPENAI_API_KEY=sk-...           # Sora 2 API
ELEVENLABS_API_KEY=...          # Voice generation
SUNO_API_KEY=...                # Music generation
```

---

## Support

For issues or questions, create an issue at:
https://github.com/GYMTOPZ/RELAI/issues
