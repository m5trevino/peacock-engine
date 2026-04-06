## 🤖 AGENT ONBOARDING GUIDE
> **Role**: AI Integration Specialist / Agentic Orchestrator  
> **Goal**: Rapid ingestion of system capabilities and precise strike execution.

## 🏁 STEP 00: INTERACTIVE HELP
If you're unsure where to start, or if you're setting up a new project, run the interactive guide:
```bash
./ai-engine agent-guide
```

## 🏁 STEP 01: SYSTEM DISCOVERY
Run the following command to get the "Ultimate Source of Truth": a total system briefing, live diagnostics, and the integration guide.
```bash
./ai-engine mission-control
```
*Alias: `./ai-engine mc`*

## 🔌 STEP 02: THE UNIFIED INTERFACE
All new agentic flows must use the **Generic Chat** endpoint. This ensures internal key rotation and forensic tagging are handled automatically.

- **Endpoint**: `POST http://localhost:3099/v1/chat`
- **Recommended Model**: `gemini-3.1-flash-lite` (High speed, low cost)

### Payload Example (JSON)
```json
{
  "model": "gemini-3.1-flash-lite",
  "prompt": "Your instruction here",
  "files": ["/path/to/project/main.py"],
  "format": "text",
  "temp": 0.5
}
```

## 📂 STEP 03: FORENSIC VERIFICATION
Every strike generates a unique **Tag ID** (e.g., `PEA-X92J`). Use this to verify the verbatim I/O in the vault.

- **Success Logs**: `vault/successful/[TAG_ID].txt`
- **Error Analysis**: `vault/failed/[TAG_ID].txt`

## 🏎️ PERFORMANCE MODES (HELLCAT PROTOCOL)
If using the CLI Strike command, you can specify a performance mode:
- `--mode stealth`: 3.0x multiplier, quiet execution.
- `--mode balanced`: 1.15x multiplier, standard throughput.
- `--mode apex`: 1.02x multiplier, peak performance for mission-critical strikes.

---

## 🏛️ ARCHITECTURE SUMMARY
The engine acts as a **Headless Gateway**. It does not maintain its own state for your application; it simply provides the "Ammo" (API Keys) and the "Rifle" (Pydantic AI Striker) to hit your targets.

> *WE DON'T RUSH, SO WE DON'T MISS.*
