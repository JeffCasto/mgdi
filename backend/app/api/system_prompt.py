# System prompt/context management module
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import threading

router = APIRouter()


# In-memory storage for system prompts (replace with persistent storage later)
class SystemPrompt(BaseModel):
    """Represents a system prompt.

    Attributes:
        id: The unique ID of the prompt.
        name: The name of the prompt.
        content: The text content of the prompt.
        description: An optional description of the prompt.
    """

    id: int
    name: str
    content: str
    description: Optional[str] = None


class SystemPromptStore:
    """A thread-safe, in-memory store for system prompts."""

    def __init__(self):
        """Initializes the system prompt store."""
        self._prompts = []
        self._lock = threading.Lock()
        self._next_id = 1

    def list_prompts(self) -> List[SystemPrompt]:
        """Lists all system prompts.

        Returns:
            A list of all system prompts.
        """
        return self._prompts.copy()

    def get_prompt(self, prompt_id: int) -> Optional[SystemPrompt]:
        """Gets a system prompt by its ID.

        Args:
            prompt_id: The ID of the prompt to get.

        Returns:
            The system prompt with the given ID, or None if not found.
        """
        for p in self._prompts:
            if p.id == prompt_id:
                return p
        return None

    def add_prompt(self, prompt: SystemPrompt):
        """Adds a system prompt to the store.

        Args:
            prompt: The system prompt to add.
        """
        with self._lock:
            prompt.id = self._next_id
            self._next_id += 1
            self._prompts.append(prompt)

    def update_prompt(self, prompt_id: int, prompt: SystemPrompt):
        """Updates a system prompt.

        Args:
            prompt_id: The ID of the prompt to update.
            prompt: The updated system prompt.

        Returns:
            True if the prompt was updated, False otherwise.
        """
        with self._lock:
            for i, p in enumerate(self._prompts):
                if p.id == prompt_id:
                    self._prompts[i] = prompt
                    return True
            return False

    def delete_prompt(self, prompt_id: int):
        """Deletes a system prompt.

        Args:
            prompt_id: The ID of the prompt to delete.
        """
        with self._lock:
            self._prompts = [p for p in self._prompts if p.id != prompt_id]


prompt_store = SystemPromptStore()


@router.get("/prompts", response_model=List[SystemPrompt])
def list_prompts():
    """Lists all system prompts.

    Returns:
        A list of all system prompts.
    """
    return prompt_store.list_prompts()


@router.get("/prompts/{prompt_id}", response_model=SystemPrompt)
def get_prompt(prompt_id: int):
    """Gets a system prompt by its ID.

    Args:
        prompt_id: The ID of the prompt to get.

    Returns:
        The system prompt with the given ID.

    Raises:
        HTTPException: If the prompt is not found.
    """
    prompt = prompt_store.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@router.post("/prompts", response_model=SystemPrompt)
def create_prompt(prompt: SystemPrompt):
    """Creates a new system prompt.

    Args:
        prompt: The system prompt to create.

    Returns:
        The created system prompt.
    """
    prompt_store.add_prompt(prompt)
    return prompt


@router.put("/prompts/{prompt_id}", response_model=SystemPrompt)
def update_prompt(prompt_id: int, prompt: SystemPrompt):
    """Updates a system prompt.

    Args:
        prompt_id: The ID of the prompt to update.
        prompt: The updated system prompt.

    Returns:
        The updated system prompt.

    Raises:
        HTTPException: If the prompt is not found.
    """
    if not prompt_store.update_prompt(prompt_id, prompt):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@router.delete("/prompts/{prompt_id}")
def delete_prompt(prompt_id: int):
    """Deletes a system prompt.

    Args:
        prompt_id: The ID of the prompt to delete.

    Returns:
        A dictionary with a "result" key indicating that the prompt was deleted.
    """
    prompt_store.delete_prompt(prompt_id)
    return {"result": "deleted"}
