# PEACOCK ENGINE - AI Agent Integration Guide

> **Version**: 3.0.0  
> **Last Updated**: 2026-04-05  
> **Purpose**: Comprehensive guide for AI coding agents integrating with PEACOCK ENGINE

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Wiring PEACOCK ENGINE with OpenClaw](#2-wiring-peacock-engine-with-openclaw)
3. [Technology Stack](#3-technology-stack)
4. [Project Structure](#4-project-structure)
5. [Build and Run Commands](#5-build-and-run-commands)
6. [Code Organization](#6-code-organization)
7. [API Architecture](#7-api-architecture)
8. [Key Concepts](#8-key-concepts)
9. [Development Conventions](#9-development-conventions)
10. [Environment Configuration](#10-environment-configuration)
11. [Testing Strategy](#11-testing-strategy)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. Project Overview

**PEACOCK ENGINE** is a production-grade, headless AI orchestration layer that provides:

- **Unified API**: Single interface for multiple AI providers (Groq, Google Gemini, DeepSeek, Mistral)
- **Key Rotation**: Automatic round-robin with shuffle across multiple API keys per provider
- **Rate Limit Tracking**: Built-in RPM/TPM/RPD tracking per model with real-time meters
- **Forensic Logging**: Dual-track logging with unique PEA-XXXX tags and verbatim vault storage
- **Usage Persistence**: SQLite database tracks key usage over time
- **Fancy CLI Output**: Gateway-specific decorative borders for logs

### Mission

To serve as the central nervous system for all FlintX AI operations, providing forensic logging, financial redlines, and universal integration for any application.

---

## 2. Wiring PEACOCK ENGINE with OpenClaw

This section explains how to integrate PEACOCK ENGINE (ai-handler) with [OpenClaw](https://github.com/openclaw/openclaw) - a personal AI assistant gateway that supports multiple messaging channels.

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              OpenClaw Gateway                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  WhatsApp   │  │  Telegram   │  │   Discord   │  │   Other Channels    │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘ │
│         └─────────────────┴─────────────────┴────────────────────┘           │
│                                    │                                         │
│                         OpenClaw Agent Runtime                               │
│                                    │                                         │
│         ┌──────────────────────────┴────────────────────┐                   │
│         │           PEACOCK ENGINE Provider              │                   │
│         │         (OpenAI-compatible endpoint)           │                   │
│         └──────────────────────────┬────────────────────┘                   │
└────────────────────────────────────┼────────────────────────────────────────┘
                                     │ HTTPS/HTTP
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PEACOCK ENGINE (VPS)                               │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  /v1/chat           - Main chat endpoint                             │  │
│  │  /v1/chat/models    - Model registry                                 │  │
│  │  /health            - Health check                                   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                    │                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │    Groq     │  │   Google    │  │  DeepSeek   │  │   Mistral   │       │
│  │   (Llama)   │  │  (Gemini)   │  │    (V3)     │  │   (Large)   │       │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### OpenClaw Configuration for PEACOCK ENGINE

OpenClaw supports custom OpenAI-compatible providers through its `models.providers` configuration. PEACOCK ENGINE acts as a unified provider that exposes all configured models through a single endpoint.

#### Method 1: Direct Config (Recommended)

Add PEACOCK ENGINE as a custom provider in your OpenClaw config:

```json5
{
  models: {
    mode: "merge",
    providers: {
      peacock: {
        // PEACOCK ENGINE endpoint URL
        baseUrl: "https://your-peacock-domain.com/v1",
        apiKey: "${PEACOCK_API_KEY}",
        api: "openai-completions",
        models: [
          {
            id: "gemini-2.0-flash-lite",
            name: "Gemini 2.0 Flash Lite",
            reasoning: false,
            input: ["text", "image"],
            cost: { input: 0.075, output: 0.30, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 1000000,
            maxTokens: 8192,
          },
          {
            id: "llama-3.3-70b-versatile",
            name: "Llama 3.3 70B",
            reasoning: false,
            input: ["text"],
            cost: { input: 0.59, output: 0.79, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 128000,
            maxTokens: 8192,
          },
          {
            id: "deepseek-chat",
            name: "DeepSeek V3",
            reasoning: true,
            input: ["text"],
            cost: { input: 0.27, output: 1.10, cacheRead: 0.07, cacheWrite: 0.27 },
            contextWindow: 64000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
  agents: {
    defaults: {
      model: { primary: "peacock/gemini-2.0-flash-lite" },
      models: {
        "peacock/gemini-2.0-flash-lite": { alias: "Flash" },
        "peacock/llama-3.3-70b-versatile": { alias: "Llama" },
        "peacock/deepseek-chat": { alias: "DeepSeek" },
      },
    },
  },
}
```

#### Method 2: Environment Variable Setup

Set the PEACOCK API key as an environment variable:

```bash
export PEACOCK_API_KEY="your-peacock-api-key"
# Or if no API key is configured on PEACOCK ENGINE:
export PEACOCK_API_KEY="dummy-key"
```

Then reference it in config:

```json5
{
  models: {
    providers: {
      peacock: {
        baseUrl: "https://your-peacock-domain.com/v1",
        apiKey: "${PEACOCK_API_KEY}",
        api: "openai-completions",
        // ... models definition
      },
    },
  },
}
```

#### Method 3: Using Onboarding

For new OpenClaw setups, you can configure PEACOCK ENGINE during onboarding:

```bash
openclaw onboard --non-interactive \
  --auth-choice custom \
  --custom-base-url "https://your-peacock-domain.com/v1" \
  --custom-model-id "gemini-2.0-flash-lite"
```

### PEACOCK ENGINE Setup for OpenClaw Integration

#### Step 1: Deploy PEACOCK ENGINE

Deploy PEACOCK ENGINE on your VPS (Hetzner, AWS, etc.):

```bash
# On your VPS
ssh root@your-vps-ip
cd /opt/peacock-engine
bash deploy/setup-server.sh
su - peacock -s /bin/bash
cd /opt/peacock-engine
bash deploy/install-app.sh
```

See `deploy/DEPLOYMENT_GUIDE.md` for detailed deployment instructions.

#### Step 2: Configure CORS (if needed)

If OpenClaw connects from a different origin, ensure PEACOCK ENGINE allows CORS:

```python
# In app/main.py (already configured for "*" by default)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to your OpenClaw gateway IP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Step 3: Add API Key (Optional)

If you want to secure PEACOCK ENGINE with an API key:

```env
# In /opt/peacock-engine/.env
API_KEY="your-secure-api-key"
```

Then use this key in OpenClaw's `apiKey` field.

#### Step 4: Verify Connectivity

Test the connection from your OpenClaw host:

```bash
# Test health endpoint
curl https://your-peacock-domain.com/health

# Test model list
curl https://your-peacock-domain.com/v1/chat/models

# Test chat completion
curl -X POST https://your-peacock-domain.com/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "model": "gemini-2.0-flash-lite",
    "prompt": "Hello from OpenClaw!",
    "format": "text"
  }'
```

### Model ID Mapping

PEACOCK ENGINE model IDs map directly to OpenClaw model IDs:

| PEACOCK Model ID | OpenClaw Reference | Gateway |
|-----------------|-------------------|---------|
| `gemini-2.0-flash-lite` | `peacock/gemini-2.0-flash-lite` | google |
| `gemini-2.0-flash` | `peacock/gemini-2.0-flash` | google |
| `llama-3.3-70b-versatile` | `peacock/llama-3.3-70b-versatile` | groq |
| `llama-3.1-8b-instant` | `peacock/llama-3.1-8b-instant` | groq |
| `deepseek-chat` | `peacock/deepseek-chat` | deepseek |
| `deepseek-reasoner` | `peacock/deepseek-reasoner` | deepseek |
| `mistral-large-latest` | `peacock/mistral-large-latest` | mistral |

### Advanced: Key Rotation Awareness

PEACOCK ENGINE automatically rotates API keys. When configured as an OpenClaw provider:

1. **OpenClaw sends request** → PEACOCK ENGINE selects optimal key from pool
2. **Rate limit protection** → ThrottleController manages RPM/TPM/RPD limits
3. **Fallback handling** → If one provider key is exhausted, PEACOCK automatically retries with next key
4. **Logging** → Every request gets a PEA-XXXX tag for forensic tracing

### Security Considerations

1. **HTTPS Only**: Always use HTTPS for production PEACOCK ENGINE deployments
2. **API Key**: Set `API_KEY` in PEACOCK ENGINE `.env` and use it in OpenClaw config
3. **Firewall**: Restrict PEACOCK ENGINE port (3099) to OpenClaw gateway IP only
4. **CORS**: Restrict `allow_origins` in `app/main.py` to your OpenClaw domain

```python
# Secure CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://openclaw.yourdomain.com"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["Authorization", "Content-Type"],
)
```

### Troubleshooting OpenClaw Integration

| Issue | Cause | Solution |
|-------|-------|----------|
| `Connection refused` | PEACOCK ENGINE not running | Check `sudo systemctl status peacock-engine` |
| `401 Unauthorized` | API key mismatch | Verify `API_KEY` in `.env` matches OpenClaw config |
| `404 Not Found` | Wrong endpoint URL | Use `/v1` suffix in `baseUrl` |
| `Unknown model` | Model not in PEACOCK registry | Check available models: `curl /v1/chat/models` |
| Slow responses | Rate limiting | Check `PEACOCK_PERF_MODE` setting |

---

## 3. Technology Stack

| Category | Technology | Version |
|----------|------------|---------|
| **Runtime** | Python | 3.11+ |
| **Web Framework** | FastAPI | Latest |
| **Server** | Uvicorn | Latest |
| **AI Framework** | Pydantic AI | Latest |
| **HTTP Client** | httpx | Latest |
| **Database** | SQLite | Built-in |
| **CLI Output** | rich, questionary | Latest |
| **Environment** | python-dotenv | Latest |

### Supported AI Gateways

| Gateway | Provider | Key Env Var | Models |
|---------|----------|-------------|--------|
| `groq` | Groq | `GROQ_KEYS` | Llama, Qwen, Moonshot/Kimi, GPT-OSS |
| `google` | Google Gemini | `GOOGLE_KEYS` | Gemini 2.0/2.5/3.x series, Embeddings |
| `deepseek` | DeepSeek | `DEEPSEEK_KEYS` | DeepSeek V3, R1 |
| `mistral` | Mistral AI | `MISTRAL_KEYS` | Mistral Large |

---

## 4. Project Structure

```
/home/flintx/ai-handler/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI entry point
│   ├── config.py                 # Model registry & performance modes
│   ├── AGENT_ONBOARDING.md       # Agent onboarding guide
│   ├── TACTICAL_COMMAND.md       # Tactical command reference
│   ├── core/                     # Core business logic
│   │   ├── __init__.py
│   │   ├── key_manager.py        # API key rotation & management
│   │   └── striker.py            # AI execution engine
│   ├── client/                   # Client SDK
│   │   ├── __init__.py
│   │   └── sdk.py
│   ├── db/                       # Database layer
│   │   ├── __init__.py
│   │   └── database.py           # SQLite operations
│   ├── models/                   # Pydantic models
│   │   └── app_profile.py
│   ├── routes/                   # FastAPI route handlers
│   │   ├── chat.py               # Main chat endpoint (/v1/chat)
│   │   ├── strike.py             # Legacy strike endpoint
│   │   ├── payload_strike.py     # Multi-file strikes
│   │   ├── striker.py            # Batch processing endpoints
│   │   ├── models.py             # Model registry endpoint
│   │   ├── keys.py               # Key management endpoints
│   │   ├── fs.py                 # Filesystem bridge
│   │   ├── docs.py               # Documentation endpoints
│   │   ├── profile.py            # Profile/syndicate strikes
│   │   ├── proxy_control.py      # Proxy configuration
│   │   ├── chat_ui.py            # Chat UI API
│   │   ├── dashboard.py          # Dashboard endpoints
│   │   └── onboarding.py         # App onboarding
│   ├── static/                   # Static files for Chat UI
│   └── utils/                    # Utility modules
│       ├── __init__.py
│       ├── formatter.py          # CLI formatting & colors
│       └── logger.py             # High-signal logging
├── deploy/                       # Production deployment files
│   ├── setup-server.sh           # Server preparation script
│   ├── install-app.sh            # Application installation
│   ├── quick-deploy.sh           # One-command deployment
│   ├── peacock-engine.service    # Systemd service definition
│   ├── Caddyfile                 # Reverse proxy config
│   ├── Dockerfile                # Container image
│   ├── docker-compose.yml        # Docker stack
│   └── DEPLOYMENT_GUIDE.md       # Full deployment docs
├── vault/                        # Forensic logging vault
│   ├── successful/               # Successful strike logs (PEA-XXXX.txt)
│   └── failed/                   # Failed strike logs
├── requirements.txt              # Python dependencies
├── ai-engine.py                  # CLI entry point
├── run_engine.sh                 # Production server launcher
├── launch.sh                     # Development server launcher
├── peacock.db                    # SQLite database
├── success_strikes.log           # Master success log
├── failed_strikes.log            # Master failure log
├── manual_strikes.log            # Manual strike log
├── frozen_models.json            # Frozen model registry
└── MISSION_MANIFEST.md           # Project manifest
```

---

## 5. Build and Run Commands

### Setup (First Time)

```bash
# Create virtual environment
python3 -m venv .venv

# Activate
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Server

```bash
# Production launch (recommended)
./run_engine.sh

# Development launch with tunnel support
./launch.sh --tunnel

# Custom port
./launch.sh --port=8080

# Quiet mode (background)
./launch.sh --quiet

# Direct Python execution
python -m app.main
```

### CLI Commands

```bash
# List available models
python ai-engine.py models

# List loaded API keys
python ai-engine.py keys

# Execute a strike
python ai-engine.py strike "Your prompt here" --model gemini-2.0-flash-lite

# Audit model health
python ai-engine.py audit

# Interactive onboarding
python ai-engine.py onboard

# Generate UI flyout snippet
python ai-engine.py flyout-snippet

# Full system diagnostics
python ai-engine.py mission-control

# Show system dossier
python ai-engine.py dossier
```

---

## 6. Code Organization

### Core Modules

| Module | Purpose | Key Classes/Functions |
|--------|---------|----------------------|
| `app/core/key_manager.py` | API key rotation & management | `KeyPool`, `KeyAsset`, `RotationStrategy` |
| `app/core/striker.py` | AI execution engine | `execute_strike()`, `execute_streaming_strike()`, `ThrottleController` |
| `app/config.py` | Model registry & config | `MODEL_REGISTRY`, `ModelConfig`, `PERFORMANCE_MODES` |
| `app/db/database.py` | Database operations | `KeyUsageDB`, `ConversationDB` |
| `app/utils/formatter.py` | CLI output formatting | `CLIFormatter`, `Colors` |
| `app/utils/logger.py` | Forensic logging | `HighSignalLogger` |

### Route Modules

| Route | Endpoint Prefix | Purpose |
|-------|-----------------|---------|
| `chat.py` | `/v1/chat` | Main unified chat endpoint |
| `strike.py` | `/v1/strike` | Legacy strike endpoint |
| `payload_strike.py` | `/v1/payload-strike` | Multi-file context strikes |
| `striker.py` | `/v1/striker/*` | Batch processing |
| `models.py` | `/v1/models` | Model registry |
| `keys.py` | `/v1/keys/*` | Key usage stats |
| `docs.py` | `/v1/docs/*` | API documentation |

---

## 7. API Architecture

### Primary Endpoint: `/v1/chat` (RECOMMENDED)

**Method**: POST  
**Purpose**: Generic, unified endpoint for any model

```bash
curl -X POST http://localhost:3099/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.0-flash-lite",
    "prompt": "Hello, what can you do?",
    "format": "text"
  }'
```

**Request Fields**:
- `model` (required): Model ID from registry
- `prompt` (required): The prompt text
- `files` (optional): Array of file paths to include as context
- `format` (optional): 'text' | 'json' | 'pydantic', default: 'text'
- `schema` (optional): Schema definition for 'pydantic' format
- `temp` (optional): Temperature 0.0-2.0, default: 0.7
- `key` (optional): Specific key account to use (bypasses rotation)
- `timeout` (optional): Timeout in seconds

**Response**:
```json
{
  "content": "Response content",
  "model": "gemini-2.0-flash-lite",
  "gateway": "google",
  "key_used": "PEACOCK_MAIN",
  "format": "text",
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 50,
    "total_tokens": 60
  },
  "duration_ms": 1240
}
```

### Health Check

```bash
curl http://localhost:3099/health
```

### List Models

```bash
curl http://localhost:3099/v1/chat/models
```

### Key Usage Stats

```bash
curl http://localhost:3099/v1/keys/usage
```

---

## 8. Key Concepts

### 8.1 Key Pool System

- **KeyAsset**: A single API key with label/account tracking
- **KeyPool**: A collection of API keys for a gateway with rotation strategy
- **Rotation Strategies**: 
  - `ShuffleStrategy`: Random order (default)
  - `RoundRobinStrategy`: Sequential rotation

### 8.2 The Strike Lifecycle

1. **The Call**: Client sends a prompt to the Engine
2. **The Strategy**: `KeyPool` picks the optimal API key based on rotation strategy
3. **The Throttle**: `ThrottleController` applies rate limiting based on performance mode
4. **The Tunnel**: If enabled, traffic routes through SOCKS5 proxy (127.0.0.1:1081)
5. **The Strike**: `Pydantic AI` executes the prompt against the target model
6. **The Analysis**: Tokens counted, cost calculated, RPM/TPM meters updated
7. **The Vault**: `HighSignalLogger` generates PEA-XXXX tag, saves to vault
8. **The Return**: Response + Tag ID + Usage metrics returned to client

### 8.3 Performance Modes (Hellcat Protocol)

| Mode | Name | Multiplier | Use Case |
|------|------|------------|----------|
| `stealth` | BLACK KEY | 3.0x | Conservative rate limiting |
| `balanced` | BLUE KEY | 1.15x | Default balanced approach |
| `apex` | RED KEY | 1.02x | Aggressive, near-limit |

Set via environment variable: `PEACOCK_PERF_MODE=stealth`

### 8.4 Forensic Logging

Every strike generates:
- **Tag ID**: 8-character unique identifier (PEA-XXXX)
- **Master Log**: Appended to `success_strikes.log` or `failed_strikes.log`
- **Vault File**: Verbatim I/O stored in `vault/successful/` or `vault/failed/`
- **Manual Log**: Manual strikes also logged to `manual_strikes.log`

---

## 9. Development Conventions

### 9.1 Code Style

- **Imports**: Group by standard library, third-party, local (separated by blank line)
- **Type Hints**: Use full type annotations for function signatures
- **Docstrings**: Google-style docstrings for all public functions
- **Line Length**: 100 characters max
- **Quotes**: Double quotes for strings, single quotes for dict keys where appropriate

### 9.2 Error Handling

```python
try:
    result = await execute_strike(...)
except Exception as e:
    # Log the error with tag
    tag = HighSignalLogger.log_strike(..., is_success=False, error=str(e))
    # Re-raise or handle gracefully
    raise HTTPException(status_code=500, detail=str(e))
```

### 9.3 Adding New Endpoints

1. Create route file in `app/routes/my_feature.py`:
```python
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class MyRequest(BaseModel):
    input: str

@router.post("")
async def my_endpoint(request: MyRequest):
    return {"result": f"Processed: {request.input}"}
```

2. Register in `app/main.py`:
```python
from app.routes.my_feature import router as my_feature_router
app.include_router(my_feature_router, prefix="/v1/my-feature", tags=["MY_FEATURE"])
```

3. Add to `app/routes/docs.py` ENDPOINTS list for documentation

### 9.4 Model Registration

Add new models to `app/config.py` MODEL_REGISTRY:

```python
ModelConfig(
    id="model-id",
    gateway="google",  # or groq, deepseek, mistral
    tier="cheap",      # free, cheap, expensive, custom, deprecated
    note="Description",
    rpm=100,           # Requests per minute
    tpm=100000,        # Tokens per minute
    rpd=1000,          # Requests per day
    input_price_1m=0.10,
    output_price_1m=0.30,
    context_window=1000000
)
```

---

## 10. Environment Configuration

Required environment variables (typically in `.env`):

| Variable | Description | Format |
|----------|-------------|--------|
| `GROQ_KEYS` | Comma-separated Groq API keys | `label1:key1,label2:key2` |
| `GOOGLE_KEYS` | Comma-separated Gemini API keys | `label1:key1,label2:key2` |
| `DEEPSEEK_KEYS` | DeepSeek API key | `key` or `label:key` |
| `MISTRAL_KEYS` | Mistral API key | `key` or `label:key` |
| `PROXY_ENABLED` | Enable proxy routing | `true` or `false` |
| `PROXY_URL` | Proxy URL | `http://proxy:port` |
| `PORT` | Server port | `3099` (default) |
| `CHAT_UI_ENABLED` | Enable web chat UI | `true` or `false` |
| `PEACOCK_DEBUG` | Debug logging | `true` or `false` |
| `PEACOCK_VERBOSE` | Verbose output | `true` or `false` |
| `PEACOCK_PERF_MODE` | Performance mode | `stealth`, `balanced`, `apex` |
| `PEACOCK_TUNNEL` | Enable tunnel mode | `true` or `false` |
| `API_KEY` | Optional API key for client auth | `your-secret-key` |

---

## 11. Testing Strategy

### Manual Testing

```bash
# Test health endpoint
curl http://localhost:3099/health

# Test model list
curl http://localhost:3099/v1/chat/models

# Test simple strike
curl -X POST http://localhost:3099/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"model": "gemini-2.0-flash-lite", "prompt": "Hello"}'

# Test with file context
curl -X POST http://localhost:3099/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"model": "gemini-2.0-flash-lite", "prompt": "Review this code", "files": ["/path/to/file.py"]}'
```

### Model Audit

```bash
# Audit all active models
python ai-engine.py audit

# Audit specific gateway
python ai-engine.py audit --gateway google

# Audit specific model
python ai-engine.py audit --id gemini-2.0-flash-lite
```

### Testing OpenClaw Integration

```bash
# From OpenClaw host, test PEACOCK ENGINE connectivity
curl https://your-peacock-domain.com/health

# Test through OpenClaw
openclaw agent --message "Test message" --model peacock/gemini-2.0-flash-lite
```

---

## 12. Troubleshooting

### 12.1 429 Rate Limit Errors

**Cause**: Provider rate limit hit  
**Solution**: PEACOCK automatically rotates keys. The `ThrottleController` proactively manages rate limits based on performance mode.

### 12.2 Key Exhaustion

**Check**: `GET /v1/keys/usage`  
**Solution**: Add more keys to the pool in `.env` file

### 12.3 Model Not Found

**Error**: `400 Unknown model '...'`  
**Solution**: Check available models with `GET /v1/chat/models`

### 12.4 Database Issues

**Check**: Verify `peacock.db` exists and is writable  
**Solution**: Delete `peacock.db` to reinitialize (loses usage history only)

### 12.5 Port Already in Use

The launch scripts automatically kill processes on port 3099. For manual cleanup:
```bash
kill -9 $(lsof -ti:3099)
```

### 12.6 Gemini Token Counting Issues

**Note**: Some Gemini responses may show 0 tokens. This is a known limitation of the Google API. The engine attempts to extract tokens from response metadata when available.

### 12.7 OpenClaw Connection Issues

**Error**: `Connection refused` or `timeout`  
**Solution**: 
- Verify PEACOCK ENGINE is running: `sudo systemctl status peacock-engine`
- Check firewall rules allow OpenClaw host IP
- Verify CORS settings in `app/main.py`
- Test connectivity: `curl -v https://your-peacock-domain.com/health`

---

## Quick Reference

| Task | Command |
|------|---------|
| Start server | `./run_engine.sh` |
| List models | `python ai-engine.py models` |
| Execute strike | `python ai-engine.py strike "prompt" --model gemini-2.0-flash-lite` |
| Audit models | `python ai-engine.py audit` |
| Health check | `curl http://localhost:3099/health` |
| API docs | `curl http://localhost:3099/v1/docs/endpoints` |
| Deploy to VPS | `bash deploy/quick-deploy.sh` |
| Update app | `bash deploy/update.sh` |
| Backup data | `bash deploy/backup.sh` |

---

## Resources

- **OpenClaw Repository**: https://github.com/openclaw/openclaw
- **OpenClaw Docs**: https://docs.openclaw.ai
- **PEACOCK ENGINE Deployment**: See `deploy/DEPLOYMENT_GUIDE.md`
- **Model Registry**: `app/config.py`

---

**END OF DOCUMENT**

For questions or issues, check `/v1/docs/endpoints` for the most up-to-date endpoint list.
