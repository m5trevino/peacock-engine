# PEACOCK ENGINE - PRODUCTION DEPLOYMENT TASK BREAKDOWN
> **Complete Task List for VPS-Ready System**
> **Version**: 4.1.0 | **Date**: 2026-04-05 | **Status**: Planning

---

## 📋 EXECUTIVE SUMMARY

**Total Estimated Effort**: ~2-3 weeks of focused development
**Priority Order**: Core → Testing → WebUI → Security → Deployment
**Critical Path**: Token Counters → Validators → Tool Calling → WebUI API → Security → VPS Deploy

---

## 🎯 SECTION 1: CORE ENGINE FOUNDATION (Week 1)

### 1.1 Token Counting System

#### 1.1.1 Gemini Token Counter
- [ ] Create `app/utils/gemini_token_counter.py`
- [ ] Implement Google GenAI SDK `count_tokens()` API method
- [ ] Implement offline regex-based estimation fallback (from gemini-tree-token-counter)
- [ ] Add multimodal token calculation (images, video, audio, PDF)
- [ ] Create token counting endpoint in API
- [ ] Add token pre-count before sending requests
- [ ] Integrate into striker.py for accurate usage tracking

**Files to Create/Modify:**
- `app/utils/gemini_token_counter.py` (NEW)
- `app/core/striker.py` (MODIFY - integrate token counter)

#### 1.1.2 Groq Token Counter  
- [ ] Create `app/utils/groq_token_counter.py`
- [ ] Implement tiktoken integration
- [ ] Create model-to-encoding mapping (MODEL_ENCODING_MAP)
- [ ] Implement message format overhead calculations
- [ ] Add tool definition token counting
- [ ] Add batch request token counting
- [ ] Integrate into striker.py

**Files to Create/Modify:**
- `app/utils/groq_token_counter.py` (NEW)
- `app/core/striker.py` (MODIFY)

#### 1.1.3 Unified Token Counter Interface
- [ ] Create `app/utils/token_counter.py` (unified interface)
- [ ] Add provider detection (auto-select Gemini vs Groq counter)
- [ ] Add cost estimation using model pricing from registry
- [ ] Create `/v1/tokens/count` API endpoint
- [ ] Add token counting to CLI (`ai-engine tokens count`)

**Files to Create:**
- `app/utils/token_counter.py` (NEW)
- `app/routes/tokens.py` (NEW)

---

### 1.2 Rate Limiting & Throttling Improvements

#### 1.2.1 Per-Model Rate Limiting
- [ ] Replace gateway-level ThrottleController with per-model tracking
- [ ] Implement sliding window rate limiter (vs current simple timestamp)
- [ ] Add RPD (requests per day) tracking with daily reset
- [ ] Add per-key rate limit tracking (not just per-gateway)
- [ ] Implement predictive throttling (slow down before hitting limits)

**Files to Modify:**
- `app/core/striker.py` (MODIFY ThrottleController)
- `app/core/rate_limiter.py` (NEW - AdvancedRateLimiter class)

#### 1.2.2 Rate Limit Response Handling
- [ ] Parse rate limit headers from Groq (x-ratelimit-*)
- [ ] Parse rate limit info from Gemini responses
- [ ] Implement automatic backoff with exponential retry
- [ ] Add jitter to prevent thundering herd
- [ ] Mark keys on cooldown automatically

**Files to Modify:**
- `app/core/striker.py` (MODIFY retry logic)
- `app/core/key_manager.py` (MODIFY cooldown handling)

---

### 1.3 Key Manager Enhancements

#### 1.3.1 Smart Key Rotation
- [ ] Implement health-scored rotation (prefer healthy keys)
- [ ] Add key performance tracking (success rate, latency)
- [ ] Track per-key error counts
- [ ] Implement automatic key exclusion on repeated failures
- [ ] Add "dead key" detection and alerting

**Files to Modify:**
- `app/core/key_manager.py` (MODIFY KeyPool class)
- `app/db/database.py` (ADD key_health table)

#### 1.3.2 Key Usage Persistence
- [ ] Track per-key daily usage (requests, tokens)
- [ ] Track per-key error rates
- [ ] Store key health metrics in database
- [ ] Add key usage analytics endpoint

**Files to Modify:**
- `app/db/database.py` (MODIFY)
- `app/routes/keys.py` (ADD analytics endpoints)

---

