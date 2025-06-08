# FastAPI entrypoint
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .api import chat, auth, workflow, plugin, system_prompt, memory
from .config import config
from dotenv import load_dotenv
import os
import logging

# Load .env file on startup
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MGDI API",
    description="Multimodal GPT Dev Interface",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}

# API Routers
app.include_router(system_prompt.router, prefix='/api/system', tags=["System"])
app.include_router(chat.router, prefix='/api/chat', tags=["Chat"])
app.include_router(auth.router, prefix='/api/auth', tags=["Auth"])
app.include_router(workflow.router, prefix='/api/workflow', tags=["Workflow"])
app.include_router(plugin.router, prefix='/api/plugin', tags=["Plugin"])
app.include_router(memory.router, prefix='/api/memory', tags=["Memory"])

# Serve static files for frontend
if os.path.exists("../frontend/dist"):
    app.mount("/static", StaticFiles(directory="../frontend/dist"), name="static")
    
    @app.get("/")
    async def serve_frontend():
        return FileResponse("../frontend/dist/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
