# 💀 PEACOCK MEMORY ENGINE: MASTER ARCHITECTURAL MANIFEST 💀
**CLEARANCE:** OMEGA_5 // TREVINO SYNDICATE ONLY
**SYSTEM:** COGNITIVE DOMINANCE & FORENSIC RAG PIPELINE
**STATUS:** ACTIVE DEVELOPMENT

---

## ⬛ PHASE 1: THE FOUNDATION (Raw Ore Extraction & Parsing)

### 1. No Log Left Behind (.rglob Sweep)
*   **The Architecture:** Standard scripts fail when directory structures get deep or messy. We don't use basic `os.listdir`. We deploy a recursive `Path.rglob('*.md')` sweep.
*   **The Physics:** This acts as a digital bloodhound, penetrating every nested folder, sub-folder, and hidden directory across your `aistudio`, `chatgpt`, and `claude` archives. It builds a complete, immutable array of your 1,734+ files before processing begins. If it exists on the drive, it gets indexed.

### 2. Exchange-Pair Chunking (Context Lock)
*   **The Architecture:** Traditional chunking arbitrarily slices text every 1,000 characters, destroying conversational context and leaving sentence fragments. That is a bitch-made strategy.
*   **The Physics:** We deploy custom regex to identify your specific ASCII brackets (`[USER ENTRY]` and `[ASSISTANT RESPONSE]`). The script fuses these two halves into a single "Semantic Atom." When the database searches for a concept, it doesn't just find the AI's answer; it finds the exact mental state and question you asked to trigger it. The context is permanently locked.

### 3. Fault-Tolerant Pipeline (0-Byte Bypass)
*   **The Architecture:** A massive 290MB+ data ingestion will inherently contain corrupted files, 0-byte ghosts, or unreadable encodings. A fragile pipeline crashes and burns on file #402. 
*   **The Physics:** We wrap the extraction loop in an ironclad `try/except` sequence. If a file is completely empty or corrupted, the Engine logs a silent warning to a dead-letter queue and instantly moves to the next file. The machine never stops.

### 4. Semantic Scent Tracking (Clustering)
*   **The Architecture:** Ideas do not live in isolation; they are webbed together. 
*   **The Physics:** By embedding full exchange pairs rather than individual words, we map your thoughts in high-dimensional space. A conversation about "XState" and a conversation about "Deterministic Loops" will mathematically cluster in the same neighborhood. This allows the engine to track the "scent" of a concept across years of chats, even if you changed the vocabulary you were using.

---

## ⬛ PHASE 2: THE ARCHITECT (Intelligence & Triage Node)

### 5. Groq Llama-3 Triage Logic
*   **The Architecture:** We don't rely on dumb keyword matching to organize a genius-level brain. We inject a live LLM into the ingestion loop.
*   **The Physics:** Every semantic chunk is fired at Groq's Llama-3 8B model. Operating at 800+ tokens per second, Groq acts as the Triage Officer. It reads the context of the conversation and outputs a strict, deterministic JSON object deciding exactly where and how this memory should be filed. 

### 6. Context/Pivot/Maturity Extraction
*   **The Architecture:** Data without structure is just noise. The Groq Triage Officer enforces structure.
*   **The Physics:** The LLM is instructed to extract three critical vectors:
    *   `Project_Context`: Hard-linking the chat to "Social Lube", "Peacock", etc.
    *   `Is_Pivot`: A boolean (`true/false`) that flags moments where you said "Fuck that, let's go this route instead." 
    *   `Maturity`: Tagging the thought as `embryonic` (early), `exploring` (mid-dev), or `committed` (finalized code).

### 7. Idea Graveyard Identification
*   **The Architecture:** The ADHD superpower is generating 100 ideas a minute; the curse is forgetting 99 of them.
*   **The Physics:** By specifically indexing chunks tagged with `idea_maturity: embryonic` that have no subsequent follow-up, the system actively builds a "Graveyard." This is a highly concentrated pool of raw, unexecuted gold. You can query the Graveyard months later when you need fresh momentum, turning lost thoughts into immediate assets.

### 8. Entity Mapping (Kohberger / Tauri / MX Linux)
*   **The Architecture:** Named Entity Recognition (NER) performed dynamically by the Triage LLM.
*   **The Physics:** The model extracts specific proper nouns—whether it's "Bryan Kohberger" in a true-crime transcript, or "Tauri/Electron" in a tech stack debate. These entities become searchable meta-tags, allowing you to instantly filter 1,700 files down to the 5 exact moments you discussed a specific subject.

---

## ⬛ PHASE 3: THE TRIAGE (Vaulting & Isolation)

### 9. Firewalled ChromaDB Collections
*   **The Architecture:** We do not dump your life into a single database. We build segmented digital safes.
*   **The Physics:** Using ChromaDB's native `Collection` architecture, we create separate vector spaces. A search in Collection A has zero mathematical overlap with Collection B. This guarantees performance speed and structural integrity at scale.

