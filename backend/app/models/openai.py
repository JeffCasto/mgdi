import asyncio
from typing import AsyncGenerator, Optional, Dict, Any, List
import openai
from ..config import config
from .base import BaseModelProvider

class OpenAIProvider(BaseModelProvider):
    def __init__(self):
        if not config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
        self.client = openai.AsyncOpenAI(api_key=config.OPENAI_API_KEY)
    
    async def generate(
        self, 
        messages: list[Dict[str, str]], 
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        stream: bool = False,
        **kwargs
    ) -> str | AsyncGenerator[str, None]:
        """Generate text using OpenAI API"""
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=stream,
                **kwargs
            )
            
            if stream:
                return self._stream_response(response)
            else:
                return response.choices[0].message.content
                
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def _stream_response(self, response) -> AsyncGenerator[str, None]:
        """Stream response chunks"""
        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    async def generate_stream(self, messages: List[Dict], **kwargs):
        """Stream text generation"""
        # TODO: Implement streaming for OpenAI
        pass
    
    async def get_embedding(self, text: str) -> List[float]:
        """Generate text embedding for vector storage"""
        try:
            response = await self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"OpenAI embedding error: {str(e)}")
    
    def get_available_models(self) -> list[str]:
        """Get list of available models"""
        return [
            "gpt-4",
            "gpt-4-turbo", 
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k"
        ]
