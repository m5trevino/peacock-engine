# 🦚 PEACOCK ENGINE V3: TACTICAL MANUAL
# ┖━─━─━─━─━─━─━─━─━─━─━─━─━─━─━┚

> [!TIP]
> **NEW ENTRY POINT**: Use `./ai-engine mission-control` (or `./ai-engine mc`) for a total system context dump.
> **INTERACTIVE GUIDE**: Use `./ai-engine agent-guide` for a step-by-step walkthrough of common missions (Setup, Repair, API).

> **March 2026 Edition** | **Codebase: AI-HANDLER V3** | **Status: BATTLE-READY**

## 🛠️ I. CLI COMMAND CENTER
Drive the engine directly from the project root using the `./ai-engine` wrapper. This automatically handles the virtual environment and dependencies.

### 1. The Registry (`models`)
List every model in the arsenal with verified prices, rate limits, and status.
- **Usage**: `./ai-engine models`
- **Utility**: Check `ID`, `Tier`, `RPM/TPM`, and `Input/Output Cost per 1M tokens`.

### 2. The Arsenal (`keys`)
Audit your loaded API keys across all gateways (Google, Groq, DeepSeek, Mistral).
- **Usage**: `./ai-engine keys`
- **Security**: Keys are masked. "Deck of Cards" rotation ensures no single key is burned.

### 3. The Precision Strike (`strike`)
Execute manual AI operations directly from your terminal.
- **Direct Prompt**: `./ai-engine strike "Analyze the tactical situation"`
- **File Payload**: `./ai-engine strike -f /path/to/intel.txt`
- **Targeting**: `--model gemini-3.1-pro` (Default: `gemini-3.1-flash-lite`)
- **Stealth Mode**: `--quiet` (Silences debug telemetry)
- **Hellcat Multipliers**: `--mode [stealth|balanced|apex]` (Controls execution speed/cost)
- **Zero-Print**: `--no-print` (Executes & logs to vault without terminal output)
- **MetroPCS Bypass**: `--tunnel` (Routes traffic through SOCKS5: `127.0.0.1:1081`)

### 4. Health & Dossier (`audit`, `dossier`)
Verify the integrity of specific gateways or get a full AI-ready system briefing.
- **Audit All**: `./ai-engine audit`
- **Audit Gateway**: `./ai-engine audit --gateway groq`
- **System Dossier**: `./ai-engine dossier` (Recommended for AI Agents/Bots)

---

## 🚀 II. ENGINE OPERATIONS
The PEACOCK ENGINE runs as a Headless Platform for universal integration.

### 1. Ignition (Start Server)
Initialize the FastAPI orchestration layer on port `3099`.
```bash
./run_engine.sh
```
*Flags: `--no-proxy` (Bypasses system proxies), `--proxy=SOCKS5://...`*

### 2. System-Wide Access (PRO TIP)
To run the engine from anywhere in your terminal, add this alias to your `~/.zshrc` or `~/.bashrc`:
```bash
alias peacock='/home/flintx/ai-handler/ai-engine'
```
*After adding, run `source ~/.zshrc`. Now you can just type `peacock strike "Hello"` from any directory.*

### 3. Physical Health Check
Verify the server is online and key pools are healthy.
```bash
curl http://localhost:3099/health
```

---

## 🧠 III. NEW APP ONBOARDING
Setting up a new application or AI bot to use the engine? Follow this flow:

1. **Mission Control**: Run `./ai-engine mc` for the ultimate source of truth.
2. **Interactive Guide**: Run `./ai-engine agent-guide` for a guided setup.
3. **Register**: Use `./ai-engine onboard` to get your `App ID` and `API Secret`.
3. **Agent Integration**: If building an AI-driven app, point your agent to [AGENT_ONBOARDING.md](file:///home/flintx/ai-handler/app/AGENT_ONBOARDING.md).
4. **UI Blueprint**: Need a frontend? Use `./ai-engine ui-guide` for a chatbot-ready React/HTML spec.

---

## 🛰️ IV. DEVELOPER STRIKE API
Recommended integration patterns for new AI bots and applications.

### 1. The Unified Endpoint (RECOMMENDED)
**`POST /v1/chat`** is the single source of truth for all V3 integrations.

**Payload Structure:**
```json
{
  "model": "gemini-3.1-flash-lite",
  "prompt": "Synthesize the report",
  "files": ["/absolute/path/to/file.py"],
  "format": "text", // OPTIONS: text, json, pydantic
  "temp": 0.7
}
```

### 2. Structured Output (First-Class Citizens)
Force JSON or Pydantic schemas for high-signal data extraction.
```bash
# Example: Extracting JSON
curl -X POST http://localhost:3099/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"model": "gemini-3.1-flash-lite", "prompt": "Extract names from text", "format": "json"}'
```

---

## 📂 IV. THE FORENSIC VAULT
Every strike leaves a trace. The engine logs verbatim I/O for audit and debugging.

- **Check Success**: `ls vault/successful/` (Look for Tag IDs like `PEA-X92J`)
- **Inspect Failed**: `ls vault/failed/` (Check why a strike didn't land)
- **Live Logs**: `tail -f server.log`

---

## 🛠️ V. INTEGRATION & ONBOARDING
Tools to speed up the development of new UI or backend services.

- **`./ai-engine onboard`**: Interactive guide to register a new app.
- **`./ai-engine ui-guide`**: Prints a technical blueprint for AI-assisted UI generation.
- **`./ai-engine flyout-snippet`**: Outputs the code for a professional model selector UI.

---

## 🏁 MISSION HANDOFF
**CURRENT OBJECTIVE**: Maintain "Sand Hill Road" quality execution. Ensure all integrations use the `/v1/chat` endpoint for maximum reliability and rotation support.

> *WE DON'T RUSH, SO WE DON'T MISS.*
