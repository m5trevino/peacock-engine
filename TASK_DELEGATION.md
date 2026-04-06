# PEACOCK ENGINE - TASK DELEGATION
> **Who Does What - Clear Assignment of Work**
> **Version**: 1.0 | **Last Updated**: 2026-04-05

---

## 👥 TEAM ROLES

| Role | Who | Responsibilities |
|------|-----|------------------|
| **Human (You)** | @flintx | Research, testing, validation, design coordination, final integration |
| **AI (Me - Kimi)** | @kimi-cli | Core implementation: token counters, validators, tool calling, security |
| **Bot 2 (Optional)** | TBD | WebUI backend API, monitoring, CLI polish, deployment files |

---

## ✅ ASSIGNMENTS

### 🔴 KIMI (AI) - Core Implementation

#### Priority 1: Token Counting System (Days 1-2)
**Files to Create:**
- [ ] `app/utils/gemini_token_counter.py`
- [ ] `app/utils/groq_token_counter.py`
- [ ] `app/utils/token_counter.py` (unified interface)

**Files to Modify:**
- [ ] `app/core/striker.py` - Integrate token counters into execute_strike()
- [ ] `app/routes/tokens.py` - Create token counting API endpoint

**Key Implementation Details:**
- Gemini: Use `google.genai.Client().models.count_tokens()` API
- Gemini fallback: Regex-based estimation from gemini-tree-token-counter
- Groq: tiktoken with MODEL_ENCODING_MAP
- Groq overhead: 4 tokens per message + 3 for conversation

---

#### Priority 2: Validation Scripts (Days 3-4)
**Files to Create:**
- [ ] `scripts/validate_google.py`
- [ ] `scripts/validate_groq.py`

**Files to Modify:**
- [ ] `ai-engine.py` - Add `test` subcommand
- [ ] `app/commands/test_commands.py` - Command handlers

**Key Implementation Details:**
- Google: Test with `client.models.list()` and `generate_content()`
- Groq: Test with `/models` endpoint and chat completions
- Auto-freeze on discontinued patterns: "model not found", "404", "deprecated"
- DON'T freeze on temporary errors: "429", "503", "at capacity"
- Rich console output with tables

---

#### Priority 3: Tool Calling System (Days 5-7)
**Files to Create:**
- [ ] `app/core/tools.py` - Tool models and ToolRegistry
- [ ] `app/tools/gemini_builtin.py` - Gemini built-in tools
- [ ] `app/tools/groq_tools.py` - Groq tool support
- [ ] `app/tools/executor.py` - Tool execution engine
- [ ] `app/routes/tools.py` - Tool API endpoints

**Files to Modify:**
- [ ] `app/core/striker.py` - Handle tool calls in responses
- [ ] `app/routes/chat.py` - Add tool support to chat endpoint

**Key Implementation Details:**
- OpenAI-compatible function calling format
- Gemini built-ins: google_search, google_maps, code_execution, url_context
- Tool execution flow: Detect → Parse → Execute → Return result → Final response
- Support multiple tool calls in single response

---

#### Priority 4: Security Foundation (Days 8-9)
**Files to Create:**
- [ ] `app/security/auth.py` - API key validation
- [ ] `app/security/rate_limit.py` - Rate limiting
- [ ] `app/middleware/auth.py` - FastAPI middleware

**Files to Modify:**
- [ ] `app/main.py` - Add security middleware

**Key Implementation Details:**
- API key required for all endpoints except /health
- Per-key rate limiting
- Per-IP rate limiting
- Request size limits

---

**KIMI TOTAL: ~9 days of focused implementation**

---

### 🟡 YOU (Human) - Research, Testing, Integration

#### Task 1: Designer Coordination (Parallel with Kimi Days 1-4)
- [ ] Hand off `WEBUI_FEATURE_SPEC.md` to designer
- [ ] Review design mockups when ready
- [ ] Provide feedback on feature placement
- [ ] Approve final design before implementation

**Deliverable**: Design mockups (Figma/Sketch/HTML) for all WebUI features

---

#### Task 2: Environment Setup (Day 1)
- [ ] Ensure all API keys are valid and have quota
- [ ] Test current engine: `python ai-engine.py models`
- [ ] Test a strike: `python ai-engine.py strike -m gemini-2.0-flash-lite`
- [ ] Verify database is working

**Deliverable**: Working dev environment, confirmed keys work

---

#### Task 3: VPS Preparation (Days 5-7)
- [ ] Set up VPS (Hetzner/AWS/etc)
- [ ] Configure domain DNS
- [ ] Install Docker
- [ ] Test SSH access

**Deliverable**: VPS ready for deployment

---

#### Task 4: Testing Kimi's Work (As completed)
- [ ] Test token counters with known prompts
- [ ] Run validation scripts against real APIs
- [ ] Verify auto-freeze works correctly
- [ ] Test tool calling with real tools
- [ ] Verify security middleware blocks unauthorized requests

**Deliverable**: Bug reports, validation that features work

---

#### Task 5: Integration & Deployment (Days 10-12)
- [ ] Review all Kimi's code
- [ ] Merge any Bot 2 contributions
- [ ] Run full test suite
- [ ] Deploy to VPS
- [ ] Verify production works

