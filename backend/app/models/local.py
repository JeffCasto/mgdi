# Local model provider stub
from .base import BaseModelProvider

from typing import AsyncGenerator, Dict


class LocalProvider(BaseModelProvider):
    """A provider for local models.

    This is a stub for a local model provider.
    """

    async def generate(
        self,
        messages: list[Dict[str, str]],
        model: str,
        max_tokens: int,
        temperature: float,
        stream: bool = False,
        **kwargs
    ) -> str | AsyncGenerator[str, None]:
        """Generates a response from the local model.

        Args:
            messages: A list of messages in the conversation.
            model: The model to use for the chat.
            max_tokens: The maximum number of tokens to generate.
            temperature: The temperature for the generation.
            stream: Whether to stream the response.
            **kwargs: Additional keyword arguments to pass to the model.

        Returns:
            The generated text, or an async generator of text chunks if streaming.
        """
        return "Local model response"

    def get_available_models(self) -> list[str]:
        """Gets a list of available models for this provider.

        Returns:
            A list of available models.
        """
        return ["local-model"]