## 🧪 SECTION 2: TESTING & VALIDATION SYSTEM (Week 1-2)

### 2.1 Google/Gemini Validator

#### 2.1.1 Core Validator Implementation
- [ ] Create `scripts/validate_google.py`
- [ ] Implement key validation (test auth with list models)
- [ ] Implement model validation (test inference on each model)
- [ ] Add error pattern detection (discontinued vs temporary)
- [ ] Add latency tracking
- [ ] Create rich console output report

**Files to Create:**
- `scripts/validate_google.py` (NEW)

#### 2.1.2 Auto-Freeze Integration
- [ ] Implement freeze decision logic
- [ ] Add DISCONTINUED pattern detection
- [ ] Add QUOTA_EXCEEDED detection  
- [ ] Implement `_freeze_model()` method
- [ ] Add freeze reason logging
- [ ] Create freeze report generation

**Files to Modify:**
- `app/config.py` (MODIFY freeze logic)
- `frozen_models.json` (auto-generated)

---

### 2.2 Groq Validator

#### 2.2.1 Core Validator Implementation
- [ ] Create `scripts/validate_groq.py`
- [ ] Implement key validation (test with models endpoint)
- [ ] Parse rate limit headers from responses
- [ ] Implement model validation for each Groq model
- [ ] Add queue status detection (at capacity)
- [ ] Create rich console output report

**Files to Create:**
- `scripts/validate_groq.py` (NEW)

#### 2.2.2 Groq-Specific Features
- [ ] Detect LPU capacity issues (503 errors)
- [ ] Handle Groq's rapid model churn
- [ ] Support for fetching live model list from Groq API
- [ ] Add queue depth tracking

**Files to Create:**
- `scripts/validate_groq.py` (NEW)

---

### 2.3 CLI Test Commands

#### 2.3.1 Test Command Structure
- [ ] Add `ai-engine test google` subcommand
- [ ] Add `ai-engine test groq` subcommand
- [ ] Add `ai-engine test all` subcommand
- [ ] Add `--key` filter (test specific key)
- [ ] Add `--model` filter (test specific model)
- [ ] Add `--no-freeze` flag (disable auto-freeze)
- [ ] Add `--output` flag (save JSON report)

**Files to Modify:**
- `ai-engine.py` (ADD test subcommands)
- `app/commands/test_commands.py` (NEW)

#### 2.3.2 Validation Reports
- [ ] Create HTML report generation
- [ ] Create JSON report generation
- [ ] Add historical comparison (vs last run)
- [ ] Add trend analysis

**Files to Create:**
- `app/utils/validation_reports.py` (NEW)

---

## 🔧 SECTION 3: TOOL CALLING SYSTEM (Week 2)

### 3.1 Tool Registry & Definitions

#### 3.1.1 Core Tool System
- [ ] Create `app/core/tools.py`
- [ ] Define Tool, ToolCall, ToolResult models
- [ ] Create ToolRegistry class
- [ ] Implement tool registration API
- [ ] Add tool execution engine

**Files to Create:**
- `app/core/tools.py` (NEW)

#### 3.1.2 Gemini Built-in Tools
- [ ] Add Google Search tool support
- [ ] Add Google Maps tool support
- [ ] Add Code Execution tool support
- [ ] Add URL Context tool support
- [ ] Add File Search tool support
- [ ] Add Computer Use tool support

**Files to Create:**
- `app/tools/gemini_builtin.py` (NEW)

#### 3.1.3 Groq/OpenAI Tool Format
- [ ] Support function calling format
- [ ] Support web_search built-in tool
- [ ] Support code_interpreter built-in tool
- [ ] Support browser_automation tool

**Files to Create:**
- `app/tools/groq_tools.py` (NEW)

---

### 3.2 Tool Execution Flow

#### 3.2.1 Tool Call Detection
- [ ] Detect tool calls in model responses
- [ ] Parse tool call arguments
- [ ] Validate tool call schema
- [ ] Handle multiple tool calls

**Files to Modify:**
- `app/core/striker.py` (ADD tool call handling)

#### 3.2.2 Tool Execution
- [ ] Execute tool handlers
- [ ] Handle async tool execution
- [ ] Manage tool timeouts
- [ ] Handle tool errors gracefully

**Files to Create:**
- `app/tools/executor.py` (NEW)

