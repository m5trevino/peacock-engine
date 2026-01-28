# 🦅 Peacock Engine V2 (Python Edition) - System Guide

## Project Overview
This is a **headless AI orchestration server** built with Python and FastAPI. It serves as a unified "Tactical Middleware" that sits between your frontend applications (CLI, Web UI, Mobile) and various AI providers (Groq, Google, DeepSeek, Mistral).

### Core Capabilities
1.  **Unified API Gateway**: Routes requests to the correct provider based on `modelId` via the `/v1/strike` endpoint.
2.  **Smart Key Rotation**: Manages pools of API keys for each provider (Groq, Google, DeepSeek, Mistral). It shuffles them on startup and rotates through them for every request.
3.  **Filesystem Access (FS)**: Acts as a bridge to the local filesystem for reading/writing "Ammo" (context files) and "Prompt" templates.
4.  **Proxy Support**: Native support for routing traffic through a proxy server via environment configuration.

## 🛠️ Tech Stack
- **Language**: Python 3.11+
- **Web Framework**: FastAPI
- **Server**: Uvicorn
- **AI Engine**: Pydantic-AI (Unified LLM interface)
- **HTTP Client**: HTTPX (Async requests with proxy support)
- **Configuration**: Pydantic-Settings & python-dotenv
- **Key Management**: Custom `KeyPool` class (Shuffling and Round-Robin rotation)

## 📡 API Endpoints & Port
**Active Port**: `3099`
**Base URL**: `http://localhost:3099`

### 1. Core System
- **`GET /health`**: Checks system status and returns the count of active keys in each provider pool.

### 2. AI Operations
- **`POST /v1/strike`**: Executes a prompt against a specific model.
- **`GET /v1/models`**: Returns the list of all configured models and their gateways.

### 3. Filesystem Bridge
- **`GET /v1/fs/ammo`**: Lists context files in `/home/flintx/ammo`.
- **`GET /v1/fs/ammo/{filename}`**: Reads a specific ammo file.
- **`GET /v1/fs/prompts/{phase}`**: Lists prompt templates for a specific phase.
- **`POST /v1/fs/prompts/{phase}`**: Saves a prompt template.

## 🚀 Setup & Execution

### Environment Variables (.env)
```bash
GROQ_KEYS="key1,key2,வுகளை"
GOOGLE_KEYS="key1,வுகளை"
# etc.
PROXY_URL="http://..."
PROXY_ENABLED="true"
```

### Start Command
```bash
# Ensure venv is active
source .venv/bin/activate

# Run the engine
python -m app.main
```

### Example Usage (cURL)
```bash
curl -X POST http://localhost:3099/v1/strike \
  -H "Content-Type: application/json" \
  -d '{
    "modelId": "llama-3.1-8b-instant",
    "prompt": "How does the key rotation work?",
    "temp": 0.7
  }'
```
