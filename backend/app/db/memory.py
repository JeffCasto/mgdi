# DB memory stub

from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from .config import Base
import uuid
from datetime import datetime


class MemoryEntry(Base):
    """Represents a memory entry in the database.

    Attributes:
        id: The unique ID of the memory entry.
        user_id: The ID of the user who owns the memory.
        content: The text content of the memory.
        embedding: The vector embedding of the memory content.
        entry_metadata: A JSON string of metadata for the memory.
        created_at: The timestamp when the memory was created.
    """

    __tablename__ = "memory_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        String, nullable=False, index=True
    )  # TODO(codex): FK to users table
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1536))  # OpenAI ada-002 dimensions
    entry_metadata = Column(
        Text, nullable=True
    )  # Store as JSON string for tags, context
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Memory {self.id}: {self.content[:50]}...>"
