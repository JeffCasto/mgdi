from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Any

class BaseModelProvider(ABC):
    """Base class for all model providers"""
    
    @abstractmethod
    async def generate(
        self, 
        messages: list[Dict[str, str]], 
        model: str,
        max_tokens: int,
        temperature: float,
        stream: bool = False,
        **kwargs
    ) -> str | AsyncGenerator[str, None]:
        """Generate text response from the model"""
        raise NotImplementedError
    
    @abstractmethod
    def get_available_models(self) -> list[str]:
        """Get list of available models for this provider"""
        raise NotImplementedError
