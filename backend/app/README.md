# Backend for Multimodal ChatGPT Dev App

This backend is built with FastAPI and is designed to support multimodal chat, plugin/function calling, developer workflows, and secure local/proxy deployment.

## Structure
- `main.py`: FastAPI entrypoint
- `api/`: API routers (chat, auth, workflow, plugin)
- `models/`: Model abstraction layer
- `plugins/`: Function calling, code interpreter, image/audio analysis
- `security/`: Auth, encryption, audit
- `db/`: DB config and memory
- `utils/`: Utilities

## Install
```sh
pip install -r app/requirements.txt
```

## Run
```sh
uvicorn app.main:app --reload
```
