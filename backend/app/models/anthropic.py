from typing import AsyncGenerator, Dict, Any
import anthropic
from ..config import config
from .base import BaseModelProvider

class AnthropicProvider(BaseModelProvider):
    """A provider for the Anthropic API.

    This class provides methods for generating text and getting available models
    from the Anthropic API.
    """
    def __init__(self):
        """Initializes the Anthropic provider.

        Raises:
            ValueError: If the ANTHROPIC_API_KEY is not set.
        """
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
        """Generates text using the Anthropic API.

        Args:
            messages: A list of messages in the conversation.
            model: The model to use for the chat.
            max_tokens: The maximum number of tokens to generate.
            temperature: The temperature for the generation.
            stream: Whether to stream the response.
            **kwargs: Additional keyword arguments to pass to the Anthropic API.

        Returns:
            The generated text, or an async generator of text chunks if streaming.

        Raises:
            Exception: If an error occurs with the Anthropic API.
        """
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
    
    async def _stream_response(self, response: AsyncGenerator) -> AsyncGenerator[str, None]:
        """Streams response chunks from the Anthropic API.

        Args:
            response: The response from the Anthropic API.

        Yields:
            Text chunks from the response.
        """
        async for chunk in response:
            if chunk.type == "content_block_delta":
                yield chunk.delta.text

    def get_available_models(self) -> list[str]:
        """Gets a list of available models from the Anthropic API.

        Returns:
            A list of available models.
        """
        return [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229", 
            "claude-3-haiku-20240307"
        ]
