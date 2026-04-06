# PEACOCK ENGINE - PROJECT HANDOFF DOCUMENT
> **Single Source of Truth for Any Bot Joining the Project**
> **Version**: 1.0 | **Last Updated**: 2026-04-05

---

## 🎯 PROJECT OVERVIEW

**PEACOCK ENGINE** is a FastAPI-based AI orchestration layer that provides:
- Unified API for multiple AI providers (Google/Gemini, Groq, DeepSeek, Mistral)
- Key rotation with shuffle/round-robin strategies
- Rate limit tracking (RPM/TPM/RPD) per model
- Usage persistence in SQLite database
- Fancy CLI output with gateway-specific styling

**Current Status**: Functional but needs production hardening for VPS deployment
**Goal**: Production-ready system with token counting, validation, tool calling, and WebUI

---

## 📁 CRITICAL FILES TO KNOW

### Core Engine Files
| File | Purpose | What It Does |
|------|---------|--------------|
| `app/main.py` | FastAPI app entry | Routes, middleware, startup |
| `app/config.py` | Configuration | Model registry, performance modes, freeze persistence |
| `app/core/striker.py` | AI execution | Execute strikes (API calls), throttling, rate limiting |
| `app/core/key_manager.py` | Key rotation | KeyPool, rotation strategies, cooldown management |
| `ai-engine.py` | CLI entry | All CLI commands, rich console output |

### Model Registry (`app/config.py`)
- `ModelConfig` Pydantic model defines each model
- `MODEL_REGISTRY` list contains all Google/Groq/DeepSeek/Mistral models
- Models have: `id`, `gateway`, `tier`, `status` (active/frozen/deprecated), `rpm`, `tpm`, `rpd`, pricing
- `FROZEN_IDS` loaded from `frozen_models.json` - models here auto-set to `status="frozen"`

### Key Format (Environment Variables)
```bash
# Format: LABEL:key,LABEL2:key2
GROQ_KEYS="GROQ_01:gsk_abc...,GROQ_02:gsk_def..."
GOOGLE_KEYS="PEACOCK_MAIN:AIza...,BACKUP_01:AIza..."
```

### Database (`app/db/database.py`)
- SQLite database `peacock.db`
- `KeyUsageDB` - tracks usage per key
- `ConversationDB` - stores chat history

---

## 🔧 ARCHITECTURE PATTERNS

### Strike Execution Flow
```
Request → execute_strike() → ThrottleController.wait_if_needed()
                                ↓
                        KeyPool.get_next() → returns KeyAsset
                                ↓
                        Provider setup (GroqProvider/GoogleProvider/etc)
                                ↓
                        Agent.run() → AI model call
                                ↓
                        Usage tracking → KeyUsageDB.record_usage()
                                ↓
                        RateLimitMeter.update()
                                ↓
                        Return result with content, usage, cost, tag
```

### Freeze System
1. Models can be frozen by adding ID to `frozen_models.json`
2. On startup, `FROZEN_IDS` loaded and applied to registry
3. Frozen models skipped in rotation
4. Validation scripts auto-freeze broken/discontinued models

### Rate Limiting
- `ThrottleController` - simple per-gateway throttling (needs improvement)
- `RateLimitMeter` - tracks RPM/TPM in 60-second windows
- Current: Uses global last_strike_time per gateway (NOT per-model)
- Needed: Per-model sliding windows, RPD tracking

---

## ✅ COMPLETED WORK

1. **Basic strike execution** - Works for all 4 gateways
2. **Key rotation** - Shuffle and round-robin strategies
3. **Rate limiting basics** - ThrottleController, RateLimitMeter
4. **CLI framework** - Rich console output, multiple commands
5. **Database** - SQLite with conversation and usage tracking
6. **WebUI skeleton** - Basic HTML/CSS/JS (needs full implementation)
7. **Model registry** - All current models defined with limits
8. **Freeze system** - Basic persistence and status tracking

---

## 🚧 REMAINING WORK (Prioritized)

### P0 - CRITICAL (Must Have for VPS)

#### 1. Token Counting System
**Why**: Current usage tracking is inaccurate (Gemini often returns 0 tokens)

**Gemini Token Counter**:
- Use Google GenAI SDK `count_tokens()` API for accuracy
- Fallback to regex-based estimation (from gemini-tree-token-counter repo)
- Support multimodal: images (258 tokens per tile), video (263/sec), audio (32/sec)
- File: `app/utils/gemini_token_counter.py`

**Groq Token Counter**:
- Use tiktoken library
- Model-to-encoding mapping (cl100k_base for Llama, o200k_base for GPT-OSS)
- Message format overhead: 4 tokens per message + 3 for conversation
- File: `app/utils/groq_token_counter.py`

**Integration**:
- Pre-count tokens before sending requests
- Use count for accurate cost calculation
- Update striker.py to use counters

#### 2. Validation Scripts with Auto-Freeze
**Why**: Need to detect broken/discontinued models automatically

**Google Validator** (`scripts/validate_google.py`):
- Test each key with `genai.Client().models.list()`
- Test each model with simple generation request
- Detect discontinued patterns: "model not found", "deprecated", "404"
- Auto-freeze models that fail with discontinued errors
- Generate rich console report

