from typing import AsyncGenerator, Dict, Any
import anthropic
from ..config import config
from .base import BaseModelProvider

class AnthropicProvider(BaseModelProvider):
    def __init__(self):
        if not config.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is required")
        self.client = anthropic.AsyncAnthropic(api_key=config.ANTHROPIC_API_KEY)
    
    async def generate(
        self, 
        messages: list[Dict[str, str]], 
        model: str = "claude-3-haiku-20240307",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        stream: bool = False,
        **kwargs
    ) -> str | AsyncGenerator[str, None]:
        """Generate text using Anthropic API"""
        try:
            # Convert messages to Anthropic format
            system_messages = [m for m in messages if m["role"] == "system"]
            user_messages = [m for m in messages if m["role"] != "system"]
            
            system_prompt = "\n".join([m["content"] for m in system_messages]) if system_messages else None
            
            response = await self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=user_messages,
                stream=stream,
                **kwargs
            )
            
            if stream:
                return self._stream_response(response)
            else:
                return response.content[0].text
                
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    async def _stream_response(self, response) -> AsyncGenerator[str, None]:
        """Stream response chunks"""
        async for chunk in response:
            if chunk.type == "content_block_delta":
                yield chunk.delta.text
    
    def get_available_models(self) -> list[str]:
        """Get list of available models"""
        return [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229", 
            "claude-3-haiku-20240307"
        ]
