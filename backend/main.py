from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
import aiofiles
import uuid
from pathlib import Path

from services.sora_service import SoraService
from services.voice_service import VoiceService
from services.music_service import MusicService
from services.suggestion_service import SuggestionService

load_dotenv()

app = FastAPI(title="RELAI API", version="1.0.0")

# CORS configuration
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
UPLOAD_DIR = Path("uploads")
VIDEOS_DIR = Path("generated_videos")
UPLOAD_DIR.mkdir(exist_ok=True)
VIDEOS_DIR.mkdir(exist_ok=True)

# Initialize services
sora_service = SoraService()
voice_service = VoiceService()
music_service = MusicService()
suggestion_service = SuggestionService()


class VideoRequest(BaseModel):
    user_image_id: str
    prompt: str
    voice_type: str = "ai"  # "ai" or "custom"
    voice_file_id: Optional[str] = None
    duration: int = 30


class SuggestionRequest(BaseModel):
    context: str
    user_preferences: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "RELAI API - Relax and create AI videos!"}


@app.post("/api/upload/image")
async def upload_image(file: UploadFile = File(...)):
    """Upload user's photo for video generation"""
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_extension = file.filename.split(".")[-1]
        file_path = UPLOAD_DIR / f"{file_id}.{file_extension}"

        # Save file
        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)

        return {
            "file_id": file_id,
            "filename": file.filename,
            "message": "Image uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload/voice")
async def upload_voice(file: UploadFile = File(...)):
    """Upload user's voice sample for cloning"""
    try:
        # Validate file type
        if not file.content_type.startswith("audio/"):
            raise HTTPException(status_code=400, detail="File must be an audio file")

        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_extension = file.filename.split(".")[-1]
        file_path = UPLOAD_DIR / f"voice_{file_id}.{file_extension}"

        # Save file
        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)

        return {
            "file_id": file_id,
            "filename": file.filename,
            "message": "Voice uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/suggestions/generate")
async def generate_suggestions(request: SuggestionRequest):
    """Generate video idea suggestions based on context"""
    try:
        suggestions = await suggestion_service.generate_suggestions(
            request.context,
            request.user_preferences
        )
        return {"suggestions": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/video/generate")
async def generate_video(request: VideoRequest):
    """Generate video using Sora 2 API with voice and music"""
    try:
        # Get user image path
        image_files = list(UPLOAD_DIR.glob(f"{request.user_image_id}.*"))
        if not image_files:
            raise HTTPException(status_code=404, detail="User image not found")
        user_image_path = str(image_files[0])

        # Generate music
        music_path = await music_service.generate_music(request.prompt)

        # Generate or use voice
        voice_path = None
        if request.voice_type == "custom" and request.voice_file_id:
            voice_files = list(UPLOAD_DIR.glob(f"voice_{request.voice_file_id}.*"))
            if voice_files:
                voice_path = str(voice_files[0])

        if request.voice_type == "ai":
            voice_path = await voice_service.generate_voice(request.prompt)

        # Generate video with Sora 2
        video_id = await sora_service.generate_video(
            prompt=request.prompt,
            image_path=user_image_path,
            voice_path=voice_path,
            music_path=music_path,
            duration=request.duration
        )

        return {
            "video_id": video_id,
            "status": "processing",
            "message": "Video generation started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/video/status/{video_id}")
async def get_video_status(video_id: str):
    """Check video generation status"""
    try:
        status = await sora_service.get_video_status(video_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/video/download/{video_id}")
async def download_video(video_id: str):
    """Download generated video"""
    try:
        video_path = VIDEOS_DIR / f"{video_id}.mp4"
        if not video_path.exists():
            raise HTTPException(status_code=404, detail="Video not found")

        return FileResponse(
            path=str(video_path),
            media_type="video/mp4",
            filename=f"relai_video_{video_id}.mp4"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