#### 3.2.3 Tool Response Integration
- [ ] Send tool results back to model
- [ ] Handle multi-turn tool conversations
- [ ] Display tool execution in responses

**Files to Modify:**
- `app/core/striker.py` (MODIFY)
- `app/routes/chat.py` (ADD tool support)

---

### 3.3 Custom Tools

#### 3.3.1 Custom Tool Registration
- [ ] Create custom tool config file
- [ ] Add tool schema validation
- [ ] Support HTTP endpoint tools
- [ ] Support Python function tools

**Files to Create:**
- `app/tools/custom.py` (NEW)
- `config/custom_tools.yaml` (NEW)

---

## 🖥️ SECTION 4: WEBUI BACKEND API (Week 2)

### 4.1 Chat API Enhancements

#### 4.1.1 Streaming Improvements
- [ ] Improve SSE streaming reliability
- [ ] Add heartbeat/ping to keep connection alive
- [ ] Handle client disconnects gracefully
- [ ] Add streaming pause/resume support

**Files to Modify:**
- `app/routes/chat.py` (MODIFY streaming endpoint)
- `app/core/striker.py` (MODIFY execute_streaming_strike)

#### 4.1.2 Conversation Management
- [ ] Add conversation CRUD endpoints
- [ ] Add message history pagination
- [ ] Add conversation search
- [ ] Add conversation export (JSON, Markdown)

**Files to Modify:**
- `app/routes/chat.py` (ADD conversation endpoints)
- `app/db/database.py` (MODIFY ConversationDB)

#### 4.1.3 File Handling
- [ ] Add file upload endpoint
- [ ] Add file storage management
- [ ] Add file type validation
- [ ] Add file size limits
- [ ] Add file deletion/cleanup

**Files to Create:**
- `app/routes/files.py` (NEW)
- `app/core/file_manager.py` (NEW)

---

### 4.2 Tool Calling API

#### 4.2.1 Tool Configuration Endpoints
- [ ] GET /v1/tools (list available tools)
- [ ] POST /v1/tools/custom (register custom tool)
- [ ] DELETE /v1/tools/custom/{id} (remove custom tool)
- [ ] GET /v1/tools/executions (tool execution history)

**Files to Create:**
- `app/routes/tools.py` (NEW)

#### 4.2.2 Tool Execution WebSocket
- [ ] Create WebSocket endpoint for real-time tool updates
- [ ] Stream tool execution progress
- [ ] Handle tool result callbacks

**Files to Create:**
- `app/routes/ws_tools.py` (NEW)

---

### 4.3 Model & Key Management API

#### 4.3.1 Model Registry API
- [ ] GET /v1/models (list all models with full details)
- [ ] POST /v1/models/{id}/freeze (freeze model)
- [ ] DELETE /v1/models/{id}/freeze (unfreeze model)
- [ ] GET /v1/models/frozen (list frozen models)
- [ ] POST /v1/models/{id}/test (test specific model)

**Files to Modify:**
- `app/routes/models.py` (EXPAND)

#### 4.3.2 Key Management API
- [ ] GET /v1/keys (list all keys with health status)
- [ ] POST /v1/keys (add new key)
- [ ] DELETE /v1/keys/{gateway}/{label} (delete key)
- [ ] POST /v1/keys/{gateway}/{label}/test (test key)
- [ ] GET /v1/keys/usage (key usage analytics)
- [ ] POST /v1/keys/{gateway}/{label}/toggle (enable/disable)

**Files to Modify:**
- `app/routes/keys.py` (EXPAND)

---

### 4.4 Token & Cost API

#### 4.4.1 Token Counting Endpoints
- [ ] POST /v1/tokens/count (count tokens for text)
- [ ] POST /v1/tokens/count-file (count tokens for file)
- [ ] GET /v1/tokens/models/{id} (get model token info)

**Files to Create:**
- `app/routes/tokens.py` (NEW)

#### 4.4.2 Cost Tracking Endpoints
- [ ] GET /v1/costs/daily (daily cost breakdown)
- [ ] GET /v1/costs/models (cost by model)
- [ ] GET /v1/costs/gateways (cost by gateway)
- [ ] GET /v1/costs/budget (budget status & alerts)

**Files to Create:**
- `app/routes/costs.py` (NEW)

---

### 4.5 Dashboard & Monitoring API

#### 4.5.1 Health & Status
- [ ] GET /v1/health (detailed health check)
- [ ] GET /v1/health/gateways (per-gateway health)
- [ ] GET /v1/health/keys (per-key health)
- [ ] GET /v1/metrics (real-time metrics)

