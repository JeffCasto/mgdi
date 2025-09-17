from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from pydantic import BaseModel
from typing import List, Optional
from ..db.config import get_db
from ..db.memory import MemoryEntry
from ..models.openai import OpenAIProvider
import json

router = APIRouter()

class MemoryRequest(BaseModel):
    """Represents a request to store a memory.

    Attributes:
        content: The text content of the memory.
        metadata: An optional dictionary of metadata for the memory.
    """
    content: str
    metadata: Optional[dict] = None

class MemoryResponse(BaseModel):
    """Represents a memory returned from the API.

    Attributes:
        id: The unique ID of the memory.
        content: The text content of the memory.
        metadata: A dictionary of metadata for the memory.
        created_at: The timestamp when the memory was created.
        similarity: The similarity score of the memory to a search query.
    """
    id: str
    content: str
    metadata: dict
    created_at: str
    similarity: Optional[float] = None

@router.post("/store", response_model=MemoryResponse)
async def store_memory(
    memory: MemoryRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = "default"  # TODO: Extract from JWT
):
    """Stores a memory with a vector embedding.

    Args:
        memory: The memory to store.
        db: The database session.
        user_id: The ID of the user who owns the memory.

    Returns:
        The stored memory.

    Raises:
        HTTPException: If the memory storage fails.
    """
    try:
        # Generate embedding
        provider = OpenAIProvider()
        embedding = await provider.get_embedding(memory.content)
        
        # Create entry
        entry = MemoryEntry(
            user_id=user_id,
            content=memory.content,
            embedding=embedding,
            entry_metadata=json.dumps(memory.metadata) if memory.metadata else None,
        )
        
        db.add(entry)
        await db.commit()
        await db.refresh(entry)
        
        return MemoryResponse(
            id=str(entry.id),
            content=entry.content,
            metadata=json.loads(entry.metadata),
            created_at=entry.created_at.isoformat()
        )
    except Exception as e:
        raise HTTPException(500, f"Memory storage failed: {str(e)}")

@router.get("/search", response_model=List[MemoryResponse])
async def search_memories(
    query: str,
    limit: int = 10,
    threshold: float = 0.8,
    db: AsyncSession = Depends(get_db),
    user_id: str = "default"  # TODO: Extract from JWT
):
    """Performs a vector similarity search for memories.

    Args:
        query: The search query.
        limit: The maximum number of memories to return.
        threshold: The similarity threshold.
        db: The database session.
        user_id: The ID of the user who owns the memories.

    Returns:
        A list of memories that match the search query.

    Raises:
        HTTPException: If the memory search fails.
    """
    try:
        # Generate query embedding
        provider = OpenAIProvider()
        query_embedding = await provider.get_embedding(query)
        
        # Vector search with similarity
        sql = text("""
            SELECT id, content, metadata, created_at,
                   1 - (embedding <=> :query_embedding) as similarity
            FROM memory_entries
            WHERE user_id = :user_id
              AND 1 - (embedding <=> :query_embedding) > :threshold
            ORDER BY similarity DESC
            LIMIT :limit
        """)
        
        result = await db.execute(sql, {
            "query_embedding": query_embedding,
            "user_id": user_id,
            "threshold": threshold,
            "limit": limit
        })
        
        memories = []
        for row in result:
            memories.append(MemoryResponse(
                id=str(row.id),
                content=row.content,
                metadata=json.loads(row.metadata),
                created_at=row.created_at.isoformat(),
                similarity=float(row.similarity)
            ))
        
        return memories
        
    except Exception as e:
        raise HTTPException(500, f"Memory search failed: {str(e)}")

@router.get("/timeline", response_model=List[MemoryResponse])
async def get_timeline(
    db: AsyncSession = Depends(get_db),
    user_id: str = "default",  # TODO: Extract from JWT
    limit: int = 50
):
    """Gets a chronological timeline of memories.

    Args:
        db: The database session.
        user_id: The ID of the user who owns the memories.
        limit: The maximum number of memories to return.

    Returns:
        A list of memories in reverse chronological order.

    Raises:
        HTTPException: If the timeline fetch fails.
    """
    try:
        stmt = (
            select(MemoryEntry)
            .where(MemoryEntry.user_id == user_id)
            .order_by(MemoryEntry.created_at.desc())
            .limit(limit)
        )
        
        result = await db.execute(stmt)
        entries = result.scalars().all()
        
        return [
            MemoryResponse(
                id=str(entry.id),
                content=entry.content,
                metadata=json.loads(entry.metadata),
                created_at=entry.created_at.isoformat()
            )
            for entry in entries
        ]
        
    except Exception as e:
        raise HTTPException(500, f"Timeline fetch failed: {str(e)}")
