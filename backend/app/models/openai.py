from typing import AsyncGenerator, Dict, List
import openai
from ..config import config
from .base import BaseModelProvider


class OpenAIProvider(BaseModelProvider):
    """A provider for the OpenAI API.

    This class provides methods for generating text, getting embeddings, and
    getting available models from the OpenAI API.
    """

    def __init__(self):
        """Initializes the OpenAI provider.

        Raises:
            ValueError: If the OPENAI_API_KEY is not set.
        """
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
        **kwargs,
    ) -> str | AsyncGenerator[str, None]:
        """Generates text using the OpenAI API.

        Args:
            messages: A list of messages in the conversation.
            model: The model to use for the chat.
            max_tokens: The maximum number of tokens to generate.
            temperature: The temperature for the generation.
            stream: Whether to stream the response.
            **kwargs: Additional keyword arguments to pass to the OpenAI API.

        Returns:
            The generated text, or an async generator of text chunks if streaming.

        Raises:
            Exception: If an error occurs with the OpenAI API.
        """
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=stream,
                **kwargs,
            )

            if stream:
                return self._handle_stream(response)
            else:
                return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    async def get_embedding(self, text: str) -> List[float]:
        """Generates a text embedding for vector storage.

        Args:
            text: The text to get an embedding for.

        Returns:
            A list of floats representing the embedding.

        Raises:
            Exception: If an error occurs with the OpenAI API.
        """
        try:
            response = await self.client.embeddings.create(
                model="text-embedding-ada-002", input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"OpenAI embedding error: {str(e)}")

    def get_available_models(self) -> list[str]:
        """Gets a list of available models from the OpenAI API.

        Returns:
            A list of available models.
        """
        return ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"]