**Files to Modify:**
- `app/routes/dashboard.py` (EXPAND)

#### 4.5.2 Logs & Debugging
- [ ] GET /v1/logs (request logs)
- [ ] GET /v1/logs/errors (error logs)
- [ ] GET /v1/logs/audit (audit logs)
- [ ] WebSocket for real-time logs

**Files to Create:**
- `app/routes/logs.py` (NEW)

---

## 🎨 SECTION 5: CLI IMPROVEMENTS (Week 2-3)

### 5.1 Visual Polish

#### 5.1.1 Rich Output Formatting
- [ ] Enhance all table outputs with icons
- [ ] Add color-coded status indicators
- [ ] Create progress bars for long operations
- [ ] Add animated spinners for async operations
- [ ] Implement "strike execution" visualization

**Files to Modify:**
- `ai-engine.py` (ENHANCE all outputs)
- `app/utils/formatter.py` (ADD rich helpers)

#### 5.1.2 New Commands
- [ ] `ai-engine doctor` (full diagnostic)
- [ ] `ai-engine status` (quick status overview)
- [ ] `ai-engine freeze <model>` (freeze model)
- [ ] `ai-engine unfreeze <model>` (unfreeze model)
- [ ] `ai-engine frozen` (list frozen models)
- [ ] `ai-engine report` (generate system report)
- [ ] `ai-engine config validate` (validate config)
- [ ] `ai-engine config optimize` (suggest optimizations)

**Files to Create:**
- `app/commands/doctor.py` (NEW)
- `app/commands/freeze_commands.py` (NEW)
- `app/commands/config_commands.py` (NEW)

---

### 5.2 Mission Control 2.0

#### 5.2.1 Live Dashboard
- [ ] Implement `ai-engine mission-control --watch`
- [ ] Add live-updating metrics display
- [ ] Add recent strikes list with sparklines
- [ ] Add gateway health gauges
- [ ] Add cost tracking graphs (ASCII art)

**Files to Modify:**
- `app/commands/mission_control.py` (NEW or MODIFY)

---

## 🔒 SECTION 6: SECURITY & AUTHENTICATION (Week 3)

### 6.1 API Authentication

#### 6.1.1 API Key Auth
- [ ] Implement API key validation middleware
- [ ] Add key-based rate limiting
- [ ] Create API key generation/management
- [ ] Add key expiration support

**Files to Create:**
- `app/security/auth.py` (NEW)
- `app/middleware/auth.py` (NEW)

#### 6.1.2 JWT Authentication (Optional)
- [ ] Add JWT token support
- [ ] Implement token refresh
- [ ] Add role-based access control

**Files to Create:**
- `app/security/jwt.py` (NEW)

---

### 6.2 Rate Limiting & Protection

#### 6.2.1 Request Rate Limiting
- [ ] Implement per-IP rate limiting
- [ ] Implement per-API-key rate limiting
- [ ] Add rate limit headers to responses
- [ ] Create rate limit bypass for admin keys

**Files to Create:**
- `app/security/rate_limit.py` (NEW)

#### 6.2.2 DDoS Protection
- [ ] Add request size limits
- [ ] Implement slow request protection
- [ ] Add concurrent request limits per client

**Files to Modify:**
- `app/main.py` (ADD middleware)

---

### 6.3 Audit & Logging

#### 6.3.1 Security Logging
- [ ] Log all authentication attempts
- [ ] Log API key usage
- [ ] Log model freeze/unfreeze actions
- [ ] Log configuration changes

**Files to Create:**
- `app/security/audit.py` (NEW)

#### 6.3.2 Request Logging
- [ ] Log all API requests (method, path, key, response time)
- [ ] Log request/response sizes
- [ ] Log errors with full context

**Files to Modify:**
- `app/main.py` (ADD logging middleware)

---

## 📊 SECTION 7: MONITORING & ALERTING (Week 3)

### 7.1 Metrics Collection

#### 7.1.1 System Metrics
- [ ] Track requests per minute/hour/day
- [ ] Track tokens per minute/hour/day
- [ ] Track error rates
- [ ] Track latency percentiles (p50, p95, p99)
- [ ] Track cost per gateway/model

**Files to Create:**
- `app/monitoring/metrics.py` (NEW)

