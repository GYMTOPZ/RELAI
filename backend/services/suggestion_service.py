import os
from openai import AsyncOpenAI
from typing import List, Optional

class SuggestionService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def generate_suggestions(
        self,
        context: str,
        user_preferences: Optional[str] = None
    ) -> List[dict]:
        """
        Generate creative video ideas for social media content
        Uses GPT-4 to create engaging, trendy suggestions
        """
        try:
            # Build the prompt for GPT
            system_prompt = """You are a creative social media content strategist specializing in viral video ideas.
Generate engaging, creative video concepts that work well with AI video generation (Sora 2).

For each suggestion, provide:
1. A catchy title
2. A detailed scene description (be specific about actions, settings, clothing, props)
3. Estimated duration (15-60 seconds)
4. Platform recommendations (TikTok, Instagram Reels, YouTube Shorts)
5. Hashtag suggestions

Focus on:
- Trendy, viral-worthy concepts
- Clear, filmable scenes
- Engaging hooks in the first 3 seconds
- Content that showcases personality and expertise
- Ideas that work well with AI generation (no complex face-to-face interactions)
"""

            user_prompt = f"""Generate 5 creative video ideas based on this context:

Context: {context}

{f"User preferences: {user_preferences}" if user_preferences else ""}

Make the ideas specific, actionable, and perfect for social media. Include interesting details like specific locations, clothing, props, or scenarios that make the content unique and engaging.

Format each suggestion as:
Title: [catchy title]
Description: [detailed scene description for AI video generation]
Duration: [seconds]
Platforms: [best platforms]
Hashtags: [5 relevant hashtags]
Hook: [first 3 seconds description]
"""

            # Call GPT-4
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=2000
            )

            # Parse response into structured suggestions
            suggestions_text = response.choices[0].message.content
            suggestions = self._parse_suggestions(suggestions_text)

            return suggestions

        except Exception as e:
            raise Exception(f"Error generating suggestions: {str(e)}")

    def _parse_suggestions(self, text: str) -> List[dict]:
        """
        Parse GPT response into structured suggestion objects
        """
        suggestions = []
        current_suggestion = {}

        lines = text.split("\n")

        for line in lines:
            line = line.strip()

            if line.startswith("Title:"):
                # Save previous suggestion if exists
                if current_suggestion:
                    suggestions.append(current_suggestion)
                current_suggestion = {"title": line.replace("Title:", "").strip()}

            elif line.startswith("Description:"):
                current_suggestion["description"] = line.replace("Description:", "").strip()

            elif line.startswith("Duration:"):
                duration_text = line.replace("Duration:", "").strip()
                # Extract number
                try:
                    current_suggestion["duration"] = int(''.join(filter(str.isdigit, duration_text)))
                except:
                    current_suggestion["duration"] = 30

            elif line.startswith("Platforms:"):
                platforms_text = line.replace("Platforms:", "").strip()
                current_suggestion["platforms"] = [p.strip() for p in platforms_text.split(",")]

            elif line.startswith("Hashtags:"):
                hashtags_text = line.replace("Hashtags:", "").strip()
                current_suggestion["hashtags"] = [h.strip() for h in hashtags_text.split(",")]

            elif line.startswith("Hook:"):
                current_suggestion["hook"] = line.replace("Hook:", "").strip()

        # Add last suggestion
        if current_suggestion:
            suggestions.append(current_suggestion)

        return suggestions

    async def enhance_prompt(self, basic_prompt: str) -> str:
        """
        Enhance a user's basic prompt with more details for better Sora generation
        """
        try:
            system_prompt = """You are an expert at creating detailed prompts for AI video generation.
Transform basic video ideas into detailed, specific prompts that will produce high-quality results.

Include details about:
- Camera angles and movements
- Lighting conditions
- Specific actions and movements
- Environment details
- Clothing and appearance details
- Mood and atmosphere
- Pacing and timing

Keep the enhanced prompt clear and concise but detailed."""

            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Enhance this video prompt: {basic_prompt}"}
                ],
                temperature=0.7,
                max_tokens=500
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            # If enhancement fails, return original prompt
            return basic_prompt
