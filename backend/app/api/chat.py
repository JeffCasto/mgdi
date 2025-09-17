import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from ..models.openai import OpenAIProvider
from ..models.anthropic import AnthropicProvider
from ..config import config

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize providers (with graceful fallback if API keys missing)
PROVIDERS = {}
try:
    PROVIDERS["openai"] = OpenAIProvider()
except ValueError as e:
    logger.warning(f"OpenAI provider disabled: {e}")

try:
    PROVIDERS["anthropic"] = AnthropicProvider()
except ValueError as e:
    logger.warning(f"Anthropic provider disabled: {e}")

class ChatMessage(BaseModel):
    """Represents a single message in a chat conversation.

    Attributes:
        role: The role of the message sender (e.g., 'user', 'assistant', 'system').
        content: The text content of the message.
    """
    role: str  # 'user', 'assistant', 'system'
    content: str
    
class ChatRequest(BaseModel):
    """Represents a request to the chat endpoint.

    Attributes:
        messages: A list of messages in the conversation.
        model: The model to use for the chat.
        max_tokens: The maximum number of tokens to generate.
        temperature: The temperature for the generation.
        provider: The provider to use for the chat (e.g., 'openai', 'anthropic').
        stream: Whether to stream the response.
    """
    messages: List[ChatMessage]
    model: str = config.DEFAULT_MODEL
    max_tokens: int = config.MAX_TOKENS
    temperature: float = config.TEMPERATURE
    provider: str = "openai"
    stream: bool = False
    
class ChatResponse(BaseModel):
    """Represents a response from the chat endpoint.

    Attributes:
        content: The content of the response.
        model: The model used for the chat.
        provider: The provider used for the chat.
        metadata: A dictionary of metadata about the response.
    """
    content: str
    model: str
    provider: str
    metadata: Dict[str, Any] = {}

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    """Processes a chat request with the selected AI provider.

    This endpoint takes a chat request, selects the appropriate provider,
    and then generates a response. It supports both streaming and non-streaming
    responses.

    Args:
        req: The chat request.

    Returns:
        A `ChatResponse` object with the generated content, or a
        `StreamingResponse` if streaming is enabled.

    Raises:
        HTTPException: If the provider is not supported or if an error occurs
            during chat processing.
    """
    provider_name = req.provider.lower()
    if provider_name not in PROVIDERS:
        raise HTTPException(
            status_code=400, 
            detail=f"Provider '{provider_name}' not supported or not configured."
        )
    
    provider = PROVIDERS[provider_name]
    
    try:
        # Convert messages to dict format
        messages = [{
            "role": msg.role,
            "content": msg.content
        } for msg in req.messages]
        
        if req.stream:
            # Return streaming response
            async def generate_stream():
                async for chunk in await provider.generate(
                    messages=messages,
                    model=req.model,
                    max_tokens=req.max_tokens,
                    temperature=req.temperature,
                    stream=True
                ):
                    yield f"data: {chunk}\n\n"
                yield "data: [DONE]\n\n"
            
            return StreamingResponse(
                generate_stream(),
                media_type="text/plain",
                headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
            )
        else:
            # Non-streaming response
            content = await provider.generate(
                messages=messages,
                model=req.model,
                max_tokens=req.max_tokens,
                temperature=req.temperature,
                stream=False
            )
            
            return ChatResponse(
                content=content,
                model=req.model,
                provider=provider_name,
                metadata={"tokens": len(content.split()) if content else 0}
            )
            
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/providers")
async def list_providers():
    """Lists the available chat model providers and their models.

    Returns:
        A dictionary containing information about the available providers.
    """
    provider_info = {}
    for name, provider in PROVIDERS.items():
        try:
            provider_info[name] = {
                "available": True,
                "models": provider.get_available_models()
            }
        except Exception as e:
            provider_info[name] = {
                "available": False,
                "error": str(e)
            }
    
    return {"providers": provider_info}

@router.get("/models")
async def list_models():
    """Lists all available models across all providers.

    Returns:
        A dictionary containing a list of all available models.
    """
    all_models = []
    for provider_name, provider in PROVIDERS.items():
        try:
            models = provider.get_available_models()
            for model in models:
                all_models.append({
                    "id": model,
                    "provider": provider_name,
                    "name": model
                })
        except Exception as e:
            logger.warning(f"Error getting models for {provider_name}: {e}")
    
    return {"models": all_models}
