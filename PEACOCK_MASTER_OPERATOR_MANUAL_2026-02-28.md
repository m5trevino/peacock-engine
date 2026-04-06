# THE PEACOCK ENGINE V2: MASTER OPERATOR TACTICAL MANUAL (2026-02-28)

## 💀 IDENTITY & MISSION
The **Peacock Engine V2** is the iron-clad backbone of the Trevino War Room. Built with INTP architectural precision and street-hardened logic, it’s a high-performance AI gateway designed to dominate the digital landscape. We don't just "call APIs"; we execute **Strikes**. We don't just "handle errors"; we deploy **Rescue Protocols**. This system is built to scale from the gutter to Sand Hill Road, ensuring that no "boot-see" malformed response stops the mission.

---

## 💥 ENDPOINT DEEP-DIVE

### 1. `/v1/strike` (The Precision Hit)
The bread and butter. Execute a single prompt against any model in the registry.
- **Method**: `POST`
- **Logic**: Routes the request through the designated Gateway (Groq, Google, DeepSeek, Mistral) and pulls a fresh key from the Vault.
- **Special Mode**: `format_mode="eagle_scaffold"` triggers structured output (EagleScaffold).

### 2. `/v1/payload-strike` (The Heavy Artillery)
When you need to drop a massive codebase context into a prompt.
- **Method**: `POST`
- **Logic**: Recursively crawls provided file paths, "wastes" nothing, and builds a combined payload with clear `--- FILE: [PATH] ---` delimiters.
- **Payload Injection**: Automatically appends the combined codebase at the end of your prompt under the `PAYLOAD:` header.

### 3. `/v1/striker` (The Batch Mission Control)
The autonomous processing unit for large-scale intel gathering and file analysis.
- **`GET /files`**: Scans `chat_logs` for "signal" (code blocks) and targets that haven't been "washed" yet.
- **`POST /execute`**: Initiates a background batch strike.
- **`POST /pause` / `POST /resume` / `POST /abort`**: Tactical control over active missions.
- **`GET /status`**: Live telemetry (RPM, TPM, RPD, current target, and proxy status).
- **`GET /target/{filename}`**: Fetches extracted intel from the **Mission Vault**.

### 4. `/v1/fs` (The Logistics Hub)
Direct access to the engine's operational assets.
- **`/start`**: Boot scripts and initialization templates.
- **`/ammo`**: Pre-loaded prompts and reference datasets.
- **`/prompts/{phase}`**: Version-controlled prompt assets.
- **`/browse`**: Tactical directory navigation.

### 5. `/v1/proxy` (The Cloak)
Manages the engine's external visibility.
- **`POST /v1/proxy/toggle`**: Hot-swaps between **DataImpulse** (External Proxy) and **Local Proxy** (tun0/1081) by modifying the `.env` on the fly.

---

## 🛡️ THE RESCUE PROTOCOL
Standard AI frameworks fold when a model returns garbage. The Peacock Engine deploys a **5-Level Multi-Stage Parser** to recover "failed_generation" content:
1. **JSON Recovery**: Targeted extraction of raw JSON objects from error bodies.
2. **Markdown Code Blocks**: Regex-based extraction of `**filename: path**` paired with code blocks.
3. **EOF Blocks**: Parsing `cat << 'EOF' > path` structures.
4. **Aggressive Header Match**: Searching for `### path` or `File: path` patterns.
5. **Project Tree Stack**: A recursive, stack-based parser that reconstructs full project structures from visual directory trees.

---

## 🏦 THE VAULT (KEY ROTATION)
We don't get rate-limited. We rotate.
- **Dynamic Pools**: Separate "decks" for Groq, Google, DeepSeek, and Mistral.
- **Shuffling Logic**: The `KeyPool` shuffles the deck on initialization and reshuffles automatically when the "pointer" reaches the end.
- **Account Tracking**: Every strike logs the specific account ID used, ensuring total visibility into asset utilization.

---

## 🌐 THE PROXY GATE
Technical setup for maximum stealth:
- **`httpx.AsyncClient`**: High-performance asynchronous execution.
- **`trust_env=False`**: Hard-coded isolation from system-level proxy leaks.
- **Dual-Mode Routing**:
    - `PROXY_ENABLED=true`: Routes through `PROXY_URL` (DataImpulse).
    - `PROXY_ENABLED=false`: Routes through `LOCAL_PROXY` (VPN/Tunnel).

---

## 🗃️ MISSION VAULT & GENESIS INTEL
Every successful analysis mission results in a "washed" asset stored in `/home/flintx/MissionVault`.
- **Washing Logic**: Original content is prepended with a **YAML Frontmatter** containing:
    - **Title/Summary/Category**: High-level intel.
    - **Genesis Fields**: `completeness`, `contextType`, `buildStatus`, `logicUsed`, `troublesSolved`, `realWorldPainPoint`, `marketPotential`, `sellable`, `portfolioWorthy`, `isAppSeed`.
- **Deduplication**: Uses SHA-256 short-hashes for ID generation to prevent duplicate intel.

---

## 🛠️ OPERATIONAL RITUALS
1. **Setup**: Ensure `.env` is loaded with `GROQ_KEYS`, `GOOGLE_KEYS`, etc.
2. **Initialization**: Run `run_engine.sh` to spin up the FastAPI server on port `3099`.
3. **Monitoring**: Watch `server.log` for real-time strike telemetry.
4. **Troubleshooting**: If a strike fails, check `MISFIRE_DIR` for the raw failure dump.

**PEACOCK ENGINE V2 // MISSION READY // 4SHO.**
