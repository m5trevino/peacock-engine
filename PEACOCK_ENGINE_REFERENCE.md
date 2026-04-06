# 🦅 PEACOCK ENGINE: ARCHITECTURAL REFERENCE & MOUNTING GUIDE

**VERSION:** 2.0 (TACTICAL REVISION)
**SYSTEM:** FASTAPI MIDDLEWARE // PYTHON 3.10+

This document serves as the definitive high-level breakdown of the Peacock Engine (ai-handler) and provides instructions for "mounting" or integrating this engine into new projects.

---

## 🏛️ 1. ARCHITECTURAL BREAKDOWN

The **Peacock Engine** is a tactical middleware designed to abstract multiple AI providers into a unified **"Strike Protocol."** It handles key rotation, deep context injection, and structured output rescue logic.

### **Core Components**
1.  **The Gateway (`app/main.py`)**: The central entry point. It manages API route inclusion (`app.include_router`), handles global middleware (CORS, logging), and mounts static assets for the Chat UI.
2.  **Key Manager (`app/core/key_manager.py`)**: The "Intelligence Officer." It maintains `KeyPool` objects for Groq, Google, DeepSeek, and Mistral. It uses **Round-Robin rotation with shuffling** to bypass rate limits and maximize uptime.
3.  **The Striker Engine (`app/core/striker.py`)**: The execution heart. Built on `pydantic-ai`, it runs prompts against the selected model. 
    - **EagleScaffold**: Structured code generation template.
    - **Rescue Logic**: Heuristic-based fixing for malformed JSON responses from "cheaper" models.
4.  **Filesystem Bridge (`app/routes/fs.py`)**: Provides "Scouting" capabilities. It can recursively scrape local directories and bundle them into massive context blocks (Heavy Payloads).
5.  **Mission Vault (`MISSION_VAULT_DIR`)**: A standardized directory for storing processed intelligence, YAML/JSON metadata, and batch run results.

### **Data Flow: The "Strike" Lifecycle**
1.  **Request**: Client sends JSON to `/v1/strike` (Precision) or `/v1/payload-strike` (Heavy Context).
2.  **Intelligence**: `Key Manager` retrieves the next healthy key for the requested provider.
3.  **Scouting**: For Heavy Payloads, the `FS Bridge` scrapes the specified files/dirs and appends them to the prompt.
4.  **Execution**: The `Striker` calls the AI Provider.
5.  **Extraction**: Results are parsed, "rescued" if malformed, and returned to the client.

---

## 🛠️ 2. THE MOUNTING RITUAL (HOW TO USE ON NEW PROJECTS)

When you want to deploy this engine as the AI backbone for a new project, follow these steps:

### **Method A: Sidecar Deployment (Recommended)**
Use the Peacock Engine as a standalone API service that your new project calls.
1.  **Clone & Configure**: Clone this `ai-handler` workspace.
2.  **Environment Setup**: Copy your `.env` containing `GROQ_KEYS`, `GOOGLE_KEYS`, etc.
3.  **Launch**: Run `./run_engine.sh` (Defaults to port `3099`).
4.  **Integration**: In your new project's code, point your AI requests to the engine:
    ```bash
    # Precision Strike Template
    curl -X POST http://localhost:3099/v1/strike \
    -H "Content-Type: application/json" \
    -d '{
      "modelId": "deepseek-reasoner",
      "prompt": "Analyze my new project...",
      "temp": 0.7
    }'
    ```

### **Method B: Internal Feature Mounting**
If you are building a new feature *inside* the engine itself:
1.  **Core Logic**: Place your backend logic in `app/core/your_feature.py`.
2.  **Router Definition**: Create `app/routes/your_feature.py` using `APIRouter`.
3.  **Registry**: Import and include the router in `app/main.py`:
    ```python
    from app.routes import your_feature
    app.include_router(your_feature.router, prefix="/v1/your-feature", tags=["New Project"])
    ```
4.  **Static UI**: If your feature has a web frontend, mount its build folder:
    ```python
    app.mount("/your-ui", StaticFiles(directory="path/to/dist"), name="your_ui")
    ```

### **Method C: Heavy Context Mounting**
To give the AI full awareness of your new project's source code:
1.  Use the `/v1/payload-strike` endpoint.
2.  Provide the **absolute path** to your new project's source directory in the `files` array.
3.  The engine will automatically scrape all `.py`, `.js`, `.ts`, `.md`, and `.json` files and inject them as context.

---

## 💀 3. THE BLOOD OATH (OPERATIONAL LAWS)
1.  **Zero Scraps**: Never return snippets. Always return complete, executable file blocks.
2.  **Key Integrity**: The engine handles keys; never expose raw strings in the client.
3.  **Proxy First**: If `PROXY_ENABLED` is true, ensure all outgoing traffic routes through the encrypted tunnel.

**[ENGINE STATUS: FULL_REFERENCE_GENERATED]**
**[AUTHORIZATION: ARCHITECT_LEVEL_BOTS_ONLY]**