**Groq Validator** (`scripts/validate_groq.py`):
- Test keys with `/models` endpoint
- Test models with chat completion
- Detect: 404 = discontinued, 503 = at capacity, 429 = rate limited
- Parse rate limit headers from responses
- Auto-freeze discontinued models

**CLI Integration**:
- `ai-engine test google` - Run Google validation
- `ai-engine test groq` - Run Groq validation
- `ai-engine test all` - Test both
- Flags: `--key`, `--model`, `--no-freeze`, `--output`

#### 3. Security & Authentication
**Why**: Required before exposing to internet

- API key middleware for all endpoints (except /health)
- Per-key rate limiting
- Per-IP rate limiting
- Request size limits
- Audit logging

#### 4. VPS Deployment Files
**Why**: Need to actually deploy to server

- Dockerfile (multi-stage, non-root user)
- docker-compose.yml (persistent volumes)
- systemd service file
- Caddyfile (HTTPS, reverse proxy)
- fail2ban config (brute force protection)
- UFW firewall rules

---

### P1 - HIGH (Should Have)

#### 5. Rate Limiting Improvements
- Replace global ThrottleController with per-model sliding windows
- Add RPD (requests per day) tracking with midnight reset
- Add predictive throttling (slow down before hitting limits)
- Parse and respect rate limit headers from providers

#### 6. Tool Calling System
**Why**: Major feature for agent capabilities

**Architecture**:
- `app/core/tools.py` - Tool, ToolCall, ToolResult models
- `ToolRegistry` class for registering/executing tools
- Support OpenAI-compatible function calling format

**Gemini Built-in Tools**:
- google_search, google_maps, code_execution
- url_context, file_search, computer_use

**Groq Tools**:
- Function calling (OpenAI format)
- Built-in: web_search, code_interpreter

**Execution Flow**:
1. Model returns tool call
2. Parse tool call (name + arguments)
3. Execute tool handler
4. Send result back to model
5. Model generates final response

#### 7. WebUI Backend API
**Why**: Frontend needs endpoints for all features

**Required Endpoints**:
- `POST /v1/chat` - Already exists, enhance with tool support
- `GET /v1/models` - List all models with full details
- `POST /v1/models/{id}/freeze` - Freeze/unfreeze models
- `GET /v1/keys` - List keys with health status
- `POST /v1/keys` - Add/delete keys
- `POST /v1/tokens/count` - Count tokens for text
- `GET /v1/costs/daily` - Cost analytics
- `GET /v1/health` - Detailed health check
- `GET /v1/logs` - Request/error logs
- WebSocket for real-time updates

#### 8. Monitoring & Alerting
- Metrics collection (requests, tokens, latency, errors)
- Alert triggers (key exhaustion, rate limits, cost thresholds)
- Webhook notifications
- Health dashboard endpoint

---

### P2 - MEDIUM (Nice to Have)

#### 9. CLI Improvements
- Rich visual polish (tables, spinners, progress bars)
- `ai-engine doctor` - Diagnostic & auto-fix
- `ai-engine mission-control --watch` - Live dashboard
- `ai-engine freeze/unfreeze` commands

#### 10. Advanced Features
- Batch request processing
- Prompt templates library
- Structured output (JSON/Pydantic) enhancements
- JWT authentication option

---

## 📚 REFERENCE MATERIALS

### Documentation Files in Repo
| File | Contains |
|------|----------|
| `AGENTS.md` | API integration guide for external apps |
| `PRODUCTION_TASK_BREAKDOWN.md` | Complete 9-section task breakdown |
| `WEBUI_FEATURE_SPEC.md` | WebUI feature specification for designers |
| `PEACOCK_ENGINE_REFERENCE.md` | Technical reference |

### External Resources
- **Gemini Token Counter Logic**: `/recon/gemini/gemini-tree-token-counter/`
- **Groq Token Counter Logic**: `/recon/groq/CustomGroqChat/`
- **Gemini Docs**: Token counting, tool calling, Interactions API
- **Groq Docs**: Rate limits, models, OpenAI compatibility

---

## 🧪 TESTING APPROACH

1. **Unit Tests**: Token counter accuracy, rate limiter edge cases
2. **Integration Tests**: Full strike lifecycle, validation scripts
3. **End-to-End**: Deploy to staging, run full workload

---

## 🚨 COMMON PITFALLS

1. **Token Counting**: Gemini API sometimes returns 0 tokens - always have fallback estimation
2. **Rate Limits**: Groq uses different headers than Gemini - parse both
3. **Key Rotation**: All keys might be on cooldown - handle gracefully
4. **Model Freezing**: Don't freeze for temporary errors (429, 503) - only permanent (404, discontinued)
5. **Tool Calling**: Different formats for Gemini vs Groq - normalize to OpenAI format

---

## 💬 QUESTIONS? ASK ABOUT:

- Current file structure and where things live
- How the key rotation works
- Model registry format
- Rate limiting strategy
- Token counting implementation details
- Tool calling flow
- Deployment requirements

---

**END OF HANDOFF DOCUMENT**

*This document + PRODUCTION_TASK_BREAKDOWN.md + WEBUI_FEATURE_SPEC.md = Complete project context*
