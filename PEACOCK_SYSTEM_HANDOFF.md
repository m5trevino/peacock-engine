# 🦅 PEACOCK ENGINE V2: MISSION INTELLIGENCE (PYTHON EDITION)

**STATUS:** OPERATIONAL // **BASE PORT:** 3099 // **SYSTEM:** FASTAPI MIDDELWARE

## 1. CORE ARCHITECTURE
The Peacock Engine is a **Tactical Middleware Strike Center**. It abstracts different AI providers (Groq, Google, DeepSeek, Mistral) into a single, unified protocol. It handles the "dirty work"—key rotation, proxying, and multi-file context bundling—so your frontend stays clean.

## 2. KEY CAPABILITIES
*   **Smart Key Rotation**: Manages pools of API keys for every provider. It shuffles them on boot and rotates per request to stay under rate limits and maximize uptime.
*   **Unified Strike Gateway**: One endpoint to rule them all. Switch models/gateways by just changing a string in the JSON.
*   **Filesystem Bridge**: Direct access to local "Ammo" (context files) and "Prompts" templates.
*   **Multi-File Payload Bundle**: The ability to scrape entire directories or specific file lists and inject them as a massive context block into any LLM call.

## 3. TACTICAL ENDPOINTS

| ENDPOINT | METHOD | DESCRIPTION |
| :--- | :--- | :--- |
| `/v1/strike` | `POST` | **Precision Strike**. Single prompt to a single model. |
| `/v1/payload-strike` | `POST` | **Heavy Payload**. Bundles multiple files/dirs into one call. |
| `/v1/striker/execute` | `POST` | **Batch Strike**. Iterates through a list of files as individual tasks. |
| `/v1/models` | `GET` | **Intelligence**. Returns all supported models, tiers, and rate limits. |
| `/v1/fs/browse` | `GET` | **Scouting**. Browse the local filesystem for directories/files. |
| `/health` | `GET` | **Integrity**. Checks status and reports active key counts per pool. |

## 4. THE COMMANDS (PAYLOAD EXAMPLES)

### A. THE PRECISION STRIKE (`/v1/strike`)
Use this for standard chat or single-shot logic.
```json
{
  "modelId": "llama-3.3-70b-versatile",
  "prompt": "Analyze this code logic...",
  "temp": 0.7
}
```

### B. THE HEAVY PAYLOAD STRIKE (`/v1/payload-strike`)
The heavy hitter. Point it at files or folders; it handles the rest.
```json
{
  "modelId": "deepseek-reasoner",
  "prompt": "Map the connections between these files:",
  "files": [
    "/home/flintx/ai-handler/app/core",
    "/home/flintx/ai-handler/app/main.py"
  ]
}
```
*   **Logic**: If it's a dir, it recursively finds all `.py`, `.js`, `.ts`, `.json`, `.md`, `.txt` files and bundles them with absolute path headers.

### C. THE BATCH STRIKE (`/v1/striker/execute`)
Automated workflow for processing many files one by one.
```json
{
  "files": ["/path/file1.md", "/path/file2.md"],
  "prompt": "Extract keywords from this file",
  "modelId": "models/gemini-2.0-flash",
  "delay": 5
}
```

## 5. THE BLOOD OATH (OPERATIONAL RULES)
1.  **Zero Scraps**: All responses must be complete and ready for deployment.
2.  **Key Integrity**: The engine handles the keys; never expose raw strings in logs.
3.  **Proxy First**: If `PROXY_ENABLED` is true, all traffic routes through the encrypted tunnel.

---
**[ENGINE STATUS: FULLY_INTEGRATED]**
**[AUTHORIZATION: ARCHITECT_LEVEL_BOTS_ONLY]**
