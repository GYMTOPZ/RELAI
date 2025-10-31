import os
import uuid
from pathlib import Path
from elevenlabs import VoiceSettings
from elevenlabs.client import AsyncElevenLabs

class VoiceService:
    def __init__(self):
        self.client = AsyncElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        self.output_dir = Path("uploads/voices")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def generate_voice(self, text: str, voice_id: str = "EXAVITQu4vr4xnSDxMaL") -> str:
        """
        Generate AI voice narration for the video
        Uses ElevenLabs API to generate natural-sounding voice
        Default voice: "Sarah" - professional, clear female voice
        """
        try:
            # Extract key information from prompt to create narration
            narration_text = self._create_narration(text)

            # Generate audio
            audio_generator = await self.client.text_to_speech.convert(
                voice_id=voice_id,
                text=narration_text,
                model_id="eleven_multilingual_v2",
                voice_settings=VoiceSettings(
                    stability=0.5,
                    similarity_boost=0.75,
                    style=0.5,
                    use_speaker_boost=True
                )
            )

            # Save audio file
            audio_id = str(uuid.uuid4())
            audio_path = self.output_dir / f"voice_{audio_id}.mp3"

            # Write the audio stream to file
            with open(audio_path, "wb") as f:
                async for chunk in audio_generator:
                    if chunk:
                        f.write(chunk)

            return str(audio_path)

        except Exception as e:
            raise Exception(f"Error generating voice: {str(e)}")

    async def clone_voice(self, voice_sample_path: str, text: str) -> str:
        """
        Clone user's voice and generate narration
        """
        try:
            # Create narration from prompt
            narration_text = self._create_narration(text)

            # Upload voice sample and create voice clone
            with open(voice_sample_path, "rb") as f:
                voice_data = f.read()

            # Add voice to library (voice cloning)
            voice = await self.client.voices.add(
                name=f"user_voice_{uuid.uuid4().hex[:8]}",
                files=[voice_data]
            )

            # Generate audio with cloned voice
            audio_generator = await self.client.text_to_speech.convert(
                voice_id=voice.voice_id,
                text=narration_text,
                model_id="eleven_multilingual_v2"
            )

            # Save audio
            audio_id = str(uuid.uuid4())
            audio_path = self.output_dir / f"voice_cloned_{audio_id}.mp3"

            with open(audio_path, "wb") as f:
                async for chunk in audio_generator:
                    if chunk:
                        f.write(chunk)

            return str(audio_path)

        except Exception as e:
            raise Exception(f"Error cloning voice: {str(e)}")

    def _create_narration(self, prompt: str) -> str:
        """
        Create a natural narration script from the video prompt
        This extracts the key points and creates engaging narration
        """
        # For now, we'll use a simple extraction
        # In production, you might want to use GPT to create better narration

        # Simple narration template
        if "gym" in prompt.lower() or "workout" in prompt.lower():
            narration = f"Hey everyone! Today I'm showing you an amazing workout. {prompt}. Let's get started and crush this training session!"
        elif "exercise" in prompt.lower():
            narration = f"What's up! Ready for today's exercise routine? {prompt}. Let's do this together!"
        else:
            narration = f"Hello! Check out what I've got for you today. {prompt}. Stay tuned and don't forget to like and subscribe!"

        return narration

    async def get_available_voices(self):
        """
        Get list of available AI voices from ElevenLabs
        """
        try:
            voices = await self.client.voices.get_all()
            return [{"id": v.voice_id, "name": v.name} for v in voices.voices]
        except Exception as e:
            raise Exception(f"Error getting voices: {str(e)}")
