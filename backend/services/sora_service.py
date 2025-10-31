import os
import asyncio
from openai import AsyncOpenAI
from typing import Optional
import uuid
from pathlib import Path

class SoraService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.videos_dir = Path("generated_videos")
        self.videos_dir.mkdir(exist_ok=True)
        self.video_jobs = {}

    async def generate_video(
        self,
        prompt: str,
        image_path: str,
        voice_path: Optional[str] = None,
        music_path: Optional[str] = None,
        duration: int = 30
    ) -> str:
        """
        Generate video using Sora 2 API
        """
        video_id = str(uuid.uuid4())

        try:
            # Read the image file
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()

            # Enhanced prompt for Sora 2
            enhanced_prompt = self._enhance_prompt(prompt, duration)

            # Call Sora 2 API (using the new image-to-video capability)
            response = await self.client.videos.generate(
                model="sora-2.0",
                prompt=enhanced_prompt,
                image=image_data,
                duration=duration,
                resolution="1080p",
                fps=30,
                # Include audio if available
                audio={
                    "voice": open(voice_path, "rb").read() if voice_path else None,
                    "music": open(music_path, "rb").read() if music_path else None
                } if (voice_path or music_path) else None
            )

            # Store job info
            self.video_jobs[video_id] = {
                "status": "processing",
                "sora_job_id": response.id,
                "prompt": prompt
            }

            # Start background task to check status and download
            asyncio.create_task(self._monitor_video_generation(video_id, response.id))

            return video_id

        except Exception as e:
            self.video_jobs[video_id] = {
                "status": "failed",
                "error": str(e)
            }
            raise Exception(f"Error generating video: {str(e)}")

    def _enhance_prompt(self, prompt: str, duration: int) -> str:
        """
        Enhance the user's prompt with additional details for better Sora 2 generation
        """
        enhanced = f"""
Create a high-quality, professional video for social media.

Scene Description: {prompt}

Technical Requirements:
- Duration: {duration} seconds
- Maintain the person's appearance, clothing, and features exactly as shown in the reference image
- Professional cinematography with smooth camera movements
- High-quality lighting (cinematic, well-lit)
- Natural movements and realistic physics
- Sharp focus and 1080p quality
- Maintain continuity throughout the video

Style: Professional social media content, engaging, dynamic, visually appealing
"""
        return enhanced.strip()

    async def _monitor_video_generation(self, video_id: str, sora_job_id: str):
        """
        Monitor Sora video generation and download when ready
        """
        try:
            while True:
                # Check status
                status_response = await self.client.videos.retrieve(sora_job_id)

                if status_response.status == "completed":
                    # Download video
                    video_url = status_response.output.url
                    video_path = self.videos_dir / f"{video_id}.mp4"

                    # Download the video file
                    import httpx
                    async with httpx.AsyncClient() as client:
                        response = await client.get(video_url)
                        with open(video_path, "wb") as f:
                            f.write(response.content)

                    self.video_jobs[video_id]["status"] = "completed"
                    self.video_jobs[video_id]["video_path"] = str(video_path)
                    break

                elif status_response.status == "failed":
                    self.video_jobs[video_id]["status"] = "failed"
                    self.video_jobs[video_id]["error"] = "Sora generation failed"
                    break

                # Wait before checking again
                await asyncio.sleep(5)

        except Exception as e:
            self.video_jobs[video_id]["status"] = "failed"
            self.video_jobs[video_id]["error"] = str(e)

    async def get_video_status(self, video_id: str) -> dict:
        """
        Get the status of a video generation job
        """
        if video_id not in self.video_jobs:
            raise Exception("Video job not found")

        return self.video_jobs[video_id]
