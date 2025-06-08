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
    content: str
    metadata: Optional[dict] = None

class MemoryResponse(BaseModel):
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
    """Store memory with vector embedding"""
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
    """Vector similarity search"""
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
    """Get chronological memory timeline"""
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