**Deliverable**: Live production system

---

**YOU TOTAL: ~7-8 days of coordination, testing, deployment**

---

### 🟢 BOT 2 (Optional AI) - API & Deployment

*If you bring in another bot, assign them:*

#### Section 1: WebUI Backend API (Days 1-4)
**Files to Create:**
- [ ] `app/routes/models.py` - Enhanced model endpoints
- [ ] `app/routes/keys.py` - Key management API
- [ ] `app/routes/costs.py` - Cost tracking endpoints
- [ ] `app/routes/logs.py` - Logs API
- [ ] `app/routes/files.py` - File upload/management
- [ ] `app/routes/ws_tools.py` - WebSocket for tools

**Files to Modify:**
- [ ] `app/routes/chat.py` - Add conversation CRUD
- [ ] `app/db/database.py` - Add needed tables/queries

---

#### Section 2: Monitoring & Dashboard (Days 5-6)
**Files to Create:**
- [ ] `app/monitoring/metrics.py`
- [ ] `app/monitoring/alerts.py`
- [ ] `app/monitoring/notifiers.py`
- [ ] `app/monitoring/health_checker.py`
- [ ] `app/routes/dashboard.py` - Enhanced dashboard

---

#### Section 3: CLI Polish (Days 7-8)
**Files to Create:**
- [ ] `app/commands/doctor.py`
- [ ] `app/commands/freeze_commands.py`
- [ ] `app/commands/config_commands.py`
- [ ] `app/commands/mission_control.py`

**Files to Modify:**
- [ ] `ai-engine.py` - Add new commands
- [ ] `app/utils/formatter.py` - Rich output helpers

---

#### Section 4: Deployment Files (Days 9-10)
**Files to Create:**
- [ ] `deploy/Dockerfile`
- [ ] `deploy/docker-compose.yml`
- [ ] `deploy/systemd/peacock-engine.service`
- [ ] `deploy/caddy/Caddyfile`
- [ ] `deploy/security/fail2ban/jail.local`
- [ ] `deploy/security/ufw/rules.sh`
- [ ] `deploy/scripts/install.sh`
- [ ] `deploy/scripts/update.sh`

---

**BOT 2 TOTAL: ~10 days of API and deployment work**

---

## 📅 TIMELINE SCENARIOS

### Scenario A: Just You + Kimi (Recommended)
**Week 1**: Kimi does Token Counters + Validators, You test + coordinate design
**Week 2**: Kimi does Tool Calling + Security, You do VPS prep + testing  
**Week 3**: Kimi does remaining, You integrate + deploy

**Result**: Full system in 3 weeks

---

### Scenario B: You + Kimi + Bot 2
**Week 1**: 
- Kimi: Token counters + Validators
- Bot 2: WebUI API
- You: Testing + design

**Week 2**:
- Kimi: Tool calling + Security
- Bot 2: Monitoring + Deployment files
- You: VPS prep + integration

**Result**: Full system in 2 weeks

---

## 🔄 INTEGRATION POINTS

### Where Work Overlaps

1. **Token Counters**
   - Kimi writes the counters
   - You test accuracy against real API usage
   - Bot 2 (if present) uses in cost API

2. **Validation Scripts**
   - Kimi writes scripts
   - You run against real keys/models
   - Report which models should be frozen

3. **Tool Calling**
   - Kimi implements core system
   - You test with real tools (search, maps)
   - Bot 2 exposes via WebSocket API

4. **WebUI**
   - You coordinate design
   - Kimi provides backend endpoints
   - Bot 2 (if present) implements full API

---

## 📝 DAILY CHECKLIST (For Coordination)

### Kimi's Daily Updates
- [ ] What I completed today
- [ ] What I'm working on tomorrow
- [ ] Blockers/questions
- [ ] Files created/modified

### Your Daily Tasks
- [ ] Review Kimi's commits
- [ ] Test new features
- [ ] Report bugs/issues
- [ ] Update task board

---

## 🎯 SUCCESS DEFINITION

### Kimi Done When:
- [ ] Token counters accurate within 5% of actual API usage
- [ ] Validation scripts run successfully and auto-freeze works
- [ ] Tool calling executes google_search and returns results
- [ ] Security middleware blocks requests without valid API key

### You Done When:
- [ ] Design mockups approved and ready
- [ ] VPS provisioned and accessible
- [ ] All features tested and working
- [ ] Production system deployed and live

### Bot 2 Done When:
- [ ] All WebUI API endpoints return correct data
- [ ] Monitoring shows real-time metrics
- [ ] Deployment scripts run successfully
- [ ] CLI commands work with rich output

---

## 💬 COMMUNICATION

**Questions about implementation details?** → Ask Kimi
**Found a bug in Kimi's code?** → Tag Kimi with file/line
**Need to change requirements?** → Update this document
**Bot 2 joined and needs context?** → Point to PROJECT_HANDOFF.md

---

**END OF DELEGATION DOCUMENT**

*Start with: Kimi begins token counters, You hand off design spec*
