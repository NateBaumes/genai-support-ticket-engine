import os
import json
from typing import Dict, Any, List
from openai import AsyncOpenAI
from app.core.abstractions import LLMProvider

class OpenAIProvider(LLMProvider):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"
    
    async def classify_ticket(self, text: str) -> Dict[str, Any]:
        prompt = f"""
        Analyze this support ticket. Return ONLY valid JSON with:
        {{"type": "billing|technical|feature_request|other", "sentiment": "positive|neutral|negative"}}
        
        Ticket: {text[:2000]}
        """
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    async def generate_resolution(self, text: str, similar_tickets: List[Dict]) -> str:
        prompt = f"""
        Suggest a resolution for this support ticket (max 150 words):
        
        Ticket: {text[:1500]}
        
        Resolution suggestion:
        """
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=250
        )
        
        return response.choices[0].message.content