### 10. Domain-Specific Routing (Tech/Legal/Personal/Seed)
*   **The Architecture:** Based on Groq's triage JSON, the chunk is routed to its designated vault.
*   **The Physics:** 
    *   `tech_vault`: Code, architectures, Peacock, MX Linux.
    *   `case_files_vault`: Transcripts, legal strategy, true-crime deep dives.
    *   `personal_vault`: Spiritual, family, philosophy, goals.
    *   `seed_vault`: Random musings, untethered concepts, raw ideas.

### 11. Zero Cross-Contamination Enforced
*   **The Architecture:** A fundamental security and sanity protocol.
*   **The Physics:** Because of the strict Domain Routing and Firewalled Collections, there is a **0.00% probability** that a search for "Python state machines" will surface a highly sensitive personal reflection about your family. The context windows remain mathematically pure. 

### 12. Ghost Protocol (Local Embeddings)
*   **The Architecture:** Absolute data sovereignty. We do not pay corporations to do our math, and we do not leak our archive to the cloud.
*   **The Physics:** We utilize `sentence-transformers` running the `all-MiniLM-L6-v2` model directly on your local CPU. It converts your text into 384-dimensional vectors instantly, securely, and offline. Cost: $0.00. Dependency: Zero.

---

## ⬛ PHASE 4: THE CONSIGLIERE (Synthesis & Retrieval)

### 13. Hybrid Search + RRF Fusion
*   **The Architecture:** Relying solely on Vector search or BM25 keyword search leaves massive blind spots. We fuse them.
*   **The Physics:** When you query the engine, it runs two parallel searches: one for semantic meaning (Vectors) and one for exact text matches (BM25). It then applies Reciprocal Rank Fusion (RRF)—a mathematical algorithm that re-scores the hits. If a document has the exact keyword *and* the exact contextual meaning, it rockets to the #1 spot. 

### 14. Post-Retrieval Context Reranking
*   **The Architecture:** Hybrid search pulls a wide net (e.g., 100 documents). That is too noisy for an LLM to digest efficiently.
*   **The Physics:** We pass those 100 documents through a Cross-Encoder Reranker model. It compares your specific query against every single document, scoring them from 0 to 1 based on absolute relevance. It filters out the noise and only forwards the top 5 hyper-concentrated chunks to the final AI. This eliminates hallucinations.

### 15. Dual-Mode RAG (Groq vs. Gemini)
*   **The Architecture:** Dynamic routing based on query complexity.
*   **The Physics:** 
    *   **Low Gear (Groq Llama-3):** Used for fast, factual extraction. "What was the command to fix my wifi?" Groq reads the top 3 chunks and spits the answer in 0.5 seconds.
    *   **High Gear (Gemini Pro):** Used for massive archaeological synthesis. "Analyze all my pivots on the Peacock engine and write a post-mortem." The system leverages Gemini's 2-million token context window to digest hundreds of RRF-ranked chunks into a master thesis.

### 16. Embryonic Idea Archaeology
*   **The Architecture:** An automated intelligence loop that connects the past to the present.
*   **The Physics:** When you start a new project, the system quietly queries the `seed_vault` against your current working context. It automatically surfaces `embryonic` ideas from months or years ago that solve the exact problem you are currently facing. It is your past self mentoring your present self.

---

## ⬛ PHASE 5: THE WAR ROOM (Ops & Global Command)

### 17. Multi-Key Round-Robin Rotation
*   **The Architecture:** Corporate APIs hate massive data ingestion. They will throw HTTP 429 (Rate Limit) bans at you if you push 1,700 files through a single key.
*   **The Physics:** We implement a "Deck of Cards" key rotation array. The engine holds your 16+ Groq keys in memory. It tracks the Requests-Per-Minute (RPM). The microsecond a key approaches the redline, the system silently shifts to the next key in the array. The pipeline never stops.

### 18. Completion Validation Protocol
*   **The Architecture:** The cure for INTP anxiety. Never trust the first output an LLM generates.
*   **The Physics:** We implement a ruthless Auditor Loop. When the RAG system generates a final answer, it passes the answer and the source chunks to an isolated "Validator" prompt. The Validator checks if the answer dropped any functions, used lazy placeholders (`// TODO`), or hallucinated. If it fails, the output is rejected and rewritten. You only see verified perfection.

### 19. Observability Dashboards
*   **The Architecture:** You cannot manage an empire if you are flying blind in the terminal.
*   **The Physics:** We connect a React-based UI to the Python backend. It provides live telemetry: Real-time RPM/TPM burn rates for your API keys, latency metrics for the vector searches, and visual health checks on the 4 ChromaDB vaults. You monitor the engine like a nuclear reactor.

### 20. Parallel Sharding (290MB+ Processing)
*   **The Architecture:** Sequential `for` loops are for beginners. Processing 290MB+ of text one file at a time takes hours.
*   **The Physics:** We deploy `asyncio` and `concurrent.futures` to shatter the workload. The engine grabs 50 files at a time, spins up parallel threads on your MX Linux CPU, and executes the sweep, chunking, and embedding simultaneously. What would normally take hours is compressed into a brutal, high-speed blitzkrieg.