#### 7.1.2 Key Health Metrics
- [ ] Track per-key success/failure rates
- [ ] Track per-key average latency
- [ ] Track per-key remaining quota
- [ ] Track key cooldown events

**Files to Modify:**
- `app/core/key_manager.py` (ADD metrics)

---

### 7.2 Alert System

#### 7.2.1 Alert Triggers
- [ ] Key exhaustion warning (at 80% quota)
- [ ] Key failure spike (>5 failures in 5 min)
- [ ] Rate limit approaching (at 85%)
- [ ] Cost threshold exceeded
- [ ] Model frozen alert
- [ ] Gateway down alert

**Files to Create:**
- `app/monitoring/alerts.py` (NEW)

#### 7.2.2 Alert Channels
- [ ] Webhook alerts
- [ ] Console/log alerts
- [ ] Optional: Email alerts
- [ ] Optional: Slack/Discord webhooks

**Files to Create:**
- `app/monitoring/notifiers.py` (NEW)

---

### 7.3 Health Checks

#### 7.3.1 Endpoint Health
- [ ] Create /health endpoint (basic)
- [ ] Create /health/detailed endpoint (full status)
- [ ] Add health check for each gateway
- [ ] Add health check for database

**Files to Modify:**
- `app/routes/health.py` (EXPAND)

#### 7.3.2 Background Health Monitoring
- [ ] Implement periodic health checks
- [ ] Auto-freeze models on health failures
- [ ] Auto-throttle on gateway issues

**Files to Create:**
- `app/monitoring/health_checker.py` (NEW)

---

## 🚀 SECTION 8: VPS DEPLOYMENT (Week 3-4)

### 8.1 Docker Configuration

#### 8.1.1 Dockerfile
- [ ] Create production Dockerfile
- [ ] Multi-stage build (reduce image size)
- [ ] Non-root user for security
- [ ] Health check instruction

**Files to Create:**
- `deploy/Dockerfile` (NEW)
- `deploy/.dockerignore` (NEW)

#### 8.1.2 Docker Compose
- [ ] Create docker-compose.yml
- [ ] Add persistent volume for database
- [ ] Add environment variable configuration
- [ ] Add restart policies

**Files to Create:**
- `deploy/docker-compose.yml` (NEW)

---

### 8.2 Systemd Services

#### 8.2.1 Service Configuration
- [ ] Create peacock-engine.service
- [ ] Configure auto-restart on failure
- [ ] Set resource limits
- [ ] Configure logging to journald

**Files to Create:**
- `deploy/systemd/peacock-engine.service` (NEW)

#### 8.2.2 Setup Scripts
- [ ] Create install script
- [ ] Create update script
- [ ] Create backup script

**Files to Create:**
- `deploy/scripts/install.sh` (NEW)
- `deploy/scripts/update.sh` (NEW)

---

### 8.3 Reverse Proxy (Caddy)

#### 8.3.1 Caddy Configuration
- [ ] Create Caddyfile
- [ ] Configure HTTPS (auto TLS)
- [ ] Configure reverse proxy to engine
- [ ] Add security headers
- [ ] Configure rate limiting at edge

**Files to Create:**
- `deploy/caddy/Caddyfile` (NEW)

#### 8.3.2 Security Hardening
- [ ] Add fail2ban configuration
- [ ] Configure UFW firewall rules
- [ ] Add DDoS protection (rate limiting)

**Files to Create:**
- `deploy/security/fail2ban/jail.local` (NEW)
- `deploy/security/ufw/rules.sh` (NEW)

---

### 8.4 Environment Configuration

#### 8.4.1 Production Environment
- [ ] Create .env.production template
- [ ] Document all required env vars
- [ ] Add secrets management guide

**Files to Create:**
- `.env.production.example` (NEW)
- `deploy/ENVIRONMENT.md` (NEW)

---

## 🧩 SECTION 9: DOCUMENTATION (Week 4)

### 9.1 API Documentation

#### 9.1.1 OpenAPI/Swagger
- [ ] Ensure all endpoints have docstrings
- [ ] Generate OpenAPI spec
- [ ] Host Swagger UI at /docs

**Files to Modify:**
- `app/main.py` (ADD Swagger)
- All route files (ADD docstrings)

#### 9.1.2 Integration Guides
- [ ] Update AGENTS.md
- [ ] Create API usage examples
- [ ] Create WebSocket usage guide

