import os
import uuid
import httpx
import asyncio
from pathlib import Path
from typing import Optional

class MusicService:
    def __init__(self):
        self.api_key = os.getenv("SUNO_API_KEY")
        self.base_url = "https://api.suno.ai/v1"
        self.output_dir = Path("uploads/music")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def generate_music(self, video_prompt: str, duration: int = 30) -> str:
        """
        Generate background music using Suno AI based on video context
        Falls back to a music generation prompt if Suno is not available
        """
        try:
            # Determine music style from video prompt
            music_prompt = self._create_music_prompt(video_prompt)

            # Generate music with Suno AI
            music_id = str(uuid.uuid4())
            music_path = self.output_dir / f"music_{music_id}.mp3"

            # Call Suno API (using httpx for async)
            async with httpx.AsyncClient() as client:
                # Generate music
                response = await client.post(
                    f"{self.base_url}/generate",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "prompt": music_prompt,
                        "duration": duration,
                        "instrumental": True,  # No lyrics, just background music
                        "style": "modern"
                    },
                    timeout=60.0
                )

                if response.status_code != 200:
                    raise Exception(f"Suno API error: {response.text}")

                result = response.json()
                generation_id = result["id"]

                # Poll for completion
                music_url = await self._wait_for_music(client, generation_id)

                # Download music
                download_response = await client.get(music_url)
                with open(music_path, "wb") as f:
                    f.write(download_response.content)

            return str(music_path)

        except Exception as e:
            # If Suno fails, create a fallback (silent or use a default track)
            print(f"Warning: Music generation failed: {str(e)}")
            # Return None to indicate no music (Sora can still generate the video)
            return None

    async def _wait_for_music(self, client: httpx.AsyncClient, generation_id: str, max_wait: int = 120) -> str:
        """
        Wait for music generation to complete
        """
        start_time = asyncio.get_event_loop().time()

        while True:
            response = await client.get(
                f"{self.base_url}/generate/{generation_id}",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )

            if response.status_code != 200:
                raise Exception("Failed to check music status")

            result = response.json()

            if result["status"] == "completed":
                return result["audio_url"]

            if result["status"] == "failed":
                raise Exception("Music generation failed")

            # Check timeout
            if asyncio.get_event_loop().time() - start_time > max_wait:
                raise Exception("Music generation timeout")

            await asyncio.sleep(3)

    def _create_music_prompt(self, video_prompt: str) -> str:
        """
        Create an appropriate music prompt based on video content
        """
        prompt_lower = video_prompt.lower()

        # Gym/Workout content
        if any(word in prompt_lower for word in ["gym", "workout", "exercise", "fitness", "training"]):
            return "Energetic upbeat electronic gym workout music, motivational, powerful beats, 128 BPM, modern EDM style"

        # Luxury/Lifestyle content
        elif any(word in prompt_lower for word in ["luxury", "miami", "beach", "lifestyle"]):
            return "Smooth modern hip-hop beat, luxury lifestyle vibes, clean production, laid-back but confident"

        # Tutorial/Educational content
        elif any(word in prompt_lower for word in ["tutorial", "how to", "guide", "learn", "explain"]):
            return "Light corporate background music, clean and professional, subtle melody, not distracting"

        # Comedy/Fun content
        elif any(word in prompt_lower for word in ["funny", "comedy", "joke", "fun"]):
            return "Playful upbeat music, fun and quirky, lighthearted melody, modern pop elements"

        # Inspirational content
        elif any(word in prompt_lower for word in ["inspire", "motivation", "success", "dream"]):
            return "Inspirational uplifting music, emotional but powerful, modern cinematic elements, building progression"

        # Default - versatile background music
        else:
            return "Modern versatile background music, clean production, energetic but not overpowering, perfect for social media"
