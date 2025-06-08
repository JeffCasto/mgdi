# DB memory stub

from sqlalchemy import Column, Integer, String, DateTime, Text, func
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from .config import Base
import uuid
from datetime import datetime

class MemoryEntry(Base):
    __tablename__ = "memory_entries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False, index=True)  # TODO: FK to users table
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1536))  # OpenAI ada-002 dimensions
    entry_metadata = Column(Text, nullable=True)  # Store as JSON string for tags, context
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Memory {self.id}: {self.content[:50]}...>"