**Files to Modify:**
- `AGENTS.md` (UPDATE)

---

### 9.2 Deployment Documentation

#### 9.2.1 VPS Setup Guide
- [ ] Step-by-step VPS setup instructions
- [ ] Domain configuration guide
- [ ] SSL/TLS setup guide
- [ ] Troubleshooting guide

**Files to Create:**
- `deploy/README.md` (NEW)
- `deploy/TROUBLESHOOTING.md` (NEW)

---

## 📅 IMPLEMENTATION TIMELINE

### Week 1: Foundation
- Days 1-2: Token counters (Gemini + Groq)
- Days 3-4: Validators (Google + Groq)
- Day 5: Rate limiting improvements

### Week 2: Features
- Days 1-2: Tool calling system
- Days 3-4: WebUI backend API
- Day 5: CLI improvements

### Week 3: Production
- Days 1-2: Security & authentication
- Days 3-4: Monitoring & alerting
- Day 5: Docker & deployment prep

### Week 4: Polish & Deploy
- Days 1-2: Documentation
- Days 3-4: Testing & bug fixes
- Day 5: VPS deployment

---

## 🎯 SUCCESS CRITERIA

### Performance
- [ ] Token counting: 95%+ accuracy vs actual API usage
- [ ] API response time: <100ms for non-AI endpoints
- [ ] Streaming: First token within 2 seconds

### Reliability
- [ ] Key rotation: Automatic on 429 errors
- [ ] Model freezing: Automatic on discontinued detection
- [ ] Uptime target: 99.9%

### Security
- [ ] API key authentication: Required for all endpoints
- [ ] Rate limiting: Enforced per-key and per-IP
- [ ] No secrets in logs or responses

### Usability
- [ ] WebUI: Mobile-responsive
- [ ] CLI: All commands work with rich output
- [ ] Documentation: Complete for all features

---

## 📁 FINAL FILE STRUCTURE

```
ai-handler/
├── ai-engine.py                    # CLI entry point
├── app/
│   ├── main.py                     # FastAPI app
│   ├── config.py                   # Model registry & config
│   ├── commands/                   # CLI commands
│   │   ├── doctor.py
│   │   ├── freeze_commands.py
│   │   ├── config_commands.py
│   │   ├── test_commands.py
│   │   └── openclaw_wizard.py
│   ├── core/                       # Core engine
│   │   ├── striker.py
│   │   ├── key_manager.py
│   │   ├── rate_limiter.py
│   │   ├── tools.py
│   │   └── file_manager.py
│   ├── db/                         # Database
│   │   └── database.py
│   ├── middleware/                 # FastAPI middleware
│   │   └── auth.py
│   ├── monitoring/                 # Monitoring
│   │   ├── metrics.py
│   │   ├── alerts.py
│   │   ├── notifiers.py
│   │   └── health_checker.py
│   ├── routes/                     # API routes
│   │   ├── chat.py
│   │   ├── models.py
│   │   ├── keys.py
│   │   ├── tokens.py
│   │   ├── costs.py
│   │   ├── tools.py
│   │   ├── files.py
│   │   ├── logs.py
│   │   ├── health.py
│   │   └── dashboard.py
│   ├── security/                   # Security
│   │   ├── auth.py
│   │   ├── jwt.py
│   │   ├── rate_limit.py
│   │   └── audit.py
│   ├── tools/                      # Tool implementations
│   │   ├── gemini_builtin.py
│   │   ├── groq_tools.py
│   │   ├── custom.py
│   │   └── executor.py
│   └── utils/                      # Utilities
│       ├── formatter.py
│       ├── logger.py
│       ├── visual.py
│       ├── validation_reports.py
│       ├── token_counter.py
│       ├── gemini_token_counter.py
│       └── groq_token_counter.py
├── scripts/                        # Standalone scripts
│   ├── validate_google.py
│   └── validate_groq.py
├── deploy/                         # Deployment files
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── Caddyfile
│   ├── systemd/
│   ├── security/
│   └── scripts/
├── tests/                          # Test suite
├── static/                         # WebUI static files
│   ├── chat.html
│   ├── chat.css
│   └── chat.js
└── docs/                           # Documentation
    ├── AGENTS.md
    ├── WEBUI_FEATURE_SPEC.md
    └── deploy/
```

---

**END OF TASK BREAKDOWN**

Let's get this done! 🦚
