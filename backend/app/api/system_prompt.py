# System prompt/context management module
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import threading

router = APIRouter()

# In-memory storage for system prompts (replace with persistent storage later)
class SystemPrompt(BaseModel):
    id: int
    name: str
    content: str
    description: Optional[str] = None

class SystemPromptStore:
    def __init__(self):
        self._prompts = []
        self._lock = threading.Lock()
        self._next_id = 1

    def list_prompts(self) -> List[SystemPrompt]:
        return self._prompts.copy()

    def get_prompt(self, prompt_id: int) -> Optional[SystemPrompt]:
        for p in self._prompts:
            if p.id == prompt_id:
                return p
        return None

    def add_prompt(self, prompt: SystemPrompt):
        with self._lock:
            prompt.id = self._next_id
            self._next_id += 1
            self._prompts.append(prompt)

    def update_prompt(self, prompt_id: int, prompt: SystemPrompt):
        with self._lock:
            for i, p in enumerate(self._prompts):
                if p.id == prompt_id:
                    self._prompts[i] = prompt
                    return True
            return False

    def delete_prompt(self, prompt_id: int):
        with self._lock:
            self._prompts = [p for p in self._prompts if p.id != prompt_id]

prompt_store = SystemPromptStore()

@router.get("/prompts", response_model=List[SystemPrompt])
def list_prompts():
    return prompt_store.list_prompts()

@router.get("/prompts/{prompt_id}", response_model=SystemPrompt)
def get_prompt(prompt_id: int):
    prompt = prompt_store.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

@router.post("/prompts", response_model=SystemPrompt)
def create_prompt(prompt: SystemPrompt):
    prompt_store.add_prompt(prompt)
    return prompt

@router.put("/prompts/{prompt_id}", response_model=SystemPrompt)
def update_prompt(prompt_id: int, prompt: SystemPrompt):
    if not prompt_store.update_prompt(prompt_id, prompt):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

@router.delete("/prompts/{prompt_id}")
def delete_prompt(prompt_id: int):
    prompt_store.delete_prompt(prompt_id)
    return {"result": "deleted"}
